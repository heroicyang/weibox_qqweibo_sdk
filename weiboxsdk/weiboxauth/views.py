#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from auth import oauth,qqweiboauth
from api import qqweiboapi
import ImageFile,os,uuid

def get_auth_client(request):
    access_token_string=request.session.get('access_token',None)
    if access_token_string:
        access_token=oauth.OAuthToken.from_string(access_token_string)
        qqweibo=qqweiboauth.QQWeiboAuthClient(settings.QQWEIBO_CONSUMER_KEY,settings.QQWEIBO_CONSUMER_SECRET)
        qqweibo.set_access_token(access_token.key,access_token.secret)
        return qqweibo

def index(request):
    return render_to_response('index.html')

def qqweibo_login(request):
    qqweibo=qqweiboauth.QQWeiboAuthClient(settings.QQWEIBO_CONSUMER_KEY,settings.QQWEIBO_CONSUMER_SECRET)
    request_token=qqweibo.fetch_request_token(callback_url=request.build_absolute_uri(reverse('weiboxauth_qqweibo_login_done')))
    request.session['request_token']=request_token.to_string()
    signin_url=qqweibo.authorize_token_url(request_token)
    return redirect(signin_url)

def qqweibo_login_done(request):
    request_token=request.session.get('request_token',None)
    if not request_token:
        return redirect(reverse('weiboxauth_index'))
        
    verifier=request.GET.get('oauth_verifier',None)
    if 'request_token' in request.session:
        del request.session['request_token']
    
    token=oauth.OAuthToken.from_string(request_token)
    qqweibo=qqweiboauth.QQWeiboAuthClient(settings.QQWEIBO_CONSUMER_KEY,settings.QQWEIBO_CONSUMER_SECRET)
    access_token=qqweibo.fetch_access_token(token,verifier)
    request.session['access_token'] = access_token.to_string()
    
    return redirect(reverse('weiboxauth_home'))

def qqweibo_login_out(request):
    if 'access_token' in request.session:
        del request.session['access_token']
    return redirect(reverse('weiboxauth_index'))

def home(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    user_info=api.get_user_info()['data']

    return render_to_response('index.html',{'userinfo':user_info})

def qqweibo_home_timeline(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    home_timeline=api.get_home_timeline(0,0,reqnum=30,type=0,contenttype=0)['data']
    return render_to_response('timeline.html',{'timeline':home_timeline,'timeline_cate':'主页时间线'})

def qqweibo_tweet(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    my_timeline=api.get_broadcast_timeline(0,0,0,reqnum=10,type=0,contenttype=0)['data']
    return render_to_response('tweet.html',{'timeline':my_timeline})

def qqweibo_mentions_timeline(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    mentions_timeline=api.get_mentions_timeline(0,0,0,reqnum=30,type=0,contenttype=0)['data']

    return render_to_response('timeline.html',{'timeline':mentions_timeline,'timeline_cate':'提及我的时间线'})

def qqweibo_user_timeline(request,username):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    mentions_timeline=api.get_user_timeline(username,0,0,0,reqnum=30,type=0,contenttype=0)['data']

    return render_to_response('timeline.html',{'timeline':mentions_timeline,'timeline_cate':'其他用户发表的时间线'})

def qqweibo_public_timeline(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    public_timeline=api.get_public_timeline(0,reqnum=30)['data']

    return render_to_response('timeline.html',{'timeline':public_timeline,'timeline_cate':'广播大厅时间线'})

def add_tweet(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    
    if request.method == "POST":
        ip = request.META['REMOTE_ADDR']
        content=request.POST.get('content',None)
    
        if request.FILES.get('pic'):
            f = request.FILES["pic"]  
            parser = ImageFile.Parser()  
            for chunk in f.chunks():  
                parser.feed(chunk)  
            img = parser.close()
            path=os.path.join(settings.STATIC_ROOT,'upload')
            file_name=str(uuid.uuid1())+".jpg"
            file_path=os.path.join(path,file_name)

            img.save(file_path,'jpeg')
            resp_content=api.add_pic_tweet(content,ip,'','',file_path)
        
            os.remove(file_path)
        else:
            resp_content=api.add_tweet(content,ip,'','')
        
    return redirect(reverse('weiboxauth_qqweibo_tweet'))

@csrf_exempt
def re_add_tweet(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    
    if request.method == "POST":
        ip = request.META['REMOTE_ADDR']
        print request.POST
        content=request.POST.get('content',None)
        rid=request.POST.get('rid',None)
        
        resp_content=api.re_add_tweet(content,ip,'','',rid)
    return HttpResponse(json.dumps(resp_content),mimetype='application/javascript')

@csrf_exempt
def comment_tweet(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    
    if request.method == "POST":
        ip = request.META['REMOTE_ADDR']
        print request.POST
        content=request.POST.get('content',None)
        rid=request.POST.get('rid',None)
        
        resp_content=api.comment_tweet(content,ip,'','',rid)
    return HttpResponse(json.dumps(resp_content),mimetype='application/javascript')

def del_tweet(request,id):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    resp_content=api.del_tweet(id)
    return redirect(reverse('weiboxauth_qqweibo_tweet'))

def qqweibo_get_fanslist(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    fans_list=api.get_fanslist(0,reqnum=30)['data']['info']

    return render_to_response('friends.html',{'friends_list':fans_list,'friends_type':'我的听众列表'})

def qqweibo_get_idollist(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    idol_list=api.get_idollist(0,reqnum=30)['data']['info']

    return render_to_response('friends.html',{'friends_list':idol_list,'friends_type':'我的收听列表'})

def qqweibo_get_speciallist(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    special_list=api.get_speciallist(0,reqnum=30)['data']['info']

    return render_to_response('friends.html',{'friends_list':special_list,'friends_type':'我的特别收听列表'})

def qqweibo_get_blacklist(request):
    qqweibo=get_auth_client(request)
    if not qqweibo:
        return redirect(reverse('weiboxauth_index'))
    api=qqweiboapi.QQWeiboAPI(qqweibo)
    black_list=api.get_blacklist(0,reqnum=30)['data']['info']

    return render_to_response('friends.html',{'friends_list':black_list,'friends_type':'我的黑名单列表'})

    
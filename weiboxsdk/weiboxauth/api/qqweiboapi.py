#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import mimetypes
from urllib2 import urlopen,Request
from urllib import urlencode
from django.utils import simplejson as json
from symbol import except_clause

class QQWeiboAPIBase(object):
    def __init__(self,auth_client=None):
        self.auth=auth_client
        
    def generate_parameters(self,parameter_keys,args,kargs):
        self.parameters={'format':'json'}
        for idx,arg in enumerate(args):
            try:
                self.parameters[parameter_keys[idx]]=QQWeiboAPIBase.convert_to_utf8_str(arg)
            except IndexError:
                raise Exception('')
        for k,arg in kargs.items():
            if k not in self.parameters:
                self.parameters[k]=QQWeiboAPIBase.convert_to_utf8_str(arg)
                
    def call_request(self,url,http_method,post_data=None,hearders={}):
        self.headers=hearders
        self.post_data=post_data
        if len(self.parameters):
            if http_method == 'GET':
                url='%s?%s' % (url,urlencode(self.parameters))
            else:
                self.headers.setdefault("User-Agent", "weiboxauth")
                if post_data is None:
                    self.headers.setdefault("Accept", "text/html")
                    self.headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
                    self.post_data = urlencode(self.parameters)
                
        authed_url=self.auth.get_authed_url(url,http_method,self.parameters)
        if http_method == 'POST':
            req=Request(authed_url, data=self.post_data, headers=self.headers)
        else:
            req=Request(authed_url)
        resp=urlopen(req)
        resp_content=resp.read()
        return resp_content

    @staticmethod
    def convert_to_utf8_str(arg):
        unicodeType = __builtins__['unicode']
        if type(arg) == unicodeType:
            return arg.encode('utf-8')
        elif type(arg) == str:
            return arg
        # assume list
        if hasattr(arg, '__iter__'):
            arg = ','.join(map(convert_to_utf8_str, arg))
        return str(arg)

class QQWeiboAPI(QQWeiboAPIBase):
    def __init__(self,auth_client=None):
        QQWeiboAPIBase.__init__(self, auth_client)
    
    ## 时间线 ##
    """ Statuses/home_timeline 主页时间线 """
    def get_home_timeline(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['pageflag','pagetime','reqnum','type','contenttype'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/statuses/home_timeline',
            'GET'
        )
        
        return json.loads(rep_content,encoding='utf-8')
    
    """ Statuses/public_timeline 广播大厅时间线 """
    def get_public_timeline(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['pos','reqnum'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/statuses/public_timeline',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ Statuses/user_timeline 其他用户发表时间线 """
    def get_user_timeline(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['name','pageflag','pagetime','lastid','reqnum','type','contenttype'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/statuses/user_timeline',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ Statuses/mentions_timeline 用户提及时间线 """
    def get_mentions_timeline(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['pageflag','pagetime','lastid','reqnum','type','contenttype'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/statuses/mentions_timeline',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ Statuses/ht_timeline 话题时间线 """
    def get_ht_timeline(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['httext','pageflag','pageinfo','reqnum'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/statuses/ht_timeline',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ Statuses/broadcast_timeline 我发表时间线 """
    def get_broadcast_timeline(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['pageflag','pagetime','lastid','reqnum','type','contenttype'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/statuses/broadcast_timeline',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ Statuses/special_timeline 特别收听的人发表时间线 """
    def get_special_timeline(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['pageflag','pagetime','reqnum'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/statuses/special_timeline',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    ## 微博相关 ##
    """ t/show 获取一条微博数据 """
    def get_tweet(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['id'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/t/show',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ t/add 发表一条微博 """
    def add_tweet(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['content','clientip','jing','wei'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/t/add',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ t/del 删除一条微博 """
    def del_tweet(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['id'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/t/del',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ t/re_add 转播一条微博 """
    def re_add_tweet(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['content','clientip','jing','wei','reid'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/t/re_add',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ t/reply 回复一条微博 """
    def reply_tweet(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['content','clientip','jing','wei','reid'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/t/reply',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ t/add_pic 发表一条带图片的微博 """
    def add_pic_tweet(self,content,clientip,jing,wei,file_path):
        headers,post_data=QQWeiboAPI.pack_image(file_path, contentname='pic', 
                                                content=content, clientip=clientip, jing=jing, wei=wei)
        args=[content,clientip,jing,wei]
        QQWeiboAPIBase.generate_parameters(
            self,
            ['content','clientip','jing','wei'],
            args,{}
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/t/add_pic',
            'POST',
            post_data=post_data,hearders=headers
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ t/comment 点评一条微博 """
    def comment_tweet(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['content','clientip','jing','wei','reid'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/t/comment',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
        
        
    ## 帐户相关 ##
    """ User/info 获取自己的详细资料 """
    def get_user_info(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,[],args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/user/info',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ user/update 更新用户信息 """
    def update_user_info(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['nick','sex','year','month','day','countrycode','provincecode','citycode','introduction'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/user/update',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ user/update_head 更新用户头像信息 """
    def update_user_head(self,file_path):
        headers,post_data=QQWeiboAPI.pack_image(file_path, contentname='pic')
        QQWeiboAPIBase.generate_parameters(
            self,[],[],{}
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/user/update_head',
            'POST',
            post_data=post_data,hearders=headers
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ user/other_info 获取其他人资料 """
    def get_other_info(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['name'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/user/other_info',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    ## 关系链相关 ##
    """ friends/fanslist 我的听众列表 """
    def get_fanslist(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['reqnum','startindex'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/fanslist',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ friends/idollist 我的收听的人列表 """
    def get_idollist(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['reqnum','startindex'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/idollist',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ Friends/blacklist 黑名单列表 """
    def get_blacklist(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['reqnum','startindex'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/blacklist',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ Friends/speciallist 特别收听列表 """
    def get_speciallist(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['reqnum','startindex'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/speciallist',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ friends/add 收听某个用户 """
    def add_idol(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['name','clientip'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/add',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ friends/del取消收听某个用户 """
    def del_idol(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['name'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/del',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ friends/addspecial 特别收听某个用户 """
    def add_special_idol(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['name'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/addspecial',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ friends/delspecial 取消特别收听某个用户 """
    def del_special_idol(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['name'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/delspecial',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ friends/addblacklist 添加某个用户到黑名单 """
    def add_blacklist(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['name'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/addblacklist',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ friends/delblacklist 从黑名单中删除某个用户 """
    def del_blacklist(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['name'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/delblacklist',
            'POST'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ friends/check 检测是否我听众或收听的人 """
    def check_friends(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['names','flag'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/check',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ friends/user_fanslist 其他帐户听众列表 """
    def get_user_fanslist(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['reqnum','startindex','name'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/user_fanslist',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ friends/user_idollist 其他帐户收听的人列表 """
    def get_user_idollist(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['reqnum','startindex','name'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/friends/user_idollist',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    ## 热度、趋势 ##
    """ trends/ht 话题热榜 """
    def get_ht_trends(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['type','reqnum','pos'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/trends/ht',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    """ Trends/t 转播热榜 """
    def get_t_trends(self,*args,**kargs):
        QQWeiboAPIBase.generate_parameters(
            self,
            ['reqnum','pos'],
            args,kargs
        )
        rep_content=QQWeiboAPIBase.call_request(
            self,
            'http://open.t.qq.com/api/trends/t',
            'GET'
        )
        return json.loads(rep_content,encoding='utf-8')
    
    @staticmethod
    def pack_image(filename, contentname, max_size=1024, **params):
        """Pack image from file into multipart-formdata post body"""
        # image must be less than 700kb in size
        try:
            if os.path.getsize(filename) > (max_size * 1024):
                raise Exception('File is too big, must be less than 700kb.')
        except os.error:
            raise Exception('Unable to access file')

        # image must be gif, jpeg, or png
        file_type = mimetypes.guess_type(filename)
        if file_type is None:
            raise Exception('Could not determine file type')
        file_type = file_type[0]
        if file_type.split('/')[0] != 'image':
            raise Exception('Invalid file type for image: %s' % file_type)

        # build the mulitpart-formdata body
        BOUNDARY = 'WeiboxQQAPI'
        body = []
        for key, val in params.items():
            if val is not None:
                body.append('--' + BOUNDARY)
                body.append('Content-Disposition: form-data; name="%s"' % key)
                body.append('Content-Type: text/plain; charset=UTF-8')
                body.append('Content-Transfer-Encoding: 8bit')
                body.append('')
                body.append(QQWeiboAPIBase.convert_to_utf8_str(val))
        fp = open(filename, 'rb')
        body.append('--' + BOUNDARY)
        body.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (contentname, filename.encode('utf-8')))
        body.append('Content-Type: %s' % file_type)
        body.append('Content-Transfer-Encoding: binary')
        body.append('')
        body.append(fp.read())
        body.append('--%s--' % BOUNDARY)
        body.append('')
        fp.close()
        body.append('--%s--' % BOUNDARY)
        body.append('')
        
        body = '\r\n'.join(body)
        # build headers
        headers = {
            'Content-Type': 'multipart/form-data; boundary=%s' % BOUNDARY,
            'Content-Length': len(body)
        }

        return headers, body
        
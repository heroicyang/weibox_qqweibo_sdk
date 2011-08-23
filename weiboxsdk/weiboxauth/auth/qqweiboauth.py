#!/usr/bin/env python
# -*- coding: utf-8 -*-
from weiboxauth.auth import oauth
from urllib2 import urlopen,Request

REQUEST_TOKEN_URL='https://open.t.qq.com/cgi-bin/request_token'
AUTHORIZE_URL='https://open.t.qq.com/cgi-bin/authorize'
ACCESS_TOKEN_URL='https://open.t.qq.com/cgi-bin/access_token'

class QQWeiboAuthClient(oauth.OAuthClient):
    def __init__(self,consumer_key,consumer_secret,request_token_url=REQUEST_TOKEN_URL,authorize_url=AUTHORIZE_URL,access_token_url=ACCESS_TOKEN_URL):
        self.consumer_key=consumer_key
        self.consumer_secret=consumer_secret
        self.consumer=oauth.OAuthConsumer(consumer_key,consumer_secret)
        self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self.request_token_url=request_token_url
        self.authorize_url=authorize_url
        self.access_token_url=access_token_url
        self.access_token=None
    
    def fetch_request_token(self,callback_url=None):
        if not callback_url:
            callback_url='null'
        self.callback_url=callback_url
        oauth_request=oauth.OAuthRequest.from_consumer_and_token(
            self.consumer,http_url=self.request_token_url,callback=self.callback_url
        )
        oauth_request.sign_request(self.signature_method,self.consumer,None)
        return oauth.OAuthToken.from_string(urlopen(Request(oauth_request.to_url())).read())
    
    def authorize_token_url(self,token):
        oauth_request=oauth.OAuthRequest.from_consumer_and_token(
            self.consumer,token=token,http_url=self.authorize_url,callback=self.callback_url
        )
        oauth_request.sign_request(self.signature_method,self.consumer,token)
        return oauth_request.to_url()
    
    def fetch_access_token(self,token,verifier):
        oauth_request=oauth.OAuthRequest.from_consumer_and_token(
            self.consumer,token=token,verifier=verifier,http_url=self.access_token_url
        )
        oauth_request.sign_request(self.signature_method,self.consumer,token)
        return oauth.OAuthToken.from_string(urlopen(Request(oauth_request.to_url())).read())
    
    def set_access_token(self,token_key,token_secret):
        self.access_token=oauth.OAuthToken(token_key,token_secret)
        
    def get_authed_url(self,url,method,parameters):
        oauth_request=oauth.OAuthRequest.from_consumer_and_token(
            self.consumer,token=self.access_token,http_method=method,http_url=url,parameters=parameters
        )
        oauth_request.sign_request(self.signature_method,self.consumer,self.access_token)
        return oauth_request.to_url()
        
#!/usr/bin/env python
# encoding:utf-8

import json
import urllib
from weibo import APIClient

#微博id
WEIBO_STATUS_ID = 'xxxx'
#id
SOURCE_ID = 'xxxx'

APP_KEY = 'xxxx'
APP_SECRET = 'xxxx'
CALLBACK_URL = 'http://xxxx' # callback url 

#token
ACCESS_TOKEN = '2.00w5oHhFqlnWfBbec36e43950w_U81'

class Weibo_API:
    '''
    Based on sinaweibopy
    1.初始化对象，获取跳转URL，跳转页面并等待用户授权
    2.授权后，会跳转到回调地址
    3.从request中获取code，获取access_token
    4.使用API接口
    '''
    def __init__(self, APP_KEY, APP_SECRET, CALLBACK_URL=''):
        self.app_key = APP_KEY
        self.app_secret = APP_SECRET
        self.callback_url = CALLBACK_URL
        self.access_token = None
        self.jump_url = None
        self.client = APIClient(app_key=self.app_key, app_secret=self.app_secret, redirect_uri=self.callback_url) 
        self._get_jump_url()

    def get_access_token(self, code):
        ''' get access token by app_key and app_secret 
            @code   return from sinaweibo
        '''
        r = self.client.request_access_token(code)
        self.access_token = r.access_token
        #self.acces_token = ACCESS_TOKEN
        return access_token
        
    def _get_jump_url(self):
        ''' get next url to jump '''
        self.jump_url = self.client.get_authorize_url()

    def get_repost_uid_by_sid(self, id):
        ''' get repost user id by message id 
            @id      source status id
            @return  all repost user id
        '''
        json_result = json.loads(self.client.statuses.repost_timeline.get(id=id, count=200))
        json_result['next_cursor']
        result = [id for id in json_result['reposts']['user']]
        page = 2 
        while json_result['next_cursor']:
            json_result = json.loads(self.client.statuses.repost_timeline.get(id=id, count=200, page=page))
            page += 1
            result += [id for id in json_result['reposts']['user']] 
        return result

    def is_follower(self, sid, tid):
        ''' source id is following or not by target id 
            @sid  source id 
            @tid  target id
        ''' 
        json_result = self.client.friendships.show.get(source_id=sid, target_id=tid, access_token=self.access_token)
        if json_result['source']['following']:
            return True
        return False

    def following(self, uid):
        ''' following someone 
            @uid following user id
        '''
        self.client.friendships.create.post(uid=uid, access_token=self.access_token)

    def post(self, text, pic=''):
        ''' post a status 
            @text  post content
            @pic   the pic path
        '''
        text_encode = urllib.urlencode(text)
        if pic:
            f = open(pic, 'rb')
            self.client.statuses.upload.post(pic=f, status=text_encode, access_token=self.access_token)
        else:
            self.client.statuses.update.post(status=text_encode, access_token=self.access_token)

    def repost(self, id, text=''):
        ''' repost a status by status id, and add a comment 
            @id : status id
            @text : comment
        '''
        if text:
            text_encode = urllib.urlencode(text)
            self.client.statuses.repost.post(id=id, status=text_encode, access_token=self.access_token)
        else:
            self.client.statuses.repost.post(id=id, access_token=self.access_token)
    
    def get_user_id(self):
        ''' get user info '''    
        json_result = self.client.account.get_uid.get(access_token=self.access_token)
        return json_result['uid'] 

    def get_screen_name(self, id)
        ''' get user screen name by id '''
        json_result = self.client.users.show.get(access_token=self.access_token, uid=id)
        return json_result['screen_name']

def test():
    #初始化API
    wa = Weibo_API(APP_KEY, APP_SECRET, CALLBACK_URL)
    #获取跳转URL
    url = wa.jump_url
    #等待授权，获取code
    # code = request.POST.get('code', '')
    code = 'xxxx'
    #获取access_token
    wa.get_access_token(code)
    #使用API
    wa.is_follower(SOURCE_ID, 'target id') #是否关注
    wa.following('target id') #关注
    wa.post('微博内容') #发微博
    wa.post('微博内容', pic='图片路径') #带图片
    wa.repost('微博id') #转发微博
    wa.repost(WEIBO_STATUS_ID, text='评论信息') #带评论
    

if __name__ == '__main__':
    test()

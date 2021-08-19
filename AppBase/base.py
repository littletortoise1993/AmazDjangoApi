from django.shortcuts import render, redirect
from AppBase.models import UserDict
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
import copy
import json
import os
import sys
from django.conf import settings
import subprocess
from django.db.models import Q
from django.db.models import F
from django.core.paginator import Paginator
from django.views import View
from django.utils.decorators import method_decorator
from django.http import QueryDict
import time
import hmac
import base64
#判断用户是否登陆
def checkLogin(func):
    def wrapper(request, *args, **kwargs):
        token_user = request.headers.get("token", "")
        token=token_user.split(":")[0]
        username = token_user.split(":")[1]
        if not out_token(username, token):
            return nologinResponseCommon({}, "未登录")
        else:
            user = UserDict.objects.get(username=username)
            request.user = user
            return func(request, *args, **kwargs)
    return wrapper





def get_token(key, expire=3600):
    '''
    :param key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
    :param expire: int(最大有效时间，单位为s)
    :return: token
    '''
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")+":"+key

def out_token(key, token):
    '''
    :param key: 服务器给的固定key
    :param token: 前端传过来的token
    :return: true,false
    '''

    # token是前端传过来的token字符串
    try:
        token_str = base64.urlsafe_b64decode(token).decode('utf-8')
        token_list = token_str.split(':')
        if len(token_list) != 2:
            return False
        ts_str = token_list[0]
        if float(ts_str) < time.time():
            # token expired
            return False
        known_sha1_tsstr = token_list[1]
        sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
        calc_sha1_tsstr = sha1.hexdigest()
        if calc_sha1_tsstr != known_sha1_tsstr:
            # token certification failed
            return False
        # token certification success
        return True
    except Exception as e:
        return False




def successResponseCommon(data, message="success"):
    return HttpResponse(json.dumps({"code": 0, "data": data, "msg": message}, ensure_ascii=False), content_type="application/json")

def errorResponseCommon(data, message):
    return HttpResponse(json.dumps({"code": 1, "data": data, "msg": message}, ensure_ascii=False), content_type="application/json")

def failedResponseCommon(code,data, message="failed"):
    return HttpResponse(json.dumps({"code": code, "data": data, "msg": message}, ensure_ascii=False), content_type="application/json")

def nologinResponseCommon(data, message):
    return HttpResponse(json.dumps({"code": 401, "data": data, "msg": message}, ensure_ascii=False), content_type="application/json")

def notFoundResponseCommon(data, message):
    return HttpResponse(json.dumps({"code": 404, "data": data, "msg": message}, ensure_ascii=False), content_type="application/json")

def timeConverStr(timepar):
    return timepar.strftime('%Y-%m-%d %H:%M:%S')


# encoding: utf-8
'''
 @author :我不是大佬 
 @contact:2869210303@qq.com
 @wx     ;safeseaa
 @qq     ;2869210303
 @github ;https://github.com/U202142209
 @blog   ;https://blog.csdn.net/V123456789987654 
 @file   :SetJsonResponse.py
 @time   :2023/12/17 21:33
  '''
import datetime
import traceback

import jwt
from django.http import JsonResponse
from rest_framework.response import Response


def setErrorResponse(msg, code=500):
    return JsonResponse({
        "code": code,
        "msg": msg, "data": [],
    }, json_dumps_params={'ensure_ascii': False},
        content_type="application/json; charset=utf-8")


def setSuccessResponse(msg="ok", data=None):
    return JsonResponse({
        "code": 200,
        "msg": msg,
        "data": data,
    },
        json_dumps_params={'ensure_ascii': False},
        content_type="application/json; charset=utf-8")


def setMyJson(msg="ok", data=None):
    return Response({
        "code": 200,
        "msg": msg,
        "data": data,
    },
        content_type="application/json; charset=utf-8")


def setMyError(msg, code=500):
    return JsonResponse({
        "code": code,
        "msg": msg, "data": [],
    }, content_type="application/json; charset=utf-8")

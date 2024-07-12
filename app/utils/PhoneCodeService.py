# encoding: utf-8
'''
 @author :我不是大佬 
 @contact:2869210303@qq.com
 @wx     ;safeseaa
 @qq     ;2869210303
 @github ;https://github.com/U202142209
 @blog   ;https://blog.csdn.net/V123456789987654 
 @file   :PhoneCodeService.py
 @time   :2024/1/4 14:13
  '''

import datetime
import hashlib
import json
import random
import time

import requests
from django.conf import settings


def get_header():
    appkey = "settings.WANGYIYUNXIN_APPID"
    appsecret = "settings.WANGYIYUNXIN_APPSECRTE"
    nonce = random.randint(10000, 100000000)
    ctime = datetime.datetime.utcnow()
    curtime = str(int(time.mktime(ctime.timetuple())))
    s = appsecret + str(nonce) + curtime
    checksum = hashlib.sha1(s.encode('utf-8')).hexdigest()
    Content_Type = "application/x-www-form-urlencoded;charset=utf-8"
    header = {'Content-Type': Content_Type, 'AppKey': appkey, 'Nonce': str(nonce), 'CurTime': curtime,
              'CheckSum': checksum}
    return header


# 发送短信验证码
def sendPhoneVerificationCodeByRequests(phone_number):
    # 调试模式
    if settings.DEBUG:
        return True, "000000"
    url = "https://api.netease.im/sms/sendcode.action"
    res = requests.post(
        url=url,
        headers=get_header(),
        data={
            'mobile': str(phone_number),
            'codeLen': 6
        }).json()
    # print("发送验证码：", res)
    if res["code"] == 200:
        return True, res["obj"]
    return False, res.get("msg", "短信验证发发送失败")


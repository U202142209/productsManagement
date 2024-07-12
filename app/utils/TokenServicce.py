# -*- coding: UTF-8 -*-
'''
 @author :我不是大佬 
 @contact:2869210303@qq.com
 @wx     ;safeseaa
 @qq     ;2869210303
 @github ;https://github.com/U202142209
 @blog   ;https://blog.csdn.net/V123456789987654 
 @file   :TokenServicce.py
 @time   :2023/12/26 14:52
  '''

import jwt
import datetime
from django.conf import settings

TOKEN_secret_key = settings.TOKEN_SECRET_KEY



def generate_token(payload, expire_time=60, secret_key=TOKEN_secret_key):
    """
    expire_time:token的失效事件，默认60秒
    """
    # 设置token的过期时间
    expire_datetime = datetime.datetime.utcnow() + datetime.timedelta(seconds=expire_time)
    # 添加过期时间到payload中
    payload['exp'] = expire_datetime
    # 生成token
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


if __name__ == '__main__':
    token = generate_token(
        payload={
            "username": "username"
        }, expire_time=60 * 60
    )
    print(token)


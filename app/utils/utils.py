# encoding: utf-8
'''
 @author :我不是大佬 
 @contact:2869210303@qq.com
 @wx     ;safeseaa
 @qq     ;2869210303
 @github ;https://github.com/U202142209
 @blog   ;https://blog.csdn.net/V123456789987654 
 @file   :utils.py
 @time   :2024/1/30 18:01
  '''

import random
import re
from datetime import datetime


def get_nid():
    """产生随机数字"""
    return datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))


def isValidPhoneNumber(tel):
    # 由于手机号位数大于11位也能匹配成功，所以修改如下：
    ret = re.match(r"^1[3456789]\d{9}$", tel)
    if ret:
        return True
    else:
        return False

# encoding: utf-8
'''
 @author :我不是大佬 
 @contact:2869210303@qq.com
 @wx     ;safeseaa
 @qq     ;2869210303
 @github ;https://github.com/U202142209
 @blog   ;https://blog.csdn.net/V123456789987654 
 @file   :UserController.py
 @time   :2024/1/30 17:44
  '''

from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User, Group, Quyu
from ..utils.SetJsonResponse import setSuccessResponse, setErrorResponse
from ..utils.TokenServicce import generate_token
from ..utils.utils import isValidPhoneNumber
from ..utils.PhoneCodeService import sendPhoneVerificationCodeByRequests


# 发验证码
@require_POST  # 仅限于post请求
@csrf_exempt  # 去除csrf token认证
def sendPhoneCode(request):
    phone_number = request.POST.get("phone_number", "")
    if not (phone_number and isValidPhoneNumber(phone_number)):
        return setErrorResponse("请输入合法的手机号")
    # 发送验证码
    # 一个手机号五分钟只能发送一次短信验证
    data = cache.get('sended_' + str(phone_number))
    if data:
        return setErrorResponse(f"已经向手机号：{phone_number} 发送了验证码，五分钟内只能发送一次")
    # 这里执行发送手机验证码的函数
    flag, code_or_msg = sendPhoneVerificationCodeByRequests(phone_number)
    if flag:
        print("手机验证码发送成功")
        # 已经发送了手机验证码，加入缓存
        cache.set('sended_' + str(phone_number), code_or_msg, timeout=5 * 60)  # 五分钟有效

        return setSuccessResponse(msg="验证码已发送", data="ok")
    print("手机验证码发送失败")
    return setErrorResponse(code_or_msg)


# 注册
@require_POST  # 仅限于post请求
@csrf_exempt  # 去除csrf token认证
def register(request):
    print(request.POST)
    pwd = request.POST.get("pwd", "")
    if len(pwd) < 5:
        return setErrorResponse("请输入长度不小于5的密码")
    group = request.POST.get("group", "")
    if not group:
        return setErrorResponse("请选择组别")
    # 检查组别是否存在
    g = Group.objects.filter(name=group).first()
    if not g:
        return setErrorResponse("组别不正确")
    quyu = request.POST.get("quyu", "")
    if not quyu:
        return setErrorResponse("请选择区域")
    # 检查组别是否存在
    y = Quyu.objects.filter(name=quyu).first()
    if not y:
        return setErrorResponse("区域不正确")
    name = request.POST.get("name", "")
    if not name:
        return setErrorResponse("请输入姓名")
    phone_number = request.POST.get("phone_number", "")
    phone_code = request.POST.get("phone_code", "aa")
    if not (phone_number and isValidPhoneNumber(phone_number)):
        return setErrorResponse("请输入有效的手机号")
    # 查询短信验证码
    if not cache.get('sended_' + str(phone_number)):
        return setErrorResponse("请先获取短信验证码")
    # 验证短信是否正确
    if str(cache.get('sended_' + str(phone_number))) != str(phone_code):
        return setErrorResponse("短信验证码不正确")
    # 查询用户
    # 判断用户是否存在
    if User.objects.filter(phone_number=phone_number).exists():
        return setErrorResponse("此手机号已经注册，请直接去登录")
    # 创建新用户
    u = User.objects.create(
        group=g,
        quyu=y,
        name=name,
        phone_number=phone_number,
        pwd=pwd
    )
    token = generate_token(
        payload={"phone_number": phone_number},
        expire_time=60 * 60 * 24 * 7)
    return setSuccessResponse(msg="ok", data={"token": token})


# http://127.0.0.1:8000/api/login/?phone_number=13333333333
@require_POST  # 仅限于post请求
@csrf_exempt  # 去除csrf token认证
def login(request):
    phone_number = request.POST.get("phone_number", "")
    print(phone_number)
    if not (phone_number and isValidPhoneNumber(phone_number)):
        return setErrorResponse("请输入合法的手机号")
    pwd = request.POST.get("pwd", "")
    u = User.objects.filter(phone_number=phone_number, pwd=pwd)
    if not u:
        return setErrorResponse("手机号或者密码错误")
    token = generate_token(
        payload={
            "phone_number": phone_number},
        expire_time=60 * 60 * 24 * 7)
    return setSuccessResponse(msg="登录成功", data={"token": token})

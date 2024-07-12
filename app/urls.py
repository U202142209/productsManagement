# encoding: utf-8
'''
 @author :我不是大佬 
 @contact:2869210303@qq.com
 @wx     ;safeseaa
 @qq     ;2869210303
 @github ;https://github.com/U202142209
 @blog   ;https://blog.csdn.net/V123456789987654 
 @file   :urls.py
 @time   :2024/1/28 20:02
  '''

from django.urls import path

from . import views
from .views import submit, api_c_ap, api_c_sxt, indexView, getSxtOpinions, getGroupAndQuyu, submit_fangan, \
    export_as_excel
from .Controller.UserController import sendPhoneCode, register, login

urlpatterns = [
    path('myfasc', views.fascView.as_view()),
    # 页面
    path("index/", indexView, name="indexView"),
    # 动态获取摄像头参数
    path("getSxtOpinions/", getSxtOpinions, name="getSxtOpinions"),
    # 获取组别和区域
    path("getGroupAndQuyu/", getGroupAndQuyu, name="getGroupAndQuyu"),

    path("submit/", submit, name="submit"),
    # 提交方案
    path("submit_fangan/", submit_fangan, name="submit_fangan"),
    path("export_as_excel/", export_as_excel, name="export_as_excel"),

    path("apiCap/", api_c_ap, name="apiCap"),
    path("apiCsxt/", api_c_sxt, name="apiCsxt"),
    # 用户
    path("sendPhoneCode/", sendPhoneCode, name="sendPhoneCode"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),

]

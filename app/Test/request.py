# encoding: utf-8
"""
 @author :我不是大佬
 @contact:2869210303@qq.com
 @wx     ;safeseaa
 @qq     ;2869210303
 @github ;https://github.com/U202142209
 @blog   ;https://blog.csdn.net/V123456789987654
 @file   :request.py
 @time   :2024/1/29 20:13
  """

import requests
import json


def printDict(res):
    print(str(res).replace("\'", "\""))


class Client:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.token = "sdfasf"

    # 纯摄像头方案提交
    def api_c_sxt(self):
        return requests.post(
            url=self.base_url + "/api/apiCsxt/",
            data={
                "sxt_number": 4,  # sxt数量
                "sxt_factory": "",  # sxt品牌
                "sxt_classify": 2,  # sxt分类
                "sxt_yeshi": 1,  # sxt 夜视
                "sxt_px": 400,  # sxt 像素
                "sxt_ccfs": 1,  # sxt 存储方式,硬盘还是SD卡
                "sxt_ccsc": 7,  # sxt 存储时长/天,是用来计算硬盘大小
                "ap_number": 0,  # AP数量
                "ap_factory": "",  # AP品牌
                "ap_classify": 2,  # AP分类
                "ap_wifi_level": 6,  # AP wifi几代
                "ap_color": "",  # AP颜色
                "wifi_sulv": 1500,  # AP 连接速率
                "user_number": 100,  # 用户数
            }
        ).json()

    def submit(self):
        return requests.post(
            url=self.base_url + "/api/submit/",
            headers={
                "Authorization": "Bear " + self.token,
            },
            data={
                "sxt_number": 4,  # sxt数量
                "sxt_factory": "",  # sxt品牌
                "sxt_classify": 2,  # sxt分类
                "sxt_yeshi": 1,  # sxt 夜视
                "sxt_px": 400,  # sxt 像素
                "sxt_ccfs": 1,  # sxt 存储方式,硬盘还是SD卡
                "sxt_ccsc": 7,  # sxt 存储时长/天,是用来计算硬盘大小
                "ap_number": 0,  # AP数量
                "ap_factory": "",  # AP品牌
                "ap_classify": 2,  # AP分类
                "ap_wifi_level": 6,  # AP wifi几代
                "ap_color": "",  # AP颜色
                "wifi_sulv": 1500,  # AP 连接速率
                "user_number": 100,  # 用户数
            }
        ).json()

    def sendPhoneCode(self):
        return requests.post(
            url=self.base_url + "/api/sendPhoneCode/",
            data={"phone_number": "13333333333", }
        ).json()

    def register(self):
        return requests.post(
            url=self.base_url + "/api/register/",
            data={
                "name": "张三",
                "phone_number": "13333333333",
                "pwd": "11111111",
                "group": "第一组",
                "quyu": "北京",
                "phone_code": "000000",
            }
        ).json()

    def login(self):
        return requests.post(
            url=self.base_url + "/api/login/",
            data={
                "phone_number": "13333333333",
                "pwd": "11111111",
            }
        ).json()

    # 提交方案
    def submit_fangan(self, content):
        return requests.post(
            url=self.base_url + "/api/submit_fangan/",
            headers={
                "Authorization": "Bear " + self.token,
            },
            data={
                "content": content,
                "name": "这是方案名称",
            }
        ).json()


if __name__ == '__main__':
    c = Client()
    c.sendPhoneCode()
    register_res = c.register()
    if register_res["code"] == 200:
        token = register_res["data"]["token"]
    else:
        # 登录
        login_res = c.login()
        if login_res["code"] == 200:
            c.token = login_res["data"]["token"]
            # 测试提交方案
            submit_res = c.submit()["data"]
            printDict(submit_res)
            # 提交方案
            res = c.submit_fangan(
                content=str(submit_res)
            )
            printDict(
                res
            )

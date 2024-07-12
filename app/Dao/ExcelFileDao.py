# encoding: utf-8
'''
 @author :我不是大佬
 @contact:2869210303@qq.com
 @wx     ;safeseaa
 @qq     ;2869210303
 @github ;https://github.com/U202142209
 @blog   ;https://blog.csdn.net/V123456789987654
 @file   :ExcelFileDao.py
 @time   :2024/1/29 16:08
  '''
import os

import pandas as pd
from django.db import transaction

from ..models import Factory, ApInfo, LyqInfo, JhjInfo, SxtInfo, NVRInfo, YinPanInfo, SDCardInfo, JiGuiInfo, DateExcel, \
    XiancaiInfo, FucaiInfo, XsqInfo, FenLeiInfo


def c_or_u_m_by_pk(Model, product_kind, factory_name):
    m = Model.objects.filter(product_kind=product_kind).first()
    if m:
        return m
    return Model.objects.create(
        product_kind=product_kind,
        factory=create_or_update_factory(factory_name)
    )


# 自己写的
def c_or_u_m_by_name(Model, name_dl):
    m = Model.objects.filter(name_dl=name_dl).first()
    if m:
        return m
    return Model.objects.create(
        name_dl=name_dl,
    )


def create_or_update_factory(factory_name):
    f = Factory.objects.filter(name=factory_name).first()
    if not f:
        print("factory 不存在")
        return Factory.objects.create(name=factory_name)
    return f


# 更新价格
def updatePrice(apInfo, item):
    apInfo.jinhuojia = item["进货价"]
    apInfo.yunwei = item["集成运维费"]
    apInfo.xiaoshoujia = item["销售价"]
    apInfo.city_e_price = item["城区施工电信单价"]
    apInfo.v_e_price = item["农村施工电信单价"]
    apInfo.city_f_price = item["城区施工员工单价"]
    apInfo.v_f_price = item["农村施工员工单价"]


@transaction.atomic
def create_or_update_data_by_excel(res):
    with transaction.atomic():
        # ApInfo
        for item in res["ApInfo"]:
            apInfo = c_or_u_m_by_pk(ApInfo, item["产品型号"], item["品牌厂商"])
            apInfo.classify = apInfo.getClassifyByText(item["产品类型"])
            apInfo.canshu_gaiyao = item["参数概要"]
            apInfo.gonghuo_fangshi = apInfo.getGongHuoFangShi(item["供货方式"])
            apInfo.color = item["颜色"]
            apInfo.lianjie_sulv = item["连接速率Mbps"]
            apInfo.wifi_level = item["wifi几"]
            apInfo.gongdian_fangshi = apInfo.getGongDianFangShi(item["供电方式"])
            apInfo.w = item["整机功耗/W"]
            updatePrice(apInfo, item)
            apInfo.save()
            print("更新 ApInfo by ", item["产品型号"])
        # LyqInfo
        for item in res["LyqInfo"]:
            m = c_or_u_m_by_pk(LyqInfo, item["产品型号"], item["品牌厂商"])
            m.classify = m.getClassifyByText(item["产品类型"])
            m.canshu_gaiyao = item["参数概要"]
            m.gonghuo_fangshi = m.getGongHuoFangShi(item["供货方式"])
            m.daijialiang = item["典型带机量"]
            m.ap_number = item["可管理AP数"]
            m.wuxian_canshu = item["无线参数"]
            m.wamgkou_leixing = m.getWangkouLeixing(item["网口类型"])
            m.WAN_LAN = item["WAN/LAN可变"]
            m.POE = item["POE口"]
            m.Console = item["Console口"]
            m.PoE_w = item["PoE总功率"]
            updatePrice(m, item)
            m.save()
            print("更新 LyqInfo by ", item["产品型号"])
        # JhjInfo
        for item in res["JhjInfo"]:
            m = c_or_u_m_by_pk(JhjInfo, item["产品型号"], item["品牌厂商"])
            m.classify = m.getClassifyByText(item["产品类型"])
            m.canshu_gaiyao = item["参数概要"]
            m.gonghuo_fangshi = m.getGongHuoFangShi(item["供货方式"])
            m.is_poe = m.get_is_poe(item["是否POE交换机"])
            m.port_number = item["端口总数"]
            m.upstream_number = item["上联端口数"]
            m.lan_number = item["lan端口数"]
            m.poe_number = item["POE端口数"]
            m.guang_mokuai = item["光模块口"]
            m.Console = item["Console口"]
            updatePrice(m, item)
            m.save()
            print("更新 JhjInfo by ", item["产品型号"])

        # SxtInfo
        for item in res["SxtInfo"]:
            m = c_or_u_m_by_pk(SxtInfo, item["产品型号"], item["品牌厂商"])
            m.classify = m.getClassifyByText(item["产品类型"])
            m.canshu_gaiyao = item["参数概要"]
            m.gonghuo_fangshi = m.getGongHuoFangShi(item["供货方式"])
            m.SD = m.get_SD(item["SD卡"])
            m.is_4G = m.get_is_4G(item["4G"])
            m.shuangxiang_yuyin = m.get_shuangxiang_yuyin(item["双向语音"])
            m.yeshi = m.gie_yeshi(item["夜视"])
            m.jiaoju = item["焦距mm"]
            m.px = item["像素"]
            m.w = item["功耗"]
            m.gongdian_fangshi = m.getGongDianFangShi(item["供电方式"])
            updatePrice(m, item)
            m.save()
            print("更新 SxtInfo by ", item["产品型号"])

        # NVRInfo
        for item in res["NVRInfo"]:
            m = c_or_u_m_by_pk(NVRInfo, item["产品型号"], item["品牌厂商"])
            m.classify = m.getClassifyByText(item["产品分类"])
            m.canshu_gaiyao = item["参数概要"]
            m.gonghuo_fangshi = m.getGongHuoFangShi(item["供货方式"])
            m.jierunshu = item["最大接入"]
            m.yingpanwei = item["硬盘位"]
            m.max_v = item["单盘最大容量"]
            m.is_poe = m.git_is_poe(item["是否POE录像机"])
            updatePrice(m, item)
            m.save()
            print("更新 NVRInfo by ", item["产品型号"])

        # YinPanInfo
        for item in res["YinPanInfo"]:
            m = c_or_u_m_by_pk(YinPanInfo, item["产品型号"], item["品牌厂商"])
            m.classify = m.getClassifyByText(item["产品分类"])
            m.canshu_gaiyao = item["参数概要"]
            m.gonghuo_fangshi = m.getGongHuoFangShi(item["供货方式"])
            m.yp_dx = item["硬盘大小T"]
            updatePrice(m, item)
            m.save()
            print("更新 YinPanInfo by ", item["产品型号"])

        # SDCardInfo
        for item in res["SDCardInfo"]:
            m = c_or_u_m_by_pk(SDCardInfo, item["产品型号"], item["品牌厂商"])
            m.classify = m.getClassifyByText(item["产品分类"])
            m.canshu_gaiyao = item["参数概要"]
            m.gonghuo_fangshi = m.getGongHuoFangShi(item["供货方式"])
            updatePrice(m, item)
            m.save()
            print("更新 SDCardInfo by ", item["产品型号"])

        # JiGuiInfo
        for item in res["JiGuiInfo"]:
            m = c_or_u_m_by_pk(JiGuiInfo, item["产品型号"], item["品牌厂商"])
            m.classify = m.getClassifyByText(item["产品分类"])
            m.canshu_gaiyao = item["参数概要"]
            m.gonghuo_fangshi = m.getGongHuoFangShi(item["供货方式"])
            updatePrice(m, item)
            m.save()
            print("更新 JiGuiInfo by ", item["产品型号"])

        # XiancaiInfo
        for item in res["XiancaiInfo"]:
            m = c_or_u_m_by_pk(XiancaiInfo, item["产品型号"], item["品牌厂商"])
            m.classify = m.getClassifyByText(item["产品类型"])
            m.canshu_gaiyao = item["参数概要"]
            m.gonghuo_fangshi = m.getGongHuoFangShi(item["供货方式"])
            m.classify_fl = item["选择分类"]
            updatePrice(m, item)
            m.save()
            print("更新 XiancaiInfo by ", item["产品型号"])

        # FucaiInfo
        for item in res["FucaiInfo"]:
            m = c_or_u_m_by_pk(FucaiInfo, item["产品型号"], item["品牌厂商"])
            m.classify = item["产品类型"]
            m.canshu_gaiyao = item["参数概要"]
            m.gonghuo_fangshi = m.getGongHuoFangShi(item["供货方式"])
            m.classify_fl = item["选择分类"]
            updatePrice(m, item)
            m.save()
            print("更新 FucaiInfo by ", item["产品型号"])

        # XsqInfo
        for item in res["XsqInfo"]:
            m = c_or_u_m_by_pk(XsqInfo, item["产品型号"], item["品牌厂商"])
            m.classify = item["产品类型"]
            m.canshu_gaiyao = item["参数概要"]
            m.gonghuo_fangshi = m.getGongHuoFangShi(item["供货方式"])
            m.classify_fl = item["选择分类"]
            updatePrice(m, item)
            m.save()
            print("更新 XsqInfo by ", item["产品型号"])

        # FenLeiInfo
        for item in res["FenLeiInfo"]:
            m = c_or_u_m_by_name(FenLeiInfo, item["商品大类"])
            m.name_form = item["数据库表名"]
            m.save()
            print("更新 FenLeiInfo by ", item["商品大类"])

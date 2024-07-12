import os
import random
from datetime import datetime

from django.core.validators import FileExtensionValidator
from django.db import models
from django.dispatch import receiver

from .utils.utils import get_nid


class MyModel(models.Model):
    field_name = models.CharField(max_length=100)


class Factory(models.Model):
    name = models.CharField(verbose_name="品牌厂商", max_length=100)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="最近编辑时间", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "管理 / 品牌厂商"
        verbose_name_plural = "管理 / 品牌厂商"


class FenLeiInfo(models.Model):
    name_dl = models.CharField(verbose_name="商品大类", max_length=100)
    name_form = models.CharField(verbose_name="数据库表名", max_length=100, default="1")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="最近编辑时间", auto_now=True)

    def __str__(self):
        return self.name_dl

    class Meta:
        verbose_name = "管理 / 商品大类"
        verbose_name_plural = "管理 / 商品大类"


# 抽象类
class AbstructModel(models.Model):
    product_kind = models.CharField(
        verbose_name="产品型号", max_length=100)
    # factory = models.SmallIntegerField(
    #     verbose_name="品牌厂商",
    #     default="普联",
    #     choices=(
    #         (1, "普联"), (2, "锐捷"),
    #         (3, "华三"), (4, "华为"),
    #         (5, "希捷"), (6, "无")
    #     ))
    factory = models.ForeignKey(
        verbose_name="品牌厂商",
        to=Factory,
        on_delete=models.CASCADE
    )
    gonghuo_fangshi = models.SmallIntegerField(
        verbose_name="供货方式",
        choices=(
            (1, "标品"), (2, "市采"), (3, "省采")
        ), default=1
    )
    canshu_gaiyao = models.TextField(verbose_name="参数概要", default="..")

    # 产品价格
    jinhuojia = models.DecimalField(verbose_name="进货价", default=0, max_digits=10, decimal_places=2)
    yunwei = models.DecimalField(verbose_name="集成运维费", default=0, max_digits=10, decimal_places=2)
    xiaoshoujia = models.DecimalField(verbose_name="销售价", default=0, max_digits=10, decimal_places=2)
    city_e_price = models.DecimalField(verbose_name="城区施工电信单价", default=0, max_digits=10, decimal_places=2)
    v_e_price = models.DecimalField(verbose_name="农村施工电信单价", default=0, max_digits=10, decimal_places=2)
    city_f_price = models.DecimalField(verbose_name="城区施工员工单价", default=0, max_digits=10, decimal_places=2)
    v_f_price = models.DecimalField(verbose_name="农村施工员工单价", default=0, max_digits=10, decimal_places=2)

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="最近编辑时间", auto_now=True)
    z_index = models.PositiveSmallIntegerField(verbose_name="排序规则，越小越排在前面（取值大于0）", default=100)

    def getGongHuoFangShi(self, text):
        if text == "标品":
            return 1
        elif text == "市采":
            return 2
        elif text == "省采":
            return 3
        raise Exception("供货方式不正确")

    def getGongDianFangShi(self, text):
        if str(text).upper() == "POE/DC":
            return 1
        elif str(text).upper() == "POE":
            return 2
        elif str(text).upper() == "DC":
            return 3
        raise Exception("供电方式不正确")

    class Meta:
        abstract = True
        ordering = ['z_index']


# AP表
class ApInfo(AbstructModel):
    classify_choices = (
        (1, "面板式AP"),
        (2, "吸顶式AP")
    )
    classWiFi_choices = (
        (5, "5"), (6, "6"), (7, "7")
    )
    classify = models.SmallIntegerField(
        verbose_name="产品类型",
        choices=classify_choices, default=1)
    color = models.CharField(verbose_name="颜色", max_length=100, default="...")
    lianjie_sulv = models.SmallIntegerField(verbose_name="连接速率Mbps", default=0)
    wifi_level = models.SmallIntegerField(
        verbose_name="wifi几",
        choices=classWiFi_choices, default=6
    )
    gongdian_fangshi = models.SmallIntegerField(
        verbose_name="供电方式",
        choices=(
            (1, "POE/DC"), (2, "POE"), (3, "DC")
        ), default=1
    )
    w = models.FloatField(verbose_name="整机功耗,W", default=0)

    def getClassifyByText(self, text):
        if text == "面板式AP":
            return 1
        elif text == "吸顶式AP":
            return 2
        raise Exception("产品类型不正确")

    def to_dict(self, number: int):
        # 计算
        return {
            "设备类型": self.get_classify_display(),
            "型号": self.product_kind,
            "参数概要": self.canshu_gaiyao,
            "数量": number,
            "单位": "台",
            "设备单价": self.xiaoshoujia,
            "设备小计": self.xiaoshoujia * number,
            "施工费": self.city_e_price * number,
            "备注": self.get_gonghuo_fangshi_display(),

            # "factory": self.factory.name,
            # "gonghuo_fangshi": self.gonghuo_fangshi,
            #
            # "classify": self.classify,
            #
            # "color": self.color,
            # "lianjie_sulv": self.lianjie_sulv,
            # "wifi_level": self.wifi_level,
            # "wifi_level_label": self.get_wifi_level_display(),
            # "gongdian_fangshi": self.gongdian_fangshi,
            # "gongdian_fangshi_label": self.get_gongdian_fangshi_display(),
            # "w": self.w,
            # # ge'zhong价格
            # "jinhuojia": self.jinhuojia,
            # "yunwei": self.yunwei,
            # "city_e_price": self.city_e_price,
            # "v_e_price": self.v_e_price,
            # "city_f_price": self.city_f_price,
            # "v_f_price": self.v_f_price,
            # "update_time": str(self.update_time),
            # "create_time": str(self.create_time),
            # #
        }

    class Meta:
        verbose_name = "管理 / AP"
        verbose_name_plural = "管理 / AP"


# 路由器
class LyqInfo(AbstructModel):
    classify = models.SmallIntegerField(
        verbose_name="产品类型",
        choices=(
            (1, "一体化"),
            (2, "企业路由"),
            (3, "桌面路由")
        ),
        default=1
    )
    daijialiang = models.SmallIntegerField(verbose_name="典型带机量", default=100)
    ap_number = models.SmallIntegerField(verbose_name="可管理AP数", default=50)
    wuxian_canshu = models.BooleanField(verbose_name="无线参数", default=False)
    wamgkou_leixing = models.SmallIntegerField(
        verbose_name="网口类型",
        choices=(
            (1, "千兆"),
            (2, "百兆")
        ), default=1)
    WAN_LAN = models.SmallIntegerField(verbose_name="WAN/LAN可变", default=0)
    POE = models.SmallIntegerField(verbose_name="POE口", default=0)
    Console = models.BooleanField(verbose_name="Console口", default=False)
    PoE_w = models.SmallIntegerField(verbose_name="PoE总功率/单口功率", default=0)

    def getClassifyByText(self, text):
        if text == "一体化":
            return 1
        elif text == "企业路由":
            return 2
        elif text == "桌面路由":
            return 3
        raise Exception("产品类型不正确")

    def getWangkouLeixing(self, text):
        if text == "千兆":
            return 1
        elif text == "百兆":
            return 2
        raise Exception("网口类型不正确")

    def to_dict(self, number: int):
        # 计算
        return {
            "设备类型": self.get_classify_display(),
            "型号": self.product_kind,
            "参数概要": self.canshu_gaiyao,
            "数量": number,
            "单位": "台",
            "设备单价": self.xiaoshoujia,
            "设备小计": self.xiaoshoujia * number,
            "施工费": self.city_e_price * number,
            "备注": self.get_gonghuo_fangshi_display(),

        }

    class Meta:
        verbose_name = "管理 / 路由器"
        verbose_name_plural = "管理 / 路由器"


# 交换机
class JhjInfo(AbstructModel):
    classify = models.SmallIntegerField(
        verbose_name="产品类型",
        choices=(
            (1, "普通百兆"),
            (1, "普通百兆"),
            (2, "普通千兆"),
            (3, "POE百兆"),
            (4, "POE千兆"),
            (5, "三层交换")
        ), default=1)

    is_poe = models.BooleanField(verbose_name="是否POE交换机", default=False)
    port_number = models.SmallIntegerField(verbose_name="端口总数", default=0)
    upstream_number = models.SmallIntegerField(verbose_name="上联端口数", default=0, help_text="独立的上联口")
    lan_number = models.SmallIntegerField(verbose_name="lan端口数", default=0)
    poe_number = models.SmallIntegerField(verbose_name="POE端口数", default=0)
    guang_mokuai = models.SmallIntegerField(verbose_name="光模块口", default=0)
    Console = models.BooleanField(verbose_name="Console口", default=False)
    PoE_w = models.SmallIntegerField(verbose_name="PoE总功率W", default=0)

    def getClassifyByText(self, text):
        if text == "普通百兆":
            return 1
        elif text == "普通千兆":
            return 2
        elif text == "POE百兆":
            return 3
        elif text == "POE千兆":
            return 4
        elif text == "三层交换":
            return 5
        raise Exception("产品类型不正确")

    def get_is_poe(self, text):
        if text == "是":
            return True
        elif text == "否":
            return False
        raise Exception("是否POE交换机 输入不正确")

    def to_dict(self, number: int):
        # 计算
        return {
            "设备类型": self.get_classify_display(),
            "型号": self.product_kind,
            "参数概要": self.canshu_gaiyao,
            "数量": number,
            "单位": "台",
            "设备单价": self.xiaoshoujia,
            "设备小计": self.xiaoshoujia * number,
            "施工费": self.city_e_price * number,
            "备注": self.get_gonghuo_fangshi_display(),

        }

    class Meta:
        verbose_name = "管理 / 交换机"
        verbose_name_plural = "管理 / 交换机"


# 摄像头
class SxtInfo(AbstructModel):
    classify_choices = (
        (1, "半球"),
        (2, "枪机"),
        (3, "球机"),
    )
    classify = models.SmallIntegerField(
        verbose_name="产品类型",
        choices=classify_choices, default=2)

    SD = models.SmallIntegerField(
        verbose_name="SD卡",
        choices=(
            (1, "不支持"),
            (2, "32"),
            (3, "64"),
            (4, "128"),
            (5, "256"),
            (6, "512")
        ), default=1
    )
    is_4G = models.BooleanField(verbose_name="是否支持4G", default=False)
    shuangxiang_yuyin = models.BooleanField(verbose_name="双向语音", default=False)
    yeshi_choices = ((1, "红外"), (2, "全彩"))
    yeshi = models.SmallIntegerField(
        verbose_name="夜视",
        choices=yeshi_choices, default=1
    )
    jiaoju = models.CharField(
        verbose_name="焦距mm", max_length=300, default="4mm"
    )
    px = models.SmallIntegerField(verbose_name="像素", default=400)
    w = models.FloatField(verbose_name="功耗", default=0)
    gongdian_fangshi = models.SmallIntegerField(
        verbose_name="供电方式",
        choices=(
            (1, "POE/DC"),
            (2, "POE"),
            (3, "DC")
        ), default=1
    )

    # 处理产品类型
    def getClassifyByText(self, text):
        if text == "半球":
            return 1
        elif text == "枪机":
            return 2
        elif text == "球机":
            return 3
        raise Exception("产品类型不正确")

    def gie_yeshi(self, text):
        if text == "红外":
            return 1
        elif text == "全彩":
            return 2
        raise Exception("夜视类型输入不正确")

    # 处理SD卡
    def get_SD(self, text):
        if text == "不支持":
            return 1
        elif text == 32:
            return 2
        elif text == 64:
            return 3
        elif text == 128:
            return 4
        elif text == 256:
            return 5
        elif text == 512:
            return 6
        raise Exception("SD卡不正确")

    # 处理是否支持4G卡的bool类型
    def get_is_4G(self, text):
        if text == 1:
            return True
        elif text == 0:
            return False
        raise Exception("是否支持4G卡 输入不正确")

    # 处理是否支持双向语音 的bool类型
    def get_shuangxiang_yuyin(self, text):
        if text == 1:
            return True
        elif text == 0:
            return False
        raise Exception("是否支持双向语音 输入不正确")

    def to_dict(self, haomishu, number: int):
        # 计算
        return {
            "设备类型": self.get_classify_display() + haomishu,
            "型号": self.product_kind,
            "参数概要": self.canshu_gaiyao,
            "数量": number,
            "单位": "台",
            "设备单价": self.xiaoshoujia,
            "设备小计": self.xiaoshoujia * number,
            "施工费": self.city_e_price * number,
            "备注": self.get_gonghuo_fangshi_display(),

        }

    class Meta:
        verbose_name = "管理 / 摄像头"
        verbose_name_plural = "管理 / 摄像头"


# NVR
class NVRInfo(AbstructModel):
    classify = models.SmallIntegerField(
        verbose_name="产品分类",
        choices=(
            (1, "4路NVR"),
            (2, "8路NVR"),
            (3, "16路NVR"),
            (4, "32路NVR"),
            (5, "64路NVR")
        ), default=1)
    jierunshu = models.SmallIntegerField(verbose_name="最大接入", default=4)
    yingpanwei = models.SmallIntegerField(verbose_name="硬盘位", default=1)
    max_v = models.CharField(verbose_name="单盘最大容量", max_length=100, default="10T")
    is_poe = models.BooleanField(verbose_name="是否POE录像机", default=False)

    def getClassifyByText(item, text):
        if text == "4路NVR":
            return 1
        elif text == "8路NVR":
            return 2
        elif text == "16路NVR":
            return 3
        elif text == "32路NVR":
            return 4
        elif text == "64路NVR":
            return 5
        raise Exception("是否支持双向语音 输入不正确")

    def git_is_poe(self, text):
        if text == "是":
            return True
        elif text == "否":
            return False
        raise Exception("是否POE录像机 输入不正确")

    def to_dict(self, number: int):
        # 计算
        return {
            "设备类型": self.get_classify_display(),
            "型号": self.product_kind,
            "参数概要": self.canshu_gaiyao,
            "数量": number,
            "单位": "台",
            "设备单价": self.xiaoshoujia,
            "设备小计": self.xiaoshoujia * number,
            "施工费": self.city_e_price * number,
            "备注": self.get_gonghuo_fangshi_display(),

        }

    class Meta:
        verbose_name = "管理 / NVR"
        verbose_name_plural = "管理 / NVR"


# 硬盘
class YinPanInfo(AbstructModel):
    classify = models.SmallIntegerField(
        verbose_name="产品类型",
        choices=(
            (1, "1T"),
            (2, "2T"),
            (3, "4T"),
            (4, "6T"),
            (5, "8T"),
        ), default=1)
    yp_dx = models.SmallIntegerField(verbose_name="硬盘大小T", default=1)

    def getClassifyByText(item, text):
        if text == "1T":
            return 1
        elif text == "2T":
            return 2
        elif text == "4T":
            return 3
        elif text == "6T":
            return 4
        elif text == "8T":
            return 5
        raise Exception("硬盘分类 输入不正确")

    def to_dict(self, number: int):
        # 计算
        return {
            "设备类型": self.get_classify_display(),
            "型号": self.product_kind,
            "参数概要": self.canshu_gaiyao,
            "数量": number,
            "单位": "块",
            "设备单价": self.xiaoshoujia,
            "设备小计": self.xiaoshoujia * number,
            "施工费": self.city_e_price * number,
            "备注": self.get_gonghuo_fangshi_display(),

        }

    class Meta:
        verbose_name = "管理 / 硬盘"
        verbose_name_plural = "管理 / 硬盘"


# SD卡
class SDCardInfo(AbstructModel):
    classify = models.SmallIntegerField(
        verbose_name="产品类型",
        choices=(
            (1, "32G"),
            (2, "64G"),
            (3, "128G"),
            (4, "256G"),
            (5, "512G")
        ), default=1)

    def getClassifyByText(item, text):
        if text == "32G":
            return 1
        elif text == "64G":
            return 2
        elif text == "128G":
            return 3
        elif text == "256G":
            return 4
        elif text == "512G":
            return 5
        raise Exception("SD卡分类 输入不正确")

    def to_dict(self, number: int):
        # 计算
        return {
            "设备类型": self.get_classify_display(),
            "型号": self.product_kind,
            "参数概要": self.canshu_gaiyao,
            "数量": number,
            "单位": "台",
            "设备单价": self.xiaoshoujia,
            "设备小计": self.xiaoshoujia * number,
            "施工费": self.city_e_price * number,
            "备注": self.get_gonghuo_fangshi_display(),

        }

    class Meta:
        verbose_name = "管理 / SD卡"
        verbose_name_plural = "管理 / SD卡"


# 机柜
class JiGuiInfo(AbstructModel):
    classify = models.SmallIntegerField(
        verbose_name="产品类型",
        choices=(
            (1, "4U机柜"),
            (2, "6U机柜"),
            (3, "9U机柜"),
            (4, "12U机柜"),
            (5, "18U机柜"),
            (6, "32U机柜")
        ), default=1)

    def getClassifyByText(item, text):
        if text == "4U机柜":
            return 1
        elif text == "6U机柜":
            return 2
        elif text == "9U机柜":
            return 3
        elif text == "12U机柜":
            return 4
        elif text == "18U机柜":
            return 5
        elif text == "32U机柜":
            return 6
        raise Exception("机柜分类 输入不正确")

    def to_dict(self, number: int):
        # 计算
        return {
            "设备类型": self.get_classify_display(),
            "型号": self.product_kind,
            "参数概要": self.canshu_gaiyao,
            "数量": number,
            "单位": "台",
            "设备单价": self.xiaoshoujia,
            "设备小计": self.xiaoshoujia * number,
            "施工费": self.city_e_price * number,
            "备注": self.get_gonghuo_fangshi_display(),

        }

    class Meta:
        verbose_name = "管理 / 机柜"
        verbose_name_plural = "管理 / 机柜"


# 线村数据表
class XiancaiInfo(AbstructModel):
    classify = models.SmallIntegerField(
        verbose_name="产品类型",
        choices=(
            (1, "网线"),
            (2, "光皮"),
            (3, "光缆"),
            (4, "电源线"),
        ), default=2)
    classify_fl = models.CharField(verbose_name="选择分类", max_length=100)

    def getClassifyByText(item, text):
        if text == "网线":
            return 1
        elif text == "光皮":
            return 2
        elif text == "光缆":
            return 3
        elif text == "电源线":
            return 4
        raise Exception("线材分类 输入不正确")

    def to_dict(self, number: int):
        # 计算
        return {
            "设备类型": self.get_classify_display(),
            "型号": self.product_kind,
            "参数概要": self.canshu_gaiyao,
            "数量": number,
            "单位": "台",
            "设备单价": self.xiaoshoujia,
            "设备小计": self.xiaoshoujia * number,
            "施工费": self.city_e_price * number,
            "备注": self.get_gonghuo_fangshi_display(),

        }

    class Meta:
        verbose_name = "管理 / 线材"
        verbose_name_plural = "管理 / 线材"


# 辅材数据表
class FucaiInfo(AbstructModel):
    classify = models.CharField(verbose_name="产品类型", max_length=100)
    classify_fl = models.CharField(verbose_name="选择分类", max_length=100)

    def to_dict(self, number: int):
        # 计算
        return {
            "设备类型": self.classify,
            "型号": self.product_kind,
            "参数概要": self.canshu_gaiyao,
            "数量": number,
            "单位": "台",
            "设备单价": self.xiaoshoujia,
            "设备小计": self.xiaoshoujia * number,
            "施工费": self.city_e_price * number,
            "备注": self.get_gonghuo_fangshi_display(),

        }

    class Meta:
        verbose_name = "管理 / 辅材"
        verbose_name_plural = "管理 / 辅材"


# 辅材数据表
class XsqInfo(AbstructModel):
    classify = models.CharField(verbose_name="产品类型", max_length=100)
    classify_fl = models.CharField(verbose_name="选择分类", max_length=100)

    def to_dict(self, number: int):
        # 计算
        return {
            "设备类型": self.classify,
            "型号": self.product_kind,
            "参数概要": self.canshu_gaiyao,
            "数量": number,
            "单位": "台",
            "设备单价": self.xiaoshoujia,
            "设备小计": self.xiaoshoujia * number,
            "施工费": self.city_e_price * number,
            "备注": self.get_gonghuo_fangshi_display(),

        }

    class Meta:
        verbose_name = "管理 / 显示器"
        verbose_name_plural = "管理 / 显示器"


# 上传excel文件
class DateExcel(models.Model):
    excelFile = models.FileField(
        verbose_name="上传.xlsx文件",
        upload_to="excel/", validators=[FileExtensionValidator(['xlsx'])],
        max_length=1000)
    description = models.TextField(
        verbose_name="文件备注（选填）",
        default="请上传excel文件")
    filename = models.CharField(verbose_name="文件名（程序自动填写）", max_length=250, default="程序自动填写")
    hash_value = models.CharField(verbose_name="文件哈希值", max_length=300, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="最近编辑时间", auto_now=True)

    def __str__(self):
        return str(self.filename)

    class Meta:
        verbose_name = "文件 / 上传.xlsx文件导入数据"
        verbose_name_plural = "文件 / 上传.xlsx文件导入数据"


# 通过django的信号机制实现自动删除EXCEL文件
@receiver(models.signals.post_delete, sender=DateExcel)
def auto_delete_file(sender, instance, **kwargs):
    if instance.excelFile:
        if os.path.isfile(instance.excelFile.path):
            os.remove(instance.excelFile.path)
            print("成功删除文件：" + instance.excelFile.path)
        else:
            print("删除文件失败:路径不存在", instance.excelFile.path)


# 区域表
class Quyu(models.Model):
    name = models.CharField(verbose_name="区域名称", max_length=100)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="最近编辑时间", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "管理 / 区域"
        verbose_name_plural = "管理 / 区域"


# 班组名
class Group(models.Model):
    name = models.CharField(verbose_name="组名", max_length=100, unique=True)
    quyu = models.ForeignKey(verbose_name="区域", to=Quyu, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="最近编辑时间", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "管理 / 班组"
        verbose_name_plural = "管理 / 班组"


# 用户表
class User(models.Model):
    group = models.ForeignKey(verbose_name="班组", to=Group, on_delete=models.CASCADE)
    quyu = models.ForeignKey(verbose_name="区域", to=Quyu, on_delete=models.CASCADE)

    is_group_vip = models.BooleanField(verbose_name="是否为组长", default=False)
    is_quyu_vip = models.BooleanField(verbose_name="是否为区域管理", default=False)

    is_management_vip = models.BooleanField(verbose_name="是否为方案审核专员", default=False)

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="最近编辑时间", auto_now=True)

    name = models.CharField(verbose_name="人员姓名", max_length=100)
    phone_number = models.CharField(verbose_name="手机号", max_length=20)
    pwd = models.CharField(verbose_name="密码", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "管理 / 人员"
        verbose_name_plural = "管理 / 人员"


# 方案表
class Management(models.Model):
    content = models.JSONField(verbose_name="方案内容")
    user = models.ForeignKey(verbose_name="提交方案的用户", to=User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="方案名称", max_length=200)
    nid = models.CharField(max_length=20, verbose_name="编号", default=get_nid())
    status = models.SmallIntegerField(
        verbose_name="审核状态",
        choices=(
            (1, "未审核"),
            (2, "审核通过"),
            (3, "审核失败")
        ),
        default=1
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(verbose_name="最近编辑时间", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "管理 / 方案"
        verbose_name_plural = "管理 / 方案"

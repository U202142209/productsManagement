import hashlib
import os
import traceback

from django.contrib import admin
from django.utils.html import format_html
from openpyxl.workbook import Workbook

from .models import ApInfo, LyqInfo, JhjInfo, SxtInfo, NVRInfo, YinPanInfo, SDCardInfo, JiGuiInfo, DateExcel, Factory, \
    XiancaiInfo, FucaiInfo, XsqInfo, FenLeiInfo, Group, Quyu, User, Management
from .utils.ExcelReader import addDataByExcelFile


# 品牌商家
@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "update_time", "create_time")
    search_fields = ["name"]


# 商品大类表
@admin.register(FenLeiInfo)
class FenLeiInfoAdmin(admin.ModelAdmin):
    list_display = (
        "name_dl", "name_form",
        "update_time", "create_time")
    search_fields = ["name_dl"]


# ap表显示字段设置
@admin.register(ApInfo)
class ApInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product_kind", "factory", "gonghuo_fangshi", "classify", "color", "lianjie_sulv", "wifi_level", "w",
        "xiaoshoujia", "update_time", "create_time")
    search_fields = ["product_kind", "factory", "gonghuo_fangshi", "classify", "color", "lianjie_sulv", "wifi_level",
                     "w","xiaoshoujia", ]


# 路器表显示字段设置
@admin.register(LyqInfo)
class LyqInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product_kind", "factory", "classify", "daijialiang", "ap_number", "wuxian_canshu", "wamgkou_leixing",
        "WAN_LAN", "POE", "Console", "PoE_w", "xiaoshoujia", "gonghuo_fangshi", "update_time", "create_time")
    search_fields = ["product_kind", "factory", "classify", "daijialiang", "ap_number", "wuxian_canshu",
                     "wamgkou_leixing", "WAN_LAN", "POE", "Console", "PoE_w", "xiaoshoujia", ]


# 交换机表显示字段设置
@admin.register(JhjInfo)
class JhjInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product_kind", "factory", "classify", "is_poe", "upstream_number", "lan_number", "poe_number", "guang_mokuai",
        "Console", "PoE_w", "gonghuo_fangshi", "xiaoshoujia", "update_time", "create_time")
    search_fields = ["product_kind", "factory", "classify", "is_poe", "upstream_number", "lan_number", "poe_number",
                     "guang_mokuai", "Console", "PoE_w", "xiaoshoujia", ]


# 摄像头表显示字段设置
@admin.register(SxtInfo)
class SxtInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product_kind", "factory", "classify", "SD", "is_4G", "shuangxiang_yuyin", "yeshi", "jiaoju", "px", "w",
        "gongdian_fangshi", "gonghuo_fangshi", "xiaoshoujia", "update_time", "create_time")
    search_fields = ["product_kind", "factory", "classify", "SD", "is_4G", "shuangxiang_yuyin", "yeshi", "jiaoju", "px",
                     "w", "gongdian_fangshi", "xiaoshoujia", ]


# 录像机表显示字段设置
@admin.register(NVRInfo)
class NVRInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product_kind", "factory", "classify", "jierunshu", "yingpanwei", "is_poe", "gonghuo_fangshi", "xiaoshoujia",
        "update_time",
        "create_time")
    search_fields = ["product_kind", "factory", "classify", "yingpanwei", "is_poe", "gonghuo_fangshi", "xiaoshoujia", ]


# 硬盘表显示字段设置
@admin.register(YinPanInfo)
class YinPanInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product_kind", "factory", "factory", "classify", "gonghuo_fangshi", "yp_dx", "xiaoshoujia", "update_time",
        "create_time")
    search_fields = ["product_kind", "factory", "classify", "gonghuo_fangshi", "xiaoshoujia", ]


# SD卡表显示字段设置
@admin.register(SDCardInfo)
class SDCardInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product_kind", "factory", "classify", "gonghuo_fangshi", "xiaoshoujia", "update_time", "create_time")
    search_fields = ["product_kind", "factory", "classify", "gonghuo_fangshi", "xiaoshoujia", ]


# 机柜表显示字段设置
@admin.register(JiGuiInfo)
class JiGuiInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product_kind", "factory", "gonghuo_fangshi", "xiaoshoujia", "update_time", "create_time")
    search_fields = ["product_kind", "factory", "gonghuo_fangshi", "xiaoshoujia", ]


# 线材表显示字段设置
@admin.register(XiancaiInfo)
class XiancaiInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product_kind", "factory", "gonghuo_fangshi", "classify", "classify_fl", "xiaoshoujia", "update_time",
        "create_time")
    search_fields = ["product_kind", "factory", "gonghuo_fangshi", "classify", "classify_fl", "xiaoshoujia", ]


# 辅材表显示字段设置
@admin.register(FucaiInfo)
class FucaiInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product_kind", "factory", "gonghuo_fangshi", "classify", "classify_fl", "xiaoshoujia", "update_time",
        "create_time")
    search_fields = ["product_kind", "factory", "gonghuo_fangshi", "classify", "classify_fl", "xiaoshoujia", ]


# 显示器表显示字段设置
@admin.register(XsqInfo)
class XsqInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product_kind", "factory", "gonghuo_fangshi", "classify_fl", "xiaoshoujia", "update_time", "create_time")
    search_fields = ["product_kind", "factory", "gonghuo_fangshi", "classify", "classify_fl", "xiaoshoujia", ]


# 班组表
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name", "create_time", "update_time",
    )
    search_fields = ["name", "create_time", "update_time", ]


# 区域表
@admin.register(Quyu)
class QuyuAdmin(admin.ModelAdmin):
    list_display = (
        "name", "create_time", "update_time",
    )
    search_fields = ["name", "create_time", "update_time", ]


# 用户表
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "name", "phone_number", "quyu", "group", "is_group_vip", "is_quyu_vip", "is_management_vip", "create_time",
        "update_time",
    )
    search_fields = ["name", "phone_number", "quyu", "group", "is_group_vip", "is_quyu_vip", "is_management_vip",
                     "create_time",
                     "update_time", ]


# 方案保存表
@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = (
        "nid", "user", "name", "status", "export_as_excel", "create_time", "update_time",
    )
    search_fields = ["nid", "user", "name", "status", "content", "create_time", "update_time", ]

    # 自定义导出为excel
    def export_as_excel(self, obj):
        filename = f"P{obj.user.name}-{obj.name}"
        return format_html('<a target="_blank"  href="{}">下载方案</a>',
                           "/api/export_as_excel?id=" + str(obj.id))

    export_as_excel.short_description = "导出Excel"


# 上传excel工作溥导入数据库相关
@admin.register(DateExcel)
class DateExcelAdmin(admin.ModelAdmin):
    list_display = ("filename", "description", "update_time", "create_time")

    def save_model(self, request, obj, form, change):
        file_path = obj.excelFile.path  # 获取上传文件的路径
        file_name = os.path.basename(file_path)  # 获取文件名
        # 检查是否有相同文件名的文件
        if DateExcel.objects.filter(excelFile__exact=file_name).exclude(pk=obj.pk).exists():
            os.remove(file_path)  # 如果存在，删除之前的文件
            print("已经删除了之前的文件：" + file_path)
        # 执行保存操作
        super().save_model(request, obj, form, change)
        file = form.cleaned_data['excelFile']
        obj.hash_value = hashlib.md5(file.read()).hexdigest()
        file_path = obj.excelFile.path
        # 获取上传文件的文件名
        obj.filename = os.path.basename(file_path)
        super().save_model(request, obj, form, change)
        try:
            addDataByExcelFile(os.path.basename(file_path))
        except Exception as e:
            obj.delete()
            traceback.print_exc()
            self.message_user(request, str(e), level='ERROR')
            return

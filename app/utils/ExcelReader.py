# encoding: utf-8
'''
 @author :我不是大佬 
 @contact:2869210303@qq.com
 @wx     ;safeseaa
 @qq     ;2869210303
 @github ;https://github.com/U202142209
 @blog   ;https://blog.csdn.net/V123456789987654 
 @file   :ExcelReader.py
 @time   :2024/1/29 15:46
  '''
import os

import pandas as pd

from ..Dao.ExcelFileDao import create_or_update_data_by_excel


def addDataByExcelFile(rarfilename):
    # 构建完整文件路径
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../media/excel")
    assert os.path.exists(file_path)
    excelFilePath = os.path.normpath(os.path.join(file_path, rarfilename))
    assert os.path.exists(excelFilePath)
    # 开始解析文件
    res = readExcelData(filePath=excelFilePath)
    create_or_update_data_by_excel(res)


def readExcelData(filePath="data.xlsx"):
    label = [
        {
            "sheet_name": "ApInfo",
            "columns": [
                "产品型号", "品牌厂商", "产品类型", "参数概要", "供货方式",
                "颜色", "连接速率Mbps", "wifi几", "供电方式", "整机功耗/W",
                "进货价", "集成运维费", "销售价", "城区施工电信单价", "农村施工电信单价",
                "城区施工员工单价", "农村施工员工单价"
            ]
        },
        {
            "sheet_name": "LyqInfo",
            "columns": [
                "产品型号", "品牌厂商", "产品类型", "参数概要", "供货方式",
                "典型带机量", "可管理AP数", "无线参数", "网口类型", "WAN/LAN可变", "LAN口",
                "POE口", "Console口", "PoE总功率",
                "进货价", "集成运维费", "销售价", "城区施工电信单价", "农村施工电信单价",
                "城区施工员工单价", "农村施工员工单价"
            ]
        },
        {
            "sheet_name": "JhjInfo",
            "columns": [
                "产品型号", "品牌厂商", "产品类型", "参数概要", "供货方式", "是否POE交换机", "端口总数", "上联端口数",
                "lan端口数", "POE端口数", "光模块口", "Console口", "PoE总功率W", "进货价", "集成运维费", "销售价",
                "城区施工电信单价", "农村施工电信单价", "城区施工员工单价", "农村施工员工单价"
            ]
        },
        {
            "sheet_name": "SxtInfo",
            "columns": [
                "产品型号", "品牌厂商", "产品类型", "参数概要", "供货方式", "SD卡", "4G", "双向语音", "夜视", "焦距mm",
                "像素", "功耗", "供电方式", "进货价", "集成运维费", "销售价", "城区施工电信单价", "农村施工电信单价",
                "城区施工员工单价", "农村施工员工单价"
            ]
        },
        {
            "sheet_name": "NVRInfo",
            "columns": [
                "产品型号", "品牌厂商", "产品分类", "参数概要", "供货方式", "最大接入", "硬盘位", "单盘最大容量", "是否POE录像机",
                "进货价", "集成运维费", "销售价", "城区施工电信单价", "农村施工电信单价", "城区施工员工单价", "农村施工员工单价"
            ]
        },
        {
            "sheet_name": "YinPanInfo",
            "columns": [
                "产品型号", "品牌厂商", "产品分类", "参数概要", "供货方式", "硬盘大小T", "进货价", "集成运维费", "销售价",
                "城区施工电信单价", "农村施工电信单价", "城区施工员工单价", "农村施工员工单价"
            ]
        },
        {
            "sheet_name": "SDCardInfo",
            "columns": [
                "产品型号", "品牌厂商", "产品分类", "参数概要", "供货方式", "进货价", "集成运维费", "销售价",
                "城区施工电信单价", "农村施工电信单价", "城区施工员工单价", "农村施工员工单价"
            ]
        },
        {
            "sheet_name": "JiGuiInfo",
            "columns": [
                "产品型号", "品牌厂商", "产品分类", "参数概要", "供货方式", "进货价", "集成运维费", "销售价",
                "城区施工电信单价", "农村施工电信单价", "城区施工员工单价", "农村施工员工单价"
            ]
        },
        {
            "sheet_name": "XiancaiInfo",
            "columns": [
                "产品型号", "品牌厂商", "产品类型", "参数概要", "供货方式", "选择分类", "进货价", "集成运维费", "销售价",
                "城区施工电信单价", "农村施工电信单价", "城区施工员工单价", "农村施工员工单价"
            ]
        },
        {
            "sheet_name": "FucaiInfo",
            "columns": [
                "产品型号", "品牌厂商", "产品类型", "参数概要", "供货方式", "选择分类", "进货价", "集成运维费",
                "销售价",
                "城区施工电信单价", "农村施工电信单价", "城区施工员工单价", "农村施工员工单价"
            ]
        },
        {
            "sheet_name": "XsqInfo",
            "columns": [
                "产品型号", "品牌厂商", "产品类型", "参数概要", "供货方式", "选择分类", "进货价", "集成运维费",
                "销售价",
                "城区施工电信单价", "农村施工电信单价", "城区施工员工单价", "农村施工员工单价"
            ]
        },
        {
            "sheet_name": "FenLeiInfo",
            "columns": [
                "商品大类", "数据库表名",
            ]
        },
    ]
    data = {}
    for label_item in label:
        data[label_item["sheet_name"]] = []
        df = pd.read_excel(filePath, sheet_name=label_item["sheet_name"]).convert_dtypes()
        for index, row in df.iterrows():
            items = {"idx": index}
            for c in label_item["columns"]:
                items[c] = row[c]
            data[label_item["sheet_name"]].append(items)
    return data


def printDict(res):
    print(str(res).replace("\'", "\""))


if __name__ == '__main__':
    filename = r"D:\代码\python\PycharmProjects\django项目\productsManagement\产品(2).xlsx"
    res = readExcelData(
        filePath=filename
    )
    printDict(
        res
    )

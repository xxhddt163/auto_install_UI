'''
Author: xxh
coding: utf-8
Date: 2021-08-03 18:14:38
LastEditTime: 2022-09-21 23:54:30
FilePath: \PYQT\scripts\menu.py
'''
from os.path import join
from scripts.PriorityQueue import PriorityQueue


def menu_to_file(path, choose):
    """
    将选择的程序转换成文件
    :param choose: 选择的软件
    :param path: 文件保存路径
    :return: None
    """
    with open(join(path, "menu.ini"), "w") as menu_file:
        pri = PriorityQueue()       # 优先级队列

        for name in choose:
            if name in ['DX', 'NF3', 'VCRedist']:
                pri.push(name, 1)
                continue
            if name == 'Xunlei':
                pri.push(name, 50)
                continue
            if name == 'baidu_Netdisk':
                pri.push(name, 49)
                continue
            if name == 'Chrome':
                pri.push(name, 48)
                continue
            if name == 'Winrar':
                pri.push(name, 47)
                continue
            pri.push(name, 5)
            
        choose = pri.to_list()
        menu_file.write("、".join(choose))


def menu_format(choice_list):
    """将中文选单格式为菜单简写名"""

    menu_dir = {"微信": "Wechat",
                "Net Framework3": "NF3",
                "360驱动大师": "360drv",
                "谷歌浏览器": "Chrome",
                "腾讯视频": "TXvideo",
                "爱奇艺(推荐)": "IQIYI",
                "DirectX9": "DX",
                "网易云音乐": "163music",
                "搜狗输入法": "SougouPY",
                "QQ音乐": "QQmusic",
                "钉钉": "Dtalk",
                "酷狗音乐(推荐)": "Kugou",
                "联想软件商店": "Lensto",
                "CorelDRAW 2020": "cdr2020",
                "WPS(推荐)": "WPS",
                "After Effects CC2019": "AECC2019",
                "天正建筑T20": "T20",
                "PhotoShop CS3": "PSCS3",
                "PhotoShop CC2019": "PSCC2019",
                "Office 2021 专业增强版": "OFFICE2021LTSC",
                "Premiere CC2020": "PRCC2020",
                "迅雷11": "Xunlei",
                "Adobe indesign CC2021": "ID2021",
                "百度网盘": "baidu_Netdisk",
                "Adobe illustrator 2021": "AI2021",
                "Adobe Acrobat DC 2021": "DC2021"
                }

    menu_temp = choice_list.copy()
    for item in menu_temp:
        if item in menu_dir:
            menu_temp[menu_temp.index(item)] = menu_dir[item]
    return menu_temp

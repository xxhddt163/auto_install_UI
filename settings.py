'''
Author: xxh
coding: utf-8
Date: 2022-09-01 01:58:37
LastEditTime: 2022-11-06 13:04:20
FilePath: \PYQT\settings.py
'''
class Setting():
    def __init__(self):
        self.year = "2022"
        self.month = "12"
        self.host = "wanghuoyao.top"
        self.user = "root"
        self.port = 9003
        self.password = ".,?!920414"
        self.database = "test"
        self.update_url = ["http://wanghuoyao.top:9006/main_ui.exe", "http://wanghuoyao.top:9006/rename.exe"]
        self.headers = {'User-Agent': 'UI Update'}
        self.filename = ['Update_temp.exe','rename_temp.exe', 'filename_temp.txt']
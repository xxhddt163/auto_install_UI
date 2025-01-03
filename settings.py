'''
Author: xxh
coding: utf-8
Date: 2022-09-01 01:58:37
LastEditTime: 2022-11-06 13:04:20
FilePath: \PYQT\settings.py
'''
class Setting():
    def __init__(self):
        self.year = "2025"
        self.month = "01"
        self.host = "liuzidan.top"
        self.user = "root"
        self.port = 9003
        self.password = ".,?!920414"
        self.database = "test"
        self.update_url = ["http://liuzidan.top:9006/main_ui.exe", "http://liuzidan.top:9006/auto_install.exe", "http://liuzidan.top:9006/rename.exe"]
        self.headers = {'User-Agent': 'UI Update'}
        self.filename = ['main_ui.exe', 'auto_install.exe','rename_temp.exe', 'filename_temp.txt']      # 缓存文件一直都放在末尾2个
        self.tempfile_name = self.filename[-2:]    # 所有缓存文件
        self.checkfile_name = self.filename[:2]     # 每次更新完需要检查md5的文件
        self.download_path = 'temp'
        
'''
Author: xxh
coding: utf-8
Date: 2021-08-03 18:14:38
LastEditTime: 2022-09-21 19:43:24
FilePath: \PYQT\thread.py
'''
import zipfile
import win32con
import win32api
import os
import traceback
import sys
import shutil
# import time

from PyQt5.QtCore import *
from log import Logger

# def run_time(f):
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         f(*args, **kwargs)
#         print(time.time() - start)
#     return wrapper


def error_log(f):
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            logfile = os.path.join(os.getcwd(), 'error.log')        # 错误日志
            log = Logger(logfile).logger
            log.error(f"{e.args}:--->{traceback.format_exc()}")
            sys.exit(1)
    return wrapper


class New_Thread(QThread):  # 用作执行多线程的类 需要继承QThread类
    """多线程解压文件"""
    finishSignal = pyqtSignal(str)
    programsSignal = pyqtSignal(bool)

    def __init__(self, programs, path, parent=None,):
        super(New_Thread, self).__init__(parent)
        self.programs = programs
        self.path = path
        self.result = False  # 判断线程是否执行结束的标记

    # @run_time
    @error_log
    def run(self):
        zip_file = zipfile.ZipFile("auto_install.zip", "r")
        for _ in self.programs:
            check = False
            self.finishSignal.emit(str(_))  # j解压之前先修改lineEdit信息
            for name in zip_file.namelist():
                root_dir_name = os.path.dirname(name).split(
                    '/')[1] if len(os.path.dirname(name).split('/')) > 1 else os.path.dirname(name).split('/')[0]

                if _ not in root_dir_name:
                    if check:
                        break
                    continue
                if _ == root_dir_name or f"{_}_shot" in root_dir_name:
                    check = True
                    zip_file.extract(name, self.path)
            self.programsSignal.emit(True)      # 解压完一个程序修改一次进度

        zip_file.extract('auto_install.exe', self.path)
        zip_file.extract('app_pkg/sound/run_click.wav', self.path)
        if not os.path.isfile(os.path.join(self.path, 'setup.ico')):
            zip_file.extract('setup.ico', self.path)
        win32api.SetFileAttributes(os.path.join(
            self.path, 'setup.ico'), win32con.FILE_ATTRIBUTE_HIDDEN)
        
        if os.path.isfile(os.path.join(os.getcwd(),'auto_install.exe')):    # install文件热替换
            shutil.copy(os.path.join(os.getcwd(),'auto_install.exe'), os.path.join(self.path, 'auto_install.exe'))
            win32api.SetFileAttributes(os.path.join(
            self.path, 'auto_install.exe'), win32con.FILE_ATTRIBUTE_NORMAL)
            
        zip_file.close()
        self.result = True
        self.finishSignal.emit(str(_))



if __name__ == '__main__':
    n = New_Thread(['Wechat'],'D:\\python-projects\\PYQT\\1')
    n.run()
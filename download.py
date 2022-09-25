from PyQt5.QtCore import QThread, pyqtSignal
from settings import Setting
import requests
import sys
import os


class Download(QThread):
    file_size = pyqtSignal(float)     # 文件总大小
    now_download = pyqtSignal(float)        # 当前下载大小
    pland = pyqtSignal(float)                 # 下载进度
    end = pyqtSignal(bool)           # 程序下载完毕发送的信号

    def __init__(self):
        super().__init__()
        s = Setting()
        self.total = 0          # 已下载的大小
        self.url = s.update_url  # 文件下载地址
        self.chunk_size = 1024  # 单次请求最大值

    def run(self):
        """下载文件到当前目录"""
        try:
            r = requests.get(self.url, stream=True)
            content_size = int(r.headers['content-length'])  # 内容体总大小
            self.file_size.emit(
                float(f'{content_size / 1024 / 1024 :.2f}'))       # 提交文件总大小
            download_dir = os.getcwd()
            with open(os.path.join(download_dir, "unzip_2.exe"), "wb") as f:
                for date in r.iter_content(chunk_size=self.chunk_size):
                    f.write(date)
                    self.total += self.chunk_size
                    self.now_download.emit(
                        float(f'{self.total / 1024 / 1024 :.2f}'))       # # 提交当前下载文件大小
                    # 提交下载的百分比
                    self.pland.emit(
                        float(f'{self.total / content_size * 100 :.2f}'))
                self.end.emit(True)
        except requests.ConnectionError:
            sys.exit()

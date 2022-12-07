'''
Author: xxh
coding: utf-8
Date: 2022-09-01 14:36:00
LastEditTime: 2022-10-27 01:04:49
FilePath: \PYQT\download.py
'''
from __future__ import annotations
from PyQt5.QtCore import QThread, pyqtSignal
from settings import Setting
import requests
import multitasking

class Download(QThread):
    file_size = pyqtSignal(float)     # 文件总大小
    now_download = pyqtSignal(float)        # 当前下载大小
    pland = pyqtSignal(float)                 # 下载进度
    end = pyqtSignal(bool)           # 程序下载完毕发送的信号

    def split(self, start: int, end: int, step: int) -> list[tuple[int, int]]:
        """将下载的文件分块"""
        return [(start, min(start + step, end)) for start in range(0, end, step)]

    def get_file_size(self, url: str, raise_error: bool = False) -> int:
        """获取下载文件大小"""
        response = requests.head(url,headers={'User-Agent': 'Get_Size'})
        file_size = response.headers.get('Content-Length')
        if file_size is None:
            if raise_error:
                raise ValueError('该文件不支持多线程分段下载！')
            return file_size
        return int(file_size)       # 获得的文件大小单位为B

    def __init__(self):
        super().__init__()
        self.s = Setting()

    def run(self):
        """下载文件到当前目录"""
        MB = 1 * 1024 ** 2
        each_size = 16 * MB   # 每个分块按16MB进行分块
        urls = self.s.update_url  # 文件下载地址
        headers = self.s.headers
        filenames = self.s.filename
        for url, filename in zip(urls, filenames):

            with open(filename, 'wb') as f:
                file_size = self.get_file_size(url=url)
                self.file_size.emit(
                    float(f'{file_size / 1024 / 1024 :.2f}'))       # 提交文件总大小
                self.already_download = 0      # 已经下载的文件大小

                @multitasking.task      # 多线程下载模块
                def start_download(start: int, end: int) -> None:
                    _headers = headers.copy()
                    # 分段下载的核心
                    _headers['Range'] = f'bytes={start}-{end}'
                    # 发起请求并获取响应（流式）
                    response = session.get(url, headers=_headers, stream=True)
                    # 每次读取的流式响应大小
                    chunk_size = 1024
                    # 暂存已获取的响应，后续循环写入
                    chunks = []
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        # 暂存获取的响应
                        chunks.append(chunk)
                        self.already_download += chunk_size
                        self.now_download.emit(
                            float(f'{self.already_download / 1024 / 1024 :.2f}'))       # 提交当前下载文件大小
                        self.pland.emit(
                            float(f'{self.already_download / file_size * 100 :.2f}'))   # 提交下载百分比
                    f.seek(start)
                    for chunk in chunks:
                        f.write(chunk)
                    # 释放已写入的资源
                    del chunks

                session = requests.Session()
                # 分块文件如果比文件大，就取文件大小为分块大小
                each_size = min(each_size, file_size)

                # 分块
                parts = self.split(0, file_size, each_size)
                for part in parts:
                    start, end = part
                    start_download(start, end)
                # 等待全部线程结束
                multitasking.wait_for_tasks()
        self.end.emit(True)
        
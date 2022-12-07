import os
from settings import Setting
import psutil
from time import sleep
import win32api

s = Setting()


def check_program(name: str):
    """检查目标进程是否已经启动"""

    for proc in psutil.process_iter(['name']):
            if name == proc.info['name']:
                return True


def get_filename():
    with open(s.filename[2], 'r') as f:
        return f.read()


if __name__ == '__main__':
    """将下载的新文件自动重命名"""

    filename = get_filename()
    while check_program(filename):      # 检查主程序进程结束后才执行后续操作防止os.remove报错权限不足
        sleep(.5)
    
    if os.path.isfile(s.filename[0]) and os.path.isfile(filename):
        os.remove(filename)
        os.rename(s.filename[0], filename)
        sleep(.5)
        win32api.ShellExecute(0, 'open', filename, '', '', 1)   # 无cmd背景黑框打开改名后的文件

import os
from settings import Setting
import psutil, shutil
from time import sleep
import win32api

s = Setting()


def check_program(name: str):
    """检查目标进程是否已经启动"""

    for proc in psutil.process_iter(['name']):
            if name == proc.info['name']:
                return True


def get_filename():
    with open(s.filename[3], 'r') as f:
        return f.read()


if __name__ == '__main__':
    """将下载的新文件自动重命名"""

    filename = get_filename()
    while check_program(filename):      # 检查主程序进程结束后才执行后续操作防止os.remove报错权限不足
        sleep(.5)
    
    if os.path.isfile(os.path.join(os.getcwd(), 'temp', s.checkfile_name[0])) and os.path.isfile(filename):
        os.remove(filename)
        os.rename(os.path.join(os.getcwd(), 'temp', s.checkfile_name[0]), os.path.join(os.getcwd(), 'temp', filename))
        sleep(.5)
        shutil.copy(os.path.join(os.getcwd(),'temp', filename),os.path.join(os.getcwd(), filename))
        shutil.rmtree(os.path.join(os.getcwd(),'temp'))
        win32api.ShellExecute(0, 'open', filename, '', '', 1)   # 无cmd背景黑框打开改名后的文件

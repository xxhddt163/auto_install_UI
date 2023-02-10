'''
Author: xxh
coding: utf-8
Date: 2022-09-01 01:55:55
LastEditTime: 2022-10-27 01:11:50
FilePath: \PYQT\show_download_ui.py
'''
import sys
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import Qt
from download_ui import Ui_MainWindow
from download import Download
from PyQt5 import QtCore
from check_file import get_local_file_md5, Checkfile
from settings import Setting
import os
import win32con
import win32api


class Show_Download_Ui(QMainWindow, Ui_MainWindow):
    """显示下载界面"""

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.Qt.CustomizeWindowHint)          # 去掉QT程序的标题栏
        self.min = 0    # 分
        self.sec = 0    # 秒
        self.s = Setting()
        self.timer = QtCore.QTimer()
        # 时间对象到时间时触发函数showtime
        self.timer.timeout.connect(self.showtime)
        self.start()

    def starttime(self):
        """每隔1秒触发一次"""
        self.timer.start(1000)

    def stoptime(self):
        """停止计时器计时"""
        self.timer.stop()

    def showtime(self):
        """用label_2显示安装时间"""
        _translate = QtCore.QCoreApplication.translate
        self.sec += 1
        if self.sec == 60:
            self.sec = 0
            self.min += 1
        if self.sec < 9:
            self.label_2.setText(_translate(
                "MainWindow", f"{self.min}:{self.sec:02d}"))
        else:
            self.label_2.setText(_translate(
                "MainWindow", f"{self.min}:{self.sec}"))

    def check_download_md5(self, file, subcommand):       # 检查下载好的文件是否完整
        c = Checkfile()
        localmd5 = get_local_file_md5(file)
        md5 = c.get_net_md5(subcommand=subcommand)

        return localmd5 == md5

    def end(self, _):  # sourcery skip: last-if-guard
        if _:
            self.stoptime()
            if os.path.isfile(os.path.join(os.getcwd(), self.s.download_path, self.s.checkfile_name[1])):
                for name in self.s.checkfile_name:
                    if not self.check_download_md5(os.path.join(os.getcwd(), self.s.download_path, name), subcommand=f"SELECT `md5` FROM `{name.split('.')[0]}_md5`"):
                        QMessageBox.information(
                            None, "离线更新包下载失败", "离线更新包下载失败，请重新运行程序重新下载", QMessageBox.Yes)
                        sys.exit(0)
            elif not self.check_download_md5(os.path.join(os.getcwd(), self.s.download_path, self.s.filename[0]), subcommand=f"SELECT `md5` FROM `{self.s.filename[0].split('.')[0]}_md5`"):
                QMessageBox.information(
                    None, "离线更新包下载失败", "离线更新包下载失败，请重新运行程序重新下载", QMessageBox.Yes)
                sys.exit(0)

            if os.path.isfile(os.path.join(os.getcwd(), self.s.download_path, self.s.checkfile_name[1])):
                if os.path.isfile(os.path.join(os.getcwd(), self.s.checkfile_name[1])):
                    # 将老版本的隐藏文件恢复防止复制时提示权限不够
                    win32api.SetFileAttributes(
                        self.s.filename[1], win32con.FILE_ATTRIBUTE_NORMAL)

                shutil.copy(os.path.join(os.getcwd(), self.s.download_path, self.s.checkfile_name[1]), os.path.join(
                    os.getcwd(), self.s.checkfile_name[1]))
            shutil.copy(os.path.join(os.getcwd(), self.s.download_path, self.s.tempfile_name[0]), os.path.join(
                os.getcwd(), self.s.tempfile_name[0]))

            win32api.SetFileAttributes(
                self.s.tempfile_name[0], win32con.FILE_ATTRIBUTE_HIDDEN)      # 隐藏rename.exe文件

            win32api.SetFileAttributes(
                self.s.filename[1], win32con.FILE_ATTRIBUTE_HIDDEN)     # 隐藏新版的installer文件

            # 将当前文件的文件名写入filename.txt
            with open(self.s.filename[-1], 'w') as f:
                f.write(os.path.basename(sys.argv[0]))

            win32api.SetFileAttributes(
                self.s.filename[-1], win32con.FILE_ATTRIBUTE_HIDDEN)

            win32api.ShellExecute(
                0, 'open', self.s.tempfile_name[0], '', '', 0)     # 后台隐藏运行改名程序
            sys.exit(0)

    def start(self):
        self.download = Download()
        self.download.start()
        self.starttime()
        self.download.file_size.connect(self.changelabel_6_text)
        self.download.now_download.connect(self.changelabel_4_text)
        self.download.pland.connect(self.changeprogressBar_value)
        self.download.end.connect(self.end)

    def changelabel_6_text(self, value):    # 修改label数据
        _translate = QtCore.QCoreApplication.translate
        self.label_6.setText(_translate("MainWindow", f'{value}MB'))
        self.file_size = value

    def changelabel_4_text(self, value):
        _translate = QtCore.QCoreApplication.translate
        self.label_4.setText(_translate("MainWindow", f'{value}MB'))

    def changeprogressBar_value(self, value):       # 修改进度条数据
        self.progressBar.setProperty("value", value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    download_window = Show_Download_Ui()
    download_window.show()
    sys.exit(app.exec_())

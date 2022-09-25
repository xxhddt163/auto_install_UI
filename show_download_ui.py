import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import Qt
from download_ui import Ui_MainWindow
from download import Download
from PyQt5 import QtCore


class Show_Download_Ui(QMainWindow, Ui_MainWindow):
    """显示下载界面"""

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.Qt.CustomizeWindowHint)          # 去掉QT程序的标题栏
        self.min = 0    # 分
        self.sec = 0    # 秒
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

    def end(self, _):
        if _:
            self.stoptime()
            reply = QMessageBox.information(
                None, "离线更新包下载完成", "离线更新包下载完成，请用本目录下unzip_2.exe 替换本程序", QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                sys.exit()

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

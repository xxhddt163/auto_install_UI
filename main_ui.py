import contextlib
import sys
import win32con
import win32api
from os import mkdir, getcwd, remove, startfile
from os.path import isdir, join, isfile
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from thread import New_Thread
from time import strftime
from settings import Setting
from mainwindow import *
from scripts.menu import menu_format, menu_to_file
from check_file import Checkfile, UpdateInfo
from show_download_ui import Show_Download_Ui
from playsound import playsound


class MainWindow(QMainWindow, Ui_mainwindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.checkBox_26.setEnabled(False)      # 暂时关闭CDR
        self.pushButton_2.clicked.connect(self.pushButton2_clicked)  # 按下浏览按钮
        self.pushButton.clicked.connect(self.pushButton_clicked)    # 按下解压按钮
        self.radioButton_4.clicked.connect(self.radioButton_4_true)  # 按下上次选择按钮
        self.radioButton_2.clicked.connect(self.radioButton_2_true)  # 按下取消勾选按钮
        self.choose = []
        self.last_choose = []
        self.menu_dir = {'Wechat': '微信', 'NF3': 'Net Framework3', '360drv': '360驱动大师', 'Chrome': '谷歌浏览器', 'TXvideo': '腾讯视频',
                         'IQIYI': '爱奇艺(推荐)', 'DX': 'DirectX9', '163music': '网易云音乐', 'SougouPY': '搜狗输入法', 'QQmusic': 'QQ音乐',
                         'Dtalk': '钉钉', 'Kugou': '酷狗音乐(推荐)', 'Lensto': '联想软件商店', 'cdr2020': 'CorelDRAW 2020', 'WPS': 'WPS(推荐)',
                         'AECC2019': 'After Effects CC2019', 'T20': '天正建筑T20', 'PSCS3': 'PhotoShop CS3', 'PSCC2019': 'PhotoShop CC2019',
                         'OFFICE2021LTSC': 'Office 2021 专业增强版', 'PRCC2020': 'Premiere CC2020', 'Xunlei': '迅雷11', 'ID2021': 'Adobe indesign CC2021',
                         'baidu_Netdisk': '百度网盘', 'AI2021': 'Adobe illustrator 2021', 'DC2021': 'Adobe Acrobat DC 2021'}

    @staticmethod
    def load_menu() -> list:
        with open(join(getcwd(), "last.txt")) as file:
            return file.readline().split('、')

    def radioButton_2_true(self):
        for _ in range(1, 34):       # 检查checkBox1-33状态
            exec(f"self.checkBox_{_}.setChecked(False)")

    def radioButton_4_true(self):
        """按下上次选择按钮时的操作"""
        if isfile(join(getcwd(), 'last.txt')):
            last_choose = MainWindow.load_menu()
            for _ in last_choose:
                _ = int(_)
                exec(f"self.checkBox_{_}.setChecked(True)")
        else:
            QMessageBox.information(self, "上次并未有任何选择", "上次并未有任何文件的选择")

    def pushButton2_clicked(self):
        """按下浏览按钮时的操作
        """
        with contextlib.suppress(Exception):        # 防止文件目录存在中文出错
                playsound(join(getcwd(), 'run_click.wav'))
        _translate = QtCore.QCoreApplication.translate
        self.path = QFileDialog.getExistingDirectory(None, "选择文件夹路径")
        self.path = self.path.replace('/', '\\')
        if self.path != '':
            self.lineEdit.setText(_translate("mainwindow", self.path))

    def change_edit_text(self, _):
        """通过unzip传入参数修改lineEdit信息"""
        _translate = QtCore.QCoreApplication.translate
        if len(self.choose) != 0:
            self.lineEdit.setText(_translate(
                "mainwindow", f"正在解压{self.menu_dir[_] if _ in self.menu_dir else _}..."))
            self.choose.remove(self.menu_dir[_] if _ in self.menu_dir else _)
        if self.Unzip.result:  # 解压完后执行的操作
            reply = QMessageBox.information(
                self, "安装包解压完毕", "所有安装包解压完毕，点击OK按钮关闭本程序", QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                startfile(self.path)      # 解压完成后自动打开解压目录
                self.close()

    def change_progressbar(self, _):
        """修改进度"""
        self.programers_bar_value = (
            1 - len(self.choose) / self.initialValue) * 100     # 计算进度
        self.progressBar.setProperty(
            "value", self.programers_bar_value)  # 实时更改进度

    def check_directory(self):
        """[检测lineEdit上填入的目录是否存在，不存在则创建]
        """
        if not isdir(self.path):
            mkdir(self.path)

    def pushButton_clicked(self):
        """按下解压按钮执行的操作
        """
        self.path = self.lineEdit.text()
        self.frame_2.setEnabled(False)
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.lineEdit.setReadOnly(True)

        for _ in range(1, 34):       # 检查checkBox1-33状态
            exec(f'''if self.checkBox_{_}.isChecked():
                        self.choose.append(self.checkBox_{_}.text())
                        self.last_choose.append(str({_}))
                        ''')

        if len(self.choose) == 0:
            # 当用户没选择任何安装包时弹出提示并恢复解压按钮及frame2
            QMessageBox.information(self, "请选择安装包", "请选择任意要解压的安装包后继续")
            self.frame_2.setEnabled(True)
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.lineEdit.setReadOnly(False)
        else:
            if isfile(join(getcwd(), 'last.txt')):
                remove(join(getcwd(), 'last.txt'))

            # 将本次选择的checkBox存入last.txt中
            with open(join(getcwd(), "last.txt"), "w") as last_choose_file:
                last_choose_file.write("、".join(self.last_choose))

            win32api.SetFileAttributes(
                'last.txt', win32con.FILE_ATTRIBUTE_HIDDEN)      # 隐藏last.txt文件
            with contextlib.suppress(Exception):        # 防止文件目录存在中文出错
                playsound(join(getcwd(), 'run_click.wav'))       # 播放音效声音
            self.check_directory()
            menu_to_file(path=self.path, choose=menu_format(self.choose))
            self.initialValue = len(self.choose)  # 获取用户初始选择的程序数用做进度计算
            self.Unzip = New_Thread(menu_format(self.choose), self.path)
            # 将pyqt5的信号传递给self.change函数处理
            self.Unzip.finishSignal.connect(self.change_edit_text)
            self.Unzip.programsSignal.connect(self.change_progressbar)
            self.Unzip.start()  # 启动多线程


class ShowWindow():
    """用于显示主体窗口的类"""

    def __init__(self, obj_cls=MainWindow):
        self.app = QApplication(sys.argv)
        self.mainWindow = obj_cls()

    def show_window(self):
        self.mainWindow.show()
        sys.exit(self.app.exec_())

    def message(self, title, message, button):
        return QMessageBox().information(None, title, message, *button) if isinstance(button, tuple) else QMessageBox().information(None, title, message, button)


if __name__ == "__main__":
    s = Setting()
    
    # 如果存在更新留下的缓存文件则删除
    
    for _ in s.tempfile_name:
        if isfile(_):
            remove(_)
    
        
    show = ShowWindow()
    if strftime("%Y%m") == f"{s.year}{s.month}":
        show.show_window()

    c = Checkfile()         # 检查目标服务器与当前文件的md5值 只要md5值相同 就算程序过期了也能打开
    if c.check_file():      # md5验证通过的情况
        updateinfo = UpdateInfo()
        reply = show.message(title='发现新的程序版本', message=f'下载更新新版离线版(Yes)，继续以当前在线版运行(No)\n\n更新内容:\n{updateinfo.get_update_info()}', button=(
            QMessageBox.Yes, QMessageBox.No))

        if reply == QMessageBox.No:
            show.show_window()

        if reply == QMessageBox.Yes:
            show2 = ShowWindow(Show_Download_Ui)
            show2.show_window()
    else:           # 程序版本过低且MD5值与服务器不匹配
        if isfile('auto_install.zip'):
            remove('auto_install.zip')
        show.message(title='程序版本过低', message='程序版本过低且无法更新，请联系管理员',
                     button=QMessageBox.Yes)

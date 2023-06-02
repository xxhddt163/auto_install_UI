import sys
import hashlib
from PyQt5.QtWidgets import QMessageBox, QApplication
import pymysql
from settings import Setting


def get_local_file_md5(file_path):
    # sourcery skip: reintroduce-else, swap-if-else-branches, use-named-expression
    """
    计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()  # 创建md5对象
    with open(file_path, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  # 更新md5对象

    return m.hexdigest()  # 返回md5对象





class Checkfile():
   
    def __init__(self):
        s = Setting()
        try:
            self.db = pymysql.connect(host=s.host,
                            user=s.user,
                            password=s.password,
                            database=s.database,
                            port=s.port)
            
            self.cursor = self.db.cursor()
        except (AttributeError, pymysql.OperationalError):
            app = QApplication(sys.argv)
            QMessageBox().information(None,"获取MD5值失败","获取MD5值失败,请检查网络连接后重试",QMessageBox.Yes)
            sys.exit(1)
            
    def get_net_md5(self, subcommand="SELECT `md5` FROM `unzip_md5`"):
        try:
            self.cursor.execute(subcommand)
            return self.cursor.fetchall()[0][0]
        except (AttributeError, pymysql.OperationalError):
            app = QApplication(sys.argv)
            QMessageBox().information(None,"获取MD5值失败","获取MD5值失败,请检查网络连接后重试",QMessageBox.Yes)
            sys.exit(1)
            
    def check_file(self):
        # local_md5 = get_local_file_md5(sys.argv[0])
        local_md5 = "2"
        obj_md5 = self.get_net_md5()
        return local_md5 == obj_md5
    
class UpdateInfo(Checkfile):
    def __init__(self):
        super().__init__()
    
    def get_update_info(self):
        try:
            self.cursor.execute("SELECT `updateinfo` FROM `updateinfo`")
            return self.cursor.fetchall()[0][0].replace('\\n', '\n')        # 数据库中\n会自动改成\\n
        except (AttributeError, pymysql.OperationalError):
            app = QApplication(sys.argv)
            QMessageBox().information(None,"更新信息获取失败","更新信息获取失败请检查网络",QMessageBox.Yes)
            sys.exit(1)
        
    


if __name__ == '__main__':
    print(get_local_file_md5('D:\python-projects\PYQT\dist\main_ui.exe'))
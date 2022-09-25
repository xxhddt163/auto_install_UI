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


def get_net_md5(cursor):
    try:
        cursor.execute("SELECT `md5` FROM `unzip_md5`")
        return cursor.fetchall()[0][0]
    except (AttributeError, pymysql.OperationalError):
        app = QApplication(sys.argv)
        QMessageBox().information(None,"程序版本过低","程序版本过低，请联网后重新打开该程序后重试",QMessageBox.Yes)
        sys.exit(1)


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
            QMessageBox().information(None,"程序版本过低","程序版本过低，请联网后重新打开该程序后重试",QMessageBox.Yes)
            sys.exit(1)
    
    def check_file(self):
        # local_md5 = get_local_file_md5(sys.argv[0])
        local_md5 = "1"
        obj_md5 = get_net_md5(self.cursor)
        return local_md5 == obj_md5
    
    


if __name__ == '__main__':
    print(get_local_file_md5('D:\python-projects\PYQT\dist\main_ui.exe'))
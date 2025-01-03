import pymysql, hashlib

class UpdateMD5():
    """服务器上每天更新md5脚本"""
    def __init__(self):
        self.db = pymysql.connect(host = "liuzidan.top",
                        user = "root",
                        password = ".,?!920414",
                        database = "test",
                        port = 9003)
        
        self.cursor = self.db.cursor()
        self.md5 = ''
        
    def commit(self, subcommand):
        # self.sql = f"UPDATE `client` SET `Final_Date`=NOW() WHERE ProcessorId='{self.sn}'"
        self.sql = subcommand
        self.cursor.execute(self.sql)
        self.db.commit()
        
    def get_local_file_md5(self, file_path):
        
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

        self.md5 = m.hexdigest()  # 返回md5对象
    

if __name__ == '__main__':
    u = UpdateMD5()
    file_name = ['main_ui.exe', 'auto_install.exe']
    file_path = ['/usr/local/updateserver/main_ui.exe', '/usr/local/updateserver/auto_install.exe']
    for name, path in zip(file_name, file_path):
        u.get_local_file_md5(path)
        command = f"UPDATE `{name.split('.')[0]}_md5` SET `md5`='{u.md5}'"
        u.commit(command)
 
import pymysql
import readConfig as readConfig
from common.configLog import MyLog as Log

localReadConfig = readConfig.ReadConfig()
host = localReadConfig.get_db("host")
port = localReadConfig.get_db("port")
username = localReadConfig.get_db("username")
password = localReadConfig.get_db("password")
database = localReadConfig.get_db("database")

# log = Log.get_log()
# log.build_log_format()


class DB:

    def __init__(self):
        try:
            # Connect to the database
            self.connection = pymysql.connect(host=host,
                                              port=int(port),
                                              user=username,
                                              password=password,
                                              db=database,
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
            # log.build_start_line("连接数据库成功。")
        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            # log.get_logger().error("Mysql Error!")

    # 删除数据表数据
    def clear(self, table_name):
        # real_sql = "truncate table " + table_name + ";"
        real_sql = "delete from " + table_name + ";"
        with self.connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.connection.commit()

    # 插入数据表数据
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        #print(real_sql)

        with self.connection.cursor() as cursor:
            cursor.execute(real_sql)
        self.connection.commit()

    # 关闭数据库
    def close(self):
        self.connection.close()

    # 初始化数据
    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()


if __name__ == '__main__':
    db = DB()
    table_name = "sign_event"
    data = {'id':1,'name':'红米','`limit`':2000,'status':1,'address':'北京会展中心',
            'start_time':'2018-08-20','create_time':'2018-12-20'}
    table_name2 = "sign_guest"
    data2 = {'id': '1', 'realname': 'alen', 'phone': 12312341234, 'email': 'alen@mail.com', 'sign': 0,
             'create_time': '2018-12-20', 'event_id': 1}
    db.clear(table_name)
    db.insert(table_name, data)
    db.close()

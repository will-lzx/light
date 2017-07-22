import pymysql
import sys
pymysql.install_as_MySQLdb()


class MySQL:
    conn = ''
    cursor = ''

    def __init__(self, host='106.14.151.3', usr='root', pwd='Password01?', db='light'):
        try:
            self.conn = pymysql.connect(host, usr, pwd, db)
        except Exception as e:
            print(e)
            sys.exit()
        self.cursor = self.conn.cursor()

    def exec_query(self, sql):
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
        except Exception as ex:
            print('Mysql exception {0}'.format(ex))
            sys.exit()
        self.cursor.close()
        self.conn.close()
        return rows

    def exec_none_query(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            print('Mysql exception {0}'.format(ex))
            sys.exit()
        self.cursor.close()
        self.conn.close()

    def get_accecc_token(self):
        sql = 'select token from access_token where id=1'
        access_token = self.exec_query(sql)[0][0]
        return access_token


if __name__ == '__main__':
    mysql = MySQL()
    mysql.exec_none_query('insert into light.access_token (token, expire_time) values ({0},{1})'.format("12", 4200))
    print('')


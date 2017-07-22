from lib.utils.sql_help import *


def get_lendtime(mobile_number):
    mysql = MySQL(db='management')
    rows = mysql.exec_query('select id from home_lendhistory where mobile_number={0}'.format(mobile_number))
    return len(rows)


def get_money(mobile_number):
    mysql = MySQL(db='management')
    deposit = mysql.exec_query('select deposit from home_customer where mobile_number={0} order by create_time desc'.format(mobile_number))[0][0]
    return deposit
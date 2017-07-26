import datetime

from lib.utils.sql_help import *


def get_lendtime(mobile_number):
    mysql = MySQL(db='management')
    rows = mysql.exec_query('select id from home_lendhistory where mobile_number={0}'.format(mobile_number))
    return len(rows)


def get_money(mobile_number):
    mysql = MySQL(db='management')
    deposit = mysql.exec_query('select deposit from home_customer where mobile_number={0} order by create_time desc'.format(mobile_number))[0][0]
    return deposit


def get_max_id(table_name):
    mysql = MySQL(db='management')
    max_id = mysql.exec_query('select id from {0} order by id desc'.format(table_name))[0][0]
    return max_id + 1


def subcribe_save_openid(openid):
    is_usr_exist = is_weixin_usr_exist(openid)
    if not is_usr_exist:
        mysql = MySQL(db='management')
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        id = get_max_id('home_customer')
        mysql.exec_none_query('insert into home_customer (id, weixin_number, mobile_number, alipay, credit_score, deposit, deposit_status, create_time) values({0}, "{1}", "{2}", "{3}", {4}, {5}, {6}, "{7}")'.format(id, openid, '', '', 0, 0, 0, create_time))


def is_weixin_usr_exist(openid):
    mysql = MySQL(db='management')
    results = mysql.exec_none_query('select weixin_number from home_customer where weixin_number="{0}"'.format(openid))
    print('results', results)
    if results:
        return True
    else:
        return False


def is_deposit_exist(openid):
    mysql = MySQL(db='management')
    deposit = mysql.exec_query('select deposit from home_customer WHERE weixin_number="{0}"'.format(openid))[0][0]

    if deposit > 0:
        return True
    else:
        return False

if __name__ == '__main__':
    #subcribe_save_openid('123')
    is_esit = is_deposit_exist('oWJUp0XapjayHP5kLqXC3uADC73w')
    print('')
import datetime

from wechatpy import WeChatClient

from lib.utils.sql_help import *
from light.settings import *


def get_lendtime(customer_id):
    mysql = MySQL(db='management')
    lendtime = mysql.exec_query('select count(*) from home_lendhistory where customer_id="{0}"'.format(customer_id))[0][0]
    return lendtime


def get_deposit(weixin_number):
    mysql = MySQL(db='management')
    deposit = mysql.exec_query('select deposit from home_customer where weixin_number="{0}" order by create_time desc'.format(weixin_number))[0][0]
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
    results = mysql.exec_query('select weixin_number from home_customer where weixin_number="{0}"'.format(openid))
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


def get_customer_id_by_openid(openid):
    mysql = MySQL(db='management')
    customer_id = mysql.exec_query('select id from home_customer WHERE weixin_number="{0}"'.format(openid))[0][0]

    return customer_id


def get_access_token():
    mysql = MySQL(db='light')
    access_token = mysql.exec_query('select token from access_token WHERE id=1')[0][0]
    return access_token


def get_user_info(openid):
    client = WeChatClient(WEIXIN_APPID, WEIXIN_APPSECRET)
    user = client.user.get(openid)
    return user




if __name__ == '__main__':
    #subcribe_save_openid('123')
    get_user_info('oWJUp0aKcITU3A6QbNY-aamzwyF4')
    is_esit = get_lendtime('oWJUp0XapjayHP5kLqXC3uADC73w')
    print('')
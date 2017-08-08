import datetime
import traceback

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


def get_order_id(weixin_number):
    mysql = MySQL(db='management')
    order_id = mysql.exec_query('select deposit_order_id from home_customer where weixin_number="{0}" order by create_time desc'.format(weixin_number))[0][0]
    return order_id


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
        mysql.exec_none_query('insert into home_customer (id, weixin_number, mobile_number, alipay, credit_score, deposit, deposit_order_id, create_time) values({0}, "{1}", "{2}", "{3}", {4}, {5}, {6}, "{7}")'.format(id, openid, '', '', 0, 0, 0, create_time))


def update_deposit(openid, deposit, order_id):
    is_usr_exist = is_weixin_usr_exist(openid)
    if is_usr_exist:
        mysql = MySQL(db='management')
        mysql.exec_none_query('update home_customer set deposit={0}, deposit_order_id="{1}" where weixin_number="{2}"'.format(deposit, order_id, openid))


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


def save_order(openid, order_no, pay_no):
    is_order = is_order_exist(openid, order_no)
    if not is_order:
        mysql = MySQL(db='management')
        create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mysql.exec_none_query('insert into home_order (weixin_number, order_number, pay_number, create_time) values("{0}", "{1}", "{2}", "{3}")'.format(openid, order_no, pay_no, create_time))


def is_order_exist(openid, order_id):
    mysql = MySQL(db='management')
    order = mysql.exec_query('select count(*) from home_order WHERE weixin_number="{0}" and order_number="{1}"'.format(openid, order_id))[0][0]

    if order > 0:
        return True
    else:
        return False


def is_lend_exist(openid):
    mysql = MySQL(db='management')
    is_lend = mysql.exec_query('select count(*) from home_lendhistory WHERE customer_id="{0}" and start_time is not NUll and return_time is NULL'.format(openid))[0][0]

    if is_lend > 0:
        return True
    else:
        return False


def is_pay_finished(openid):
    mysql = MySQL(db='management')
    status = mysql.exec_query('select status from home_lendhistory WHERE customer_id="{0}" order by start_time desc'.format(openid))[0][0]

    if status == 2:
        return True
    else:
        return False


def is_has_capacity(cabinet_code):
    mysql = MySQL(db='management')

    capacity = mysql.exec_query('select capacity from home_cabinet where number="{0}"'.format(cabinet_code))[0][0]

    if int(capacity) < int(CABINET_CAPACITY):
        return True
    else:
        return False


def is_has_pole(cabinet_code):
    mysql = MySQL(db='management')

    capacity = mysql.exec_query('select capacity from home_cabinet where number="{0}"'.format(cabinet_code))[0][0]

    if int(capacity) > 0:
        return True
    else:
        return False


def insert_lendhistory(customer_id, rule_id, cabinet_id):
    mysql = MySQL(db='management')
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        mysql.exec_none_query('insert into home_lendhistory (customer_id, start_time, money, status, rule_id, cabinet_id) '
                          'values("{0}", "{1}", {2}, {3}, "{4}", {5})'.format(customer_id, start_time, 0, 0, rule_id, cabinet_id))
        return True
    except:
        print('Customer {0} lend save fail'.format(customer_id))
        return False


def update_history(customer_id):
    mysql = MySQL(db='management')
    return_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = 1

    start_time = get_start_time(customer_id)
    id = get_lendhistory_id(customer_id)
    time_by_seconds = (datetime.datetime.now() - start_time).seconds

    money = get_money(customer_id, time_by_seconds)

    try:
        mysql.exec_none_query('update home_lendhistory set return_time="{0}", status={1}, money={2} where id={3}'.format(return_time, status, money, id))
        return True
    except:
        print('Customer {0} return save fail'.format(customer_id))
        return False


def get_histories(customer_id):
    mysql = MySQL(db='management')
    histories = mysql.exec_query('select * from home_lendhistory where customer_id="{0}" order by start_time desc'.format(customer_id))
    return histories


def get_cabinet_id(cabinet_code):
    mysql = MySQL(db='management')

    id = mysql.exec_query('select id from home_cabinet where number="{0}"'.format(cabinet_code))[0][0]

    return id


def get_cabinets():
    mysql = MySQL(db='management')
    cabinets = mysql.exec_query('select * from home_cabinet')
    return cabinets


def get_spots():
    mysql = MySQL(db='management')
    spots = mysql.exec_query('select * from home_spot')
    return spots


def get_start_time(customer_id):
    mysql = MySQL(db='management')
    start_time = mysql.exec_query('select start_time from home_lendhistory where customer_id="{0}" order by start_time desc'.format(customer_id))[0][0]
    return start_time


def get_lendhistory_id(customer_id):
    mysql = MySQL(db='management')
    id = mysql.exec_query('select id from home_lendhistory where customer_id="{0}" order by start_time desc'.format(customer_id))[0][0]
    return id


def get_money(customer_id, time_by_seconds):
    mysql = MySQL(db='management')
    rule_id = mysql.exec_query('select rule_id from home_lendhistory where customer_id="{0}" order by start_time desc'.format(customer_id))[0][0]

    mysql = MySQL(db='management')

    rule = mysql.exec_query('select start_time_long, unit_price from home_rule where id="{0}"'.format(rule_id))[0]

    start_time_long = rule[0]
    unit_price = rule[1]

    hour = time_by_seconds // 3600

    time_long = hour - start_time_long

    minute = (time_by_seconds / 60) % 60

    if time_long < 0:
        return 0
    else:
        if minute > 0:
            return (time_long + 1) * unit_price
        else:
            return time_long * unit_price


def get_pay_money(customer_id):
    mysql = MySQL(db='management')
    money = mysql.exec_query(
        'select money from home_lendhistory where customer_id="{0}" order by start_time desc'.format(customer_id))[0][
        0]
    return money


def update_lendhistorystatus(customer_id, status):
    mysql = MySQL(db='management')

    id = get_lendhistory_id(customer_id)

    try:
        mysql.exec_none_query('update home_lendhistory set status={0} where id={1}'.format(status, id))
        return True
    except:
        print('Customer {0} pay status fail'.format(customer_id))
        return False


if __name__ == '__main__':
    #subcribe_save_openid('123')
    #get_user_info('oWJUp0aKcITU3A6QbNY-aamzwyF4')
    #is_esit = get_lendtime('oWJUp0XapjayHP5kLqXC3uADC73w')
    #save_order('open', '121', '211')
    #update_deposit('oWJUp0XapjayHP5kLqXC3uADC73w', 0, 0)
    #is_lend = is_deposit_exist('oWJUp0S5BZy3OGR92KIDJWUkD_jQ')
    #has_capacity = has_capacity('12-1213-21')

    #result = insert_lendhistory('oWJUp0XapjayHP5kLqXC3uADC73w', "0")

    #histories = get_histories('oWJUp0XapjayHP5kLqXC3uADC73w')
    #history = get_histories('oWJUp0XapjayHP5kLqXC3uADC73w')[1]
    #money = get_money('oWJUp0XapjayHP5kLqXC3uADC73w', 14800)

    result = is_pay_finished('oWJUp0XapjayHP5kLqXC3uADC73w')
    print('')
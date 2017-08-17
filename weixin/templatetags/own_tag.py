import time
import datetime
from django import template

from lib.utils.sql_help import MySQL
from lib.weixin.weixin_sql import get_money

register = template.Library()


def datetime_format(timestamp):
    current_time = datetime.datetime.utcfromtimestamp(timestamp)

    time_str = (current_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    return str(time_str)


def get_time_long(start_time, return_time=None):
    if return_time:
        return round((return_time - start_time).seconds / 60, 1)
    else:
        now_time = datetime.datetime.now()

        return round((now_time - start_time).seconds / 60, 1)


def convert_time(old_time):
    return (old_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")


def get_tmp_money(history_id):
    mysql = MySQL(db='management')
    history = mysql.exec_query('select * from home_lendhistory where id={0}'.format(id))[0]

    if history[3] is None:
        time_by_seconds = (datetime.datetime.now() - history[2]).seconds
    else:
        time_by_seconds = (history[3] - history[2]).seconds

    if history[4] != 0:
        money = history[4]
    else:
        money = get_money(history_id[1], time_by_seconds)

    return money

register.filter('datetime_format', datetime_format)
register.filter('get_time_long', get_time_long)
register.filter('convert_time', convert_time)
register.filter('get_tmp_money', get_tmp_money)



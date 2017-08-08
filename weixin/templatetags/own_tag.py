import time
import datetime
from django import template
register = template.Library()


def datetime_format(timestamp):
    current_time = datetime.datetime.utcfromtimestamp(timestamp)

    time_str = (current_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    return str(time_str)


def get_time_long(start_time, return_time=None):
    if return_time:
        return round((return_time - start_time).seconds / 60, 1)
    else:
        now_time = datetime.datetime.now() + datetime.timedelta(hours=8)

        return round((now_time - start_time).seconds / 60, 1)


def convert_time(old_time):
    return (old_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

register.filter('datetime_format', datetime_format)
register.filter('get_time_long', get_time_long)
register.filter('convert_time', convert_time)


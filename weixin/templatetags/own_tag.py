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
        return return_time - start_time
    else:
        return datetime.datetime.now() - start_time


def convert_time(old_time):
    return old_time.strftime("%Y-%m-%d %H:%M:%S")

register.filter('datetime_format', datetime_format)
register.filter('get_time_long', get_time_long)
register.filter('convert_time', convert_time)


import time
import datetime
from django import template
register = template.Library()


def datetime_format(timestamp):
    timeArray = time.localtime(timestamp)

    time_str = time.strftime("%Y-%m-%d %H:%M:%S", timeArray + datetime.timedelta(hours=8))
    return time_str

register.filter('datetime_format', datetime_format)

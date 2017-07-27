import time
import datetime
from django import template
register = template.Library()


def datetime_format(timestamp):
    now = datetime.datetime.now()

    time_str = time.strftime("%Y-%m-%d %H:%M:%S", now + datetime.timedelta(hours=8))
    return time_str

register.filter('datetime_format', datetime_format)

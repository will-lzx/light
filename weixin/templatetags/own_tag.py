import time
import datetime
from django import template
register = template.Library()


def datetime_format(timestamp):
    current_time = datetime.datetime.utcfromtimestamp(timestamp)

    time_str = (current_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    return str(time_str)

register.filter('datetime_format', datetime_format)

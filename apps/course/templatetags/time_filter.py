from django.utils.timezone import now as now_func
from django import template
from datetime import datetime

register = template.Library()


@register.filter
def time_since(value):
    if isinstance(value, datetime):
        now = now_func()
        timestramp = (now - value).total_seconds()
        if timestramp < 60:
            return '刚刚'
        elif timestramp > 60 and timestramp < 60 * 60:
            minutes = int(timestramp / 60)
            return '%s分钟前' % minutes
        elif timestramp > 60 * 60 and timestramp < 60 * 60 * 24:
            hours = int(timestramp / (60 * 60))
            return '%s小时前' % hours
        elif timestramp > 60 * 60 * 24 and timestramp < 60 * 60 * 24 * 30:
            days = int(timestramp / (60 * 60 * 24))
            return '%s天前' % days
        else:
            return value.strftime("%Y-%m-%d %H:%M")
    else:
        return value

@register.filter
def result_type(value):
    return value.type
# templatetags/course_extras.py

from django import template

register = template.Library()

@register.filter
def clean_decimal(value):
    if value is None:
        return ""

    if value == int(value):
        return int(value)

    return value
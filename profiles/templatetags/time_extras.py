from django import template

from profiles.utils.time_formating import format_hours_duration

register = template.Library()


@register.filter
def hours_duration(value):
    return format_hours_duration(value)





@register.filter
def clean_decimal(value):
    if value is None:
        return ""

    if value == int(value):
        return int(value)

    return value
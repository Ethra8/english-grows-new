from django import template
from django.utils.safestring import mark_safe
from datetime import date, datetime

register = template.Library()


@register.filter
def ordinal_sup(value):
    if not value:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, datetime):
        value = value.date()

    if not isinstance(value, date):
        return value

    day = value.day

    if 10 <= day % 100 <= 20:
        suffix = "th"
    else:
        suffix = {
            1: "st",
            2: "nd",
            3: "rd",
        }.get(day % 10, "th")

    return mark_safe(
        value.strftime(f"%A, {day}<sup>{suffix}</sup> %B")
    )

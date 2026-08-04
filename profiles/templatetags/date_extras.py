from django import template
from django.utils.safestring import mark_safe
from datetime import date, datetime

register = template.Library()



def _ordinal_suffix(day):
    if 10 <= day % 100 <= 20:
        return "th"
    return {
        1: "st",
        2: "nd",
        3: "rd",
    }.get(day % 10, "th")


@register.filter
def ordinal_sup(value):
    """
    Example:
    Wednesday, 5<sup>th</sup> August
    """
    if not value:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, datetime):
        value = value.date()

    if not isinstance(value, date):
        return value

    day = value.day
    suffix = _ordinal_suffix(day)

    return mark_safe(
        value.strftime(f"%A, {day}<sup>{suffix}</sup> %B")
    )


@register.filter
def ordinal_sup_short(value):
    """
    Example:
    Wed., 5<sup>th</sup> August
    """
    if not value:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, datetime):
        value = value.date()

    if not isinstance(value, date):
        return value

    day = value.day
    suffix = _ordinal_suffix(day)

    weekday = value.strftime("%a") + "."

    return mark_safe(
        f"{weekday} {day}<sup>{suffix}</sup> {value.strftime('%B')}"
    )
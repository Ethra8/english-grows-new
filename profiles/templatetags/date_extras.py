from django import template

register = template.Library()


@register.filter
def ordinal_sup(value):
    day = value.day

    if 10 <= day % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    return f'{value.strftime("%a")} {day}<sup>{suffix}</sup> {value.strftime("%b")} \'{value.strftime("%y")}'
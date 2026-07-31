from decimal import Decimal, ROUND_HALF_UP


def format_hours_duration(hours):
    if not hours:
        return "0h"

    total_minutes = int(
        (Decimal(hours) * Decimal("60")).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP
        )
    )

    whole_hours = total_minutes // 60
    minutes = total_minutes % 60

    if whole_hours and minutes:
        return f"{whole_hours}h{minutes:02d}"

    if whole_hours:
        return f"{whole_hours}h"

    return f"{minutes}min"
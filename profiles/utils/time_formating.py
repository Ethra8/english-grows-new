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


def get_session_minutes(sessions):
    total_minutes = 0

    for session in sessions:
        if session.start_time and session.end_time:
            duration = session.end_time - session.start_time
            total_minutes += round(
                duration.total_seconds() / 60
            )

    return total_minutes


def format_minutes_duration(minutes):
    whole_hours, remaining_minutes = divmod(
        minutes,
        60,
    )

    if whole_hours and remaining_minutes:
        return f"{whole_hours}h{remaining_minutes:02d}"

    if whole_hours:
        return f"{whole_hours}h"

    if remaining_minutes:
        return f"{remaining_minutes}min"

    return "0h"
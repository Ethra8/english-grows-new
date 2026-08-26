from datetime import timedelta


def get_bank_holiday_dates():
    """
    Return every date covered by an active BankHoliday.
    """

    # Local import avoids circular import with courses.models.
    from courses.models import BankHoliday

    holiday_dates = set()

    holidays = BankHoliday.objects.filter(
        is_active=True,
        start_date__isnull=False,
    )

    for holiday in holidays:
        start_date = holiday.start_date
        end_date = holiday.end_date or start_date

        current_date = start_date

        while current_date <= end_date:
            holiday_dates.add(current_date)

            current_date += timedelta(days=1)

    return holiday_dates


def calculate_course_schedule(course):
    """
    Calculate all scheduled lesson dates/slots for a Course.

    Bank holidays are excluded.
    """

    if not course.start_date:
        return []

    if not course.number_of_classes:
        return []

    timetable_slots = list(
        course.timetable_slots.all().order_by(
            "day_of_week",
            "start_time",
        )
    )

    if not timetable_slots:
        return []

    slots_by_day = {}

    for slot in timetable_slots:
        slots_by_day.setdefault(
            slot.day_of_week,
            []
        ).append(slot)

    holiday_dates = get_bank_holiday_dates()

    schedule = []

    current_date = course.start_date

    while len(schedule) < course.number_of_classes:

        weekday = current_date.isoweekday()

        if current_date not in holiday_dates:

            for slot in slots_by_day.get(
                weekday,
                [],
            ):

                if len(schedule) >= course.number_of_classes:
                    break

                schedule.append(
                    {
                        "date": current_date,
                        "slot": slot,
                        "class_number": len(schedule) + 1,
                    }
                )

        current_date += timedelta(days=1)

    return schedule


def calculate_course_end_date(course):
    """
    Return the final scheduled teaching date.
    """

    schedule = calculate_course_schedule(course)

    if not schedule:
        return None

    return schedule[-1]["date"]
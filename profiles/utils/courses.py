from collections import defaultdict

# Helper used in course views in views.py 
def build_formatted_timetable(course):
    timetable_groups = defaultdict(list)

    for slot in course.timetable_slots.all():
        key = (
            slot.start_time.strftime("%Hh%M"),
            slot.end_time.strftime("%Hh%M"),
        )

        timetable_groups[key].append(
            slot.get_day_of_week_display()[:3]
        )

    return [
        {
            "days": " / ".join(days),
            "start": start,
            "end": end,
        }
        for (start, end), days in timetable_groups.items()
    ]
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime

from .models import ClassSession, CourseEnrollment

from profiles.models import UserProfile


@login_required
def my_calendar(request):
    active_enrollment = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
            status="active"
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
        .first()
    )

    context = {
        "active_enrollment": active_enrollment,
    }


    return render(request, "courses/my_calendar.html", context)


# displays my_calendar linked to in profile side-bar
@login_required
def my_calendar_events(request):
    start = request.GET.get("start")
    end = request.GET.get("end")

    active_course_ids = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
            status="active",
        )
        .values_list("course_id", flat=True)
    )

    sessions = (
        ClassSession.objects
        .filter(
            course_id__in=active_course_ids,
            is_cancelled=False,
        )
        .select_related("course")
        .order_by("start_time")
    )

    if start and end:
        start_date = parse_datetime(start)
        end_date = parse_datetime(end)

        sessions = sessions.filter(
            start_time__gte=start_date,
            start_time__lt=end_date,
        )

    events = []

    for session in sessions:
        events.append({
            "id": session.id,
            "title": session.title,
            "start": session.start_time.isoformat(),
            "end": session.end_time.isoformat() if session.end_time else None,
            "extendedProps": {
                "course": session.course.name,
                "class_number": session.class_number,
                "meeting_link": session.meeting_link,
            },
        })

    return JsonResponse(events, safe=False)

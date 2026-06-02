from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from datetime import timedelta

from .models import UserProfile
from .forms import UserProfileForm

from courses.models import CourseEnrollment, ClassSession, BankHoliday, Attendance



@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

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

    next_class = None

    current_level = None

    if active_enrollment:
        next_class = (
            ClassSession.objects
            .filter(
                course=active_enrollment.course,
                is_cancelled=False,
                start_time__gte=timezone.now()
            )
            .order_by("start_time")
            .first()
        )
    
    context = {
        "profile": user_profile,
        "current_level": current_level,
        "active_enrollment": active_enrollment,
        "next_class": next_class,
    }

    return render(request, "profiles/profile.html", context)


@login_required
def profile_settings(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

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

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profiles:profile_settings")

    else:
        form = UserProfileForm(instance=user_profile, user=request.user)

    context = {
        "profile": user_profile,
        "active_enrollment": active_enrollment,
        "form": form,
    }

    return render(request, "profiles/profile_settings.html", context)

@login_required
def my_course(request):
    profile = get_object_or_404(UserProfile, user=request.user)

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

    enrollment_status = None

    if active_enrollment:
        enrollment_status = active_enrollment.status

    timetable_slots = None

    if active_enrollment:
        timetable_slots = (
            active_enrollment.course.timetable_slots
            .all()
            .order_by("day_of_week", "start_time")
        )

    context = {
        "profile": profile,
        "active_enrollment": active_enrollment,
        "enrollment_status": enrollment_status,
        "timetable_slots": timetable_slots,
    }

    return render(request, "profiles/my_course.html", context)



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


    return render(request, "profiles/my_calendar.html", context)


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

    bank_holidays = (
        BankHoliday.objects
        .filter(
            is_active=True,
        )
        .order_by("start_date")
    )

    if start and end:
        start_date = parse_datetime(start)
        end_date = parse_datetime(end)

        if start_date and end_date:
            sessions = sessions.filter(
                start_time__gte=start_date,
                start_time__lt=end_date,
            )

            bank_holidays = bank_holidays.filter(
                start_date__lt=end_date.date()
            ).filter(
                Q(end_date__isnull=True) |
                Q(end_date__gte=start_date.date())
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

    for holiday in bank_holidays:
        event = {
            "id": f"holiday-{holiday.id}",
            "title": holiday.title,
            "start": holiday.start_date.isoformat(),
            "allDay": True,
            "display": "block",
            "className": "bank-holiday-event",
            "extendedProps": {
                "type": "bank_holiday",
            },
        }

        if holiday.end_date:
            event["end"] = (holiday.end_date + timedelta(days=1)).isoformat()

        events.append(event)

    return JsonResponse(events, safe=False)



@login_required
def my_attendance(request):
    profile = get_object_or_404(UserProfile, user=request.user)

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

    recent_attendance = (
        Attendance.objects
        .filter(
            student=request.user,
            class_session__course=active_enrollment.course,
            status="attended",
        )
        .select_related(
            "class_session",
            "class_session__course",
        )
        .order_by("-class_session__start_time")
    )

    recent_absences = (
        Attendance.objects
        .filter(
            student=request.user,
            class_session__course=active_enrollment.course,
            status__in=["missed", "excused"],
        )
        .select_related(
            "class_session",
            "class_session__course",
        )
        .order_by("-class_session__start_time")
    )

    context = {
        "profile": profile,
        "active_enrollment": active_enrollment,
        "recent_attendance": recent_attendance,
        "recent_absences": recent_absences
    }

    return render(request, "profiles/my_attendance.html", context)
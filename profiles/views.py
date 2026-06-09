from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from datetime import timedelta, datetime, time

from .models import UserProfile, TeacherProfile
from .forms import UserProfileForm, TeacherProfileForm

from courses.models import Course, CourseEnrollment, ClassSession, BankHoliday, Attendance


# STUDENT for UserProfile
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

    form = UserProfileForm(
        request.POST,
        request.FILES,
        instance=user_profile,
        user=request.user
    )

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
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=user_profile,
            user=request.user
        )

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


# ************************************|
# STUDENT PROFILE  *******************|
# ************************************|

# STUDENT COURSE INFO PAGE
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

    return render(request, "profiles/student/my_course.html", context)


# STUDENT CALENDAR PAGE
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


    return render(request, "profiles/student/my_calendar.html", context)


# STUDENT CALENDAR PAGE
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


# STUDENT ATTENDANCE PAGE
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

    if not active_enrollment:
        return render(request, "profiles/student/my_attendance.html", {
            "profile": profile,
            "active_enrollment": None,
            "recent_attendance": [],
            "recent_missed_classes": [],
            "recent_excused_classes": [],
        })

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

    return render(request, "profiles/student/my_attendance.html", context)


# ***********************************************|
# TEACHER PROFILE  ******************************|
# ***********************************************|

@login_required
def teacher_dashboard(request):
    if request.user.profile.role != "teacher":
        return redirect("home")

    # Shows Today's Sessions
    today = timezone.localdate()

    start_of_day = timezone.make_aware(
        datetime.combine(today, time.min)
    )

    end_of_day = timezone.make_aware(
        datetime.combine(today, time.max)
    )

    todays_sessions = (
        ClassSession.objects
        .filter(
            course__teacher=request.user,
            course__status="active",
            is_cancelled=False,
            start_time__gte=start_of_day,
            start_time__lte=end_of_day,
        )

    .select_related("course")
    .prefetch_related("course__enrollments")
    .order_by("start_time")
    )

    courses = (
        Course.objects
        .filter(teacher=request.user)
        .prefetch_related(
            "enrollments__student__profile",
            "class_sessions"
        )
    )

    context = {
        "courses": courses,
        "todays_sessions": todays_sessions,
        "today": today,
    }

    return render(request, "profiles/teacher/teacher_dashboard.html", context)


@login_required
def teacher_classes_list(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    now = timezone.now()
    today = timezone.localdate()

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    start_of_month = today.replace(day=1)

    sessions = (
        ClassSession.objects
        .filter(course__teacher=request.user)
        .select_related(
            "course",
            "course__course_type",
            "course__company",
        )
        .prefetch_related(
            "course__enrollments",
            "course__enrollments__student",
            "course__enrollments__student__profile",
        )
        .order_by("start_time")
    )

    for session in sessions:
        session_date = timezone.localdate(session.start_time)

        if session.is_cancelled:
            session.class_period = "cancelled"
        elif session.start_time < now:
            session.class_period = "past"
        elif session_date == today:
            session.class_period = "today"
        elif start_of_week <= session_date <= end_of_week:
            session.class_period = "weekly"
        elif session_date.month == today.month and session_date.year == today.year:
            session.class_period = "monthly"
        else:
            session.class_period = "termly"

    context = {
        "sessions": sessions,
        "now": now,
    }

    return render(request, "profiles/teacher/teacher_classes_list.html", context)


@login_required
def teacher_courses(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    courses = (
        Course.objects
        .filter(teacher=request.user)
        .select_related(
            "course_type",
            "company",
            "teacher",
        )
        .prefetch_related(
            "enrollments__student__profile",
            "class_sessions",
        )
        .order_by("name")
    )


    total_courses = courses.count()
    active_courses = courses.filter(status="active").count()
    confirmed_courses = courses.filter(status="confirmed").count()
    cancelled_courses = courses.filter(status="cancelled").count()
    paused_courses = courses.filter(status="paused").count()

    active_courses_list = courses.filter(status="active")

    context = {
        "profile": profile,
        "courses": courses,
        "total_courses": total_courses,
        "active_courses": active_courses,
        "confirmed_courses": confirmed_courses,
        "cancelled_courses": cancelled_courses,
        "paused_courses": paused_courses,
        "active_courses_list": active_courses_list,  
    }

    return render(request, "profiles/teacher/teacher_courses.html", context)



@login_required
def teacher_course_details(request, course_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user
    )

    enrollments = (
        course.enrollments
        .select_related("student", "student__profile")
        .filter(status="active")
    )

    sessions = (
        course.class_sessions
        .all()
        .order_by("start_time")
    )

    now = timezone.now()

    completed_sessions = course.class_sessions.filter(
        is_cancelled=False,
        start_time__lt=now,
    ).count()

    context = {
        "profile": profile,
        "course": course,
        "enrollments": enrollments,
        "sessions": sessions,
        "completed_sessions": completed_sessions,
    }

    return render(request, "profiles/teacher/teacher_course_details.html", context)


@login_required
def teacher_calendar(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")
    
    courses = (
        Course.objects
        .filter(teacher=request.user)
        .select_related(
            "course_type",
            "company",
            "teacher",
        )
        .order_by("name")
    )

    context = {
        "profile": profile,
        "courses": courses,
    }

    return render(request, "profiles/teacher/teacher_calendar.html", context)


# TEACHER CALENDAR PAGE
@login_required
def teacher_calendar_events(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return JsonResponse([], safe=False)

    start = request.GET.get("start")
    end = request.GET.get("end")

    teacher_course_ids = (
        Course.objects
        .filter(teacher=request.user)
        .values_list("id", flat=True)
        )    
    
    sessions = (
        ClassSession.objects
        .filter(
            course_id__in=teacher_course_ids,
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

        status_class = ""

        if session.course.status == "confirmed":
            status_class = "course-confirmed-event"
        elif session.course.status == "paused":
            status_class = "course-paused-event"
        elif session.course.status == "cancelled":
            status_class = "course-cancelled-event"

        events.append({
            "id": session.id,
            "title": session.title,
            "start": session.start_time.isoformat(),
            "end": session.end_time.isoformat() if session.end_time else None,
            "className": status_class,
            "extendedProps": {
                "course": session.course.name,
                "course_status": session.course.status,
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
def teacher_attendance(request):
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

    if not active_enrollment:
        return render(request, "profiles/teacher/teacher_attendance.html", {
            "profile": profile,
            "active_enrollment": None,
            "recent_attendance": [],
            "recent_missed_classes": [],
            "recent_excused_classes": [],
        })

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

    return render(request, "profiles/teacher/teacher_attendance.html", context)



# TEACHER PROFILE SETTINGS
@login_required
def teacher_profile_settings(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    teacher_profile, created = TeacherProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        user_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=user_profile,
            user=request.user
        )

        teacher_form = TeacherProfileForm(
            request.POST,
            instance=teacher_profile
        )

        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save()
            teacher_form.save()

            messages.success(request, "Your teacher profile has been updated.")
            return redirect("profiles:teacher_profile_settings")

    else:
        user_form = UserProfileForm(
            instance=user_profile,
            user=request.user
        )

        teacher_form = TeacherProfileForm(
            instance=teacher_profile
        )

    context = {
        "profile": user_profile,
        "teacher_profile": teacher_profile,
        "user_form": user_form,
        "teacher_form": teacher_form,
    }

    return render(
        request,
        "profiles/teacher/teacher_profile_settings.html",
        context
    )

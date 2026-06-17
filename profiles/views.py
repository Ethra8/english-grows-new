from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from datetime import timedelta, datetime, time
from collections import defaultdict

from .models import UserProfile, TeacherProfile
from .forms import UserProfileForm, TeacherProfileForm

from courses.models import Course, CourseEnrollment, ClassSession, BankHoliday, Attendance



@login_required
def login_redirect(request):
    profile = request.user.profile

    if profile.role == "teacher":
        return redirect("profiles:teacher_dashboard")

    return redirect("profiles:profile")


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

from datetime import datetime, time, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from courses.models import Course, ClassSession, Attendance


@login_required
def teacher_dashboard(request):
    profile = request.user.profile

    if profile.role != "teacher":
        return redirect("home")

    today = timezone.localdate()
    now = timezone.now()

    # Today range
    start_of_day = timezone.make_aware(
        datetime.combine(today, time.min)
    )
    end_of_day = timezone.make_aware(
        datetime.combine(today, time.max)
    )

    # Week range: Monday - Sunday
    start_of_week_date = today - timedelta(days=today.weekday())
    end_of_week_date = start_of_week_date + timedelta(days=6)

    start_of_week = timezone.make_aware(
        datetime.combine(start_of_week_date, time.min)
    )
    end_of_week = timezone.make_aware(
        datetime.combine(end_of_week_date, time.max)
    )

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

    active_courses = courses.filter(status="active").count()

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

    weekly_sessions = (
        ClassSession.objects
        .filter(
            course__teacher=request.user,
            course__status="active",
            is_cancelled=False,
            start_time__gte=start_of_week,
            start_time__lte=end_of_week,
        )
        .select_related("course")
        .prefetch_related("attendance_set")
    )

    total_weekly_sessions = weekly_sessions.count()

    completed_weekly_sessions = weekly_sessions.filter(
        start_time__lt=now
    ).count()

    upcoming_weekly_sessions = weekly_sessions.filter(
        start_time__gte=now
    ).count()

    attendance_completed_sessions = (
        weekly_sessions
        .filter(attendance_records__status__in=["attended", "missed", "excused"])
        .distinct()
        .count()
    )
    
    def get_percentage(value, total):
        if total == 0:
            return 0
        return round((value / total) * 100)

    completed_weekly_percentage = get_percentage(
        completed_weekly_sessions,
        total_weekly_sessions
    )

    upcoming_weekly_percentage = get_percentage(
        upcoming_weekly_sessions,
        total_weekly_sessions
    )

    attendance_completed_percentage = get_percentage(
        attendance_completed_sessions,
        total_weekly_sessions
    )

    total_students = (
        courses
        .filter(status="active")
        .filter(enrollments__status="active")
        .values("enrollments__student")
        .distinct()
        .count()
    )

    attendance_records = Attendance.objects.filter(
        class_session__course__teacher=request.user,
        class_session__course__status="active",
        status__in=["attended", "missed", "excused"],
    )

    total_attendance_records = attendance_records.count()

    attended_records = attendance_records.filter(
        status="attended"
    ).count()

    if total_attendance_records > 0:
        total_attendance_rate = round(
            (attended_records / total_attendance_records) * 100
        )
    else:
        total_attendance_rate = 0


    context = {
        "profile": profile,
        "courses": courses,
        "todays_sessions": todays_sessions,
        "today": today,
        "active_courses": active_courses,

        # Students
        "total_students": total_students,

        # Weekly data
        "total_weekly_sessions": total_weekly_sessions,

        "completed_weekly_sessions": completed_weekly_sessions,
        "completed_weekly_percentage": completed_weekly_percentage,

        "upcoming_weekly_sessions": upcoming_weekly_sessions,
        "upcoming_weekly_percentage": upcoming_weekly_percentage,

        "attendance_completed_sessions": attendance_completed_sessions,
        "attendance_completed_percentage": attendance_completed_percentage,
        "total_attendance_rate": total_attendance_rate,
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

    class_filter_counts = {
        "upcoming": 0,
        "today": 0,
        "weekly": 0,
        "past": 0,
        "all": 0,
    }

    for session in sessions:
        session_date = timezone.localdate(session.start_time)

        session.is_today = (
            session_date == today
            and not session.is_cancelled
        )

        session.is_this_week = (
            start_of_week <= session_date <= end_of_week
            and not session.is_cancelled
        )

        session.is_upcoming = (
            session.end_time >= now
            and not session.is_cancelled
        )

        session.is_list_past = (
            session.end_time < now
            and not session.is_cancelled
        )

        if session.is_cancelled:
            session.class_period = "cancelled"
        elif session.is_today:
            session.class_period = "today"
        elif session.is_list_past:
            session.class_period = "past"
        elif session.is_upcoming:
            session.class_period = "upcoming"
        else:
            session.class_period = "termly"

        class_filter_counts["all"] += 1

        if session.is_upcoming:
            class_filter_counts["upcoming"] += 1

        if session.is_today:
            class_filter_counts["today"] += 1

        if session.is_this_week:
            class_filter_counts["weekly"] += 1

        if session.is_list_past:
            class_filter_counts["past"] += 1

    context = {
        "sessions": sessions,
        "now": now,
        "class_filter_counts": class_filter_counts,
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
            "timetable_slots",    
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

    total_classes = course.class_sessions.filter(
        is_cancelled=False
    ).count()

    completed_classes = course.class_sessions.filter(
        is_cancelled=False,
        start_time__lt=now,
    ).count()

    remaining_classes = total_classes - completed_classes

    completion_percentage = 0
    if total_classes:
        completion_percentage = round(
            (completed_classes / total_classes) * 100
        )

    attendance_percentages = []

    for enrollment in enrollments:
        total_completed = enrollment.total_completed_classes

        if total_completed > 0:
            attendance_percentages.append(
                (enrollment.classes_attended / total_completed) * 100
            )

    average_attendance = 0
    if attendance_percentages:
        average_attendance = round(
            sum(attendance_percentages) / len(attendance_percentages)
        )
    
    timetable_groups = defaultdict(list)

    for slot in course.timetable_slots.all():
        key = (
            slot.start_time.strftime("%Hh%M"),
            slot.end_time.strftime("%Hh%M")
        )

        timetable_groups[key].append(
            slot.get_day_of_week_display()[:3]
        )

    formatted_timetable = []

    for (start, end), days in timetable_groups.items():
        formatted_timetable.append({
            "days": " & ".join(days),
            "start": start,
            "end": end,
        })

    # create list of all ss emails to send groupal email
    student_emails = [
        enrollment.student.email
        for enrollment in enrollments
        if enrollment.student.email
    ]

    bcc_student_emails = ",".join(student_emails)

    context = {
        "profile": profile,
        "course": course,
        "enrollments": enrollments,
        "sessions": sessions,

        # Progress timeline data
        "total_classes": total_classes,
        "completed_classes": completed_classes,
        "remaining_classes": remaining_classes,
        "completion_percentage": completion_percentage,
        "average_attendance": average_attendance,
        "formatted_timetable": formatted_timetable,
        "bcc_student_emails": bcc_student_emails,
    }

    return render(
        request,
        "profiles/teacher/teacher_course_details.html",
        context
    )


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


@login_required
def teacher_course_students_list(request, course_id):
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

    total_classes = course.class_sessions.filter(
        is_cancelled=False
    ).count()

    completed_classes = course.class_sessions.filter(
        is_cancelled=False,
        start_time__lt=now,
    ).count()

    remaining_classes = total_classes - completed_classes

    completion_percentage = 0
    if total_classes:
        completion_percentage = round(
            (completed_classes / total_classes) * 100
        )

    attendance_percentages = []

    for enrollment in enrollments:
        total_completed = enrollment.total_completed_classes

        if total_completed > 0:
            attendance_percentages.append(
                (enrollment.classes_attended / total_completed) * 100
            )

    average_attendance = 0
    if attendance_percentages:
        average_attendance = round(
            sum(attendance_percentages) / len(attendance_percentages)
        )
    
    timetable_groups = defaultdict(list)

    for slot in course.timetable_slots.all():
        key = (
            slot.start_time.strftime("%Hh%M"),
            slot.end_time.strftime("%Hh%M")
        )

        timetable_groups[key].append(
            slot.get_day_of_week_display()[:3]
        )

    formatted_timetable = []

    for (start, end), days in timetable_groups.items():
        formatted_timetable.append({
            "days": " & ".join(days),
            "start": start,
            "end": end,
        })

    # create list of all ss emails to send groupal email
    student_emails = [
        enrollment.student.email
        for enrollment in enrollments
        if enrollment.student.email
    ]

    bcc_student_emails = ",".join(student_emails)

    context = {
        "profile": profile,
        "course": course,
        "enrollments": enrollments,
        "sessions": sessions,

        # Progress timeline data
        "total_classes": total_classes,
        "completed_classes": completed_classes,
        "remaining_classes": remaining_classes,
        "completion_percentage": completion_percentage,
        "average_attendance": average_attendance,
        "formatted_timetable": formatted_timetable,
        "bcc_student_emails": bcc_student_emails,
        "level_choices": UserProfile.LEVEL_CHOICES,
    }

    return render(
        request,
        "profiles/teacher/teacher_course_students_list.html",
        context
    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from courses.models import Course, CourseEnrollment, Attendance
from .models import UserProfile


@login_required
def teacher_student_detail(request, course_id, enrollment_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user
    )

    enrollment = get_object_or_404(
        CourseEnrollment.objects.select_related(
            "student",
            "student__profile",
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        ),
        id=enrollment_id,
        course=course,
    )

    student = enrollment.student
    student_profile = student.profile

    attendances = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course
        )
        .select_related("class_session")
        .order_by("-class_session__start_time")
    )

    total_attendance_records = attendances.count()
    attended_count = attendances.filter(status="attended").count()
    missed_count = attendances.filter(status="missed").count()
    excused_count = attendances.filter(status="excused").count()
   
    completed_classes = course.class_sessions.filter(
        start_time__lt=timezone.now(),
        is_cancelled=False,
    ).count()

    if total_attendance_records > 0:
        attendance_percentage = round(
            (attended_count / completed_classes) * 100
        )
    else:
        attendance_percentage = 0


    total_classes = course.number_of_classes or course.class_sessions.filter(
        is_cancelled=False
    ).count()

    remaining_classes = max(total_classes - completed_classes, 0)

    if total_classes > 0:
        completion_percentage = round(
            (completed_classes / total_classes) * 100
        )
    else:
        completion_percentage = 0

    recent_attendance = attendances[:5]

    context = {
        "course": course,
        "enrollment": enrollment,
        "student": student,
        "student_profile": student_profile,
        "level_choices": UserProfile.LEVEL_CHOICES,

        "attended_count": attended_count,
        "missed_count": missed_count,
        "excused_count": excused_count,
        "total_attendance_records": total_attendance_records,
        "attendance_percentage": attendance_percentage,

        "completed_classes": completed_classes,
        "remaining_classes": remaining_classes,
        "total_classes": total_classes,
        "completion_percentage": completion_percentage,

        "recent_attendance": recent_attendance,
        "active_tab": "overview",
    }

    return render(
        request,
        "profiles/teacher/teacher_student_detail.html",
        context
    )



@login_required
def update_student_level(request, course_id, enrollment_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user
    )

    enrollment = get_object_or_404(
        CourseEnrollment,
        id=enrollment_id,
        course=course
    )

    profile = enrollment.student.profile

    if request.method == "POST":
        new_level = request.POST.get("current_level")

        valid_levels = [level[0] for level in UserProfile.LEVEL_CHOICES]

        if new_level in valid_levels:
            profile.current_level = new_level
            profile.save()
            messages.success(request, "Student level updated successfully.")
        else:
            messages.error(request, "Invalid level selected.")

    return redirect(
        "profiles:teacher_student_detail",
        course_id=course.id,
        enrollment_id=enrollment.id
    )



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

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    now = timezone.now()

    sessions_queryset = (
        ClassSession.objects
        .filter(
            course__teacher=request.user,
            start_time__lte=now,
            is_cancelled=False,
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
        .prefetch_related("course__enrollments")
        .order_by("-start_time")
    )

    sessions = []

    pending_count = 0
    completed_count = 0

    final_attendance_statuses = [
        "attended",
        "missed",
        "excused",
    ]

    for session in sessions_queryset:
        final_attendance_exists = Attendance.objects.filter(
            class_session=session,
            status__in=final_attendance_statuses,
        ).exists()

        session.students_count = session.course.enrollments.filter(
            status="active"
        ).count()

        if final_attendance_exists:
            session.attendance_filter_status = "completed"
            completed_count += 1
        else:
            session.attendance_filter_status = "pending"
            pending_count += 1

        sessions.append(session)

    context = {
        "profile": profile,
        "sessions": sessions,
        "pending_count": pending_count,
        "completed_count": completed_count,
    }

    return render(request, "profiles/teacher/teacher_attendance.html", context)



@login_required
def teacher_take_attendance(request, session_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    class_session = get_object_or_404(
        ClassSession.objects.select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        ),
        id=session_id,
        course__teacher=request.user,
    )

    enrollments = (
        CourseEnrollment.objects
        .filter(
            course=class_session.course,
            status="active",
        )
        .select_related(
            "student",
            "student__profile",
        )
        .order_by(
            "student__first_name",
            "student__last_name",
            "student__email",
        )
    )

    existing_attendance = Attendance.objects.filter(
        class_session=class_session
    )

    attendance_by_student_id = {
        attendance.student_id: attendance
        for attendance in existing_attendance
    }

    for enrollment in enrollments:
        enrollment.current_attendance = attendance_by_student_id.get(
            enrollment.student_id
        )

    if request.method == "POST":
        for enrollment in enrollments:
            status = request.POST.get(f"attendance_{enrollment.student_id}")

            if status in ["attended", "missed", "excused"]:
                Attendance.objects.update_or_create(
                    student=enrollment.student,
                    class_session=class_session,
                    defaults={
                        "status": status,
                    }
                )

        messages.success(request, "Attendance saved successfully.")
        return redirect(
            "profiles:teacher_attendance_detail",
            session_id=class_session.id,
        )

    context = {
        "profile": profile,
        "class_session": class_session,
        "enrollments": enrollments,
    }

    return render(
        request,
        "profiles/teacher/teacher_take_attendance.html",
        context,
    )


@login_required
def teacher_attendance_detail(request, session_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    class_session = get_object_or_404(
        ClassSession.objects.select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        ),
        id=session_id,
        course__teacher=request.user,
    )

    attendances = (
        Attendance.objects
        .filter(class_session=class_session)
        .select_related(
            "student",
            "student__profile",
        )
        .order_by(
            "student__first_name",
            "student__last_name",
            "student__email",
        )
    )

    present_count = attendances.filter(status="attended").count()
    missed_count = attendances.filter(status="missed").count()
    excused_count = attendances.filter(status="excused").count()
    total_count = attendances.count()

    context = {
        "profile": profile,
        "class_session": class_session,
        "attendances": attendances,
        "present_count": present_count,
        "missed_count": missed_count,
        "excused_count": excused_count,
        "total_count": total_count,
    }

    return render(
        request,
        "profiles/teacher/teacher_attendance_detail.html",
        context,
    )



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

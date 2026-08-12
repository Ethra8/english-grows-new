from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q, Prefetch
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime, parse_date
from django.forms import inlineformset_factory
from django.urls import reverse

import json

from datetime import timedelta, datetime, time
import calendar
from collections import defaultdict

from decimal import Decimal

from profiles.utils.time_formating import format_hours_duration

from .models import UserProfile, TeacherProfile, StudentAcademicProfile, StudentAcademicProfile, StudentSkillAssessment, StudentSubSkillAssessment, SUBSKILLS, StudentSkillTermSnapshot
from .forms import UserProfileForm, TeacherProfileForm, StudentAcademicProfileForm, StudentSkillAssessmentForm, StudentSubSkillAssessmentFormSet
from courses.models import Course, CourseEnrollment, ClassSession, BankHoliday, Attendance



@login_required
def login_redirect(request):
    profile = request.user.profile

    if profile.role == "teacher":
        return redirect("profiles:teacher_dashboard")

    return redirect("profiles:profile")



# Common login to profile... THEN custom role profile
@login_required
def profile(request):
    user_profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if user_profile.role == UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("profiles:company_admin_dashboard")

    if user_profile.role == UserProfile.ROLE_TEACHER:
        return redirect("profiles:teacher_dashboard")

    if user_profile.role in [
        UserProfile.ROLE_EMPLOYEE,
        UserProfile.ROLE_INDIVIDUAL,
    ]:
        return redirect("profiles:student_dashboard")

    return redirect("home")


@login_required
def student_dashboard(request):
    user_profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if user_profile.role not in [
        UserProfile.ROLE_EMPLOYEE,
        UserProfile.ROLE_INDIVIDUAL,
    ]:
        return redirect("home")

    active_enrollment = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
            status="active",
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

    if active_enrollment:
        next_class = (
            ClassSession.objects
            .filter(
                course=active_enrollment.course,
                start_time__gte=timezone.now(),
                status__in=[
                    ClassSession.STATUS_SCHEDULED,
                    ClassSession.STATUS_RESCHEDULED,
                ],
            )
            .order_by("start_time")
            .first()
        )

    context = {
        "profile": user_profile,
        "active_enrollment": active_enrollment,
        "next_class": next_class,
    }

    return render(
        request,
        "profiles/student/student_dashboard.html",
        context,
    )


@login_required
def profile_settings(request):
    profile_user = request.user

    profile = get_object_or_404(UserProfile, user=profile_user)

    # Security: only allow the user themselves or teachers/admins
    if profile_user != request.user:
        if request.user.profile.role != "teacher" and not request.user.is_staff:
            return redirect("home")

    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=profile_user,
        )

        if form.is_valid():
            form.save()

            profile_user.first_name = form.cleaned_data["first_name"]
            profile_user.last_name = form.cleaned_data["last_name"]
            profile_user.email = form.cleaned_data["email"]
            profile_user.save()

            return redirect("profiles:profile_settings")

    else:
        form = UserProfileForm(
            instance=profile,
            user=profile_user,
        )

    context = {
        "form": form,
        "profile": profile,
        "profile_user": profile_user,
    }

    return render(request, "profiles/profile_settings.html", context)

    

# ************************************|
# STUDENT PROFILE  *******************|
# ************************************|

# STUDENT COURSE INFO PAGE
# STUDENT COURSE INFO PAGE

@login_required
def my_course(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    # ---------------------------------------------------------
    # Get ALL enrollments that are active AND whose course
    # is also currently active.
    # ---------------------------------------------------------
    active_enrollments = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
            status="active",
            course__status="active",
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
        .order_by("course__name")
    )

    # ---------------------------------------------------------
    # Get the course selected in the <select>.
    #
    # The form sends:
    #     ?course=COURSE_ID
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")

    # ---------------------------------------------------------
    # Determine which enrollment/course should be displayed.
    # ---------------------------------------------------------
    if selected_course_id:
        active_enrollment = get_object_or_404(
            active_enrollments,
            course_id=selected_course_id,
        )
    else:
        # No selection in URL yet:
        # display the first available active enrollment.
        active_enrollment = active_enrollments.first()

    enrollment_status = None

    if active_enrollment:
        enrollment_status = active_enrollment.status

    # ---------------------------------------------------------
    # TIMETABLE
    # Must come from the SELECTED course.
    # ---------------------------------------------------------
    timetable_slots = None

    if active_enrollment:
        timetable_slots = (
            active_enrollment.course.timetable_slots
            .all()
            .order_by("day_of_week", "start_time")
        )

    # ---------------------------------------------------------
    # NEXT CLASS
    # Must also come from the SELECTED course.
    # ---------------------------------------------------------
    next_class = None

    if active_enrollment:
        next_class = (
            ClassSession.objects
            .filter(
                course=active_enrollment.course,
                start_time__gte=timezone.now(),
                status__in=[
                    ClassSession.STATUS_SCHEDULED,
                    ClassSession.STATUS_RESCHEDULED,
                ],
            )
            .order_by("start_time")
            .first()
        )

    context = {
        "profile": profile,

        # ALL courses for the dropdown
        "active_enrollments": active_enrollments,

        # ONE selected course/enrollment for the page content
        "active_enrollment": active_enrollment,

        "enrollment_status": enrollment_status,
        "timetable_slots": timetable_slots,
        "next_class": next_class,
    }

    return render(
        request,
        "profiles/student/my_course.html",
        context
    )


# STUDENT CALENDAR PAGE
@login_required
def my_calendar(request):
    active_enrollment = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
            status="active",
            course__status="active",
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
            course__status="active",
        )
        .values_list("course_id", flat=True)
    )

    sessions = (
        ClassSession.objects
        .filter(
            course_id__in=active_course_ids,
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
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



# STUDENT MY LEARNING PROGRESS PAGE
@login_required
def my_learning_progress(request):
    student = request.user
    student_profile = student.profile

    active_enrollments = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
            status="active",
            course__status="active",
        )
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
        .order_by(
            "-id",
        )
    )

    selected_course_id = request.GET.get("course")

    # ---------------------------------------------------------
    # COURSE SELECTED IN URL
    # ---------------------------------------------------------
    if selected_course_id:
        active_enrollment = get_object_or_404(
            active_enrollments,
            course_id=selected_course_id,
        )

    # ---------------------------------------------------------
    # NO COURSE SELECTED IN URL
    # ---------------------------------------------------------
    else:
        # Pick the default course according to the queryset order.
        active_enrollment = active_enrollments.first()

        # If a default course exists, redirect to the canonical URL
        # so the currently displayed course is always explicit.
        if active_enrollment:
            return redirect(
                f"{request.path}?course={active_enrollment.course_id}"
            )


    # ---------------------------------------------------------
    # NO ELIGIBLE ACTIVE COURSE
    # ---------------------------------------------------------
    if not active_enrollment:
        return render(
            request,
            "profiles/student/my_learning_progress.html",
            {
                "student": student,
                "student_profile": student_profile,

                # Full queryset for the selector
                "active_enrollments": active_enrollments,

                # No selected enrollment/course
                "active_enrollment": None,
                "course": None,

                "chart_data": {
                    "labels": [],
                    "datasets": [],
                },
            },
        )

    # ---------------------------------------------------------
    # SELECTED / DEFAULT COURSE
    # ---------------------------------------------------------
    course = active_enrollment.course

    # ---------------------------------------------------------
    # SKILLS PROGRESS GRAPH
    # ---------------------------------------------------------
    chart_data = build_skill_progress_chart_data(
        student=student,
        course=course,
    )

    # ---------------------------------------------------------
    # ATTENDANCE
    # ---------------------------------------------------------
    attendances = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course,
        )
        .select_related("class_session")
        .order_by("-class_session__start_time")
    )

    attended_count = attendances.filter(
        status="attended"
    ).count()

    missed_count = attendances.filter(
        status="missed"
    ).count()

    excused_count = attendances.filter(
        status="excused"
    ).count()

    total_attendance_records = (
        attended_count
        + missed_count
        + excused_count
    )

    completed_classes = course.completed_sessions

    attendance_percentage = (
        round(
            attended_count
            / total_attendance_records
            * 100
        )
        if total_attendance_records > 0
        else 0
    )

    total_classes = course.total_sessions

    remaining_classes = max(
        total_classes - completed_classes,
        0,
    )

    completion_percentage = (
        round(
            completed_classes
            / total_classes
            * 100
        )
        if total_classes > 0
        else 0
    )

    recent_attendance = (
        attendances
        .filter(
            status__in=[
                "attended",
                "missed",
                "excused",
            ]
        )
        .order_by("-class_session__start_time")[:5]
    )

    context = {
        "student": student,
        "student_profile": student_profile,

        "active_enrollments": active_enrollments,
        "active_enrollment": active_enrollment,
        "course": course,

        "attended_count": attended_count,
        "missed_count": missed_count,
        "excused_count": excused_count,
        "total_attendance_records": total_attendance_records,
        "attendance_percentage": attendance_percentage,
        "recent_attendance": recent_attendance,

        "completed_classes": completed_classes,
        "remaining_classes": remaining_classes,
        "total_classes": total_classes,
        "completion_percentage": completion_percentage,

        # Skills graph data
        "chart_data": chart_data,
    }

    return render(
        request,
        "profiles/student/my_learning_progress.html",
        context,
    )


# STUDENT ATTENDANCE PAGE
@login_required
def my_attendance(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    # ---------------------------------------------------------
    # ALL ACTIVE ENROLLMENTS
    # Only include courses that are also currently active.
    # These are used to populate the course selector.
    # ---------------------------------------------------------
    active_enrollments = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
            status="active",
            course__status="active",
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
        .order_by("course__name")
    )

    # ---------------------------------------------------------
    # GET SELECTED COURSE FROM URL
    #
    # Example:
    # /profiles/student/my_attendance/?course=4
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")

    # ---------------------------------------------------------
    # DETERMINE WHICH ENROLLMENT / COURSE TO DISPLAY
    # ---------------------------------------------------------
    if selected_course_id:
        active_enrollment = (
            active_enrollments
            .filter(course_id=selected_course_id)
            .first()
        )

        # If an invalid/stale course ID is supplied,
        # fall back to the first available active enrollment.
        if not active_enrollment:
            active_enrollment = active_enrollments.first()

    else:
        active_enrollment = active_enrollments.first()

    # ---------------------------------------------------------
    # NO ACTIVE COURSE
    # ---------------------------------------------------------
    if not active_enrollment:
        return render(
            request,
            "profiles/student/my_attendance.html",
            {
                "profile": profile,
                "active_enrollments": active_enrollments,
                "active_enrollment": None,
                "recent_attendance": [],
                "recent_absences": [],
            }
        )

    # ---------------------------------------------------------
    # ATTENDED CLASSES
    # Data comes from the SELECTED course only.
    # ---------------------------------------------------------
    recent_attendance = (
        Attendance.objects
        .filter(
            student=request.user,
            class_session__course=active_enrollment.course,
            class_session__status=ClassSession.STATUS_COMPLETED,
            status=Attendance.STATUS_ATTENDED,
        )
        .select_related(
            "class_session",
            "class_session__course",
        )
        .order_by("-class_session__start_time")
    )

    # ---------------------------------------------------------
    # ABSENCES
    # Data comes from the SELECTED course only.
    # ---------------------------------------------------------
    recent_absences = (
        Attendance.objects
        .filter(
            student=request.user,
            class_session__course=active_enrollment.course,
            class_session__status=ClassSession.STATUS_COMPLETED,
            status__in=[
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ],
        )
        .select_related(
            "class_session",
            "class_session__course",
        )
        .order_by("-class_session__start_time")
    )

    context = {
        "profile": profile,

        # ALL active courses -> selector
        "active_enrollments": active_enrollments,

        # ONE selected course -> page content
        "active_enrollment": active_enrollment,

        "recent_attendance": recent_attendance,
        "recent_absences": recent_absences,
    }

    return render(
        request,
        "profiles/student/my_attendance.html",
        context
    )



@login_required
def my_skills(request):
    student = request.user
    student_profile = get_object_or_404(
        UserProfile,
        user=student,
    )

    # ---------------------------------------------------------
    # SECURITY
    # Only learner roles can access this page.
    # ---------------------------------------------------------
    if student_profile.role not in [
        UserProfile.ROLE_EMPLOYEE,
        UserProfile.ROLE_INDIVIDUAL,
    ]:
        return redirect("home")


    # ---------------------------------------------------------
    # ALL ACTIVE ENROLLMENTS
    # Only include courses that are also active.
    #
    # This queryset is used for:
    # - the course selector
    # - validating ?course=...
    # ---------------------------------------------------------
    active_enrollments = (
        CourseEnrollment.objects
        .filter(
            student=student,
            status="active",
            course__status="active",
        )
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
        .order_by(
            "-id",
        )
    )


    # ---------------------------------------------------------
    # SELECTED COURSE
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")

    if selected_course_id:
        active_enrollment = get_object_or_404(
            active_enrollments,
            course_id=selected_course_id,
        )

    else:
        # Use the first active enrollment as the default.
        active_enrollment = active_enrollments.first()

        # Make the selected/default course explicit in the URL.
        #
        # /my-skills/
        #
        # becomes:
        #
        # /my-skills/?course=4
        if active_enrollment:
            return redirect(
                f"{request.path}?course={active_enrollment.course_id}"
            )


    # ---------------------------------------------------------
    # NO ACTIVE COURSE
    # ---------------------------------------------------------
    if not active_enrollment:
        return render(
            request,
            "profiles/student/my_skills.html",
            {
                "student": student,
                "student_profile": student_profile,
                "active_enrollments": active_enrollments,
                "active_enrollment": None,
                "course": None,
                "skills": [],
                "skill_notes": [],
                "skill_note_display": [],
                "academic_profile": None,
                "chart_data": {
                    "labels": [],
                    "datasets": [],
                },
                "level_choices": UserProfile.LEVEL_CHOICES,
            },
        )


    # ---------------------------------------------------------
    # SELECTED COURSE
    # ---------------------------------------------------------
    course = active_enrollment.course


    # ---------------------------------------------------------
    # SKILL ICONS
    # ---------------------------------------------------------
    skill_icons = {
        "speaking": "fa-solid fa-microphone",
        "reading": "fa-solid fa-book-open",
        "writing": "fa-solid fa-pen",
        "listening": "fa-solid fa-headphones",
    }


    # ---------------------------------------------------------
    # IMPORTANT:
    # DO NOT create assessments from the learner-facing view.
    #
    # The teacher view may use get_or_create() because the teacher
    # is responsible for evaluating/editing skills.
    #
    # The student view should only READ existing assessments.
    # ---------------------------------------------------------
    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related(
            "subskill_assessments"
        )
        .order_by("skill")
    )


    # ---------------------------------------------------------
    # SKILL NOTEs DISPLAY
    # ---------------------------------------------------------
    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]


    # ---------------------------------------------------------
    # BUILD SKILL CARDS
    # ---------------------------------------------------------
    skills = []

    for assessment in skill_assessments:
        skills.append({
            "assessment": assessment,
            "assessment_id": assessment.id,
            "skill_value": assessment.skill,
            "name": assessment.get_skill_display(),
            "icon": skill_icons.get(
                assessment.skill,
                "fa-solid fa-chart-simple",
            ),
            "percentage": assessment.average_percentage,
            "teacher_notes": assessment.teacher_notes,
            "subskills": assessment.subskill_assessments.all(),
        })


    # ---------------------------------------------------------
    # TEACHER NOTES
    # ---------------------------------------------------------
    skill_notes = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .exclude(
            teacher_notes=""
        )
        .order_by("skill")
    )


    # ---------------------------------------------------------
    # ACADEMIC PROFILE
    # ---------------------------------------------------------
    academic_profile = getattr(
        student,
        "academic_profile",
        None
    )


    # ---------------------------------------------------------
    # SKILL PROGRESS CHART
    # ---------------------------------------------------------
    chart_data = build_skill_progress_chart_data(
        student=student,
        course=course,
    )


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "student": student,
        "student_profile": student_profile,

        # ALL active enrollments -> course selector
        "active_enrollments": active_enrollments,

        # ONE selected enrollment -> current page
        "active_enrollment": active_enrollment,

        "course": course,

        "skills": skills,
        "academic_profile": academic_profile,

        # Use normal Python object because your template already
        # uses json_script.
        "chart_data": chart_data,

        "skill_notes": skill_notes,
        "skill_note_display": skill_note_display,

        "level_choices": UserProfile.LEVEL_CHOICES,
    }


    return render(
        request,
        "profiles/student/my_skills.html",
        context,
    )



@login_required
def my_learning_progress_assessment(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    # Only learners can access this page
    if profile.role not in [
        UserProfile.ROLE_INDIVIDUAL,
        UserProfile.ROLE_EMPLOYEE,
    ]:
        return redirect("home")

    student = request.user
    student_profile = profile


    # =========================================================
    # ALL ACTIVE ENROLLMENTS
    # Used by the course selector
    # =========================================================

    active_enrollments = (
        CourseEnrollment.objects
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
        )
        .filter(
            student=student,
            status="active",
            course__status="active",
        )
        .order_by("-enrolled_at")
    )


    # =========================================================
    # SELECT CURRENT COURSE
    # =========================================================

    requested_course_id = request.GET.get("course")


    if requested_course_id:
        # Use the course explicitly selected in ?course=
        #
        # Security:
        # student=student ensures a learner cannot access
        # another student's enrollment by changing the ID.
        enrollment = get_object_or_404(
            CourseEnrollment.objects.select_related(
                "course",
                "course__teacher",
                "course__course_type",
                "student",
                "student__profile",
            ),
            student=student,
            course_id=requested_course_id,
        )

    else:
        # No course supplied in URL:
        # default to the most recent ACTIVE enrollment.
        enrollment = active_enrollments.first()


    course = enrollment.course if enrollment else None


    # =========================================================
    # SKILL ASSESSMENTS
    # =========================================================

    if course:
        skill_assessments = (
            StudentSkillAssessment.objects
            .filter(
                student=student,
                course=course,
            )
            .prefetch_related("subskill_assessments")
            .order_by("skill")
        )

    else:
        skill_assessments = StudentSkillAssessment.objects.none()


    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]


    # =========================================================
    # TEACHER NOTES
    # =========================================================

    if course:
        skill_notes = (
            StudentSkillAssessment.objects
            .filter(
                student=student,
                course=course,
            )
            .exclude(teacher_notes="")
            .order_by("skill")
        )

    else:
        skill_notes = StudentSkillAssessment.objects.none()


    # =========================================================
    # TEMPORARY DEBUG
    # =========================================================

    print("ASSESSMENT requested_course_id:", requested_course_id)
    print("ASSESSMENT selected course:", course.id if course else None)
    print(
        "ASSESSMENT active courses:",
        list(active_enrollments.values_list("course_id", flat=True))
    )


    context = {
        "profile": profile,
        "student": student,
        "student_profile": student_profile,

        # All active courses — for selector
        "active_enrollments": active_enrollments,

        # Currently selected course
        "active_enrollment": enrollment,
        "enrollment": enrollment,
        "course": course,

        # Assessment
        "skill_notes": skill_notes,
        "skill_note_display": skill_note_display,
    }


    return render(
        request,
        "profiles/student/my_learning_progress_assessment.html",
        context,
    )




# ***********************************************|
# TEACHER PROFILE  ******************************|
# ***********************************************|

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

    # Month range: first day - last day
    start_of_month_date = today.replace(day=1)
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    end_of_month_date = today.replace(day=last_day_of_month)

    start_of_month = timezone.make_aware(
        datetime.combine(start_of_month_date, time.min)
    )
    end_of_month = timezone.make_aware(
        datetime.combine(end_of_month_date, time.max)
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
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
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
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
            start_time__gte=start_of_week,
            start_time__lte=end_of_week,
        )
        .select_related("course")
        .prefetch_related("attendance_records")
    )

    monthly_sessions = (
        ClassSession.objects
        .filter(
            course__teacher=request.user,
            course__status="active",
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
            start_time__gte=start_of_month,
            start_time__lte=end_of_month,
        )
        .select_related("course")
        .prefetch_related("attendance_records")
    )

    # Weekly data
    total_weekly_sessions = weekly_sessions.count()

    completed_weekly_sessions = weekly_sessions.filter(
        status=ClassSession.STATUS_COMPLETED
    ).count()

    upcoming_weekly_sessions = weekly_sessions.filter(
        status__in=[
            ClassSession.STATUS_SCHEDULED,
            ClassSession.STATUS_RESCHEDULED,
        ],
        start_time__gte=now,
    ).count()

    weekly_attendance_completed_sessions = (
        weekly_sessions
        .filter(attendance_records__status__in=["attended", "missed", "excused"])
        .distinct()
        .count()
    )

    # Monthly data
    total_monthly_sessions = monthly_sessions.count()

    total_monthly_completed_sessions = monthly_sessions.filter(
        status=ClassSession.STATUS_COMPLETED
    ).count()

    total_monthly_upcoming_sessions = monthly_sessions.filter(
        status__in=[
            ClassSession.STATUS_SCHEDULED,
            ClassSession.STATUS_RESCHEDULED,
        ],
        start_time__gte=now,
    ).count()

    monthly_attendance_completed_sessions = (
        monthly_sessions
        .filter(attendance_records__status__in=["attended", "missed", "excused"])
        .distinct()
        .count()
    )

    # Calculate attendance Percentages
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

    total_monthly_completed_percentage = get_percentage(
        total_monthly_completed_sessions,
        total_monthly_sessions
    )

    total_monthly_upcoming_percentage = get_percentage(
        total_monthly_upcoming_sessions,
        total_monthly_sessions
    )

    weekly_attendance_completed_percentage = get_percentage(
        weekly_attendance_completed_sessions,
        total_weekly_sessions
    )

    monthly_attendance_completed_percentage = get_percentage(
        monthly_attendance_completed_sessions,
        total_monthly_sessions
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
        class_session__status=ClassSession.STATUS_COMPLETED,
        status__in=[
            Attendance.STATUS_ATTENDED,
            Attendance.STATUS_MISSED,
            Attendance.STATUS_EXCUSED,
        ],
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
        "weekly_attendance_completed_sessions": weekly_attendance_completed_sessions,
        "weekly_attendance_completed_percentage": weekly_attendance_completed_percentage,

        # General attendance rate
        "total_attendance_rate": total_attendance_rate,

        # Monthly data
        "total_monthly_sessions": total_monthly_sessions,
        "total_monthly_completed_sessions": total_monthly_completed_sessions,
        "total_monthly_upcoming_sessions": total_monthly_upcoming_sessions,
        "total_monthly_completed_percentage": total_monthly_completed_percentage,
        "total_monthly_upcoming_percentage": total_monthly_upcoming_percentage,
        "monthly_attendance_completed_sessions": monthly_attendance_completed_sessions,
        "monthly_attendance_completed_percentage": monthly_attendance_completed_percentage,
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
        .filter(
            course__teacher=request.user,
            course__status="active",
        )
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
        "upcoming": {
            "today": 0,
            "weekly": 0,
            "monthly": 0,
            "all": 0,
        },
        "completed": {
            "today": 0,
            "weekly": 0,
            "monthly": 0,
            "all": 0,
        },
    }

    for session in sessions:
        session_date = timezone.localdate(session.start_time)

        session.is_upcoming = (
            session.status in [
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
            ]
            and session.start_time > now
        )

        session.is_completed = (
            session.status == ClassSession.STATUS_COMPLETED
        )

        session.is_today = session_date == today
        session.is_this_week = start_of_week <= session_date <= end_of_week
        session.is_this_month = (
            session_date.year == today.year
            and session_date.month == today.month
        )

        if session.status == ClassSession.STATUS_PENDING_RESCHEDULE:
            session.class_status_group = "pending_reschedule"
        elif session.is_completed:
            session.class_status_group = "completed"
        elif session.is_upcoming:
            session.class_status_group = "upcoming"
        else:
            # Scheduled/rescheduled but not future and not completed:
            # still outstanding until explicitly completed.
            session.class_status_group = "in_progress"

        if session.is_upcoming:
            class_filter_counts["upcoming"]["all"] += 1

            if session.is_today:
                class_filter_counts["upcoming"]["today"] += 1

            if session.is_this_week:
                class_filter_counts["upcoming"]["weekly"] += 1

            if session.is_this_month:
                class_filter_counts["upcoming"]["monthly"] += 1

        if session.is_completed:
            class_filter_counts["completed"]["all"] += 1

            if session.is_today:
                class_filter_counts["completed"]["today"] += 1

            if session.is_this_week:
                class_filter_counts["completed"]["weekly"] += 1

            if session.is_this_month:
                class_filter_counts["completed"]["monthly"] += 1

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

    total_classes = course.total_sessions
    completed_classes = course.completed_sessions
    remaining_classes = course.remaining_sessions
    completion_percentage = course.completion_percentage

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
def teacher_group_attendance(request, course_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    now = timezone.now()

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user,
    )

    class_sessions = (
        course.class_sessions
        .filter(
            start_time__lt=now,
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
        )
        .annotate(
            attended_count=Count(
                "attendance_records",
                filter=Q(attendance_records__status="attended"),
            ),
            missed_count=Count(
                "attendance_records",
                filter=Q(attendance_records__status="missed"),
            ),
            excused_count=Count(
                "attendance_records",
                filter=Q(attendance_records__status="excused"),
            ),
        )
        .order_by("-start_time")
    )   
 
    context = {
        "course": course,
        "class_sessions": class_sessions,
    }

    return render(
        request,
        "profiles/teacher/teacher_group_attendance.html",
        context,
    )



@login_required
def teacher_session_attendance_detail(request, session_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    session = get_object_or_404(
        ClassSession.objects.select_related("course"),
        id=session_id,
        course__teacher=request.user,
        start_time__lt=timezone.now(),
        status__in=[
            ClassSession.STATUS_SCHEDULED,
            ClassSession.STATUS_RESCHEDULED,
            ClassSession.STATUS_COMPLETED,
        ],
    )

    attendance_records = (
        session.attendance_records
        .select_related(
            "student",
            "student__profile",
        )
        .order_by(
            "student__first_name",
            "student__last_name",
        )
    )

    context = {
        "session": session,
        "course": session.course,
        "attendance_records": attendance_records,
    }

    return render(
        request,
        "profiles/teacher/teacher_session_attendance_detail.html",
        context,
    )



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

    total_classes = course.total_sessions
    completed_classes = course.completed_sessions
    remaining_classes = course.remaining_sessions
    completion_percentage = course.completion_percentage

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


# BUILD STD SKILLS GRAPH
def build_skill_progress_chart_data(student, course):
    snapshots = (
        StudentSkillTermSnapshot.objects
        .filter(
            skill_assessment__student=student,
            skill_assessment__course=course,
        )
        .select_related("skill_assessment")
        .order_by("recorded_at")
    )

    chart_labels = []

    for snapshot in snapshots:
        if snapshot.term_label not in chart_labels:
            chart_labels.append(snapshot.term_label)

    skill_chart_values = {
        "Speaking": [],
        "Reading": [],
        "Writing": [],
        "Listening": [],
    }

    for skill_name in skill_chart_values.keys():
        skill_value = skill_name.lower()

        for label in chart_labels:
            matching_snapshot = None

            for snapshot in snapshots:
                if (
                    snapshot.skill_assessment.skill == skill_value
                    and snapshot.term_label == label
                ):
                    matching_snapshot = snapshot
                    break

            skill_chart_values[skill_name].append(
                matching_snapshot.percentage if matching_snapshot else None
            )

    return {
        "labels": chart_labels,
        "datasets": [
            {
                "label": "Speaking",
                "data": skill_chart_values["Speaking"],
                "borderColor": "#00b894",
                "backgroundColor": "#00b894",
                "tension": 0.35,
            },
            {
                "label": "Reading",
                "data": skill_chart_values["Reading"],
                "borderColor": "#1e6bff",
                "backgroundColor": "#1e6bff",
                "tension": 0.35,
            },
            {
                "label": "Writing",
                "data": skill_chart_values["Writing"],
                "borderColor": "#ff7a00",
                "backgroundColor": "#ff7a00",
                "tension": 0.35,
            },
            {
                "label": "Listening",
                "data": skill_chart_values["Listening"],
                "borderColor": "#7c3aed",
                "backgroundColor": "#7c3aed",
                "tension": 0.35,
            },
        ],
    }


# Helper to display Teacher notes (+ future automated reports ???)
def build_skill_note_display(skill_assessment):
    subskills = skill_assessment.subskill_assessments.all()

    return {
        "skill": skill_assessment.get_skill_display(),
        "percentage": skill_assessment.average_percentage,
        "score": skill_assessment.average_score,
        "strengths": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating in ["strong", "confident"]
        ],
        "pass": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating == "passing"
        ],
        "developing": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating == "developing"
        ],
        "needs_work": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating == "needs_work"
        ],
        "plain_notes": skill_assessment.teacher_notes,
    }


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
   
    # Progress is based on the learner's actually assigned sessions.
    # A ClassSession counts as completed ONLY when status="completed".
    completed_classes = enrollment.total_completed_classes
    total_classes = enrollment.total_assigned_classes
    remaining_classes = enrollment.upcoming_classes

    if completed_classes > 0:
        attendance_percentage = round(
            (attended_count / completed_classes) * 100
        )
    else:
        attendance_percentage = 0

    completion_percentage = (
        round((completed_classes / total_classes) * 100)
        if total_classes > 0
        else 0
    )

    recent_attendance = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course,
            status__in=["attended", "missed", "excused"],
        )
        .select_related("class_session")
        .order_by("-class_session__start_time")[:5]
    )


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
        "recent_attendance": recent_attendance,

        "completed_classes": completed_classes,
        "remaining_classes": remaining_classes,
        "total_classes": total_classes,
        "completion_percentage": completion_percentage,
    }

    return render(
        request,
        "profiles/teacher/teacher_student_detail.html",
        context
    )



@login_required
def student_academic_profile_settings(request, course_id, enrollment_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user,
    )

    enrollment = get_object_or_404(
        CourseEnrollment.objects.select_related(
            "student",
            "student__profile",
            "course",
        ),
        id=enrollment_id,
        course=course,
    )

    student = enrollment.student

    academic_profile, created = StudentAcademicProfile.objects.get_or_create(
        student=student
    )

    if request.method == "POST":
        form = StudentAcademicProfileForm(
            request.POST,
            instance=academic_profile,
        )

        if form.is_valid():
            form.save()
            return redirect(
                "profiles:teacher_student_detail",
                course_id=course.id,
                enrollment_id=enrollment.id,
            )
    else:
        form = StudentAcademicProfileForm(instance=academic_profile)

    context = {
        "course": course,
        "enrollment": enrollment,
        "student": student,
        "student_profile": student.profile,
        "academic_profile": academic_profile,
        "form": form,
    }

    return render(
        request,
        "profiles/teacher/student_academic_profile_settings.html",
        context,
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



def student_attendance_record(request, course_id, enrollment_id):

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
   
    # Progress is based on the learner's actually assigned sessions.
    # A ClassSession counts as completed ONLY when status="completed".
    completed_classes = enrollment.total_completed_classes
    total_classes = enrollment.total_assigned_classes
    remaining_classes = enrollment.upcoming_classes

    if completed_classes > 0:
        attendance_percentage = round(
            (attended_count / completed_classes) * 100
        )
    else:
        attendance_percentage = 0

    completion_percentage = (
        round((completed_classes / total_classes) * 100)
        if total_classes > 0
        else 0
    )

    recent_attendance = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course,
            status__in=["attended", "missed", "excused"],
        )
        .select_related("class_session")
        .order_by("-class_session__start_time")
    )

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
        # "active_tab": "overview",
    }

    return render(
        request,
        "profiles/teacher/teacher_student_attendance_record.html",
        context
    )


# FROM STUDENT DETAIL Page --> ATTENDANCE RECORD Page
# Update attendance directly
@login_required
def update_student_attendance_status(request, course_id, enrollment_id, attendance_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user,
    )

    enrollment = get_object_or_404(
        CourseEnrollment,
        id=enrollment_id,
        course=course,
    )

    attendance = get_object_or_404(
        Attendance,
        id=attendance_id,
        student=enrollment.student,
        class_session__course=course,
    )

    if request.method == "POST":
        status = request.POST.get("status")

        if status in ["attended", "missed", "excused"]:
            attendance.status = status
            attendance.save()

    return redirect(
        "profiles:student_attendance_record",
        course_id=course.id,
        enrollment_id=enrollment.id,
    )



@login_required
def student_skills_overview(request, course_id, enrollment_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user,
    )

    enrollment = get_object_or_404(
        CourseEnrollment.objects.select_related(
            "student",
            "student__profile",
            "course",
        ),
        id=enrollment_id,
        course=course,
    )

    student = enrollment.student
    student_profile = student.profile

    skill_icons = {
        "speaking": "fa-solid fa-microphone",
        "reading": "fa-solid fa-book-open",
        "writing": "fa-solid fa-pen",
        "listening": "fa-solid fa-headphones",
    }

    for skill_value, skill_label in StudentSkillAssessment.SKILL_AREA_CHOICES:
        skill_assessment, created = StudentSkillAssessment.objects.get_or_create(
            student=student,
            course=course,
            skill=skill_value,
        )

        for subskill_value, subskill_label in SUBSKILLS.get(skill_value, []):
            StudentSubSkillAssessment.objects.get_or_create(
                skill_assessment=skill_assessment,
                subskill=subskill_value,
            )

    valid_skill_values = [
        skill_value
        for skill_value, skill_label in StudentSkillAssessment.SKILL_AREA_CHOICES
    ]

    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related("subskill_assessments")
        .order_by("skill")
    )

    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]


    skills = []

    for assessment in skill_assessments:
        skills.append({
            "assessment": assessment,
            "assessment_id": assessment.id,
            "skill_value": assessment.skill,
            "name": assessment.get_skill_display(),
            "icon": skill_icons.get(
                assessment.skill,
                "fa-solid fa-chart-simple",
            ),
            "percentage": assessment.average_percentage,
            "teacher_notes": assessment.teacher_notes,
            "subskills": assessment.subskill_assessments.all(),
        })

    skill_notes = (
    StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .exclude(teacher_notes="")
        .order_by("skill")
    )
    

    academic_profile = getattr(student, "academic_profile", None)

    chart_data = build_skill_progress_chart_data(
        student=student,
        course=course,
    )

    context = {
        "course": course,
        "enrollment": enrollment,
        "student": student,
        "student_profile": student_profile,
        "skills": skills,
        "academic_profile": academic_profile,
        "chart_data_json": json.dumps(chart_data),
        "skill_notes": skill_notes,
        "skill_note_display": skill_note_display,
        "level_choices": UserProfile.LEVEL_CHOICES,
    }

    return render(
        request,
        "profiles/teacher/student_skills_overview.html",
        context,
    )



@login_required
def teacher_edit_student_skill(request, skill_assessment_id):
    skill_assessment = get_object_or_404(
        StudentSkillAssessment.objects.select_related(
            "student",
            "course",
        ).prefetch_related(
            "subskill_assessments",
        ),
        id=skill_assessment_id,
        course__teacher=request.user,
    )

    skill = StudentSkillAssessment.SKILL_AREA_CHOICES


    if request.method == "POST":
        form = StudentSkillAssessmentForm(
            request.POST,
            instance=skill_assessment,
        )

        formset = StudentSubSkillAssessmentFormSet(
            request.POST,
            instance=skill_assessment,
        )

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            # Clear old prefetched subskills cache
            if hasattr(skill_assessment, "_prefetched_objects_cache"):
                skill_assessment._prefetched_objects_cache = {}

            skill_assessment.teacher_notes = skill_assessment.generate_teacher_notes()
            skill_assessment.save(update_fields=["teacher_notes", "updated_at"])

            current_term = timezone.localdate().strftime("%d %b %Y")

            StudentSkillTermSnapshot.objects.update_or_create(
                skill_assessment=skill_assessment,
                term_label=current_term,
                defaults={
                    "percentage": skill_assessment.average_percentage,
                },
            )

            enrollment = get_object_or_404(
                CourseEnrollment,
                student=skill_assessment.student,
                course=skill_assessment.course,
            )

            return redirect(
                "profiles:student_skills_overview",
                course_id=skill_assessment.course.id,
                enrollment_id=enrollment.id,
            )

    else:
        form = StudentSkillAssessmentForm(
            instance=skill_assessment,
        )

        formset = StudentSubSkillAssessmentFormSet(
            instance=skill_assessment,
        )

    context = {
        "skill_assessment": skill_assessment,
        "form": form,
        "formset": formset,
        "skill": skill,
    }

    return render(
        request,
        "profiles/teacher/teacher_edit_student_skill.html",
        context,
    )



def teacher_student_assessment_notes(request, course_id, enrollment_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id,
    )

    enrollment = get_object_or_404(
        CourseEnrollment.objects.select_related(
            "student",
            "student__profile",
            "course",
        ),
        id=enrollment_id,
        course=course,
    )

    student = enrollment.student
    student_profile = student.profile

    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related("subskill_assessments")
        .order_by("skill")
    )

    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]

    skills = []

    skill_notes = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .exclude(teacher_notes="")
        .order_by("skill")
    )

    context = {
        "profile": profile,
        "course": course,
        "enrollment": enrollment,
        "student": student,
        "student_profile": student_profile,
        "skills": skills,
        "skill_notes": skill_notes,
        "skill_note_display": skill_note_display,
        "level_choices": UserProfile.LEVEL_CHOICES,
    }

    return render(
        request,
        "profiles/teacher/teacher_student_assessment_notes.html",
        context,
    )



def teacher_student_progress_skills_graph(request, course_id, enrollment_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id,
    )

    enrollment = get_object_or_404(
        CourseEnrollment.objects.select_related(
            "student",
            "student__profile",
            "course",
        ),
        id=enrollment_id,
        course=course,
    )

    student = enrollment.student
    student_profile = student.profile

    skill_icons = {
        "speaking": "fa-solid fa-microphone",
        "reading": "fa-solid fa-book-open",
        "writing": "fa-solid fa-pen",
        "listening": "fa-solid fa-headphones",
    }

    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related("subskill_assessments")
        .order_by("skill")
    )

    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]

    skills = []

    for assessment in skill_assessments:
        skills.append({
            "assessment": assessment,
            "assessment_id": assessment.id,
            "skill_value": assessment.skill,
            "name": assessment.get_skill_display(),
            "icon": skill_icons.get(
                assessment.skill,
                "fa-solid fa-chart-simple",
            ),
            "percentage": assessment.average_percentage,
            "teacher_notes": assessment.teacher_notes,
            "subskills": assessment.subskill_assessments.all(),
        })

    skill_notes = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .exclude(teacher_notes="")
        .order_by("skill")
    )

    academic_profile = getattr(student, "academic_profile", None)

    chart_data = build_skill_progress_chart_data(
        student=student,
        course=course,
    )

    context = {
        "profile": profile,
        "course": course,
        "enrollment": enrollment,
        "student": student,
        "student_profile": student_profile,
        "skills": skills,
        "academic_profile": academic_profile,
        "chart_data": chart_data,
        "skill_notes": skill_notes,
        "skill_note_display": skill_note_display,
        "level_choices": UserProfile.LEVEL_CHOICES,
    }

    return render(
        request,
        "profiles/teacher/teacher_student_progress_skills_graph.html",
        context,
    )



# TEACHER CALENDAR PAGE
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


# Create Calendar EVENTS
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
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
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
            course__status="active",
            start_time__lte=now,
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
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

    for session in sessions_queryset:
        # Attendance rows are generated automatically and are the source of
        # truth for which learners are assigned to this lesson.
        session.students_count = session.attendance_records.count()

        if session.status == ClassSession.STATUS_COMPLETED:
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
        final_attendance_statuses = {
            Attendance.STATUS_ATTENDED,
            Attendance.STATUS_MISSED,
            Attendance.STATUS_EXCUSED,
        }

        for enrollment in enrollments:
            status = request.POST.get(
                f"attendance_{enrollment.student_id}"
            )

            if status in final_attendance_statuses:
                Attendance.objects.update_or_create(
                    student=enrollment.student,
                    class_session=class_session,
                    defaults={
                        "status": status,
                    }
                )

        # Once every Attendance record assigned to this session has a final
        # learner outcome, the lesson itself is completed.
        #
        # ClassSession.save() will then check whether this was the final
        # unfinished lesson and, if so, complete the Course + active
        # CourseEnrollments automatically.
        attendance_records = class_session.attendance_records.all()

        has_attendance_records = attendance_records.exists()
        has_unfinished_attendance = attendance_records.filter(
            status=Attendance.STATUS_SCHEDULED
        ).exists()

        if has_attendance_records and not has_unfinished_attendance:
            if class_session.status != ClassSession.STATUS_COMPLETED:
                class_session.status = ClassSession.STATUS_COMPLETED
                class_session.save(update_fields=["status"])

            messages.success(
                request,
                "Attendance saved and lesson marked as completed."
            )
        else:
            messages.success(
                request,
                "Attendance saved. Complete all learner records to finish the lesson."
            )

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

    course = class_session.course

    attendances = list(
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

    enrollments_by_student_id = {
        enrollment.student_id: enrollment
        for enrollment in CourseEnrollment.objects.filter(
            course=class_session.course,
            student_id__in=[
                attendance.student_id
                for attendance in attendances
            ],
        )
    }

    for attendance in attendances:
        attendance.enrollment = enrollments_by_student_id.get(
            attendance.student_id
        )

    attended_count = sum(
        1 for attendance in attendances
        if attendance.status == "attended"
    )

    missed_count = sum(
        1 for attendance in attendances
        if attendance.status == "missed"
    )

    excused_count = sum(
        1 for attendance in attendances
        if attendance.status == "excused"
    )

    total_count = len(attendances)

    context = {
        "profile": profile,
        "class_session": class_session,
        "course": course,
        "attendances": attendances,
        "attended_count": attended_count,
        "missed_count": missed_count,
        "excused_count": excused_count,
        "total_count": total_count,
    }

    return render(
        request,
        "profiles/teacher/teacher_attendance_detail.html",
        context,
    )


# SET A CLASS IN CLASS_LIST Page
# As PENDING to Reschedule
@login_required
def mark_class_pending_reschedule(request, session_id):
    session = get_object_or_404(
        ClassSession,
        id=session_id,
        course__teacher=request.user,
    )

    if request.method == "POST":
        # Rescheduling belongs to ClassSession, not Attendance.
        # Existing Attendance records remain status="scheduled" and stay
        # attached to this same ClassSession throughout the reschedule flow.
        session.status = ClassSession.STATUS_PENDING_RESCHEDULE
        session.save(update_fields=["status"])

        messages.success(
            request,
            "Class marked as pending reschedule."
        )

    return redirect("profiles:teacher_classes_list")



@login_required
def teacher_reschedule_classes(request):
    pending_sessions = (
        ClassSession.objects
        .filter(
            course__teacher=request.user,
            status=ClassSession.STATUS_PENDING_RESCHEDULE,
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
        )
        .order_by("start_time")
    )

    return render(
        request,
        "profiles/teacher/teacher_reschedule_classes.html",
        {
            "pending_sessions": pending_sessions,
        }
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


# CHOOSE NEW TIME & DATE
# To Reschedule Pending Class
@login_required
def reschedule_class_detail(request, session_id):
    session = get_object_or_404(
        ClassSession,
        id=session_id,
        course__teacher=request.user,
        status=ClassSession.STATUS_PENDING_RESCHEDULE,
    )

    if request.method == "POST":
        new_date = request.POST.get("new_date")
        new_start_time = request.POST.get("new_start_time")

        if not new_date or not new_start_time:
            messages.error(request, "Please choose both a new date and start time.")
            return redirect(
                "profiles:reschedule_class_detail",
                session_id=session.id,
            )

        old_duration = session.end_time - session.start_time

        naive_start = datetime.strptime(
            f"{new_date} {new_start_time}",
            "%Y-%m-%d %H:%M",
        )

        new_start = timezone.make_aware(
            naive_start,
            timezone.get_current_timezone(),
        )

        new_end = new_start + old_duration

        session.start_time = new_start
        session.end_time = new_end
        session.status = ClassSession.STATUS_RESCHEDULED
        session.save(update_fields=[
            "start_time",
            "end_time",
            "status",
        ])

        messages.success(
            request,
            "Class successfully rescheduled."
        )

        return redirect("profiles:teacher_reschedule_classes")

    return render(
        request,
        "profiles/teacher/reschedule_class_detail.html",
        {
            "session": session,
        }
    )



# *****************************************************|
# COMPANY ADMIN PROFILE  ******************************|
# *****************************************************|

@login_required
def company_admin_dashboard(request):
    profile = request.user.profile

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

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

    # Month range
    start_of_month_date = today.replace(day=1)
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    end_of_month_date = today.replace(day=last_day_of_month)

    start_of_month = timezone.make_aware(
        datetime.combine(start_of_month_date, time.min)
    )
    end_of_month = timezone.make_aware(
        datetime.combine(end_of_month_date, time.max)
    )

    courses = (
        Course.objects
        .filter(company=company)
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
            course__company=company,
            course__status="active",
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
            start_time__gte=start_of_day,
            start_time__lte=end_of_day,
        )
        .select_related(
            "course",
            "course__teacher",
            "course__company",
        )
        .prefetch_related(
            "course__enrollments",
            "course__enrollments__student",
        )
        .order_by("start_time")
    )

    weekly_sessions = (
        ClassSession.objects
        .filter(
            course__company=company,
            course__status="active",
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
            start_time__gte=start_of_week,
            start_time__lte=end_of_week,
        )
        .select_related("course")
        .prefetch_related("attendance_records")
    )

    monthly_sessions = (
        ClassSession.objects
        .filter(
            course__company=company,
            course__status="active",
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
            start_time__gte=start_of_month,
            start_time__lte=end_of_month,
        )
        .select_related("course")
        .prefetch_related("attendance_records")
    )

    def get_percentage(value, total):
        if total == 0:
            return 0
        return round((value / total) * 100)

    # Weekly data
    total_weekly_sessions = weekly_sessions.count()

    completed_weekly_sessions = weekly_sessions.filter(
        status=ClassSession.STATUS_COMPLETED
    ).count()

    upcoming_weekly_sessions = weekly_sessions.filter(
        status__in=[
            ClassSession.STATUS_SCHEDULED,
            ClassSession.STATUS_RESCHEDULED,
        ],
        start_time__gte=now,
    ).count()

    completed_weekly_percentage = get_percentage(
        completed_weekly_sessions,
        total_weekly_sessions
    )

    upcoming_weekly_percentage = get_percentage(
        upcoming_weekly_sessions,
        total_weekly_sessions
    )

    # Monthly data
    total_monthly_sessions = monthly_sessions.count()

    total_monthly_completed_sessions = monthly_sessions.filter(
        status=ClassSession.STATUS_COMPLETED
    ).count()

    total_monthly_upcoming_sessions = monthly_sessions.filter(
        status__in=[
            ClassSession.STATUS_SCHEDULED,
            ClassSession.STATUS_RESCHEDULED,
        ],
        start_time__gte=now,
    ).count()

    total_monthly_completed_percentage = get_percentage(
        total_monthly_completed_sessions,
        total_monthly_sessions
    )

    total_monthly_upcoming_percentage = get_percentage(
        total_monthly_upcoming_sessions,
        total_monthly_sessions
    )

    # Total active students in this company’s active courses
    total_students = (
        courses
        .filter(status="active")
        .filter(enrollments__status="active")
        .values("enrollments__student")
        .distinct()
        .count()
    )

    attendance_records = Attendance.objects.filter(
        class_session__course__company=company,
        class_session__course__status="active",
        class_session__status=ClassSession.STATUS_COMPLETED,
        status__in=[
            Attendance.STATUS_ATTENDED,
            Attendance.STATUS_MISSED,
            Attendance.STATUS_EXCUSED,
        ],
    )

    total_attendance_records = attendance_records.count()

    attended_records = attendance_records.filter(
        status="attended"
    ).count()

    total_attendance_rate = get_percentage(
        attended_records,
        total_attendance_records
    )

    weekly_attendance_records = Attendance.objects.filter(
        class_session__course__company=company,
        class_session__course__status="active",
        class_session__status=ClassSession.STATUS_COMPLETED,
        class_session__start_time__gte=start_of_week,
        class_session__start_time__lte=end_of_week,
        status__in=["attended", "missed", "excused"],
    )

    weekly_total_attendance_records = weekly_attendance_records.count()

    weekly_attended_records = weekly_attendance_records.filter(
        status="attended"
    ).count()

    weekly_attendance_rate = get_percentage(
        weekly_attended_records,
        weekly_total_attendance_records,
    )

    monthly_attendance_records = Attendance.objects.filter(
        class_session__course__company=company,
        class_session__course__status="active",
        class_session__status=ClassSession.STATUS_COMPLETED,
        class_session__start_time__gte=start_of_month,
        class_session__start_time__lte=end_of_month,
        status__in=["attended", "missed", "excused"],
    )

    monthly_total_attendance_records = monthly_attendance_records.count()

    monthly_attended_records = monthly_attendance_records.filter(
        status="attended"
    ).count()

    monthly_attendance_rate = get_percentage(
        monthly_attended_records,
        monthly_total_attendance_records
    )

    context = {
        "profile": profile,
        "company": company,
        "courses": courses,
        "todays_sessions": todays_sessions,
        "today": today,
        "active_courses": active_courses,

        "total_students": total_students,

        "total_weekly_sessions": total_weekly_sessions,
        "completed_weekly_sessions": completed_weekly_sessions,
        "completed_weekly_percentage": completed_weekly_percentage,
        "upcoming_weekly_sessions": upcoming_weekly_sessions,
        "upcoming_weekly_percentage": upcoming_weekly_percentage,

        "total_attendance_rate": total_attendance_rate,

        "total_monthly_sessions": total_monthly_sessions,
        "total_monthly_completed_sessions": total_monthly_completed_sessions,
        "total_monthly_upcoming_sessions": total_monthly_upcoming_sessions,
        "total_monthly_completed_percentage": total_monthly_completed_percentage,
        "total_monthly_upcoming_percentage": total_monthly_upcoming_percentage,

        "weekly_attendance_rate": weekly_attendance_rate,
        "monthly_attendance_rate": monthly_attendance_rate,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_dashboard.html",
        context
    )



@login_required
def company_admin_courses(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    courses = (
        Course.objects
        .filter(company=company)
        .annotate(enrollment_count=Count("enrollments"))
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
        "company": company,
        "courses": courses,
        "total_courses": total_courses,
        "active_courses": active_courses,
        "confirmed_courses": confirmed_courses,
        "cancelled_courses": cancelled_courses,
        "paused_courses": paused_courses,
        "active_courses_list": active_courses_list,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_courses.html",
        context
    )



@login_required
def company_admin_all_courses_attendance(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    now = timezone.now()

    selected_date = request.GET.get("date", "").strip()
    course_search = request.GET.get("course", "").strip()
    employee_search = request.GET.get("employee", "").strip()

    parsed_date = None

    if selected_date:
        parsed_date = parse_date(selected_date)

    # Active employees enrolled in each course.
    enrollment_queryset = (
        CourseEnrollment.objects
        .filter(status="active")
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

    # Load class sessions and their attendance records efficiently.
    class_session_queryset = (
        ClassSession.objects
        .filter(
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
        )
        .select_related(
            "course",
        )
        .prefetch_related(
            Prefetch(
                "attendance_records",
                queryset=(
                    Attendance.objects
                    .select_related(
                        "student",
                        "student__profile",
                    )
                    .order_by(
                        "student__first_name",
                        "student__last_name",
                        "student__email",
                    )
                ),
            )
        )
        .order_by("start_time")
    )

    # When a date is selected, the course figures refer only to that date.
    if parsed_date:
        class_session_queryset = class_session_queryset.filter(
            start_time__date=parsed_date,
        )

    courses = (
        Course.objects
        .filter(company=company)
        .select_related(
            "course_type",
            "company",
            "teacher",
            "teacher__profile",
        )
        .prefetch_related(
            Prefetch(
                "enrollments",
                queryset=enrollment_queryset,
                to_attr="active_enrollments",
            ),
            Prefetch(
                "class_sessions",
                queryset=class_session_queryset,
                to_attr="attendance_class_sessions",
            ),
        )
        .order_by("name")
    )

    # Search by course name or course type.
    if course_search:
        courses = courses.filter(
            Q(name__icontains=course_search)
            | Q(course_type__name__icontains=course_search)
        )

    # Find courses containing the searched employee.
    if employee_search:
        employee_parts = employee_search.split()

        employee_query = (
            Q(
                enrollments__student__email__icontains=employee_search,
            )
            | Q(
                enrollments__student__username__icontains=employee_search,
            )
            | Q(
                enrollments__student__first_name__icontains=employee_search,
            )
            | Q(
                enrollments__student__last_name__icontains=employee_search,
            )
        )

        # Supports full-name searches such as "John Smith".
        if len(employee_parts) >= 2:
            first_name_search = employee_parts[0]
            last_name_search = " ".join(employee_parts[1:])

            employee_query |= (
                Q(
                    enrollments__student__first_name__icontains=(
                        first_name_search
                    ),
                )
                & Q(
                    enrollments__student__last_name__icontains=(
                        last_name_search
                    ),
                )
            )

        courses = courses.filter(employee_query).distinct()

    # If a date was selected, only show courses with a class on that date.
    if parsed_date:
        courses = courses.filter(
            class_sessions__status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
            class_sessions__start_time__date=parsed_date,
        ).distinct()

    course_attendance_rows = []

    global_employee_ids = set()
    global_past_classes = 0
    global_submitted_classes = 0
    global_attended_count = 0
    global_missed_count = 0
    global_excused_count = 0

    for course in courses:
        active_enrollments = course.active_enrollments

        for enrollment in active_enrollments:
            global_employee_ids.add(enrollment.student_id)

        class_sessions = course.attendance_class_sessions

        past_class_sessions = [
            class_session
            for class_session in class_sessions
            if class_session.start_time < now
        ]

        future_class_sessions = [
            class_session
            for class_session in class_sessions
            if class_session.start_time >= now
        ]

        submitted_class_sessions = []

        attended_count = 0
        missed_count = 0
        excused_count = 0

        for class_session in past_class_sessions:
            # Under the new lifecycle, attendance is considered submitted
            # only when the lesson itself has been explicitly completed.
            if class_session.status != ClassSession.STATUS_COMPLETED:
                continue

            attendance_records = list(
                class_session.attendance_records.all()
            )

            if not attendance_records:
                continue

            submitted_class_sessions.append(class_session)

            attended_count += sum(
                1
                for attendance in attendance_records
                if attendance.status == "attended"
            )

            missed_count += sum(
                1
                for attendance in attendance_records
                if attendance.status == "missed"
            )

            excused_count += sum(
                1
                for attendance in attendance_records
                if attendance.status == "excused"
            )

        past_classes_count = len(past_class_sessions)
        submitted_classes_count = len(submitted_class_sessions)

        pending_submission_count = max(
            past_classes_count - submitted_classes_count,
            0,
        )

        total_final_attendance_records = (
            attended_count
            + missed_count
            + excused_count
        )

        if total_final_attendance_records:
            attendance_rate = round(
                attended_count
                / total_final_attendance_records
                * 100
            )
        else:
            attendance_rate = 0

        if past_classes_count:
            submission_rate = round(
                submitted_classes_count
                / past_classes_count
                * 100
            )
        else:
            submission_rate = 0

        last_class = (
            max(
                past_class_sessions,
                key=lambda class_session: class_session.start_time,
            )
            if past_class_sessions
            else None
        )

        next_class = (
            min(
                future_class_sessions,
                key=lambda class_session: class_session.start_time,
            )
            if future_class_sessions
            else None
        )

        # Custom attributes available directly in the template.
        course.employee_count = len(active_enrollments)

        course.past_classes_count = past_classes_count
        course.submitted_classes_count = submitted_classes_count
        course.pending_submission_count = pending_submission_count
        course.submission_rate = submission_rate

        course.attended_count = attended_count
        course.missed_count = missed_count
        course.excused_count = excused_count
        course.attendance_rate = attendance_rate

        course.last_class = last_class
        course.next_class = next_class

        course_attendance_rows.append(course)

        global_past_classes += past_classes_count
        global_submitted_classes += submitted_classes_count
        global_attended_count += attended_count
        global_missed_count += missed_count
        global_excused_count += excused_count

    global_total_attendance_records = (
        global_attended_count
        + global_missed_count
        + global_excused_count
    )

    if global_total_attendance_records:
        global_attendance_rate = round(
            global_attended_count
            / global_total_attendance_records
            * 100
        )

        global_missed_rate = round(
            global_missed_count
            / global_total_attendance_records
            * 100
        )

        global_excused_rate = round(
            global_excused_count
            / global_total_attendance_records
            * 100
        )
    else:
        global_attendance_rate = 0
        global_missed_rate = 0
        global_excused_rate = 0

    context = {
        "profile": profile,
        "company": company,

        # One item per course.
        "courses": course_attendance_rows,

        # Global summary.
        "total_courses": len(course_attendance_rows),
        "total_employees": len(global_employee_ids),
        "total_past_classes": global_past_classes,
        "total_submitted_classes": global_submitted_classes,
        "global_attended_count": global_attended_count,
        "global_missed_count": global_missed_count,
        "global_excused_count": global_excused_count,
        "global_attendance_rate": global_attendance_rate,
        "global_missed_rate": global_missed_rate,
        "global_excused_rate": global_excused_rate,

        # Keep filter values visible after submitting.
        "selected_date": selected_date,
        "course_search": course_search,
        "employee_search": employee_search,
    }

    return render(
        request,
        "profiles/company_admin/"
        "company_admin_all_courses_attendance.html",
        context,
    )



@login_required
def company_admin_course_details(request, course_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id,
        company=company,
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

    total_classes = course.total_sessions
    completed_classes = course.completed_sessions
    remaining_classes = course.remaining_sessions
    completion_percentage = course.completion_percentage

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
            slot.end_time.strftime("%Hh%M"),
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

    student_emails = [
        enrollment.student.email
        for enrollment in enrollments
        if enrollment.student.email
    ]

    bcc_student_emails = ",".join(student_emails)

    context = {
        "profile": profile,
        "company": company,
        "course": course,
        "enrollments": enrollments,
        "sessions": sessions,

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
        "profiles/company_admin/company_admin_course_details.html",
        context
    )



@login_required
def company_admin_course_students_list(request, course_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id,
        company=company,
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

    total_classes = course.total_sessions
    completed_classes = course.completed_sessions
    remaining_classes = course.remaining_sessions
    completion_percentage = course.completion_percentage

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
            slot.end_time.strftime("%Hh%M"),
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

    student_emails = [
        enrollment.student.email
        for enrollment in enrollments
        if enrollment.student.email
    ]

    bcc_student_emails = ",".join(student_emails)

    context = {
        "profile": profile,
        "company": company,
        "course": course,
        "enrollments": enrollments,
        "sessions": sessions,

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
        "profiles/company_admin/company_admin_course_students_list.html",
        context
    )



@login_required
def company_admin_course_attendance(request, course_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    course = get_object_or_404(
        Course.objects.annotate(
            enrollment_count=Count("enrollments")
        ),
        id=course_id,
        company=company,
    )    

    class_sessions = (
        ClassSession.objects
        .filter(
            course=course,
            status=ClassSession.STATUS_COMPLETED,
        )
        .select_related(
            "course",
            "course__course_type",
            "course__teacher",
        )
        .prefetch_related("attendance_records")
        .order_by("-start_time")
    )

    submitted_class_sessions = []

    for class_session in class_sessions:
        attendance_records = class_session.attendance_records.select_related(
            "student",
            "student__profile",
        )

        has_records = attendance_records.exists()
        has_scheduled_records = attendance_records.filter(status="scheduled").exists()

        if has_records and not has_scheduled_records:
            class_session.attendance_filter_status = "completed"

            class_session.employee_search_text = " ".join(
                [
                    f"{attendance.student.get_full_name()} {attendance.student.username} {attendance.student.email}"
                    for attendance in attendance_records
                ]
            )

            submitted_class_sessions.append(class_session)

    context = {
        "course": course,
        "class_sessions": submitted_class_sessions,
        "completed_count": len(submitted_class_sessions),
    }

    return render(
        request,
        "profiles/company_admin/company_admin_course_attendance.html",
        context,
    )



@login_required
def company_admin_course_attendance_detail(request, class_session_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    class_session = get_object_or_404(
        ClassSession.objects.select_related(
            "course",
            "course__course_type",
            "course__teacher",
        ),
        id=class_session_id,
        course__company=company,
    )

    attendances = (
        class_session.attendance_records
        .select_related(
            "student",
            "student__profile",
        )
        .order_by(
            "student__first_name",
            "student__last_name",
        )
    )

    context = {
        "class_session": class_session,
        "course": class_session.course,
        "attendances": attendances,
        "total_count": attendances.count(),
        "attended_count": attendances.filter(status="attended").count(),
        "missed_count": attendances.filter(status="missed").count(),
        "excused_count": attendances.filter(status="excused").count(),
    }

    return render(
        request,
        "profiles/company_admin/company_admin_course_attendance_detail.html",
        context,
    )



@login_required
def company_admin_student_detail(request, course_id, enrollment_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id,
        company=company,
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

    chart_data = build_skill_progress_chart_data(
        student=student,
        course=course,
    )

    attendances = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course,
            status__in=["attended", "missed", "excused"],
        )
        .select_related("class_session")
        .order_by("-class_session__start_time")
    )

    total_attendance_records = attendances.count()
    attended_count = attendances.filter(status="attended").count()
    missed_count = attendances.filter(status="missed").count()
    excused_count = attendances.filter(status="excused").count()

    # Learner progress is based on ClassSessions actually assigned to
    # this enrollment. Completed means status="completed", never merely past.
    completed_classes = enrollment.total_completed_classes
    total_classes = enrollment.total_assigned_classes
    remaining_classes = enrollment.upcoming_classes

    completed_session_list = list(
        enrollment.eligible_sessions.filter(
            status=ClassSession.STATUS_COMPLETED
        )
    )

    completed_hours = sum(
        (
            Decimal(str(
                (session.end_time - session.start_time).total_seconds()
            )) / Decimal("3600")
            for session in completed_session_list
        ),
        Decimal("0"),
    )

    assigned_session_list = list(enrollment.eligible_sessions)

    total_hours = sum(
        (
            Decimal(str(
                (session.end_time - session.start_time).total_seconds()
            )) / Decimal("3600")
            for session in assigned_session_list
        ),
        Decimal("0"),
    )

    remaining_hours = max(
        total_hours - completed_hours,
        Decimal("0"),
    )

    completed_hours_display = format_hours_duration(completed_hours)
    remaining_hours_display = format_hours_duration(remaining_hours)
    total_hours_display = format_hours_duration(total_hours)

    attendance_percentage = enrollment.attendance_percentage

    completion_percentage = (
        round((completed_classes / total_classes) * 100)
        if total_classes > 0
        else 0
    )

    recent_attendance = attendances[:5]

    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related("subskill_assessments")
        .order_by("skill")
    )

    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]

    context = {
        "profile": profile,
        "company": company,
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

        "total_hours_display": total_hours_display,
        "completed_hours_display": completed_hours_display,
        "remaining_hours_display": remaining_hours_display,

        "recent_attendance": recent_attendance,
        "chart_data": chart_data,
        "skill_note_display": skill_note_display,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_student_detail.html",
        context
    )



@login_required
def company_admin_student_attendance_record(request, course_id, enrollment_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id,
        company=company,
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
            class_session__course=course,
            status__in=["attended", "missed", "excused"],
        )
        .select_related("class_session")
        .order_by("-class_session__start_time")
    )

    total_attendance_records = attendances.count()
    attended_count = attendances.filter(status="attended").count()
    missed_count = attendances.filter(status="missed").count()
    excused_count = attendances.filter(status="excused").count()

    completed_classes = enrollment.total_completed_classes
    total_classes = enrollment.total_assigned_classes
    remaining_classes = enrollment.upcoming_classes

    attendance_percentage = enrollment.attendance_percentage

    completion_percentage = (
        round((completed_classes / total_classes) * 100)
        if total_classes > 0
        else 0
    )

    recent_attendance = attendances

    context = {
        "profile": profile,
        "company": company,
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
    }

    return render(
        request,
        "profiles/company_admin/company_admin_student_attendance_record.html",
        context
    )



@login_required
def company_admin_student_skills_overview(request, course_id, enrollment_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id,
        company=company,
    )

    enrollment = get_object_or_404(
        CourseEnrollment.objects.select_related(
            "student",
            "student__profile",
            "course",
        ),
        id=enrollment_id,
        course=course,
    )

    student = enrollment.student
    student_profile = student.profile

    skill_icons = {
        "speaking": "fa-solid fa-microphone",
        "reading": "fa-solid fa-book-open",
        "writing": "fa-solid fa-pen",
        "listening": "fa-solid fa-headphones",
    }

    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related("subskill_assessments")
        .order_by("skill")
    )

    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]

    skills = []

    for assessment in skill_assessments:
        skills.append({
            "assessment": assessment,
            "assessment_id": assessment.id,
            "skill_value": assessment.skill,
            "name": assessment.get_skill_display(),
            "icon": skill_icons.get(
                assessment.skill,
                "fa-solid fa-chart-simple",
            ),
            "percentage": assessment.average_percentage,
            "teacher_notes": assessment.teacher_notes,
            "subskills": assessment.subskill_assessments.all(),
        })

    skill_notes = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .exclude(teacher_notes="")
        .order_by("skill")
    )

    academic_profile = getattr(student, "academic_profile", None)

    chart_data = build_skill_progress_chart_data(
        student=student,
        course=course,
    )

    context = {
        "profile": profile,
        "company": company,
        "course": course,
        "enrollment": enrollment,
        "student": student,
        "student_profile": student_profile,
        "skills": skills,
        "academic_profile": academic_profile,
        "chart_data": chart_data,
        "skill_notes": skill_notes,
        "skill_note_display": skill_note_display,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_student_skills_overview.html",
        context,
    )



def company_admin_student_teacher_notes(request, course_id, enrollment_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id,
        company=company,
    )

    enrollment = get_object_or_404(
        CourseEnrollment.objects.select_related(
            "student",
            "student__profile",
            "course",
        ),
        id=enrollment_id,
        course=course,
    )

    student = enrollment.student
    student_profile = student.profile

    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related("subskill_assessments")
        .order_by("skill")
    )

    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]

    skills = []

    skill_notes = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .exclude(teacher_notes="")
        .order_by("skill")
    )

    context = {
        "profile": profile,
        "company": company,
        "course": course,
        "enrollment": enrollment,
        "student": student,
        "student_profile": student_profile,
        "skills": skills,
        "skill_notes": skill_notes,
        "skill_note_display": skill_note_display,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_student_teacher_notes.html",
        context,
    )



def company_admin_student_progress_skills_graph(request, course_id, enrollment_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    course = get_object_or_404(
        Course,
        id=course_id,
        company=company,
    )

    enrollment = get_object_or_404(
        CourseEnrollment.objects.select_related(
            "student",
            "student__profile",
            "course",
        ),
        id=enrollment_id,
        course=course,
    )

    student = enrollment.student
    student_profile = student.profile

    skill_icons = {
        "speaking": "fa-solid fa-microphone",
        "reading": "fa-solid fa-book-open",
        "writing": "fa-solid fa-pen",
        "listening": "fa-solid fa-headphones",
    }

    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related("subskill_assessments")
        .order_by("skill")
    )

    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]

    skills = []

    for assessment in skill_assessments:
        skills.append({
            "assessment": assessment,
            "assessment_id": assessment.id,
            "skill_value": assessment.skill,
            "name": assessment.get_skill_display(),
            "icon": skill_icons.get(
                assessment.skill,
                "fa-solid fa-chart-simple",
            ),
            "percentage": assessment.average_percentage,
            "teacher_notes": assessment.teacher_notes,
            "subskills": assessment.subskill_assessments.all(),
        })

    skill_notes = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .exclude(teacher_notes="")
        .order_by("skill")
    )

    academic_profile = getattr(student, "academic_profile", None)

    chart_data = build_skill_progress_chart_data(
        student=student,
        course=course,
    )

    context = {
        "profile": profile,
        "company": company,
        "course": course,
        "enrollment": enrollment,
        "student": student,
        "student_profile": student_profile,
        "skills": skills,
        "academic_profile": academic_profile,
        "chart_data": chart_data,
        "skill_notes": skill_notes,
        "skill_note_display": skill_note_display,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_student_progress_skills_graph.html",
        context,
    )



@login_required
def company_admin_classes_list(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    now = timezone.now()
    today = timezone.localdate()

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    sessions = (
        ClassSession.objects
        .filter(
            course__company=company,
            course__status="active",
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
        .prefetch_related(
            "course__enrollments",
            "course__enrollments__student",
            "course__enrollments__student__profile",
        )
        .order_by("start_time")
    )

    class_filter_counts = {
        "upcoming": {
            "today": 0,
            "weekly": 0,
            "monthly": 0,
            "all": 0,
        },
        "completed": {
            "today": 0,
            "weekly": 0,
            "monthly": 0,
            "all": 0,
        },
    }

    for session in sessions:
        session_date = timezone.localdate(session.start_time)

        session.is_upcoming = (
            session.status in [
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
            ]
            and session.start_time > now
        )

        session.is_completed = (
            session.status == ClassSession.STATUS_COMPLETED
        )

        session.is_today = session_date == today

        session.is_this_week = (
            start_of_week <= session_date <= end_of_week
        )

        session.is_this_month = (
            session_date.year == today.year
            and session_date.month == today.month
        )

        if session.status == ClassSession.STATUS_PENDING_RESCHEDULE:
            session.class_status_group = "pending_reschedule"
        elif session.is_completed:
            session.class_status_group = "completed"
        elif session.is_upcoming:
            session.class_status_group = "upcoming"
        else:
            # Scheduled/rescheduled but not future and not completed:
            # still outstanding until explicitly completed.
            session.class_status_group = "in_progress"

        if session.is_upcoming:
            class_filter_counts["upcoming"]["all"] += 1

            if session.is_today:
                class_filter_counts["upcoming"]["today"] += 1

            if session.is_this_week:
                class_filter_counts["upcoming"]["weekly"] += 1

            if session.is_this_month:
                class_filter_counts["upcoming"]["monthly"] += 1

        if session.is_completed:
            class_filter_counts["completed"]["all"] += 1

            if session.is_today:
                class_filter_counts["completed"]["today"] += 1

            if session.is_this_week:
                class_filter_counts["completed"]["weekly"] += 1

            if session.is_this_month:
                class_filter_counts["completed"]["monthly"] += 1

    context = {
        "profile": profile,
        "company": company,
        "sessions": sessions,
        "now": now,
        "class_filter_counts": class_filter_counts,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_classes_list.html",
        context
    )




# =========================================================
# COMPANY ADMIN CALENDAR PAGE
# =========================================================

@login_required
def company_admin_calendar(request):
    profile = get_object_or_404(
        UserProfile.objects.select_related("company"),
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    # A company admin must belong to a company.
    if not profile.company:
        return redirect("home")

    courses = (
        Course.objects
        .filter(company=profile.company)
        .select_related(
            "course_type",
            "company",
            "teacher",
            "teacher__profile",
        )
        .order_by("name")
    )

    context = {
        "profile": profile,
        "company": profile.company,
        "courses": courses,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_calendar.html",
        context,
    )


# =========================================================
# COMPANY ADMIN CALENDAR EVENTS
# =========================================================

@login_required
def company_admin_calendar_events(request):
    profile = get_object_or_404(
        UserProfile.objects.select_related("company"),
        user=request.user,
    )

    if (
        profile.role != UserProfile.ROLE_COMPANY_ADMIN
        or not profile.company
    ):
        return JsonResponse([], safe=False)

    start = request.GET.get("start")
    end = request.GET.get("end")

    sessions = (
        ClassSession.objects
        .filter(
            course__company=profile.company,
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
        )
        .select_related(
            "course",
            "course__teacher",
            "course__teacher__profile",
            "course__company",
        )
        .order_by("start_time")
    )

    bank_holidays = (
        BankHoliday.objects
        .filter(is_active=True)
        .order_by("start_date")
    )

    if start and end:
        start_datetime = parse_datetime(start)
        end_datetime = parse_datetime(end)

        if start_datetime and end_datetime:
            sessions = sessions.filter(
                start_time__gte=start_datetime,
                start_time__lt=end_datetime,
            )

            bank_holidays = (
                bank_holidays
                .filter(start_date__lt=end_datetime.date())
                .filter(
                    Q(end_date__isnull=True)
                    | Q(end_date__gte=start_datetime.date())
                )
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

        teacher = session.course.teacher

        if teacher:
            teacher_name = teacher.get_full_name() or teacher.email
        else:
            teacher_name = "Not assigned"

        events.append({
            "id": session.id,
            "title": session.title,
            "start": session.start_time.isoformat(),
            "end": (
                session.end_time.isoformat()
                if session.end_time
                else None
            ),
            "className": status_class,
            "extendedProps": {
                "type": "class_session",
                "course": session.course.name,
                "course_status": session.course.status,
                "class_number": session.class_number,
                "meeting_link": session.meeting_link,
                "teacher": teacher_name,

                "group_details_url": reverse(
                    "profiles:company_admin_course_details",
                    args=[session.course.id],
                ),
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
            event["end"] = (
                holiday.end_date + timedelta(days=1)
            ).isoformat()

        events.append(event)

    return JsonResponse(events, safe=False)



@login_required
def company_admin_employees_list(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    enrollments = (
        CourseEnrollment.objects
        .filter(
            course__company=company,
            status="active",
        )
        .select_related(
            "student",
            "student__profile",
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
        .order_by(
            "student__first_name",
            "student__last_name",
            "student__email",
            "course__name",
        )
    )

    employees_by_id = {}

    for enrollment in enrollments:
        student = enrollment.student

        if student.id not in employees_by_id:
            employees_by_id[student.id] = {
                "student": student,
                "profile": student.profile,
                "enrollments": [],
                "courses": [],
            }

        employees_by_id[student.id]["enrollments"].append(enrollment)
        employees_by_id[student.id]["courses"].append(enrollment.course)

    employees = list(employees_by_id.values())

    context = {
        "profile": profile,
        "company": company,
        "employees": employees,
        "total_employees": len(employees),
        "level_choices": UserProfile.LEVEL_CHOICES,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_employees_list.html",
        context
    )



# TEACHER PROFILE SETTINGS
@login_required
def company_admin_profile_settings(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    if request.method == "POST":
        user_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=user_profile,
            user=request.user
        )

        if user_form.is_valid():
            user_form.save()

            messages.success(request, "Your profile has been updated.")
            return redirect("profiles:company_admin_profile_settings")

    else:
        user_form = UserProfileForm(
            instance=user_profile,
            user=request.user
        )


    context = {
        "profile": user_profile,
        "user_form": user_form,
        "user_profile": user_profile,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_profile_settings.html",
        context
    )

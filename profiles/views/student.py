from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


from django.db.models import Q, Prefetch

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from django.urls import reverse

import calendar

from datetime import timedelta, datetime, time
from decimal import Decimal

from profiles.utils.courses import build_formatted_timetable
from profiles.utils.enrollments import order_enrollments_by_course_status
from profiles.utils.skills import build_student_skill_cards

from profiles.utils.time_formating import (
    format_hours_duration,
    format_minutes_duration,
    get_session_minutes,
)

from profiles.models import (
    UserProfile, 
    StudentSkillAssessment, 
    SUBSKILLS,
    StudentNeedsAnalysis,
)

from profiles.forms import (
    StudentNeedsAnalysisForm,
)

from profiles.views.shared import (
    build_skill_note_display, 
    build_overall_skill_progress_chart_data, 
    build_skill_progress_chart_data, 
    get_calendar_meeting_link,
)


from courses.models import Course, CourseEnrollment, ClassSession, BankHoliday, Attendance


User = get_user_model()


def student_can_request_reschedule(session, now=None):
    """
    A learner may request postponement at any time before
    17:00 on the calendar day immediately before the lesson.

    Example:
    Thursday lesson -> cutoff is Wednesday at 17:00.
    """
    now = now or timezone.now()

    local_now = timezone.localtime(now)
    local_start = timezone.localtime(session.start_time)

    cutoff_date = local_start.date() - timedelta(days=1)

    cutoff = timezone.make_aware(
        datetime.combine(
            cutoff_date,
            time(17, 0),
        ),
        timezone.get_current_timezone(),
    )

    valid_status = session.status in {
        ClassSession.STATUS_SCHEDULED,
        ClassSession.STATUS_RESCHEDULED,
    }

    return (
        local_now < cutoff
        and valid_status
    )



@login_required
def student_dashboard(request):
    student = request.user
    profile = get_object_or_404(
        UserProfile,
        user=student,
    )

    if profile.role not in [
        UserProfile.ROLE_EMPLOYEE,
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
    ]:
        return redirect("home")

    today = timezone.localdate()
    now = timezone.now()

    # ---------------------------------------------------------
    # DATE RANGES
    # ---------------------------------------------------------

    # Today
    start_of_day = timezone.make_aware(
        datetime.combine(today, time.min)
    )
    end_of_day = timezone.make_aware(
        datetime.combine(today, time.max)
    )

    # Week: Monday - Sunday
    start_of_week_date = today - timedelta(days=today.weekday())
    end_of_week_date = start_of_week_date + timedelta(days=6)

    start_of_week = timezone.make_aware(
        datetime.combine(start_of_week_date, time.min)
    )
    end_of_week = timezone.make_aware(
        datetime.combine(end_of_week_date, time.max)
    )

    # Month
    start_of_month_date = today.replace(day=1)

    last_day_of_month = calendar.monthrange(
        today.year,
        today.month,
    )[1]

    end_of_month_date = today.replace(
        day=last_day_of_month
    )

    start_of_month = timezone.make_aware(
        datetime.combine(start_of_month_date, time.min)
    )
    end_of_month = timezone.make_aware(
        datetime.combine(end_of_month_date, time.max)
    )

    # ---------------------------------------------------------
    # ACTIVE ENROLLMENTS / COURSES
    #
    # A Course belongs to the learner's CURRENT dashboard only
    # when BOTH:
    #
    # - CourseEnrollment is active
    # - Course itself is active
    #
    # Historical Courses remain available elsewhere but do not
    # contribute to the current dashboard.
    # ---------------------------------------------------------

    active_enrollments = (
        CourseEnrollment.objects
        .filter(
            student=student,
            status=CourseEnrollment.STATUS_ACTIVE,
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

    active_course_ids = active_enrollments.values_list(
        "course_id",
        flat=True,
    )

    courses = (
        Course.objects
        .filter(id__in=active_course_ids)
        .select_related(
            "course_type",
            "company",
            "teacher",
        )
        .order_by("name")
    )

    active_courses = courses.count()

    # Temporary compatibility with older student-dashboard
    # template code that expected one active enrollment.
    active_enrollment = active_enrollments.first()

    # ---------------------------------------------------------
    # DASHBOARD SESSION STATUSES
    #
    # Include valid current/upcoming teaching slots and both
    # genuine held-session lifecycle states.
    #
    # Exclude:
    # - pending_reschedule
    # - cancelled
    # ---------------------------------------------------------

    dashboard_session_statuses = [
        ClassSession.STATUS_SCHEDULED,
        ClassSession.STATUS_RESCHEDULED,
        ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
        ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
    ]

    # ---------------------------------------------------------
    # LEARNER ATTENDANCE PREFETCH
    #
    # Each dashboard session needs only this learner's final
    # Attendance outcome for learner-specific attendance metrics.
    # ---------------------------------------------------------

    student_final_attendance_prefetch = Prefetch(
        "attendance_records",
        queryset=Attendance.objects.filter(
            student=student,
            status__in=[
                Attendance.STATUS_ATTENDED,
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ],
        ),
        to_attr="student_final_attendance_records",
    )

    # ---------------------------------------------------------
    # BASE LEARNER SESSION QUERY
    #
    # Restrict to:
    # - active learner Courses
    # - sessions actually assigned to this learner
    #
    # Attendance records are created for assigned learner/session
    # relationships, so this avoids exposing unrelated sessions.
    # ---------------------------------------------------------

    def get_student_sessions(start_datetime, end_datetime):
        return (
            ClassSession.objects
            .filter(
                course_id__in=active_course_ids,
                course__status="active",
                attendance_records__student=student,
                status__in=dashboard_session_statuses,
                start_time__gte=start_datetime,
                start_time__lte=end_datetime,
            )
            .select_related(
                "course",
                "course__course_type",
                "course__company",
                "course__teacher",
            )
            .prefetch_related(
                student_final_attendance_prefetch,
            )
            .distinct()
            .order_by("start_time")
        )

    # ---------------------------------------------------------
    # TODAY'S CLASSES
    # ---------------------------------------------------------

    todays_sessions = get_student_sessions(
        start_of_day,
        end_of_day,
    )

    # Provide the effective meeting link without changing the
    # persisted ClassSession value.
    for session in todays_sessions:
        session.dashboard_meeting_link = (
            get_calendar_meeting_link(session)
        )

    # Compatibility with the previous student dashboard.
    next_class = (
        ClassSession.objects
        .filter(
            course_id__in=active_course_ids,
            course__status="active",
            attendance_records__student=student,
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
            ],
            start_time__gte=now,
        )
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
        .distinct()
        .order_by("start_time")
        .first()
    )

    if next_class:
        next_class.dashboard_meeting_link = (
            get_calendar_meeting_link(next_class)
        )

    # ---------------------------------------------------------
    # WEEKLY / MONTHLY CLASSES
    # ---------------------------------------------------------

    weekly_sessions = get_student_sessions(
        start_of_week,
        end_of_week,
    )

    monthly_sessions = get_student_sessions(
        start_of_month,
        end_of_month,
    )

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------

    def get_percentage(value, total):
        if total == 0:
            return 0

        return round(
            (value / total) * 100
        )

    def get_period_metrics(sessions):
        """
        Learner dashboard reporting logic.

        Total:
            All learner-assigned dashboard sessions in the period.

        Held:
            Session has actually finished.

        Upcoming:
            Session has not started yet.

        Attendance submitted:
            ClassSession lifecycle is explicitly
            COMPLETE_ATTENDANCE_SUBMITTED.

        Classes attended:
            This learner has a final Attendance outcome of ATTENDED
            for a fully submitted ClassSession.

        Attendance rate:
            ATTENDED / all of this learner's resolved Attendance
            outcomes belonging only to fully submitted ClassSessions.
        """

        session_list = list(sessions)

        total_sessions = len(session_list)

        held_sessions = [
            session
            for session in session_list
            if session.end_time < now
        ]

        upcoming_sessions = [
            session
            for session in session_list
            if session.start_time >= now
        ]

        submitted_sessions = [
            session
            for session in session_list
            if (
                session.status
                == ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            )
        ]

        held_count = len(held_sessions)
        upcoming_count = len(upcoming_sessions)
        attendance_submitted_count = len(submitted_sessions)

        attendance_pending_count = max(
            held_count - attendance_submitted_count,
            0,
        )

        total_resolved_attendance_records = 0
        attended_records = 0
        missed_records = 0
        excused_records = 0

        for session in submitted_sessions:
            attendance_records = (
                session.student_final_attendance_records
            )

            total_resolved_attendance_records += len(
                attendance_records
            )

            attended_records += sum(
                attendance.status == Attendance.STATUS_ATTENDED
                for attendance in attendance_records
            )

            missed_records += sum(
                attendance.status == Attendance.STATUS_MISSED
                for attendance in attendance_records
            )

            excused_records += sum(
                attendance.status == Attendance.STATUS_EXCUSED
                for attendance in attendance_records
            )

        return {
            "total_sessions": total_sessions,

            "held_sessions": held_count,
            "held_percentage": get_percentage(
                held_count,
                total_sessions,
            ),

            "upcoming_sessions": upcoming_count,
            "upcoming_percentage": get_percentage(
                upcoming_count,
                total_sessions,
            ),

            # Staff-side lifecycle data retained in context so the
            # shared dashboard structure remains reusable.
            "attendance_submitted_sessions":
                attendance_submitted_count,

            "attendance_pending_sessions":
                attendance_pending_count,

            "attendance_submitted_percentage":
                get_percentage(
                    attendance_submitted_count,
                    held_count,
                ),

            # Learner-specific attendance
            "attended_sessions": attended_records,
            "missed_sessions": missed_records,
            "excused_sessions": excused_records,

            "resolved_attendance_records":
                total_resolved_attendance_records,

            "attendance_rate":
                get_percentage(
                    attended_records,
                    total_resolved_attendance_records,
                ),
        }

    # ---------------------------------------------------------
    # PERIOD METRICS
    # ---------------------------------------------------------

    weekly_metrics = get_period_metrics(
        weekly_sessions
    )

    monthly_metrics = get_period_metrics(
        monthly_sessions
    )

    # ---------------------------------------------------------
    # OVERALL ATTENDANCE RATE
    #
    # Only this learner's genuine final Attendance outcomes from
    # fully submitted sessions on CURRENT active Courses count.
    # ---------------------------------------------------------

    attendance_records = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course_id__in=active_course_ids,
            class_session__course__status="active",
            class_session__status=(
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            ),
            status__in=[
                Attendance.STATUS_ATTENDED,
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ],
        )
    )

    total_attendance_records = attendance_records.count()

    attended_records = (
        attendance_records
        .filter(
            status=Attendance.STATUS_ATTENDED
        )
        .count()
    )

    total_attendance_rate = get_percentage(
        attended_records,
        total_attendance_records,
    )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------

    context = {
        "profile": profile,
        "student": student,

        # Active learner Courses
        "active_enrollments": active_enrollments,
        "active_enrollment": active_enrollment,
        "courses": courses,
        "active_courses": active_courses,

        # Today's Classes
        "todays_sessions": todays_sessions,
        "today": today,

        # Compatibility with previous dashboard
        "next_class": next_class,

        # General learner attendance
        "total_attendance_rate": total_attendance_rate,

        # -------------------------
        # WEEKLY
        # -------------------------

        "total_weekly_sessions":
            weekly_metrics["total_sessions"],

        "held_weekly_sessions":
            weekly_metrics["held_sessions"],

        "held_weekly_percentage":
            weekly_metrics["held_percentage"],

        "upcoming_weekly_sessions":
            weekly_metrics["upcoming_sessions"],

        "upcoming_weekly_percentage":
            weekly_metrics["upcoming_percentage"],

        # Learner-specific Classes Attended
        "attended_weekly_sessions":
            weekly_metrics["attended_sessions"],

        "missed_weekly_sessions":
            weekly_metrics["missed_sessions"],

        "excused_weekly_sessions":
            weekly_metrics["excused_sessions"],

        "weekly_resolved_attendance_records":
            weekly_metrics["resolved_attendance_records"],

        "weekly_attendance_rate":
            weekly_metrics["attendance_rate"],

        # Kept available for shared/compatible dashboard markup
        "weekly_attendance_submitted_sessions":
            weekly_metrics["attendance_submitted_sessions"],

        "weekly_attendance_pending_sessions":
            weekly_metrics["attendance_pending_sessions"],

        "weekly_attendance_submitted_percentage":
            weekly_metrics["attendance_submitted_percentage"],

        # -------------------------
        # MONTHLY
        # -------------------------

        "total_monthly_sessions":
            monthly_metrics["total_sessions"],

        "held_monthly_sessions":
            monthly_metrics["held_sessions"],

        "held_monthly_percentage":
            monthly_metrics["held_percentage"],

        "upcoming_monthly_sessions":
            monthly_metrics["upcoming_sessions"],

        "upcoming_monthly_percentage":
            monthly_metrics["upcoming_percentage"],

        # Learner-specific Classes Attended
        "attended_monthly_sessions":
            monthly_metrics["attended_sessions"],

        "missed_monthly_sessions":
            monthly_metrics["missed_sessions"],

        "excused_monthly_sessions":
            monthly_metrics["excused_sessions"],

        "monthly_resolved_attendance_records":
            monthly_metrics["resolved_attendance_records"],

        "monthly_attendance_rate":
            monthly_metrics["attendance_rate"],

        # Kept available for shared/compatible dashboard markup
        "monthly_attendance_submitted_sessions":
            monthly_metrics["attendance_submitted_sessions"],

        "monthly_attendance_pending_sessions":
            monthly_metrics["attendance_pending_sessions"],

        "monthly_attendance_submitted_percentage":
            monthly_metrics["attendance_submitted_percentage"],
    }

    return render(
        request,
        "profiles/student/student_dashboard.html",
        context,
    )



# STUDENT COURSE INFO PAGE
@login_required
def my_course(request):
    student = request.user
    profile = get_object_or_404(
        UserProfile,
        user=student,
    )

    if profile.role not in [
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
        UserProfile.ROLE_EMPLOYEE,
    ]:
        return redirect("home")

    # ---------------------------------------------------------
    # ALL ENROLLMENTS
    #
    # Historical courses remain accessible regardless of
    # CourseEnrollment status or Course status.
    #
    # Order:
    # 1. Active
    # 2. Confirmed
    # 3. Paused
    # 4. Completed
    # 5. Cancelled
    #
    # Completed courses:
    # - newest end date first
    #
    # Otherwise:
    # - course name A-Z
    # ---------------------------------------------------------
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects
        .filter(student=student)
        .select_related(
            "course",
            "course__teacher",
            "course__teacher__profile",
            "course__course_type",
            "course__company",
        )
        .prefetch_related(
            "course__programmes",
            "course__timetable_slots",
        )
    )

    # ---------------------------------------------------------
    # SELECTED ENROLLMENT / COURSE
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")

    if selected_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )
    else:
        enrollment = enrollments.first()

    course = enrollment.course if enrollment else None

    # ---------------------------------------------------------
    # DEFAULT COURSE DETAIL VALUES
    # ---------------------------------------------------------
    formatted_timetable = []
    delivery_percentage = 0
    past_held_classes = 0
    past_held_minutes = 0
    past_held_hours_display = "0 min"

    if course:
        # -----------------------------------------------------
        # FORMATTED TIMETABLE
        #
        # Shared helper also used by the other Course Details
        # views.
        # -----------------------------------------------------
        formatted_timetable = build_formatted_timetable(
            course
        )

        # -----------------------------------------------------
        # GENERAL COURSE PROGRESS
        #
        # Course completion remains independent from
        # attendance-submission state.
        # -----------------------------------------------------
        delivery_percentage = (
            course.delivery_percentage
        )

        # -----------------------------------------------------
        # PAST / HELD CLASSES
        #
        # A class is considered held once end_time has passed.
        #
        # Attendance submission is a separate concern.
        #
        # Exclude:
        # - cancelled sessions
        # - pending-reschedule sessions
        # -----------------------------------------------------
        held_sessions = (
            course.class_sessions
            .filter(
                end_time__lt=timezone.now(),
            )
            .exclude(
                status__in=[
                    ClassSession.STATUS_CANCELLED,
                    ClassSession.STATUS_PENDING_RESCHEDULE,
                ]
            )
        )

        past_held_classes = held_sessions.count()

        # -----------------------------------------------------
        # DELIVERED HOURS
        #
        # Use the actual duration of the held sessions rather
        # than multiplying by the standard class duration,
        # because the final class may be shorter.
        # -----------------------------------------------------
        past_held_minutes = get_session_minutes(
            held_sessions
        )

        past_held_hours_display = (
            format_minutes_duration(
                past_held_minutes
            )
        )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,

        # All historical enrollments -> course selector
        "enrollments": enrollments,

        # Selected learner/course relationship
        "enrollment": enrollment,
        "course": course,

        # Course Details page
        "formatted_timetable": formatted_timetable,
        "delivery_percentage": delivery_percentage,
        "past_held_classes": past_held_classes,
        "past_held_minutes": past_held_minutes,
        "past_held_hours_display": past_held_hours_display,

        # Course detail nav
        "active_section": "overview",
    }

    return render(
        request,
        "profiles/student/my_course.html",
        context,
    )



@login_required
def my_classes(request):
    student = request.user
    profile = get_object_or_404(
        UserProfile,
        user=student,
    )

    if profile.role not in [
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
        UserProfile.ROLE_EMPLOYEE,
    ]:
        return redirect("home")

    now = timezone.now()
    today = timezone.localdate()

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # ---------------------------------------------------------
    # ACTIVE ENROLLMENTS
    # ---------------------------------------------------------

    active_course_ids = (
        CourseEnrollment.objects
        .filter(
            student=student,
            status=CourseEnrollment.STATUS_ACTIVE,
            course__status="active",
        )
        .values_list(
            "course_id",
            flat=True,
        )
    )

    # ---------------------------------------------------------
    # CLASS SESSIONS
    #
    # Attendance rows are the source of truth for which learner
    # is assigned to each ClassSession.
    #
    # Excluded:
    # - pending_reschedule
    # - cancelled
    # ---------------------------------------------------------

    sessions = (
        ClassSession.objects
        .filter(
            course_id__in=active_course_ids,
            course__status="active",
            attendance_records__student=student,
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            ],
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
        .distinct()
        .order_by("start_time")
    )

    class_filter_counts = {
        "upcoming": {
            "today": 0,
            "weekly": 0,
            "monthly": 0,
            "all": 0,
        },
        "past": {
            "today": 0,
            "weekly": 0,
            "monthly": 0,
            "all": 0,
        },
    }

    for session in sessions:
        session_date = timezone.localdate(
            session.start_time
        )

        # --------------------------------------------------
        # UI GROUP
        #
        # Upcoming:
        # scheduled/rescheduled sessions still in the future.
        #
        # Past:
        # class held, regardless of whether attendance has
        # already been submitted.
        # --------------------------------------------------

        if (
            session.status in [
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
            ]
            and session.start_time > now
        ):
            session.class_status_group = "upcoming"

        elif session.status in [
            ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
            ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
        ]:
            session.class_status_group = "past"

        else:
            session.class_status_group = None

        # --------------------------------------------------
        # DATE FILTERS
        # --------------------------------------------------

        session.is_today = (
            session_date == today
        )

        session.is_this_week = (
            start_of_week
            <= session_date
            <= end_of_week
        )

        session.is_this_month = (
            session_date.year == today.year
            and session_date.month == today.month
        )

        # --------------------------------------------------
        # STUDENT ACTIONS
        # --------------------------------------------------

        session.meeting_link = (
            get_calendar_meeting_link(session)
        )

        session.can_request_reschedule = (
            student_can_request_reschedule(
                session,
                now=now,
            )
        )

        # --------------------------------------------------
        # LEARNER ATTENDANCE
        #
        # Useful for the student row when displaying past
        # lessons.
        # --------------------------------------------------

        session.student_attendance = (
            Attendance.objects
            .filter(
                student=student,
                class_session=session,
            )
            .first()
        )

        # --------------------------------------------------
        # COUNTS
        # --------------------------------------------------

        if session.class_status_group:
            counts = (
                class_filter_counts[
                    session.class_status_group
                ]
            )

            counts["all"] += 1

            if session.is_today:
                counts["today"] += 1

            if session.is_this_week:
                counts["weekly"] += 1

            if session.is_this_month:
                counts["monthly"] += 1

    context = {
        "profile": profile,
        "sessions": sessions,
        "now": now,
        "class_filter_counts": class_filter_counts,
    }

    return render(
        request,
        "profiles/student/my_classes.html",
        context,
    )



@login_required
@require_POST
def student_mark_class_pending_reschedule(request, session_id):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role not in [
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
        UserProfile.ROLE_EMPLOYEE,
    ]:
        return redirect("home")

    session = get_object_or_404(
        ClassSession.objects.select_related(
            "course",
        ),
        id=session_id,
        course__status="active",
        status__in=[
            ClassSession.STATUS_SCHEDULED,
            ClassSession.STATUS_RESCHEDULED,
        ],
        attendance_records__student=request.user,
    )

    enrollment_exists = CourseEnrollment.objects.filter(
        student=request.user,
        course=session.course,
        status=CourseEnrollment.STATUS_ACTIVE,
        course__status="active",
    ).exists()

    if not enrollment_exists:
        messages.error(
            request,
            "You are not currently enrolled in this course.",
        )
        return redirect("profiles:my_classes")

    if not student_can_request_reschedule(session):
        messages.error(
            request,
            "This lesson can only be postponed until 17:00 local time on the day before the class.",
        )
        return redirect("profiles:my_classes")

    session.status = ClassSession.STATUS_PENDING_RESCHEDULE
    session.save(update_fields=["status"])

    messages.success(
        request,
        "Your lesson has been marked as pending reschedule.",
    )

    return redirect("profiles:my_classes")



@login_required
def my_pending_classes(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role not in [UserProfile.ROLE_INDIVIDUAL_LEARNER, UserProfile.ROLE_EMPLOYEE]:
        return redirect("home:index")

    now = timezone.now()

    enrollments = CourseEnrollment.objects.filter(
        student=request.user,
        status__in=["active", "paused", "completed"],
    ).values_list("course_id", flat=True)

    pending_sessions = (
        ClassSession.objects
        .filter(
            course_id__in=enrollments,
            status="pending_reschedule",
        )
        .select_related("course")
        .order_by("start_time")
    )

    rescheduled_sessions = (
        ClassSession.objects
        .filter(
            course_id__in=enrollments,
            status="rescheduled",
        )
        .select_related("course")
        .order_by("-start_time")
    )

    for session in rescheduled_sessions:
        session.is_rescheduled_past = session.start_time < now
        session.is_rescheduled_upcoming = session.start_time >= now
        session.is_today = timezone.localdate(session.start_time) == timezone.localdate()

    context = {
        "profile": profile,
        "pending_sessions": pending_sessions,
        "rescheduled_sessions": rescheduled_sessions,
    }

    return render(
        request,
        "profiles/student/my_pending_classes.html",
        context,
    )



# STUDENT CALENDAR PAGE
@login_required
def my_calendar(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role not in [
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
        UserProfile.ROLE_EMPLOYEE,
    ]:
        return redirect("home")

    # ---------------------------------------------------------
    # ACTIVE ENROLLMENT
    #
    # The student calendar is available only for a learner who:
    # - has an active CourseEnrollment
    # - belongs to an active Course
    #
    # Confirmed Courses are deliberately excluded because they
    # are not yet part of the learner's active teaching lifecycle.
    #
    # Historical paused/completed/cancelled enrollments and Courses
    # remain accessible elsewhere, but do not define the learner's
    # current calendar state.
    # ---------------------------------------------------------
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
        "profile": profile,
        "active_enrollment": active_enrollment,
    }

    return render(
        request,
        "profiles/student/my_calendar.html",
        context
    )



# STUDENT CALENDAR EVENTS
# STUDENT CALENDAR EVENTS
@login_required
def my_calendar_events(request):
    """
    Calendar events for employee / individual learner profiles.

    Current teaching events:
    - scheduled
    - rescheduled

    These are shown only when:
    - the learner's CourseEnrollment is active
    - the Course itself is active

    Historical teaching events:
    - held_attendance_pending
    - complete_attendance_submitted

    These remain visible regardless of the current CourseEnrollment
    or Course status so historical calendar records are preserved.

    Excluded:
    - pending_reschedule:
        no valid teaching slot currently exists

    - cancelled:
        the lesson will not take place

    Event actions exposed to calendar.js:

    - meeting_link:
        available only for a current/upcoming scheduled or
        rescheduled ClassSession that has not yet ended

    - group_details_url:
        course-details fallback / historical navigation

    Temporal state and lifecycle state remain separate:
    - is_past is determined by end_time
    - status represents the ClassSession lifecycle
    """

    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role not in [
        UserProfile.ROLE_EMPLOYEE,
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
    ]:
        return JsonResponse(
            [],
            safe=False,
        )

    start = request.GET.get("start")
    end = request.GET.get("end")
    now = timezone.now()

    # ---------------------------------------------------------
    # ALL LEARNER COURSES
    # ---------------------------------------------------------
    #
    # Used for historical ClassSessions.
    #
    # Historical lessons must remain visible even when the
    # CourseEnrollment or Course later becomes:
    #
    # - paused
    # - completed
    # - cancelled
    #
    # The learner's enrollment establishes that the Course forms
    # part of their historical teaching record.
    # ---------------------------------------------------------
    learner_course_ids = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
        )
        .order_by()
        .values_list(
            "course_id",
            flat=True,
        )
        .distinct()
    )

    # ---------------------------------------------------------
    # CURRENT ACTIVE COURSES
    # ---------------------------------------------------------
    #
    # Used only for scheduled/rescheduled teaching.
    #
    # Future/current lessons should be exposed only when:
    # - CourseEnrollment.status == active
    # - Course.status == active
    #
    # This prevents paused/completed/cancelled historical courses
    # from exposing future teaching slots.
    # ---------------------------------------------------------
    active_course_ids = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
            status="active",
            course__status="active",
        )
        .order_by()
        .values_list(
            "course_id",
            flat=True,
        )
        .distinct()
    )

    # ---------------------------------------------------------
    # CLASS SESSIONS
    # ---------------------------------------------------------
    #
    # CURRENT / UPCOMING:
    #
    # scheduled / rescheduled
    # - require active enrollment
    # - require active Course
    #
    # HISTORICAL:
    #
    # held_attendance_pending / complete_attendance_submitted
    # - remain visible for all learner Courses
    # - independent of current Course / enrollment status
    #
    # EXCLUDED:
    #
    # pending_reschedule
    # - no valid teaching slot exists yet
    #
    # cancelled
    # - lesson will not take place
    # ---------------------------------------------------------
    sessions = (
        ClassSession.objects
        .filter(
            Q(
                course_id__in=active_course_ids,
                status__in=[
                    ClassSession.STATUS_SCHEDULED,
                    ClassSession.STATUS_RESCHEDULED,
                ],
            )
            |
            Q(
                course_id__in=learner_course_ids,
                status__in=[
                    ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                    ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
                ],
            )
        )
        .select_related(
            "course",
        )
        .order_by(
            "start_time"
        )
    )

    # ---------------------------------------------------------
    # BANK HOLIDAYS
    # ---------------------------------------------------------
    bank_holidays = (
        BankHoliday.objects
        .filter(
            is_active=True,
        )
        .order_by(
            "start_date"
        )
    )

    # ---------------------------------------------------------
    # FULLCALENDAR DATE RANGE
    # ---------------------------------------------------------
    #
    # FullCalendar sends the visible date range through start/end.
    #
    # A ClassSession is included whenever it overlaps the requested
    # range rather than only when its start_time falls inside it.
    # ---------------------------------------------------------
    if start and end:
        start_datetime = parse_datetime(start)
        end_datetime = parse_datetime(end)

        if start_datetime and end_datetime:
            sessions = sessions.filter(
                start_time__lt=end_datetime,
                end_time__gt=start_datetime,
            )

            bank_holidays = (
                bank_holidays
                .filter(
                    start_date__lt=end_datetime.date()
                )
                .filter(
                    Q(end_date__isnull=True)
                    | Q(
                        end_date__gte=start_datetime.date()
                    )
                )
            )

    # ---------------------------------------------------------
    # BUILD CLASS SESSION EVENTS
    # ---------------------------------------------------------
    events = []

    for session in sessions:
        is_past = session.end_time <= now

        # -----------------------------------------------------
        # JOINABILITY
        # -----------------------------------------------------
        #
        # Join is possible only when:
        # - the lesson has not ended
        # - lifecycle is scheduled/rescheduled
        #
        # held_attendance_pending and
        # complete_attendance_submitted are historical states.
        # -----------------------------------------------------
        is_joinable = (
            not is_past
            and session.status in [
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
            ]
        )

        events.append({
            "id": session.id,
            "title": session.title,
            "start": session.start_time.isoformat(),
            "end": session.end_time.isoformat(),

            "extendedProps": {
                "type": "class_session",
                "course": session.course.name,
                "class_number": session.class_number,

                # Lifecycle and temporal state are deliberately
                # exposed separately to calendar.js.
                "status": session.status,
                "is_past": is_past,

                # Only expose a meeting link for a genuine
                # current/upcoming teaching slot.
                "meeting_link": (
                    get_calendar_meeting_link(session)
                    if is_joinable
                    else None
                ),

                # Historical and current sessions can both link
                # back to their Course details page.
                "group_details_url": (
                    f"{reverse('profiles:my_course')}"
                    f"?course={session.course.id}"
                ),
            },
        })

    # ---------------------------------------------------------
    # BUILD BANK HOLIDAY EVENTS
    # ---------------------------------------------------------
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
                holiday.end_date
                + timedelta(days=1)
            ).isoformat()

        events.append(event)

    return JsonResponse(
        events,
        safe=False,
    )


# STUDENT MY LEARNING PROGRESS PAGE
@login_required
def my_learning_progress(request):
    student = request.user
    student_profile = student.profile

    if student_profile.role not in [
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
        UserProfile.ROLE_EMPLOYEE,
    ]:
        return redirect("home")

    ClassSession.transition_past_sessions()

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # ALL ENROLLMENTS
    # Helper in profiles/utils/enrollments.py
    #
    # Historical courses remain accessible.
    #
    # Order:
    # 1. Active
    # 2. Confirmed
    # 3. Paused
    # 4. Completed
    # 5. Cancelled
    #
    # Within each status:
    # - course name A-Z
    #
    # Completed courses additionally use end_date as a
    # tie-breaker, newest first.
    # ---------------------------------------------------------
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects
        .filter(student=student)
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
    )

    # ---------------------------------------------------------
    # SELECTED COURSE
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")

    if selected_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )

    else:
        # Because the queryset is already ordered by lifecycle
        # priority, this naturally prefers:
        #
        # active -> confirmed -> paused -> completed -> cancelled
        enrollment = enrollments.first()

        # Redirect to canonical URL so the selected course
        # is always explicit.
        if enrollment:
            return redirect(
                f"{request.path}?course={enrollment.course_id}"
            )

    # ---------------------------------------------------------
    # NO ENROLLMENTS
    # ---------------------------------------------------------
    if not enrollment:
        context = {
            "student": student,
            "student_profile": student_profile,
            "user_currently_enrolled": user_currently_enrolled,

            "enrollments": enrollments,
            "enrollment": None,
            "course": None,

            # Timetable
            "formatted_timetable": [],

            # Attendance
            "attended_count": 0,
            "missed_count": 0,
            "excused_count": 0,
            "total_attendance_records": 0,
            "attendance_percentage": 0,
            "recent_attendance": [],

            # Attendance hours
            "attended_minutes": 0,
            "attended_hours": Decimal("0"),
            "attended_hours_display": format_minutes_duration(0),
            "submitted_minutes": 0,
            "submitted_hours": Decimal("0"),
            "submitted_hours_display": format_minutes_duration(0),

            # Course-level delivery
            "course_total_hours": Decimal("0"),
            "course_total_hours_display": format_minutes_duration(0),
            "held_course_minutes": 0,
            "held_course_hours_numeric": Decimal("0"),
            "held_course_hours_display": format_minutes_duration(0),

            # Learner general progress
            "total_classes": 0,
            "held_classes": 0,
            "attendance_pending_classes": 0,
            "attendance_submitted_classes": 0,
            "remaining_classes": 0,
            "delivery_percentage": 0,

            # Assigned delivery hours
            "total_hours": Decimal("0"),
            "total_hours_display": format_hours_duration(Decimal("0")),
            "held_hours": Decimal("0"),
            "held_hours_display": format_hours_duration(Decimal("0")),
            "remaining_hours": Decimal("0"),
            "remaining_hours_display": format_hours_duration(Decimal("0")),

            # Temporary class aliases
            "completed_classes": 0,

            # Skills
            "overall_skill_chart_data": {
                "labels": [],
                "datasets": [],
            },
            "overall_average_score": None,
        }

        return render(
            request,
            "profiles/student/my_learning_progress.html",
            context,
        )

    # ---------------------------------------------------------
    # SELECTED / DEFAULT COURSE
    # ---------------------------------------------------------
    course = enrollment.course

    # ---------------------------------------------------------
    # SKILLS PROGRESS GRAPH
    #
    # Historical overall-skill development.
    # ---------------------------------------------------------
    overall_skill_chart_data = (
        build_overall_skill_progress_chart_data(
            student=student,
            course=course,
        )
    )

    # ---------------------------------------------------------
    # CURRENT OVERALL SKILLS AVERAGE
    #
    # Only display an overall score when every expected skill
    # has a valid current score.
    # ---------------------------------------------------------
    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related("subskill_assessments")
    )

    current_skill_scores = [
        assessment.average_score
        for assessment in skill_assessments
        if assessment.average_score is not None
    ]

    expected_skill_count = len(
        StudentSkillAssessment.SKILL_AREA_CHOICES
    )

    overall_average_score = (
        round(
            sum(current_skill_scores)
            / expected_skill_count,
            1,
        )
        if len(current_skill_scores) == expected_skill_count
        else None
    )

    # ---------------------------------------------------------
    # FINAL ATTENDANCE
    #
    # Attendance metrics use ONLY ClassSessions whose
    # attendance has been fully submitted.
    # ---------------------------------------------------------
    attendances = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course,
            class_session__status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            status__in=[
                Attendance.STATUS_ATTENDED,
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

    total_attendance_records = attendances.count()
    attended_count = attendances.filter(
        status=Attendance.STATUS_ATTENDED
    ).count()
    missed_count = attendances.filter(
        status=Attendance.STATUS_MISSED
    ).count()
    excused_count = attendances.filter(
        status=Attendance.STATUS_EXCUSED
    ).count()

    attendance_percentage = enrollment.attendance_percentage

    # ---------------------------------------------------------
    # ATTENDANCE HOURS
    #
    # submitted_hours:
    # Duration of all assigned sessions whose attendance has
    # been fully submitted.
    #
    # attended_hours:
    # Duration of submitted sessions actually attended by
    # this learner.
    # ---------------------------------------------------------
    submitted_sessions = [
        attendance.class_session
        for attendance in attendances
    ]

    submitted_minutes = get_session_minutes(
        submitted_sessions
    )

    submitted_hours = (
        Decimal(submitted_minutes)
        / Decimal("60")
    )

    submitted_hours_display = format_minutes_duration(
        submitted_minutes
    )

    attended_sessions = [
        attendance.class_session
        for attendance in attendances
        if attendance.status == Attendance.STATUS_ATTENDED
    ]

    attended_minutes = get_session_minutes(
        attended_sessions
    )

    attended_hours = (
        Decimal(attended_minutes)
        / Decimal("60")
    )

    attended_hours_display = format_minutes_duration(
        attended_minutes
    )

    # ---------------------------------------------------------
    # LEARNER GENERAL PROGRESS
    #
    # Held = attendance pending + attendance submitted.
    # ---------------------------------------------------------
    total_classes = enrollment.total_assigned_classes
    held_classes = enrollment.total_held_classes
    attendance_pending_classes = (
        enrollment.held_attendance_pending_classes
    )
    attendance_submitted_classes = (
        enrollment.complete_attendance_submitted_classes
    )
    remaining_classes = enrollment.remaining_classes

    delivery_percentage = (
        round(
            held_classes
            / total_classes
            * 100
        )
        if total_classes else 0
    )

    # ---------------------------------------------------------
    # COURSE-LEVEL HOURS DELIVERED
    #
    # Delivery includes BOTH held lifecycle states:
    #
    # - held, attendance pending
    # - held, attendance submitted
    # ---------------------------------------------------------
    held_course_sessions = course.class_sessions.filter(
        status__in=[
            ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
            ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
        ]
    )

    held_course_minutes = get_session_minutes(
        held_course_sessions
    )

    held_course_hours_numeric = (
        Decimal(held_course_minutes)
        / Decimal("60")
    )

    held_course_hours_display = format_minutes_duration(
        held_course_minutes
    )

    # ---------------------------------------------------------
    # ORIGINAL COURSE HOURS
    # ---------------------------------------------------------
    course_total_hours = course.total_hours or 0
    course_total_minutes = round(
        float(course_total_hours)
        * 60
    )

    course_total_hours_display = format_minutes_duration(
        course_total_minutes
    )

    # ---------------------------------------------------------
    # TOTAL ASSIGNED HOURS
    #
    # Based on the sessions actually assigned to this learner,
    # rather than the generic course total.
    # ---------------------------------------------------------
    assigned_session_list = list(
        enrollment.assigned_sessions
    )

    assigned_minutes = get_session_minutes(
        assigned_session_list
    )

    total_hours = (
        Decimal(assigned_minutes)
        / Decimal("60")
    )

    # ---------------------------------------------------------
    # ASSIGNED HOURS DELIVERED
    #
    # Includes BOTH held lifecycle states.
    # ---------------------------------------------------------
    held_assigned_sessions = list(
        enrollment.assigned_sessions.filter(
            status__in=[
                ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            ]
        )
    )

    held_assigned_minutes = get_session_minutes(
        held_assigned_sessions
    )

    held_hours = (
        Decimal(held_assigned_minutes)
        / Decimal("60")
    )

    remaining_hours = max(
        total_hours - held_hours,
        Decimal("0"),
    )

    total_hours_display = format_hours_duration(
        total_hours
    )

    held_hours_display = format_hours_duration(
        held_hours
    )

    remaining_hours_display = format_hours_duration(
        remaining_hours
    )

    # ---------------------------------------------------------
    # RECENT ATTENDANCE
    # ---------------------------------------------------------
    recent_attendance = attendances[:5]

    # ---------------------------------------------------------
    # COURSE TIMETABLE
    # Helper in profiles/utils/courses.py
    # ---------------------------------------------------------
    formatted_timetable = build_formatted_timetable(
        course
    )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "student": student,
        "student_profile": student_profile,
        "user_currently_enrolled": user_currently_enrolled,

        # Course selector
        "enrollments": enrollments,

        # Selected enrollment / course
        "enrollment": enrollment,
        "course": course,

        # Timetable
        "formatted_timetable": formatted_timetable,

        # Attendance
        "attended_count": attended_count,
        "missed_count": missed_count,
        "excused_count": excused_count,
        "total_attendance_records": total_attendance_records,
        "attendance_percentage": attendance_percentage,
        "recent_attendance": recent_attendance,

        # Attendance hours
        "attended_minutes": attended_minutes,
        "attended_hours": attended_hours,
        "attended_hours_display": attended_hours_display,
        "submitted_minutes": submitted_minutes,
        "submitted_hours": submitted_hours,
        "submitted_hours_display": submitted_hours_display,

        # Course-level delivery
        "course_total_hours": course_total_hours,
        "course_total_hours_display": course_total_hours_display,
        "held_course_minutes": held_course_minutes,
        "held_course_hours_numeric": held_course_hours_numeric,
        "held_course_hours_display": held_course_hours_display,

        # Learner general progress
        "total_classes": total_classes,
        "held_classes": held_classes,
        "attendance_pending_classes": attendance_pending_classes,
        "attendance_submitted_classes": attendance_submitted_classes,
        "remaining_classes": remaining_classes,
        "delivery_percentage": delivery_percentage,

        # Assigned delivery hours
        "total_hours": total_hours,
        "total_hours_display": total_hours_display,
        "held_hours": held_hours,
        "held_hours_display": held_hours_display,
        "remaining_hours": remaining_hours,
        "remaining_hours_display": remaining_hours_display,

        # Temporary class aliases
        "completed_classes": held_classes,

        # Skills
        "overall_skill_chart_data": overall_skill_chart_data,
        "overall_average_score": overall_average_score,
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
    # ROLE
    # ---------------------------------------------------------
    if profile.role not in [
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
        UserProfile.ROLE_EMPLOYEE,
    ]:
        return redirect("home")

    student = request.user
    student_profile = profile

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # ALL ENROLLMENTS
    # Helper in profiles/utils/enrollments.py
    # Historical courses remain accessible.
    #
    # Order:
    # 1. Active
    # 2. Confirmed
    # 3. Paused
    # 4. Completed
    # 5. Cancelled
    #
    # Within each status:
    # - course name A-Z
    #
    # Completed courses additionally use end_date as a
    # tie-breaker, newest first.
    # ---------------------------------------------------------
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects
        .filter(student=student)
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
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
        enrollment = (
            enrollments
            .filter(course_id=selected_course_id)
            .first()
        )

        # Invalid / stale course id:
        # fall back to the first available enrollment.
        if not enrollment:
            enrollment = enrollments.first()

    else:
        enrollment = enrollments.first()

    # ---------------------------------------------------------
    # COURSE CURRENTLY BEING DISPLAYED
    # ---------------------------------------------------------
    course = (
        enrollment.course
        if enrollment
        else None
    )

    # ---------------------------------------------------------
    # NO ENROLLMENTS
    #
    # Keep the normal Attendance page accessible and provide
    # the same structural context with empty/default data.
    # ---------------------------------------------------------
    if not enrollment:
        return render(
            request,
            "profiles/student/my_attendance.html",
            {
                "profile": profile,

                # Shared student header
                "student": student,
                "student_profile": student_profile,
                "user_currently_enrolled": user_currently_enrolled,
                "course": None,

                # Component course detail nav
                "active_section": "attendance",

                # Course selector
                "enrollments": enrollments,

                # No selected enrollment
                "enrollment": None,

                # Attendance
                "recent_attendance": [],
                "recent_absences": [],
                "attended_hours_display": format_minutes_duration(0),

                # Completed course hours
                "completed_minutes": 0,
                "completed_hours_display": format_minutes_duration(0),
            }
        )

    # ---------------------------------------------------------
    # ATTENDED CLASSES
    #
    # Data comes from the SELECTED course only.
    # Historical course status does not matter.
    # ---------------------------------------------------------
    recent_attendance = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course,
            class_session__status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            status=Attendance.STATUS_ATTENDED,
        )
        .select_related(
            "class_session",
            "class_session__course",
        )
        .order_by(
            "-class_session__start_time"
        )
    )

    # ---------------------------------------------------------
    # ABSENCES
    #
    # Data comes from the SELECTED course only.
    # ---------------------------------------------------------
    recent_absences = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course,
            class_session__status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            status__in=[
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ],
        )
        .select_related(
            "class_session",
            "class_session__course",
        )
        .order_by(
            "-class_session__start_time"
        )
    )

    # ---------------------------------------------------------
    # ATTENDED HOURS
    # Calculate the actual duration of every class the learner
    # attended. This correctly supports sessions with different
    # durations, including a shorter final class.
    # ---------------------------------------------------------
    attended_sessions = (
        attendance.class_session
        for attendance in recent_attendance
        if attendance.status == Attendance.STATUS_ATTENDED
    )

    attended_minutes = get_session_minutes(
        attended_sessions
    )

    # Decimal version, useful if you ever need calculations.
    attended_hours = attended_minutes / 60

    # Human-friendly display.
    attended_hours_display = format_minutes_duration(
        attended_minutes
    )

    # ---------------------------------------------------------
    # COMPLETED COURSE HOURS
    #
    # Total duration of all COMPLETED class sessions for the
    # selected course, regardless of this learner's attendance.
    # ---------------------------------------------------------
    completed_course_sessions = (
        course.class_sessions
        .filter(
            status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
        )
    )

    completed_minutes = get_session_minutes(
        completed_course_sessions
    )

    # Numeric version if needed elsewhere.
    completed_hours = completed_minutes / 60

    # Human-friendly display.
    completed_hours_display = format_minutes_duration(
        completed_minutes
    )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,

        # Shared student header
        "student": student,
        "student_profile": student_profile,
        "user_currently_enrolled": user_currently_enrolled,
        "course": course,

        # Component course detail nav
        "active_section": "attendance",

        # ALL enrollments -> course selector
        "enrollments": enrollments,

        # ONE selected enrollment -> page content
        "enrollment": enrollment,

        # Attendance
        "recent_attendance": recent_attendance,
        "recent_absences": recent_absences,
        "attended_hours_display": attended_hours_display,

        # Completed course hours
        "completed_minutes": completed_minutes,
        "completed_hours_display": completed_hours_display,
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
    # ROLE
    # ---------------------------------------------------------
    if student_profile.role not in [
        UserProfile.ROLE_EMPLOYEE,
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
    ]:
        return redirect("home")

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # ALL ENROLLMENTS
    #
    # Historical courses remain accessible.
    # Helper in profiles/utils/enrollments.py
    # ---------------------------------------------------------
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects
        .filter(student=student)
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
    )

    # ---------------------------------------------------------
    # ACADEMIC PROFILE
    #
    # Belongs to the student rather than to a particular Course,
    # so it remains available even when there is no enrollment.
    # ---------------------------------------------------------
    academic_profile = getattr(
        student,
        "academic_profile",
        None,
    )

    # ---------------------------------------------------------
    # SELECTED COURSE / ENROLLMENT
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")

    if selected_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )
    else:
        enrollment = enrollments.first()

        if enrollment:
            return redirect(
                f"{request.path}?course={enrollment.course_id}"
            )

    # ---------------------------------------------------------
    # NO ENROLLMENTS
    #
    # Keep the normal Skills page accessible.
    #
    # No assessment DB records are created. We only package the
    # four canonical skill areas so the normal empty cards render.
    # ---------------------------------------------------------
    if not enrollment:
        skill_areas = [
            ("listening", "Listening"),
            ("reading", "Reading"),
            ("speaking", "Speaking"),
            ("writing", "Writing"),
        ]

        skills = []

        for skill_value, skill_name in skill_areas:
            subskills = [
                {
                    "value": value,
                    "name": label,
                    "assessment": None,
                    "is_assessed": False,
                    "rating": None,
                    "percentage": None,
                }
                for value, label in SUBSKILLS.get(skill_value, [])
            ]

            skills.append({
                "assessment": None,
                "assessment_id": None,
                "skill_value": skill_value,
                "name": skill_name,
                "icon": None,
                "score": None,
                "subskills": subskills,
                "assessed_subskills_count": 0,
                "total_subskills_count": len(subskills),
                "strengths": [],
                "confident": [],
                "satisfactory": [],
                "developing": [],
                "needs_work": [],
            })

        return render(
            request,
            "profiles/student/my_skills.html",
            {
                "student": student,
                "student_profile": student_profile,
                "user_currently_enrolled": user_currently_enrolled,
                "active_section": "skills",
                "enrollments": enrollments,
                "enrollment": None,
                "course": None,
                "skills": skills,
                "has_skill_assessment": False,
                "skill_note_display": [],
                "academic_profile": academic_profile,
                "chart_data": {"labels": [], "datasets": []},
                "level_choices": UserProfile.LEVEL_CHOICES,
            },
        )
    # ---------------------------------------------------------
    # SELECTED COURSE
    # ---------------------------------------------------------
    course = enrollment.course

    # ---------------------------------------------------------
    # SHARED SKILL CARD DATA
    # ---------------------------------------------------------
    skill_assessments, skills = build_student_skill_cards(
        student=student,
        course=course,
        build_skill_note_display=build_skill_note_display,
    )

    has_skill_assessment = any(
        skill["assessed_subskills_count"] > 0
        for skill in skills
    )

    skill_note_display = [
        build_skill_note_display(assessment)
        for assessment in skill_assessments
    ]

    # ---------------------------------------------------------
    # CHART DATA
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
        "user_currently_enrolled": user_currently_enrolled,
        "active_section": "skills",

        # Course selector
        "enrollments": enrollments,
        "enrollment": enrollment,
        "course": course,

        # Skills
        "skills": skills,
        "has_skill_assessment": has_skill_assessment,
        "skill_note_display": skill_note_display,

        # Academic profile
        "academic_profile": academic_profile,

        # Chart
        "chart_data": chart_data,

        # Levels
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

    # ---------------------------------------------------------
    # ROLE
    # ---------------------------------------------------------
    if profile.role not in [
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
        UserProfile.ROLE_EMPLOYEE,
    ]:
        return redirect("home")

    student = request.user
    student_profile = profile

    # ---------------------------------------------------------
    # CURRENT ENROLLMENT STATUS
    #
    # Separate from the selected Course.
    # A learner may be viewing a historical Course while still
    # having another currently active enrollment.
    # ---------------------------------------------------------
    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status=CourseEnrollment.STATUS_ACTIVE,
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # ALL ENROLLMENTS
    #
    # Historical Courses remain accessible.
    #
    # Order:
    # 1. Active
    # 2. Confirmed
    # 3. Paused
    # 4. Completed
    # 5. Cancelled
    # ---------------------------------------------------------
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects
        .filter(student=student)
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
    )

    # ---------------------------------------------------------
    # SELECTED COURSE / ENROLLMENT
    # ---------------------------------------------------------
    requested_course_id = request.GET.get("course")

    if requested_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=requested_course_id,
        )
    else:
        enrollment = enrollments.first()

    course = enrollment.course if enrollment else None

    # ---------------------------------------------------------
    # SKILL ASSESSMENTS
    # ---------------------------------------------------------
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


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "student": student,
        "student_profile": student_profile,
        "user_currently_enrolled": user_currently_enrolled,

        # All historical enrollments -> course selector
        "enrollments": enrollments,

        # Selected enrollment / course
        "enrollment": enrollment,
        "course": course,

        # Temporary compatibility aliases
        # Keep these until the corresponding template/component
        # has been checked and renamed safely.
        "active_enrollments": enrollments,
        "active_enrollment": enrollment,

        # Assessment
        "skill_note_display": skill_note_display,
    }

    return render(
        request,
        "profiles/student/my_learning_progress_assessment.html",
        context,
    )



@login_required
def my_needs_analysis(request):

    # ---------------------------------------------------------
    # ROLE
    # ---------------------------------------------------------
    profile = request.user.profile

    if profile.role not in {
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
        UserProfile.ROLE_EMPLOYEE,
    }:
        return redirect("home")

    # ---------------------------------------------------------
    # CURRENT ENROLLMENT STATUS
    #
    # Independent of the selected Course.
    # Used by the shared student details header.
    # ---------------------------------------------------------
    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=request.user,
        status=CourseEnrollment.STATUS_ACTIVE,
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # ALL ENROLLMENTS
    #
    # The Needs Analysis belongs to the CourseEnrollment,
    # not directly to the student.
    #
    # A learner with no enrollments may still access the page.
    # In that case the normal interface is rendered with an
    # empty/default state.
    #
    # Historical Courses remain accessible.
    # ---------------------------------------------------------
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects
        .filter(student=request.user)
        .select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
    )

    # ---------------------------------------------------------
    # SELECTED COURSE / ENROLLMENT
    # ---------------------------------------------------------
    course_id = request.GET.get("course")

    if course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=course_id,
        )
    else:
        enrollment = enrollments.first()

    course = enrollment.course if enrollment else None

    # ---------------------------------------------------------
    # DEFAULT EMPTY-STATE VALUES
    #
    # StudentNeedsAnalysis belongs to a CourseEnrollment, so
    # no model object is created until an enrollment exists.
    #
    # The form is still provided so the normal Learning Goals
    # interface can render.
    # ---------------------------------------------------------
    needs_analysis = None
    can_edit = False
    form = StudentNeedsAnalysisForm()

    english_use_frequency_labels = []
    communication_situation_labels = []
    communication_partner_labels = []
    accent_exposure_labels = []
    priority_area_labels = []
    learning_preference_labels = []

    speaking_confidence_display = ""
    listening_confidence_display = ""
    reading_confidence_display = ""
    writing_confidence_display = ""

    # ---------------------------------------------------------
    # ENROLLMENT-SPECIFIC NEEDS ANALYSIS
    # ---------------------------------------------------------
    if enrollment:

        # -----------------------------------------------------
        # NEEDS ANALYSIS
        #
        # One Needs Analysis exists per CourseEnrollment.
        # Newly created analyses begin as PENDING.
        # -----------------------------------------------------
        needs_analysis, _ = StudentNeedsAnalysis.objects.get_or_create(
            enrollment=enrollment,
        )

        # -----------------------------------------------------
        # EDIT PERMISSION
        #
        # Learners may edit/submit only while PENDING.
        # Once submitted, the questionnaire becomes read-only.
        # -----------------------------------------------------
        can_edit = (
            needs_analysis.status ==
            StudentNeedsAnalysis.Status.PENDING
        )

        # -----------------------------------------------------
        # FORM INITIAL DATA
        #
        # StudentNeedsAnalysisForm is currently a forms.Form,
        # therefore saved model values are supplied explicitly.
        #
        # This also allows the same form definition to provide
        # labels and values for the read-only shared template.
        # -----------------------------------------------------
        form_initial = {
            "english_use_frequency": needs_analysis.english_use_frequency,
            "communication_situations": needs_analysis.communication_situations,
            "communication_partners": needs_analysis.communication_partners,
            "accent_exposure": needs_analysis.accent_exposure,
            "accent_exposure_other": needs_analysis.accent_exposure_other,
            "speaking_confidence": needs_analysis.speaking_confidence,
            "listening_confidence": needs_analysis.listening_confidence,
            "reading_confidence": needs_analysis.reading_confidence,
            "writing_confidence": needs_analysis.writing_confidence,
            "priority_areas": needs_analysis.priority_areas,
            "additional_information": needs_analysis.additional_information,
        }

        # -----------------------------------------------------
        # FORM SUBMISSION
        # -----------------------------------------------------
        if (
            request.method == "POST"
            and request.POST.get("action") == "submit_needs_analysis"
        ):

            # Do not trust the template alone to protect a submitted
            # questionnaire. Reject any later/manual POST request.
            if not can_edit:
                return redirect(
                    f"{request.path}?course={course.id}"
                )

            form = StudentNeedsAnalysisForm(
                request.POST,
            )

            if form.is_valid():
                data = form.cleaned_data

                needs_analysis.english_use_frequency = data[
                    "english_use_frequency"
                ]
                needs_analysis.communication_situations = data[
                    "communication_situations"
                ]
                needs_analysis.communication_partners = data[
                    "communication_partners"
                ]

                needs_analysis.accent_exposure = data[
                    "accent_exposure"
                ]
                needs_analysis.accent_exposure_other = data[
                    "accent_exposure_other"
                ]

                needs_analysis.speaking_confidence = data[
                    "speaking_confidence"
                ]
                needs_analysis.listening_confidence = data[
                    "listening_confidence"
                ]
                needs_analysis.reading_confidence = data[
                    "reading_confidence"
                ]
                needs_analysis.writing_confidence = data[
                    "writing_confidence"
                ]

                needs_analysis.priority_areas = data[
                    "priority_areas"
                ]

                needs_analysis.additional_information = data[
                    "additional_information"
                ]

                needs_analysis.status = (
                    StudentNeedsAnalysis.Status.SUBMITTED
                )
                needs_analysis.submitted_at = timezone.now()

                needs_analysis.save()

                return redirect(
                    f"{request.path}?course={course.id}"
                )

        else:
            form = StudentNeedsAnalysisForm(
                initial=form_initial,
            )

        # -----------------------------------------------------
        # SUBMITTED FORM LABELS & ANSWERS DISPLAY
        # -----------------------------------------------------
        english_use_frequency_labels = form.choice_labels(
            "english_use_frequency",
            needs_analysis.english_use_frequency,
        )

        communication_situation_labels = form.choice_labels(
            "communication_situations",
            needs_analysis.communication_situations,
        )

        communication_partner_labels = form.choice_labels(
            "communication_partners",
            needs_analysis.communication_partners,
        )

        accent_exposure_labels = form.choice_labels(
            "accent_exposure",
            needs_analysis.accent_exposure,
            exclude_values={"other"},
        )

        priority_area_labels = form.choice_labels(
            "priority_areas",
            needs_analysis.priority_areas,
        )

        speaking_confidence_display = form.confidence_display(
            needs_analysis.speaking_confidence,
        )

        listening_confidence_display = form.confidence_display(
            needs_analysis.listening_confidence,
        )

        reading_confidence_display = form.confidence_display(
            needs_analysis.reading_confidence,
        )

        writing_confidence_display = form.confidence_display(
            needs_analysis.writing_confidence,
        )

    # ---------------------------------------------------------
    # NO-ENROLLMENT POST SAFETY
    #
    # There is no CourseEnrollment to attach a Needs Analysis
    # to, so a manual POST must not create anything.
    # ---------------------------------------------------------
    elif (
        request.method == "POST"
        and request.POST.get("action") == "submit_needs_analysis"
    ):
        return redirect(request.path)

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "student": request.user,
        "student_profile": profile,

        "course": course,
        "enrollment": enrollment,
        "enrollments": enrollments,

        "needs_analysis": needs_analysis,
        "form": form,

        "can_edit": can_edit,
        "can_review": False,

        "user_currently_enrolled": user_currently_enrolled,
        "active_section": "needs_analysis",

        "english_use_frequency_labels": english_use_frequency_labels,
        "communication_situation_labels": communication_situation_labels,
        "communication_partner_labels": communication_partner_labels,
        "accent_exposure_labels": accent_exposure_labels,
        "priority_area_labels": priority_area_labels,
        "learning_preference_labels": learning_preference_labels,

        "speaking_confidence_display": speaking_confidence_display,
        "listening_confidence_display": listening_confidence_display,
        "reading_confidence_display": reading_confidence_display,
        "writing_confidence_display": writing_confidence_display,
    }

    return render(
        request,
        "profiles/student/my_needs_analysis.html",
        context,
    )



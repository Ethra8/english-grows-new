from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django.db.models import Count, Q, Case, When, Value, IntegerField, F
from django.db.models.functions import Coalesce, Concat, Lower, NullIf, Trim

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from django.views.decorators.http import require_POST

from django.urls import reverse

from datetime import timedelta, datetime, time
import calendar

from profiles.utils.courses import build_formatted_timetable
from profiles.utils.enrollments import order_enrollments_by_course_status
from profiles.utils.skills import build_student_skill_cards

from profiles.utils.term_assessments import (
    get_or_create_term_assessment_draft,
    update_term_subskill_rating,
    submit_term_assessment,
    submit_skill_assessment,
)

from profiles.utils.term_assessment_reports import create_term_assessment_report

from profiles.utils.time_formating import (
    format_hours_duration,
    format_minutes_duration,
    get_session_minutes,
)

from profiles.models import (
    UserProfile, 
    TeacherProfile, 
    StudentAcademicProfile, 
    StudentSkillAssessment, 
    StudentSubSkillAssessment,
    StudentTermSubSkillAssessment, 
    SUBSKILLS,
    StudentTermAssessment,
    StudentTermAssessmentReport,
    StudentNeedsAnalysis,
)

from profiles.forms import (
    UserProfileForm,
    TeacherProfileForm,
    StudentAcademicProfileForm,
    StudentSubSkillAssessmentFormSet,
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


# ***********************************************|
# TEACHER PROFILE  ******************************|
# ***********************************************|

@login_required
def teacher_dashboard(request):
    profile = request.user.profile

    if profile.role != UserProfile.ROLE_TEACHER:
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
        Teacher dashboard reporting logic.

        Held:
            Lesson has actually finished.

        Upcoming:
            Lesson has not started yet.

        Attendance submitted:
            ClassSession lifecycle is explicitly
            COMPLETE_ATTENDANCE_SUBMITTED.

        Attendance pending:
            Held lesson whose attendance workflow has not yet
            reached COMPLETE_ATTENDANCE_SUBMITTED.

        Attendance rate:
            Attended / all final Attendance records belonging
            only to fully submitted ClassSessions.
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

        submitted_session_ids = [
            session.id
            for session in submitted_sessions
        ]

        attendance_records = Attendance.objects.filter(
            class_session_id__in=submitted_session_ids,
            status__in=[
                Attendance.STATUS_ATTENDED,
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ],
        )

        total_attendance_records = attendance_records.count()

        attended_records = attendance_records.filter(
            status=Attendance.STATUS_ATTENDED,
        ).count()

        return {
            "total_sessions": total_sessions,
            "held_sessions": held_count,
            "held_percentage": get_percentage(
                held_count,
                total_sessions,
            ),
            "upcoming_sessions": upcoming_count,
            "attendance_submitted_sessions":
                attendance_submitted_count,
            "attendance_pending_sessions":
                attendance_pending_count,
            "attendance_rate": get_percentage(
                attended_records,
                total_attendance_records,
            ),
        }

    # ---------------------------------------------------------
    # COURSES
    # ---------------------------------------------------------

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

    active_courses = courses.filter(
        status="active"
    ).count()

    # ---------------------------------------------------------
    # TODAY'S SESSIONS
    # ---------------------------------------------------------

    todays_sessions = (
        ClassSession.objects
        .filter(
            course__teacher=request.user,
            course__status="active",
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            ],
            start_time__gte=start_of_day,
            start_time__lte=end_of_day,
        )
        .select_related(
            "course",
            "course__company",
        )
        .prefetch_related(
            "course__enrollments",
            "course__enrollments__student",
        )
        .order_by("start_time")
    )

    # ---------------------------------------------------------
    # WEEKLY SESSIONS
    # ---------------------------------------------------------

    weekly_sessions = (
        ClassSession.objects
        .filter(
            course__teacher=request.user,
            course__status="active",
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            ],
            start_time__gte=start_of_week,
            start_time__lte=end_of_week,
        )
        .select_related("course")
        .order_by("start_time")
    )

    # ---------------------------------------------------------
    # MONTHLY SESSIONS
    # ---------------------------------------------------------

    monthly_sessions = (
        ClassSession.objects
        .filter(
            course__teacher=request.user,
            course__status="active",
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            ],
            start_time__gte=start_of_month,
            start_time__lte=end_of_month,
        )
        .select_related("course")
        .order_by("start_time")
    )

    # ---------------------------------------------------------
    # WEEKLY / MONTHLY METRICS
    # ---------------------------------------------------------

    weekly_metrics = get_period_metrics(
        weekly_sessions
    )

    monthly_metrics = get_period_metrics(
        monthly_sessions
    )

    # ---------------------------------------------------------
    # GENERAL DATA
    # ---------------------------------------------------------

    total_students = (
        courses
        .filter(
            status="active",
            enrollments__status="active",
        )
        .values("enrollments__student")
        .distinct()
        .count()
    )

    # ---------------------------------------------------------
    # GENERAL ATTENDANCE RATE
    #
    # Only Attendance records belonging to sessions whose
    # attendance workflow is fully submitted are included.
    # ---------------------------------------------------------

    attendance_records = Attendance.objects.filter(
        class_session__course__teacher=request.user,
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

    total_attendance_records = attendance_records.count()

    attended_records = attendance_records.filter(
        status=Attendance.STATUS_ATTENDED,
    ).count()

    total_attendance_rate = get_percentage(
        attended_records,
        total_attendance_records,
    )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------

    context = {
        "profile": profile,
        "courses": courses,
        "todays_sessions": todays_sessions,
        "today": today,

        # General
        "active_courses": active_courses,
        "total_students": total_students,
        "total_attendance_rate": total_attendance_rate,

        # Weekly
        "total_weekly_sessions":
            weekly_metrics["total_sessions"],

        "held_weekly_sessions":
            weekly_metrics["held_sessions"],

        "held_weekly_percentage":
            weekly_metrics["held_percentage"],

        "upcoming_weekly_sessions":
            weekly_metrics["upcoming_sessions"],

        "weekly_attendance_submitted_sessions":
            weekly_metrics["attendance_submitted_sessions"],

        "weekly_attendance_pending_sessions":
            weekly_metrics["attendance_pending_sessions"],

        "weekly_attendance_rate":
            weekly_metrics["attendance_rate"],

        # Monthly
        "total_monthly_sessions":
            monthly_metrics["total_sessions"],

        "held_monthly_sessions":
            monthly_metrics["held_sessions"],

        "held_monthly_percentage":
            monthly_metrics["held_percentage"],

        "upcoming_monthly_sessions":
            monthly_metrics["upcoming_sessions"],

        "monthly_attendance_submitted_sessions":
            monthly_metrics["attendance_submitted_sessions"],

        "monthly_attendance_pending_sessions":
            monthly_metrics["attendance_pending_sessions"],

        "monthly_attendance_rate":
            monthly_metrics["attendance_rate"],
    }

    return render(
        request,
        "profiles/teacher/teacher_dashboard.html",
        context,
    )



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
        .filter(
            course__teacher=request.user,
            course__status="active",
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
        "past": {
            "today": 0,
            "weekly": 0,
            "monthly": 0,
            "all": 0,
        },
    }

    for session in sessions:
        session_date = timezone.localdate(session.start_time)

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
        session.is_today = session_date == today

        session.is_this_week = (
            start_of_week <= session_date <= end_of_week
        )

        session.is_this_month = (
            session_date.year == today.year
            and session_date.month == today.month
        )

        # --------------------------------------------------
        # COUNTS
        # --------------------------------------------------
        if session.class_status_group:
            counts = class_filter_counts[session.class_status_group]

            counts["all"] += 1

            if session.is_today:
                counts["today"] += 1

            if session.is_this_week:
                counts["weekly"] += 1

            if session.is_this_month:
                counts["monthly"] += 1

    context = {
        "sessions": sessions,
        "now": now,
        "class_filter_counts": class_filter_counts,
    }

    return render(
        request,
        "profiles/teacher/teacher_classes_list.html",
        context,
    )



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
    completed_courses = courses.filter(status="completed").count()
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
        "completed_courses": completed_courses,
        "active_courses_list": active_courses_list,
    }

    return render(request, "profiles/teacher/teacher_courses.html", context)



@login_required
def teacher_course_details(request, course_id=None):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    # ---------------------------------------------------------
    # AVAILABLE COURSES FOR SELECTOR
    #
    # Show ALL courses belonging to this teacher, regardless
    # of lifecycle status.
    #
    # Order:
    # 1. Active
    # 2. Confirmed
    # 3. Paused
    # 4. Completed
    # 5. Cancelled
    # ---------------------------------------------------------
    available_courses = (
        Course.objects
        .filter(
            teacher=request.user,
        )
        .annotate(
            status_order=Case(
                When(status="active", then=Value(1)),
                When(status="confirmed", then=Value(2)),
                When(status="paused", then=Value(3)),
                When(status="completed", then=Value(4)),
                When(status="cancelled", then=Value(5)),
                default=Value(99),
                output_field=IntegerField(),
            )
        )
        .select_related(
            "course_type",
            "company",
            "teacher",
            "teacher__profile",
        )
        .order_by(
            "status_order",
            "name",
        )
    )

    # ---------------------------------------------------------
    # CURRENT COURSE
    #
    # Existing ID-based route:
    # - load the requested Course
    #
    # No-course route:
    # - if the teacher already has courses, redirect to the
    #   first Course in selector order
    # - if the teacher has no courses, keep course=None and
    #   render the normal Course Details interface with
    #   empty/default data
    # ---------------------------------------------------------
    course = None

    if course_id is not None:
        course = get_object_or_404(
            available_courses,
            id=course_id,
        )
    else:
        first_course = available_courses.first()

        if first_course:
            return redirect(
                "profiles:teacher_course_details",
                course_id=first_course.id,
            )

    # ---------------------------------------------------------
    # DEFAULT EMPTY-STATE VALUES
    #
    # These allow a teacher with no courses to access and view
    # the complete Course Details interface safely.
    # ---------------------------------------------------------
    enrollments = CourseEnrollment.objects.none()
    sessions = ClassSession.objects.none()

    total_classes = 0
    held_classes = 0
    attendance_pending_classes = 0
    attendance_submitted_classes = 0
    remaining_classes = 0
    delivery_percentage = 0

    held_minutes = 0
    held_hours = 0
    held_hours_display = format_minutes_duration(0)

    average_attendance = 0
    formatted_timetable = []
    bcc_student_emails = ""

    # ---------------------------------------------------------
    # COURSE-SPECIFIC DATA
    # ---------------------------------------------------------
    if course:
        # -----------------------------------------------------
        # SESSION LIFECYCLE
        #
        # Synchronize only the selected Course.
        #
        # The final ClassSession transition may also complete
        # the Course and its active enrollments, so refresh
        # afterwards.
        # -----------------------------------------------------
        ClassSession.transition_past_sessions(
            course=course
        )

        course.refresh_from_db()

        # -----------------------------------------------------
        # ALL ENROLLMENTS
        #
        # Keep historical enrollment records visible regardless
        # of enrollment status.
        #
        # Order:
        # 1. Active
        # 2. Confirmed
        # 3. Paused
        # 4. Completed
        # 5. Cancelled
        #
        # Then alphabetically by student name.
        # -----------------------------------------------------
        enrollments = (
            course.enrollments
            .select_related(
                "student",
                "student__profile",
            )
            .annotate(
                status_order=Case(
                    When(
                        status=CourseEnrollment.STATUS_ACTIVE,
                        then=Value(1),
                    ),
                    When(
                        status=CourseEnrollment.STATUS_PAUSED,
                        then=Value(3),
                    ),
                    When(
                        status=CourseEnrollment.STATUS_COMPLETED,
                        then=Value(4),
                    ),
                    When(
                        status=CourseEnrollment.STATUS_CANCELLED,
                        then=Value(5),
                    ),
                    default=Value(99),
                    output_field=IntegerField(),
                )
            )
            .order_by(
                "status_order",
                "student__first_name",
                "student__last_name",
                "student__username",
            )
        )

        # -----------------------------------------------------
        # CLASS SESSIONS
        # -----------------------------------------------------
        sessions = (
            course.class_sessions
            .all()
            .order_by("start_time")
        )

        # -----------------------------------------------------
        # COURSE DELIVERY
        #
        # Course owns all whole-course lifecycle calculations.
        #
        # Held means explicitly:
        # - held_attendance_pending
        # - complete_attendance_submitted
        #
        # It does NOT simply mean end_time has passed.
        # -----------------------------------------------------
        total_classes = course.total_sessions
        held_classes = course.total_held_sessions
        attendance_pending_classes = (
            course.held_attendance_pending_sessions
        )
        attendance_submitted_classes = (
            course.complete_attendance_submitted_sessions
        )
        remaining_classes = course.remaining_sessions
        delivery_percentage = course.delivery_percentage

        # -----------------------------------------------------
        # COURSE DELIVERY HOURS
        #
        # Course owns delivered duration calculations.
        # -----------------------------------------------------
        held_minutes = course.held_minutes
        held_hours = course.held_hours
        held_hours_display = format_minutes_duration(
            held_minutes
        )

        # -----------------------------------------------------
        # AVERAGE COURSE ATTENDANCE
        #
        # Each CourseEnrollment owns its own attendance
        # population and attendance percentage.
        #
        # The average across learners is page-level aggregation,
        # so it remains appropriately in the view.
        # -----------------------------------------------------
        attendance_percentages = []

        for enrollment in enrollments:
            attendance_metrics = enrollment.attendance_metrics

            if (
                attendance_metrics[
                    "total_submitted_attendance_records"
                ] > 0
            ):
                attendance_percentages.append(
                    attendance_metrics[
                        "attendance_percentage"
                    ]
                )

        average_attendance = (
            round(
                sum(attendance_percentages)
                / len(attendance_percentages)
            )
            if attendance_percentages else 0
        )

        # -----------------------------------------------------
        # COURSE TIMETABLE
        # -----------------------------------------------------
        formatted_timetable = build_formatted_timetable(
            course
        )

        # -----------------------------------------------------
        # GROUP EMAIL LIST
        # -----------------------------------------------------
        student_emails = [
            enrollment.student.email
            for enrollment in enrollments
            if enrollment.student.email
        ]

        bcc_student_emails = ",".join(
            student_emails
        )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,

        # Component course details nav
        "active_section": "overview",

        # Course selector
        "available_courses": available_courses,

        # Current course
        "course": course,

        # Course learners / sessions
        "enrollments": enrollments,
        "sessions": sessions,

        # Course delivery
        "total_classes": total_classes,
        "held_classes": held_classes,
        "attendance_pending_classes": attendance_pending_classes,
        "attendance_submitted_classes": attendance_submitted_classes,
        "remaining_classes": remaining_classes,
        "delivery_percentage": delivery_percentage,

        # Course delivery hours
        "held_minutes": held_minutes,
        "held_hours": held_hours,
        "held_hours_display": held_hours_display,

        # Attendance
        "average_attendance": average_attendance,

        # Timetable
        "formatted_timetable": formatted_timetable,

        # Group email
        "bcc_student_emails": bcc_student_emails,

        # Temporary compatibility aliases
        "completed_classes": attendance_submitted_classes,
        "past_held_classes": held_classes,
        "past_held_minutes": held_minutes,
        "past_held_hours": held_hours,
        "past_held_hours_display": held_hours_display,
    }

    return render(
        request,
        "profiles/teacher/teacher_course_details.html",
        context,
    )



@login_required
def teacher_course_attendance(request, course_id=None):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    # ---------------------------------------------------------
    # AVAILABLE COURSES
    #
    # Used by the shared course selector.
    #
    # Include ALL courses belonging to this teacher regardless
    # of lifecycle status.
    #
    # Order:
    # 1. Active
    # 2. Confirmed
    # 3. Paused
    # 4. Completed
    # 5. Cancelled
    # ---------------------------------------------------------
    available_courses = (
        Course.objects
        .filter(teacher=request.user)
        .annotate(
            status_order=Case(
                When(status="active", then=Value(1)),
                When(status="confirmed", then=Value(2)),
                When(status="paused", then=Value(3)),
                When(status="completed", then=Value(4)),
                When(status="cancelled", then=Value(5)),
                default=Value(99),
                output_field=IntegerField(),
            )
        )
        .select_related(
            "course_type",
            "company",
        )
        .order_by(
            "status_order",
            "name",
        )
    )

    # ---------------------------------------------------------
    # CURRENT COURSE
    #
    # Existing ID-based route:
    # - load the requested Course
    #
    # No-course route:
    # - if the teacher already has courses, redirect to the
    #   first Course in selector order
    # - if the teacher has no courses, keep course=None and
    #   render the normal Course Attendance interface with
    #   empty/default data
    # ---------------------------------------------------------
    course = None

    if course_id is not None:
        course = get_object_or_404(
            available_courses,
            id=course_id,
        )
    else:
        first_course = available_courses.first()

        if first_course:
            return redirect(
                "profiles:teacher_course_attendance",
                course_id=first_course.id,
            )

    # ---------------------------------------------------------
    # DEFAULT EMPTY-STATE VALUES
    #
    # These values allow a teacher with no assigned courses to
    # access the complete Course Attendance page and navigation.
    # ---------------------------------------------------------
    held_classes = 0
    attendance_submitted_classes = 0
    total_classes_held = 0
    average_attendance = 0

    submitted_class_sessions = (
        ClassSession.objects.none()
    )

    # ---------------------------------------------------------
    # COURSE-SPECIFIC DATA
    # ---------------------------------------------------------
    if course:
        # -----------------------------------------------------
        # SESSION LIFECYCLE
        #
        # Synchronize only the selected Course.
        #
        # The final ClassSession transition may also complete
        # the Course and its active enrollments, so refresh
        # afterwards.
        # -----------------------------------------------------
        ClassSession.transition_past_sessions(
            course=course
        )

        course.refresh_from_db()

        # -----------------------------------------------------
        # COURSE ATTENDANCE LIFECYCLE TOTALS
        #
        # Course owns whole-course delivery/session
        # calculations.
        # -----------------------------------------------------
        held_classes = (
            course.held_attendance_pending_sessions
        )

        attendance_submitted_classes = (
            course.complete_attendance_submitted_sessions
        )

        total_classes_held = (
            course.total_held_sessions
        )

        # -----------------------------------------------------
        # SUBMITTED ATTENDANCE SESSIONS
        #
        # Only ClassSessions whose attendance workflow is
        # complete belong in the submitted-attendance history.
        #
        # Session-level attendance counts remain query
        # annotations because ClassSession does not currently
        # own group-level attendance metrics.
        # -----------------------------------------------------
        submitted_class_sessions = (
            course.class_sessions
            .filter(
                status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            )
            .annotate(
                attended_count=Count(
                    "attendance_records",
                    filter=Q(
                        attendance_records__status=Attendance.STATUS_ATTENDED
                    ),
                    distinct=True,
                ),
                missed_count=Count(
                    "attendance_records",
                    filter=Q(
                        attendance_records__status=Attendance.STATUS_MISSED
                    ),
                    distinct=True,
                ),
                excused_count=Count(
                    "attendance_records",
                    filter=Q(
                        attendance_records__status=Attendance.STATUS_EXCUSED
                    ),
                    distinct=True,
                ),
                registered_count=Count(
                    "attendance_records",
                    filter=Q(
                        attendance_records__status__in=(
                            Attendance.FINAL_OUTCOME_STATUSES
                        )
                    ),
                    distinct=True,
                ),
            )
            .prefetch_related(
                "attendance_records__student",
                "attendance_records__student__profile",
            )
            .order_by("-start_time")
        )

        # -----------------------------------------------------
        # SESSION ATTENDANCE DISPLAY DATA
        #
        # These values package each submitted session for this
        # particular page. They are not canonical Course
        # calculations.
        # -----------------------------------------------------
        total_attended = 0
        total_registered = 0

        for session in submitted_class_sessions:
            session.attendance_percentage = (
                round(
                    session.attended_count
                    / session.registered_count
                    * 100
                )
                if session.registered_count else 0
            )

            total_attended += session.attended_count
            total_registered += session.registered_count

            session.employee_search_text = " ".join(
                part
                for attendance in session.attendance_records.all()
                for part in (
                    attendance.student.first_name or "",
                    attendance.student.last_name or "",
                    attendance.student.email or "",
                    attendance.student.username or "",
                )
                if part
            ).lower()

        # -----------------------------------------------------
        # OVERALL COURSE ATTENDANCE RATE
        #
        # Aggregate over the submitted Attendance records
        # displayed on this page.
        # -----------------------------------------------------
        average_attendance = (
            round(
                total_attended
                / total_registered
                * 100
            )
            if total_registered else 0
        )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,

        # Current Course
        "course": course,

        # Course selector
        "available_courses": available_courses,

        # Attendance lifecycle
        "held_classes": held_classes,
        "attendance_submitted_classes": attendance_submitted_classes,
        "total_classes_held": total_classes_held,

        # Attendance
        "average_attendance": average_attendance,
        "submitted_class_sessions": submitted_class_sessions,

        # Component Course Details nav
        "active_section": "attendance",
    }

    return render(
        request,
        "profiles/teacher/teacher_course_attendance.html",
        context,
    )


@login_required
def teacher_course_assessment(request, course_id=None):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    # AVAILABLE COURSES
    available_courses = (
        Course.objects
        .filter(teacher=request.user)
        .annotate(
            status_order=Case(
                When(status="active", then=Value(1)),
                When(status="confirmed", then=Value(2)),
                When(status="paused", then=Value(3)),
                When(status="completed", then=Value(4)),
                When(status="cancelled", then=Value(5)),
                default=Value(99),
                output_field=IntegerField(),
            )
        )
        .select_related("course_type", "company")
        .order_by("status_order", "name")
    )

    # CURRENT COURSE
    course = None

    if course_id is not None:
        course = get_object_or_404(available_courses, id=course_id)
    else:
        first_course = available_courses.first()
        if first_course:
            return redirect("profiles:teacher_course_assessment", course_id=first_course.id)

    # DEFAULT EMPTY-STATE VALUES
    enrollments = CourseEnrollment.objects.none()
    assessment_rows = []
    assessed_learners = 0
    submitted_assessments = 0

    # COURSE-SPECIFIC DATA
    if course:
        enrollments = list(
            course.enrollments
            .select_related("student", "student__profile")
            .order_by("student__first_name", "student__last_name", "student__username")
        )

        assessments = (
            StudentTermAssessment.objects
            .filter(enrollment_id__in=[enrollment.id for enrollment in enrollments])
            .order_by("enrollment_id", "-pk")
        )

        latest_by_enrollment = {}
        assessment_counts = {}

        for assessment in assessments:
            enrollment_id = assessment.enrollment_id
            assessment_counts[enrollment_id] = assessment_counts.get(enrollment_id, 0) + 1
            latest_by_enrollment.setdefault(enrollment_id, assessment)

        assessment_rows = [
            {
                "enrollment": enrollment,
                "latest_assessment": latest_by_enrollment.get(enrollment.id),
                "assessment_count": assessment_counts.get(enrollment.id, 0),
            }
            for enrollment in enrollments
        ]

        assessed_learners = len(assessment_counts)
        submitted_assessments = sum(
            assessment.status == StudentTermAssessment.Status.SUBMITTED
            for assessment in assessments
        )

    context = {
        "profile": profile,
        "course": course,
        "available_courses": available_courses,
        "enrollments": enrollments,
        "assessment_rows": assessment_rows,
        "assessed_learners": assessed_learners,
        "submitted_assessments": submitted_assessments,
        "active_section": "assessment",
    }

    return render(request, "profiles/teacher/teacher_course_assessment.html", context)




@login_required
def teacher_course_students_list(request, course_id=None):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    # ---------------------------------------------------------
    # AVAILABLE COURSES
    #
    # Used by the course selector.
    #
    # Include ALL courses belonging to this teacher,
    # regardless of status.
    #
    # Order:
    # 1. Active
    # 2. Confirmed
    # 3. Paused
    # 4. Completed
    # 5. Cancelled
    #
    # Then alphabetically by course name.
    # ---------------------------------------------------------
    available_courses = (
        Course.objects
        .filter(teacher=request.user)
        .annotate(
            status_order=Case(
                When(status="active", then=Value(1)),
                When(status="confirmed", then=Value(2)),
                When(status="paused", then=Value(3)),
                When(status="completed", then=Value(4)),
                When(status="cancelled", then=Value(5)),
                default=Value(6),
                output_field=IntegerField(),
            )
        )
        .order_by("status_order", "name")
    )

    # ---------------------------------------------------------
    # CURRENT COURSE
    #
    # Existing ID-based route:
    # - load the requested Course
    #
    # No-course route:
    # - if the teacher already has courses, redirect to the
    #   first Course in selector order
    # - if the teacher has no courses, keep course=None and
    #   render the normal Enrollments interface with
    #   empty/default data
    # ---------------------------------------------------------
    course = None

    if course_id is not None:
        course = get_object_or_404(
            available_courses,
            id=course_id,
        )
    else:
        first_course = available_courses.first()

        if first_course:
            return redirect(
                "profiles:teacher_course_students_list",
                course_id=first_course.id,
            )

    # ---------------------------------------------------------
    # SORTING
    # ---------------------------------------------------------
    sort_by = request.GET.get("sort", "name")

    if sort_by not in ["name", "level"]:
        sort_by = "name"

    # ---------------------------------------------------------
    # DEFAULT EMPTY-STATE VALUES
    #
    # These allow a teacher with no assigned courses to access
    # the complete Course Enrollments interface safely.
    # ---------------------------------------------------------
    enrollments = CourseEnrollment.objects.none()
    sessions = ClassSession.objects.none()

    total_classes = 0
    completed_classes = 0
    remaining_classes = 0
    delivery_percentage = 0
    average_attendance = 0

    formatted_timetable = []
    bcc_student_emails = ""

    # ---------------------------------------------------------
    # COURSE-SPECIFIC DATA
    # ---------------------------------------------------------
    if course:
        # -----------------------------------------------------
        # ENROLLMENTS / SORTING
        #
        # Historical enrollments remain visible regardless of
        # enrollment status.
        #
        # Name sorting uses:
        # - first name + last name when available
        # - username when no name has been provided
        # -----------------------------------------------------
        enrollments = (
            course.enrollments
            .select_related(
                "student",
                "student__profile",
            )
            .annotate(
                level_order=Case(
                    When(student__profile__current_level="A1", then=Value(1)),
                    When(student__profile__current_level="A2", then=Value(2)),
                    When(student__profile__current_level="B1.1", then=Value(3)),
                    When(student__profile__current_level="B1.2", then=Value(4)),
                    When(student__profile__current_level="B2.1", then=Value(5)),
                    When(student__profile__current_level="B2.2", then=Value(6)),
                    When(student__profile__current_level="C1.1", then=Value(7)),
                    When(student__profile__current_level="C1.2", then=Value(8)),
                    When(student__profile__current_level="C2", then=Value(9)),
                    default=Value(10),
                    output_field=IntegerField(),
                ),
                sort_name=Lower(
                    Coalesce(
                        NullIf(
                            Trim(
                                Concat(
                                    F("student__first_name"),
                                    Value(" "),
                                    F("student__last_name"),
                                )
                            ),
                            Value(""),
                        ),
                        F("student__username"),
                    )
                ),
            )
        )

        if sort_by == "level":
            enrollments = enrollments.order_by(
                "level_order",
                "sort_name",
            )
        else:
            enrollments = enrollments.order_by(
                "sort_name",
            )

        # -----------------------------------------------------
        # CLASS SESSIONS / GENERAL PROGRESS
        # -----------------------------------------------------
        sessions = (
            course.class_sessions
            .all()
            .order_by("start_time")
        )

        total_classes = course.total_sessions
        completed_classes = (
            course.complete_attendance_submitted_sessions
        )
        remaining_classes = course.remaining_sessions
        delivery_percentage = course.delivery_percentage

        # -----------------------------------------------------
        # AVERAGE ATTENDANCE
        # -----------------------------------------------------
        attendance_percentages = []

        for enrollment in enrollments:
            total_completed = (
                enrollment.complete_attendance_submitted_classes
            )

            if total_completed > 0:
                attendance_percentages.append(
                    (
                        enrollment.attended_classes
                        / total_completed
                    )
                    * 100
                )

        if attendance_percentages:
            average_attendance = round(
                sum(attendance_percentages)
                / len(attendance_percentages)
            )

        # -----------------------------------------------------
        # COURSE TIMETABLE
        # -----------------------------------------------------
        formatted_timetable = (
            build_formatted_timetable(
                course
            )
        )

        # -----------------------------------------------------
        # GROUP EMAIL
        # -----------------------------------------------------
        student_emails = [
            enrollment.student.email
            for enrollment in enrollments
            if enrollment.student.email
        ]

        bcc_student_emails = ",".join(
            student_emails
        )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "course": course,

        # Course selector
        "available_courses": available_courses,

        # Enrollments
        "enrollments": enrollments,
        "sort_by": sort_by,

        # Sessions
        "sessions": sessions,

        # Component course detail nav
        "active_section": "enrollments",

        # Progress timeline data
        "total_classes": total_classes,
        "completed_classes": completed_classes,
        "remaining_classes": remaining_classes,
        "delivery_percentage": delivery_percentage,

        # Attendance
        "average_attendance": average_attendance,

        # Timetable / email
        "formatted_timetable": formatted_timetable,
        "bcc_student_emails": bcc_student_emails,

        # Form/display choices
        "level_choices": UserProfile.LEVEL_CHOICES,
    }

    return render(
        request,
        "profiles/teacher/teacher_course_students_list.html",
        context,
    )


@login_required
def teacher_student_detail(request, course_id, enrollment_id):
    # ---------------------------------------------------------
    # ORIGINAL COURSE / ENROLLMENT
    #
    # Establishes:
    # - the learner being viewed
    # - that the logged-in teacher owns the course
    # ---------------------------------------------------------
    original_course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user,
    )

    original_enrollment = get_object_or_404(
        CourseEnrollment.objects.select_related(
            "student",
            "student__profile",
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        ),
        id=enrollment_id,
        course=original_course,
    )

    # ---------------------------------------------------------
    # STUDENT
    # ---------------------------------------------------------
    student = original_enrollment.student
    student_profile = student.profile
    student_is_active = student.is_active

    # ---------------------------------------------------------
    # ALL ENROLLMENTS FOR THIS STUDENT + THIS TEACHER
    #
    # Historical courses remain accessible.
    # ---------------------------------------------------------
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects
        .filter(
            student=student,
            course__teacher=request.user,
        )
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
        enrollment = original_enrollment

    course = enrollment.course

    # ---------------------------------------------------------
    # SESSION LIFECYCLE
    #
    # Synchronize only the selected Course.
    #
    # The final ClassSession transition may also complete the
    # Course and its active enrollments, so refresh both objects
    # before reading their calculated properties.
    # ---------------------------------------------------------
    ClassSession.transition_past_sessions(course=course)

    course.refresh_from_db()
    enrollment.refresh_from_db()

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status=CourseEnrollment.STATUS_ACTIVE,
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # FINAL ATTENDANCE
    #
    # CourseEnrollment owns the canonical submitted-attendance
    # population and all attendance calculations.
    #
    # Ordering/select_related here is presentation/query
    # preparation only.
    # ---------------------------------------------------------
    attendances = (
        enrollment.submitted_attendances
        .select_related("class_session")
        .order_by("-class_session__start_time")
    )

    attendance_metrics = enrollment.attendance_metrics

    total_attendance_records = attendance_metrics[
        "total_submitted_attendance_records"
    ]
    attended_count = attendance_metrics["attended_classes"]
    missed_count = attendance_metrics["missed_classes"]
    excused_count = attendance_metrics["excused_classes"]
    attendance_percentage = attendance_metrics["attendance_percentage"]

    # ---------------------------------------------------------
    # ATTENDANCE HOURS
    #
    # CourseEnrollment owns submitted and attended durations.
    # ---------------------------------------------------------
    submitted_minutes = enrollment.submitted_minutes
    submitted_hours = enrollment.submitted_hours
    submitted_hours_display = format_minutes_duration(
        submitted_minutes
    )

    attended_minutes = enrollment.attended_minutes
    attended_hours = enrollment.attended_hours
    attended_hours_display = format_minutes_duration(
        attended_minutes
    )

    # ---------------------------------------------------------
    # LEARNER GENERAL PROGRESS
    #
    # CourseEnrollment owns all learner delivery calculations.
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
    delivery_percentage = enrollment.delivery_percentage

    # ---------------------------------------------------------
    # COURSE-LEVEL DELIVERY
    #
    # Course owns whole-course duration and delivery calculations.
    # ---------------------------------------------------------
    course_total_hours = course.total_hours or 0
    course_total_minutes = course.total_minutes
    course_total_hours_display = format_minutes_duration(
        course_total_minutes
    )

    held_course_minutes = course.held_minutes
    held_course_hours_numeric = course.held_hours
    held_course_hours_display = format_minutes_duration(
        held_course_minutes
    )

    # ---------------------------------------------------------
    # ASSIGNED DELIVERY HOURS
    #
    # CourseEnrollment owns learner-specific assigned, held and
    # remaining delivery durations.
    # ---------------------------------------------------------
    total_hours = enrollment.total_assigned_hours
    held_hours = enrollment.held_hours
    remaining_hours = enrollment.remaining_hours

    total_hours_display = format_hours_duration(total_hours)
    held_hours_display = format_hours_duration(held_hours)
    remaining_hours_display = format_hours_duration(remaining_hours)

    # ---------------------------------------------------------
    # RECENT ATTENDANCE
    # ---------------------------------------------------------
    recent_attendance = attendances[:5]

    # ---------------------------------------------------------
    # CURRENT SKILL ASSESSMENTS
    # ---------------------------------------------------------
    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related("subskill_assessments")
        .order_by("skill")
    )

    current_skill_scores = [
        skill_assessment.average_score
        for skill_assessment in skill_assessments
        if skill_assessment.average_score is not None
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

    overall_skill_chart_data = (
        build_overall_skill_progress_chart_data(
            student=student,
            course=course,
        )
    )

    # ---------------------------------------------------------
    # COURSE TIMETABLE
    # ---------------------------------------------------------
    formatted_timetable = build_formatted_timetable(course)

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        # Student
        "student": student,
        "student_profile": student_profile,
        "user_currently_enrolled": user_currently_enrolled,
        "student_is_active": student_is_active,

        # Course selector
        "enrollments": enrollments,

        # Current course / enrollment
        "course": course,
        "enrollment": enrollment,

        # Levels
        "level_choices": UserProfile.LEVEL_CHOICES,

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

        # Temporary compatibility aliases
        "completed_classes": attendance_submitted_classes,

        # Skills
        "skill_assessments": skill_assessments,
        "overall_average_score": overall_average_score,
        "overall_skill_chart_data": overall_skill_chart_data,
    }

    return render(
        request,
        "profiles/teacher/teacher_student_detail.html",
        context,
    )


@login_required
def teacher_student_term_assessment(request, course_id, enrollment_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    # Original course and enrollment: teacher ownership enforced.
    original_course = get_object_or_404(
        Course, id=course_id, teacher=request.user
    )

    original_enrollment = get_object_or_404(
        CourseEnrollment.objects.select_related(
            "student", "student__profile", "course"
        ),
        id=enrollment_id,
        course=original_course,
    )

    student = original_enrollment.student
    student_profile = student.profile

    # All historical and current enrollments for this teacher.
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects.filter(
            student=student,
            course__teacher=request.user,
        ).select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
    )

    # Selected course, including the shared course selector.
    selected_course_id = request.GET.get("course")

    if selected_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )
    else:
        enrollment = original_enrollment

    course = enrollment.course

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status=CourseEnrollment.STATUS_ACTIVE,
        course__status="active",
    ).exists()

    # Formal assessments only: independent of ongoing Skills Assessment.
    term_assessments = (
        StudentTermAssessment.objects
        .filter(enrollment=enrollment)
        .select_related("teacher")
        .order_by("-pk")
    )

    context = {
        "profile": profile,
        "student": student,
        "student_profile": student_profile,
        "student_is_active": student.is_active,
        "user_currently_enrolled": user_currently_enrolled,
        "course": course,
        "enrollment": enrollment,
        "enrollments": enrollments,
        "level_choices": UserProfile.LEVEL_CHOICES,
        "term_assessments": term_assessments,
    }

    return render(
        request,
        "profiles/teacher/teacher_student_term_assessment.html",
        context,
    )




@login_required
def teacher_term_assessment_detail(request, course_id, enrollment_id, assessment_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    # Teacher-owned course and selected enrollment.
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

    # Assessment must belong to this exact enrollment.
    assessment = get_object_or_404(
        StudentTermAssessment.objects
        .select_related("teacher")
        .prefetch_related("skill_snapshots__subskill_assessments"),
        id=assessment_id,
        enrollment=enrollment,
    )

    # ---------------------------------------------------------
    # FORMAL ASSESSMENT ACTIONS
    # ---------------------------------------------------------
    if request.method == "POST":
        action = request.POST.get("action")

        # Generate a permanent report only after submission.
        if action == "generate_report":
            try:
                create_term_assessment_report(assessment, request.user)
            except ValidationError as exc:
                messages.error(request, "; ".join(exc.messages))
            else:
                messages.success(request, "Assessment report generated successfully.")

            return redirect(request.path)

        # All remaining assessment actions require a draft.
        if assessment.status != StudentTermAssessment.Status.DRAFT:
            messages.error(request, "Submitted assessments cannot be edited.")
            return redirect(request.path)

        # Submit the completed formal assessment.
        if action == "submit":
            try:
                submit_term_assessment(assessment, request.user)
            except ValidationError as exc:
                messages.error(request, "; ".join(exc.messages))
            else:
                messages.success(request, "Assessment submitted successfully.")

            return redirect(request.path)

        # Save an individual formal subskill rating.
        if action in (None, "", "save_rating"):
            subskill = get_object_or_404(
                StudentTermSubSkillAssessment,
                id=request.POST.get("subskill_id"),
                skill_snapshot__term_assessment=assessment,
            )

            rating = request.POST.get("rating") or None

            try:
                update_term_subskill_rating(subskill, rating)
            except ValidationError as exc:
                messages.error(request, "; ".join(exc.messages))
            else:
                messages.success(request, "Assessment rating saved successfully.")

            return redirect(request.path)

        messages.error(request, "Invalid assessment action.")
        return redirect(request.path)

    # ---------------------------------------------------------
    # EXISTING GENERATED REPORT
    # ---------------------------------------------------------
    report = StudentTermAssessmentReport.objects.filter(
        assessment=assessment
    ).select_related("generated_by").first()

    # Preserve the shared learner course selector.
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects.filter(
            student=student,
            course__teacher=request.user,
        ).select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
    )

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status=CourseEnrollment.STATUS_ACTIVE,
        course__status="active",
    ).exists()

    skill_snapshots = assessment.skill_snapshots.all()

    total_subskills = sum(
        snapshot.subskill_assessments.count()
        for snapshot in skill_snapshots
    )

    assessed_subskills = sum(
        1
        for snapshot in skill_snapshots
        for subskill in snapshot.subskill_assessments.all()
        if subskill.rating
    )

    context = {
        "profile": profile,
        "course": course,
        "enrollment": enrollment,
        "enrollments": enrollments,
        "student": student,
        "student_profile": student_profile,
        "student_is_active": student.is_active,
        "user_currently_enrolled": user_currently_enrolled,
        "level_choices": UserProfile.LEVEL_CHOICES,
        "assessment": assessment,
        "skill_snapshots": skill_snapshots,
        "total_subskills": total_subskills,
        "assessed_subskills": assessed_subskills,
        "rating_choices": StudentSubSkillAssessment.Rating.choices,
        "report": report,
    }

    return render(
        request,
        "profiles/teacher/teacher_term_assessment_detail.html",
        context,
    )



@login_required
@require_POST
def teacher_create_term_assessment(request, course_id, enrollment_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

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

    term_label = request.POST.get("term_label", "").strip()
    history_url = reverse(
        "profiles:teacher_student_term_assessment",
        kwargs={"course_id":course.id, "enrollment_id":enrollment.id},
    )

    if not term_label or len(term_label) > 50:
        messages.error(request, "Enter an assessment period of up to 50 characters.")
        return redirect(history_url)

    existing = StudentTermAssessment.objects.filter(
        enrollment=enrollment,
        term_label=term_label,
    ).first()

    if existing:
        messages.info(request, "An assessment already exists for this period.")
        return redirect(history_url)

    get_or_create_term_assessment_draft(
        enrollment=enrollment,
        term_label=term_label,
    )

    messages.success(request, "Term assessment draft created successfully.")
    return redirect(history_url)



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



@login_required
def student_attendance_record(request, course_id, enrollment_id):

    # ---------------------------------------------------------
    # ORIGINAL COURSE / ENROLLMENT
    #
    # These establish:
    # - which learner is being viewed
    # - that the logged-in teacher owns the original course
    #
    # Once that relationship is established, the course
    # selector may switch to another enrollment belonging to
    # the same learner and teacher through:
    #
    #     ?course=<course_id>
    # ---------------------------------------------------------
    original_course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user,
    )

    original_enrollment = get_object_or_404(
        CourseEnrollment.objects
        .select_related(
            "student",
            "student__profile",
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        ),
        id=enrollment_id,
        course=original_course,
    )


    # ---------------------------------------------------------
    # STUDENT
    # ---------------------------------------------------------
    student = original_enrollment.student
    student_profile = student.profile

    # Django User account status
    student_is_active = student.is_active

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # ALL ENROLLMENTS FOR THIS STUDENT + THIS TEACHER
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
    # A teacher may only switch between courses that:
    # - belong to this learner
    # - are assigned to the logged-in teacher
    # ---------------------------------------------------------
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects
        .filter(
            student=student,
            course__teacher=request.user,
        )
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
    )

    # ---------------------------------------------------------
    # COURSE SELECTOR
    #
    # Example:
    #
    # ?course=8
    # ---------------------------------------------------------
    selected_course_id = request.GET.get(
        "course"
    )


    if selected_course_id:

        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )

    else:

        enrollment = original_enrollment


    # ---------------------------------------------------------
    # CURRENTLY SELECTED COURSE
    # ---------------------------------------------------------
    course = enrollment.course


    # ---------------------------------------------------------
    # ATTENDANCE RECORDS
    #
    # All attendance records for this learner + selected course.
    # ---------------------------------------------------------
    attendances = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course,
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
    # ATTENDANCE COUNTS
    # ---------------------------------------------------------
    total_attendance_records = (
        attendances
        .filter(
            status__in=[
                Attendance.STATUS_ATTENDED,
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ]
        )
        .count()
    )


    attended_count = (
        attendances
        .filter(
            status=Attendance.STATUS_ATTENDED
        )
        .count()
    )


    missed_count = (
        attendances
        .filter(
            status=Attendance.STATUS_MISSED
        )
        .count()
    )


    excused_count = (
        attendances
        .filter(
            status=Attendance.STATUS_EXCUSED
        )
        .count()
    )


    # ---------------------------------------------------------
    # COURSE PROGRESS
    #
    # These are based on the CURRENT selected enrollment.
    # ---------------------------------------------------------
    completed_classes = (
        enrollment.complete_attendance_submitted_classes
    )

    total_classes = (
        enrollment.total_assigned_classes
    )

    remaining_classes = (
        enrollment.remaining_classes
    )


    # ---------------------------------------------------------
    # ATTENDANCE %
    #
    # The model already contains the canonical attendance
    # calculation, so use it here as well.
    #
    # This keeps the percentage shown in the view consistent
    # with:
    #
    #     enrollment.attendance_percentage
    #
    # which your template already uses directly.
    # ---------------------------------------------------------
    attendance_percentage = (
        enrollment.attendance_percentage
    )


    # ---------------------------------------------------------
    # COMPLETION %
    # ---------------------------------------------------------
    delivery_percentage = (
        round(
            (
                completed_classes
                / total_classes
            )
            * 100
        )
        if total_classes > 0
        else 0
    )


    # ---------------------------------------------------------
    # ATTENDANCE HISTORY
    #
    # Completed/submitted attendance outcomes only.
    # ---------------------------------------------------------
    recent_attendance = (
        attendances
        .filter(
            status__in=[
                Attendance.STATUS_ATTENDED,
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ],
        )
        .order_by(
            "-class_session__start_time"
        )
    )


    # ---------------------------------------------------------
    # ABSENCE HISTORY
    #
    # Required by:
    #
    #     {% if recent_absences %}
    #
    # in teacher_student_attendance_record.html
    #
    # Includes both:
    # - missed
    # - excused
    # ---------------------------------------------------------
    recent_absences = (
        attendances
        .filter(
            status__in=[
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ],
        )
        .order_by(
            "-class_session__start_time"
        )
    )


    # ---------------------------------------------------------
    # ENROLLMENT CONTEXT
    #
    # This handles a learner who joined a course after some
    # classes had already been completed.
    #
    # The HTML uses:
    #
    #     show_enrollment_context
    #     lessons_before_enrollment
    #     completed_classes
    #
    # ---------------------------------------------------------
    lessons_before_enrollment = 0

    if enrollment.enrolled_at:
        lessons_before_enrollment = (
            course.class_sessions
            .filter(
                status__in=[
                    ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                    ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
                ],
                end_time__lt=enrollment.enrolled_at,
            )
            .count()
        )

    show_enrollment_context = (
        lessons_before_enrollment > 0
    )


    # ---------------------------------------------------------
    # ATTENDED HOURS
    #
    # Actual duration of sessions marked attended.
    # ---------------------------------------------------------
    attended_sessions = (
        attendance.class_session
        for attendance in attendances
        if attendance.status == Attendance.STATUS_ATTENDED
    )

    attended_minutes = get_session_minutes(
        attended_sessions
    )

    attended_hours = (
        attended_minutes / 60
    )

    attended_hours_display = format_minutes_duration(
        attended_minutes
    )


    # ---------------------------------------------------------
    # COMPLETED COURSE HOURS
    #
    # Total duration of completed ClassSessions for the course,
    # regardless of whether this learner attended.
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

    completed_hours = (
        completed_minutes / 60
    )

    completed_hours_display = format_minutes_duration(
        completed_minutes
    )


    # ---------------------------------------------------------
    # TOTAL COURSE HOURS
    # ---------------------------------------------------------
    total_hours = (
        course.total_hours or 0
    )


    total_minutes = round(
        float(total_hours)
        * 60
    )

    total_hours_display = format_minutes_duration(
        total_minutes
    )


    # ---------------------------------------------------------
    # COURSE TIMETABLE
    #
    # Not currently displayed in the attendance body you
    # supplied, but kept available because the learner header /
    # shared course components may use it.
    # ---------------------------------------------------------
    formatted_timetable = build_formatted_timetable(course)


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {

        # -----------------------------------------------------
        # STUDENT
        # -----------------------------------------------------
        "student": student,
        "student_profile": student_profile,

        "level_choices": (
            UserProfile.LEVEL_CHOICES
        ),

        "user_currently_enrolled": user_currently_enrolled,
        # Explicit learner account status.
        # This is User.is_active and is completely independent
        # from CourseEnrollment.status and Course.status.
        "student_is_active": student_is_active,
        # COURSE SELECTOR
        "enrollments": enrollments,
        "course": course,
        "enrollment": enrollment,

        # COURSE / TIMETABLE 
        "formatted_timetable": (
            formatted_timetable
        ),
        # ATTENDANCE
        "attended_count": (
            attended_count
        ),

        "missed_count": (
            missed_count
        ),

        "excused_count": (
            excused_count
        ),

        "total_attendance_records": (
            total_attendance_records
        ),

        "attendance_percentage": (
            attendance_percentage
        ),


        # -----------------------------------------------------
        # ATTENDANCE HISTORY
        # -----------------------------------------------------
        "recent_attendance": (
            recent_attendance
        ),

        "recent_absences": (
            recent_absences
        ),


        # -----------------------------------------------------
        # ENROLLMENT CONTEXT
        # -----------------------------------------------------
        "show_enrollment_context": (
            show_enrollment_context
        ),

        "lessons_before_enrollment": (
            lessons_before_enrollment
        ),


        # -----------------------------------------------------
        # ATTENDANCE HOURS
        # -----------------------------------------------------
        "attended_minutes": (
            attended_minutes
        ),

        "attended_hours": (
            attended_hours
        ),

        "attended_hours_display": (
            attended_hours_display
        ),


        # -----------------------------------------------------
        # COMPLETED COURSE HOURS
        # -----------------------------------------------------
        "completed_minutes": (
            completed_minutes
        ),

        "completed_hours": (
            completed_hours
        ),

        "completed_hours_display": (
            completed_hours_display
        ),


        # -----------------------------------------------------
        # TOTAL COURSE HOURS
        # -----------------------------------------------------
        "total_hours": (
            total_hours
        ),

        "total_hours_display": (
            total_hours_display
        ),


        # -----------------------------------------------------
        # COURSE PROGRESS
        # -----------------------------------------------------
        "completed_classes": (
            completed_classes
        ),

        "remaining_classes": (
            remaining_classes
        ),

        "total_classes": (
            total_classes
        ),

        "delivery_percentage": (
            delivery_percentage
        ),
    }


    return render(
        request,
        "profiles/teacher/teacher_student_attendance_record.html",
        context,
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
    # ---------------------------------------------------------
    # ORIGINAL COURSE / ENROLLMENT
    #
    # These establish:
    # - which learner is being viewed
    # - that the logged-in teacher owns the original course
    #
    # The selector can then switch course using:
    #
    #     ?course=<course_id>
    # ---------------------------------------------------------
    original_course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user,
    )


    original_enrollment = get_object_or_404(
        CourseEnrollment.objects
        .select_related(
            "student",
            "student__profile",
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        ),
        id=enrollment_id,
        course=original_course,
    )


    # ---------------------------------------------------------
    # STUDENT
    # ---------------------------------------------------------
    student = original_enrollment.student
    student_profile = student.profile


    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
        course__status="active",
    ).exists()

    # Django User account status
    student_is_active = student.is_active

    # ---------------------------------------------------------
    # ALL ENROLLMENTS FOR THIS STUDENT + THIS TEACHER
    #
    # Historical courses remain accessible.
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
        .filter(
            student=student,
            course__teacher=request.user,
        )
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
    )

    # ---------------------------------------------------------
    # SELECTED COURSE FROM QUERY STRING
    #
    # Example:
    #
    # ?course=8
    # ---------------------------------------------------------
    selected_course_id = request.GET.get(
        "course"
    )


    if selected_course_id:

        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )

    else:

        enrollment = original_enrollment


    # ---------------------------------------------------------
    # CURRENTLY SELECTED COURSE
    # ---------------------------------------------------------
    course = enrollment.course


    # ---------------------------------------------------------
    # ENSURE ALL PREDEFINED SKILLS / SUBSKILLS EXIST
    #
    # Teacher-specific behavior:
    #
    # The teacher needs editable assessment rows to exist.
    #
    # Creating an unrated subskill does NOT create a snapshot,
    # because rating=None means "Not assessed yet".
    # ---------------------------------------------------------
    for skill_value, skill_label in (
        StudentSkillAssessment.SKILL_AREA_CHOICES
    ):

        skill_assessment, created = (
            StudentSkillAssessment.objects
            .get_or_create(
                student=student,
                course=course,
                skill=skill_value,
            )
        )

        for subskill_value, subskill_label in SUBSKILLS.get(
            skill_value,
            [],
        ):

            StudentSubSkillAssessment.objects.get_or_create(
                skill_assessment=skill_assessment,
                subskill=subskill_value,
            )


    # ---------------------------------------------------------
    # SHARED SKILL CARD DATA
    #
    # Shared helper builds:
    #
    # - all four skill cards
    # - all canonical subskills
    # - assessed / pending state
    # - assessed subskill count
    # - total canonical subskill count
    # - current skill score
    # - grouped assessment categories
    #
    # assessment_id remains available for the teacher Edit
    # Skill button.
    # ---------------------------------------------------------
    skill_assessments, skills = (
        build_student_skill_cards(
            student=student,
            course=course,
            build_skill_note_display=(
                build_skill_note_display
            ),
        )
    )


    # ---------------------------------------------------------
    # CURRENT OVERALL SKILLS AVERAGE
    #
    # Each StudentSkillAssessment.average_score already gives
    # the current score for that skill on the /10 scale.
    #
    # Only show an overall score once all four skills have
    # a valid current assessment.
    # ---------------------------------------------------------
    current_skill_scores = []

    for skill_assessment in skill_assessments:

        score = (
            skill_assessment.average_score
        )

        if score is not None:

            current_skill_scores.append(
                score
            )


    expected_skill_count = len(
        StudentSkillAssessment.SKILL_AREA_CHOICES
    )


    if (
        len(current_skill_scores)
        == expected_skill_count
    ):

        overall_average_score = round(
            sum(current_skill_scores)
            / expected_skill_count,
            1,
        )

    else:

        overall_average_score = None


    # ---------------------------------------------------------
    # DISPLAY-FRIENDLY SKILL NOTE DATA
    # ---------------------------------------------------------
    skill_note_display = [
        build_skill_note_display(
            skill_assessment
        )
        for skill_assessment in skill_assessments
    ]


    # ---------------------------------------------------------
    # ACADEMIC PROFILE
    # ---------------------------------------------------------
    academic_profile = getattr(
        student,
        "academic_profile",
        None,
    )


    # ---------------------------------------------------------
    # DETAILED 4-SKILL PROGRESS GRAPH
    #
    # Uses StudentSkillAssessmentSnapshot history.
    # Same graph as learner Skills page.
    # ---------------------------------------------------------
    chart_data = (
        build_skill_progress_chart_data(
            student=student,
            course=course,
        )
    )


    # ---------------------------------------------------------
    # OVERALL SKILLS PROGRESS GRAPH
    #
    # Useful if this teacher skills template also includes
    # the overall-progress card/header.
    # ---------------------------------------------------------
    overall_skill_chart_data = (
        build_overall_skill_progress_chart_data(
            student=student,
            course=course,
        )
    )


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {

        # Student
        "student": student,
        "student_profile": student_profile,
        "user_currently_enrolled":
            user_currently_enrolled,
        "student_is_active": student_is_active,
        # Course selector
        "enrollments": enrollments,
        # Current selected course / enrollment
        "course": course,
        "enrollment": enrollment,
        # Skills
        "skills": skills,
        "skill_assessments": skill_assessments,
        "skill_note_display": skill_note_display,
        # Overall current score
        "overall_average_score": overall_average_score,
        # Graphs
        "chart_data": chart_data,
        "overall_skill_chart_data": overall_skill_chart_data,
        # Academic profile
        "academic_profile": academic_profile,
        # Level choices
        "level_choices":
            UserProfile.LEVEL_CHOICES,
    }

    return render(
        request,
        "profiles/teacher/student_skills_overview.html",
        context,
    )



@login_required
def teacher_edit_student_skill(request, skill_assessment_id):

    # ---------------------------------------------------------
    # GET SKILL ASSESSMENT
    #
    # Security:
    # The skill assessment must belong to a course taught
    # by the currently logged-in teacher.
    # ---------------------------------------------------------
    skill_assessment = get_object_or_404(
        StudentSkillAssessment.objects
        .select_related("student", "course")
        .prefetch_related("subskill_assessments"),
        id=skill_assessment_id,
        course__teacher=request.user,
    )

    skill = StudentSkillAssessment.SKILL_AREA_CHOICES

    # ---------------------------------------------------------
    # POST
    # ---------------------------------------------------------
    if request.method == "POST":
        formset = StudentSubSkillAssessmentFormSet(
            request.POST,
            instance=skill_assessment,
        )

        if formset.is_valid():

            ratings = {
                form.instance.subskill: form.cleaned_data["rating"]
                for form in formset.forms
            }

            submit_skill_assessment(
                skill_assessment=skill_assessment,
                ratings=ratings,
            )            
            # -------------------------------------------------
            # WRITTEN FEEDBACK
            #
            # Do NOT regenerate teacher_notes here.
            #
            # Written feedback will be generated separately
            # through an explicit teacher/admin action.
            # -------------------------------------------------

            # -------------------------------------------------
            # GET COURSE ENROLLMENT
            # -------------------------------------------------
            enrollment = get_object_or_404(
                CourseEnrollment,
                student=skill_assessment.student,
                course=skill_assessment.course,
            )

            # -------------------------------------------------
            # REDIRECT TO STUDENT SKILLS OVERVIEW
            # -------------------------------------------------
            return redirect(
                "profiles:student_skills_overview",
                course_id=skill_assessment.course.id,
                enrollment_id=enrollment.id,
            )

    # ---------------------------------------------------------
    # GET
    # ---------------------------------------------------------
    else:
        formset = StudentSubSkillAssessmentFormSet(
            instance=skill_assessment,
        )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "skill_assessment": skill_assessment,
        "formset": formset,
        "skill": skill,
    }

    return render(
        request,
        "profiles/teacher/teacher_edit_student_skill.html",
        context,
    )



@login_required
def teacher_student_needs_analysis(request, course_id, enrollment_id):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    # ---------------------------------------------------------
    # ENROLLMENT
    #
    # Restrict access to enrollments belonging to a Course
    # taught by the logged-in teacher.
    # ---------------------------------------------------------
    enrollment = get_object_or_404(
        CourseEnrollment.objects.select_related(
            "student",
            "student__profile",
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        ),
        id=enrollment_id,
        course_id=course_id,
        course__teacher=request.user,
    )

    student = enrollment.student
    student_profile = student.profile
    course = enrollment.course

    # ---------------------------------------------------------
    # CURRENT ENROLLMENT STATUS
    #
    # Independent of the selected Course.
    # Used by the shared student details header.
    # ---------------------------------------------------------
    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status=CourseEnrollment.STATUS_ACTIVE,
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # ALL ENROLLMENTS FOR THIS STUDENT + THIS TEACHER
    #
    # Used by the shared student course selector.
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
        .filter(
            student=student,
            course__teacher=request.user,
        )
        .select_related(
            "course",
            "course__course_type",
            "course__teacher",
            "course__company",
        )
    )

    # ---------------------------------------------------------
    # NEEDS ANALYSIS
    #
    # One Needs Analysis belongs to one CourseEnrollment.
    # ---------------------------------------------------------
    needs_analysis, _ = StudentNeedsAnalysis.objects.get_or_create(
        enrollment=enrollment,
    )

    # ---------------------------------------------------------
    # MARK AS REVIEWED
    #
    # Teacher never edits the learner's questionnaire responses.
    # The only POST action available here is reviewing a
    # previously submitted Needs Analysis.
    # ---------------------------------------------------------
    if request.method == "POST":
        if request.POST.get("action") != "mark_reviewed":
            return HttpResponseBadRequest()

        if needs_analysis.status != StudentNeedsAnalysis.Status.SUBMITTED:
            return HttpResponseForbidden(
                "Only submitted needs analyses can be reviewed."
            )

        needs_analysis.status = StudentNeedsAnalysis.Status.REVIEWED
        needs_analysis.reviewed_at = timezone.now()
        needs_analysis.save(
            update_fields=(
                "status",
                "reviewed_at",
            )
        )

        return redirect(
            "profiles:teacher_student_needs_analysis",
            course_id=course.id,
            enrollment_id=enrollment.id,
        )

    # ---------------------------------------------------------
    # FORM
    #
    # Teacher does not edit the questionnaire.
    # The form is used for field labels, choice labels and
    # human-readable display values.
    # ---------------------------------------------------------
    form = StudentNeedsAnalysisForm()

    # ---------------------------------------------------------
    # HUMAN-READABLE DISPLAY VALUES
    # ---------------------------------------------------------
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
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "student": student,
        "student_profile": student_profile,
        "course": course,
        "enrollment": enrollment,
        "enrollments": enrollments,

        "needs_analysis": needs_analysis,
        "form": form,

        "can_edit": False,
        "can_review": (
            needs_analysis.status ==
            StudentNeedsAnalysis.Status.SUBMITTED
        ),

        "user_currently_enrolled": user_currently_enrolled,
        "active_section": "needs_analysis",

        "english_use_frequency_labels": english_use_frequency_labels,
        "communication_situation_labels": communication_situation_labels,
        "communication_partner_labels": communication_partner_labels,
        "accent_exposure_labels": accent_exposure_labels,
        "priority_area_labels": priority_area_labels,

        "speaking_confidence_display": speaking_confidence_display,
        "listening_confidence_display": listening_confidence_display,
        "reading_confidence_display": reading_confidence_display,
        "writing_confidence_display": writing_confidence_display,
    }

    return render(
        request,
        "profiles/teacher/teacher_student_needs_analysis.html",
        context,
    )



@login_required
def teacher_student_assessment_notes(request, course_id, enrollment_id):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    # ---------------------------------------------------------
    # COURSE
    #
    # Restrict access to Courses belonging to the logged-in
    # teacher.
    # ---------------------------------------------------------
    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user,
    )

    # ---------------------------------------------------------
    # ENROLLMENT
    #
    # The Enrollment must belong to the selected teacher-owned
    # Course.
    # ---------------------------------------------------------
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

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
        course__status="active",
    ).exists()

    # Django User account status
    student_is_active = student.is_active

    # ---------------------------------------------------------
    # SKILL ASSESSMENTS
    # ---------------------------------------------------------
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


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,

        "user_currently_enrolled": user_currently_enrolled,

        # Django User account status
        "student_is_active": student_is_active,

        "course": course,
        "enrollment": enrollment,
        "student": student,
        "student_profile": student_profile,

        "skills": skills,
        "skill_note_display": skill_note_display,

        "level_choices": UserProfile.LEVEL_CHOICES,
    }

    return render(
        request,
        "profiles/teacher/teacher_student_assessment_notes.html",
        context,
    )



@login_required
def teacher_calendar(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    courses = (
        Course.objects
        .filter(teacher=request.user)
        .select_related("course_type", "company", "teacher")
        .order_by("name")
    )

    return render(
        request,
        "profiles/teacher/teacher_calendar.html",
        {
            "profile": profile,
            "courses": courses,
        },
    )


@login_required
def teacher_calendar_events(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_TEACHER:
        return JsonResponse([], safe=False)

    start = request.GET.get("start")
    end = request.GET.get("end")
    now = timezone.now()

    # Current/upcoming: scheduled, rescheduled.
    # Historical: held_attendance_pending, complete_attendance_submitted.
    # Excluded: pending_reschedule, cancelled.
    sessions = (
        ClassSession.objects
        .filter(
            course__teacher=request.user,
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            ],
        )
        .select_related("course")
        .order_by("start_time")
    )

    bank_holidays = BankHoliday.objects.filter(is_active=True).order_by("start_date")

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
        status_class = {
            "confirmed": "course-confirmed-event",
            "paused": "course-paused-event",
            "cancelled": "course-cancelled-event",
        }.get(session.course.status, "")

        is_past = (
            session.end_time <= now
            if session.end_time
            else session.start_time < now
        )

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
            "end": session.end_time.isoformat() if session.end_time else None,
            "className": status_class,
            "extendedProps": {
                "type": "class_session",
                "course": session.course.name,
                "course_status": session.course.status,
                "class_number": session.class_number,
                "status": session.status,
                "is_past": is_past,
                "meeting_link": (
                    get_calendar_meeting_link(session)
                    if is_joinable else None
                ),
                "group_details_url": reverse(
                    "profiles:teacher_course_details",
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
            "extendedProps": {"type": "bank_holiday"},
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

        if session.status == ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED:
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

    # ---------------------------------------------------------
    # SYNCHRONIZE SESSION LIFECYCLE
    #
    # If this scheduled/rescheduled lesson has now finished,
    # transition it immediately to held_attendance_pending.
    #
    # This gives the teacher an immediate transition without
    # waiting for the next 5-minute Cron Job run.
    # ---------------------------------------------------------
    class_session.synchronize_status_after_end()

    # ---------------------------------------------------------
    course = class_session.course

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

        class_session.refresh_from_db()

        if class_session.status == ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED:
            messages.success(
                request,
                "Attendance saved and lesson marked as completed."
            )
        elif class_session.attendance_requirements_resolved:
            messages.success(
                request,
                "Attendance saved. The lesson will be completed automatically after it ends."
            )
        else:
            messages.success(
                request,
                "Attendance saved. Complete all learner records to finish the attendance submission."
            )

        return redirect(
            "profiles:teacher_attendance_detail",
            session_id=class_session.id,
        )
    
    context = {
        "profile": profile,
        "course": course,
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

    # ---------------------------------------------------------
    # CLASS SESSION / COURSE
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # AVAILABLE COURSES
    #
    # Used by the shared course selector.
    # ---------------------------------------------------------
    available_courses = (
        Course.objects
        .filter(teacher=request.user)
        .select_related(
            "course_type",
            "company",
        )
        .order_by("name")
    )

    # ---------------------------------------------------------
    # ALL COURSE ENROLLMENTS
    #
    # Enrollment status must NOT determine whether a student
    # appears in historical course/session lists.
    #
    # Includes:
    # - active
    # - paused
    # - completed
    # - cancelled
    # ---------------------------------------------------------
    enrollments = list(
        CourseEnrollment.objects
        .filter(course=course)
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

    # ---------------------------------------------------------
    # ATTENDANCE RECORDS FOR THIS SESSION
    # ---------------------------------------------------------
    attendances_by_student_id = {
        attendance.student_id: attendance
        for attendance in (
            Attendance.objects
            .filter(class_session=class_session)
            .select_related(
                "student",
                "student__profile",
            )
        )
    }

    # Attach the relevant attendance record to each enrollment.
    # Missing attendance remains None rather than removing the
    # student from the list.
    for enrollment in enrollments:
        enrollment.attendance_record = attendances_by_student_id.get(
            enrollment.student_id
        )

    # ---------------------------------------------------------
    # ATTENDANCE COUNTS
    # ---------------------------------------------------------
    attendance_records = [
        enrollment.attendance_record
        for enrollment in enrollments
        if enrollment.attendance_record
    ]

    attended_count = sum(
        1 for attendance in attendance_records
        if attendance.status == "attended"
    )

    missed_count = sum(
        1 for attendance in attendance_records
        if attendance.status == "missed"
    )

    excused_count = sum(
        1 for attendance in attendance_records
        if attendance.status == "excused"
    )

    total_count = len(attendance_records)

    context = {
        "profile": profile,
        "class_session": class_session,
        "course": course,
        "available_courses": available_courses,
        "enrollments": enrollments,
        "attended_count": attended_count,
        "missed_count": missed_count,
        "excused_count": excused_count,
        "total_count": total_count,
        "active_section": "attendance",
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
        # Existing Attendance records remain status="pending" and stay
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
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    now = timezone.now()

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

    rescheduled_sessions = (
        ClassSession.objects
        .filter(
            course__teacher=request.user,
            status=ClassSession.STATUS_RESCHEDULED,
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
        )
        .order_by("start_time")
    )

    for session in rescheduled_sessions:
        session.is_rescheduled_past = session.start_time < now
        session.is_rescheduled_upcoming = session.start_time >= now

    return render(
        request,
        "profiles/teacher/teacher_reschedule_classes.html",
        {
            "profile": profile,
            "pending_sessions": pending_sessions,
            "rescheduled_sessions": rescheduled_sessions,
        },
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


# TEACHER PROFILE SETTINGS
@login_required
def teacher_profile_settings(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")

    teacher_profile, _ = TeacherProfile.objects.get_or_create(
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



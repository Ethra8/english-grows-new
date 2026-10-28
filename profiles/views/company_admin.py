from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.db.models import Count, Q, Prefetch, Case, When, Value, IntegerField, Exists, OuterRef
from django.db.models.functions import Coalesce, Lower, NullIf

from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.dateparse import parse_datetime, parse_date

from django.urls import reverse

from datetime import timedelta, datetime, time
import calendar
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
    StudentNeedsAnalysis,
)

from profiles.forms import (
    UserProfileForm,
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



@login_required
def company_admin_dashboard(request):
    profile = request.user.profile

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
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

    resolved_attendance_statuses = {
        Attendance.STATUS_ATTENDED,
        Attendance.STATUS_MISSED,
        Attendance.STATUS_EXCUSED,
    }

    def get_percentage(value, total):
        if total == 0:
            return 0

        return round(
            (value / total) * 100
        )

    def get_period_metrics(sessions):
        """
        Dashboard reporting logic:

        Held:
            Session has actually finished.

        Upcoming:
            Session has not started yet.

        Attendance submitted:
            ClassSession lifecycle is explicitly
            COMPLETE_ATTENDANCE_SUBMITTED.

        Attendance rate:
            Attended / resolved Attendance records belonging
            only to fully submitted ClassSessions.
        """

        session_list = list(sessions)

        total_sessions = len(session_list)

        held_sessions = []
        upcoming_sessions = []

        attendance_submitted_sessions = 0

        total_resolved_attendance_records = 0
        attended_records = 0

        for session in session_list:

            # -----------------------------
            # CLASS CHRONOLOGY
            # -----------------------------

            if session.end_time < now:
                held_sessions.append(session)

            elif session.start_time >= now:
                upcoming_sessions.append(session)

            # -----------------------------
            # ATTENDANCE SUBMITTED
            #
            # ClassSession.status owns this lifecycle state.
            # Do not reconstruct submission from Attendance rows.
            # -----------------------------

            if (
                session.status
                != ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            ):
                continue

            attendance_submitted_sessions += 1

            # -----------------------------
            # ATTENDANCE RATE
            #
            # Only fully submitted ClassSessions contribute to
            # attendance reporting.
            # -----------------------------

            attendance_records = list(
                session.attendance_records.all()
            )

            resolved_records = [
                attendance
                for attendance in attendance_records
                if attendance.status in resolved_attendance_statuses
            ]

            total_resolved_attendance_records += len(
                resolved_records
            )

            attended_records += sum(
                1
                for attendance in resolved_records
                if attendance.status == Attendance.STATUS_ATTENDED
            )

        held_count = len(held_sessions)
        upcoming_count = len(upcoming_sessions)

        attendance_pending_sessions = max(
            held_count - attendance_submitted_sessions,
            0,
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

            "attendance_submitted_sessions":
                attendance_submitted_sessions,

            "attendance_pending_sessions":
                attendance_pending_sessions,

            "attendance_submitted_percentage":
                get_percentage(
                    attendance_submitted_sessions,
                    held_count,
                ),

            "attendance_rate":
                get_percentage(
                    attended_records,
                    total_resolved_attendance_records,
                ),

            "resolved_attendance_records":
                total_resolved_attendance_records,

            "attended_records":
                attended_records,
        }

    # ---------------------------------------------------------
    # COURSES
    # ---------------------------------------------------------

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

    active_courses = courses.filter(
        status="active"
    ).count()

    # ---------------------------------------------------------
    # TODAY'S CLASSES
    # ---------------------------------------------------------

    todays_sessions = (
        ClassSession.objects
        .filter(
            course__company=company,
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
            "course__teacher",
            "course__company",
        )
        .prefetch_related(
            "course__enrollments",
            "course__enrollments__student",
            "attendance_records",
        )
        .order_by("start_time")
    )

    # ---------------------------------------------------------
    # WEEKLY CLASSES
    # ---------------------------------------------------------

    weekly_sessions = (
        ClassSession.objects
        .filter(
            course__company=company,
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
        .select_related(
            "course",
        )
        .prefetch_related(
            "attendance_records",
        )
        .order_by("start_time")
    )

    # ---------------------------------------------------------
    # MONTHLY CLASSES
    # ---------------------------------------------------------

    monthly_sessions = (
        ClassSession.objects
        .filter(
            course__company=company,
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
        .select_related(
            "course",
        )
        .prefetch_related(
            "attendance_records",
        )
        .order_by("start_time")
    )

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
    # ACTIVE EMPLOYEES
    # ---------------------------------------------------------

    total_students = (
        courses
        .filter(
            status="active",
            enrollments__status="active",
        )
        .values(
            "enrollments__student"
        )
        .distinct()
        .count()
    )

    # ---------------------------------------------------------
    # OVERALL ATTENDANCE RATE
    #
    # Attendance reporting uses only ClassSessions whose
    # attendance workflow has been fully submitted.
    # ---------------------------------------------------------

    attendance_records = (
        Attendance.objects
        .filter(
            class_session__course__company=company,
            class_session__course__status="active",
            class_session__status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            status__in=[
                Attendance.STATUS_ATTENDED,
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ],
        )
    )

    total_attendance_records = (
        attendance_records.count()
    )

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
        "company": company,
        "courses": courses,
        "todays_sessions": todays_sessions,
        "today": today,

        # General
        "active_courses": active_courses,
        "total_students": total_students,
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

        "weekly_attendance_submitted_sessions":
            weekly_metrics["attendance_submitted_sessions"],

        "weekly_attendance_pending_sessions":
            weekly_metrics["attendance_pending_sessions"],

        "weekly_attendance_submitted_percentage":
            weekly_metrics["attendance_submitted_percentage"],

        "weekly_attendance_rate":
            weekly_metrics["attendance_rate"],

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

        "monthly_attendance_submitted_sessions":
            monthly_metrics["attendance_submitted_sessions"],

        "monthly_attendance_pending_sessions":
            monthly_metrics["attendance_pending_sessions"],

        "monthly_attendance_submitted_percentage":
            monthly_metrics["attendance_submitted_percentage"],

        "monthly_attendance_rate":
            monthly_metrics["attendance_rate"],
    }

    return render(
        request,
        "profiles/company_admin/company_admin_dashboard.html",
        context,
    )



@login_required
def company_admin_courses(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    status_order = Case(
        When(status="active", then=Value(1)),
        When(status="confirmed", then=Value(2)),
        When(status="paused", then=Value(3)),
        When(status="completed", then=Value(4)),
        When(status="cancelled", then=Value(5)),
        default=Value(99),
        output_field=IntegerField(),
    )

    courses = (
        Course.objects
        .filter(company=company)
        .annotate(
            enrollment_count=Count("enrollments"),
            status_order=status_order,
        )
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
        .order_by(
            "status_order",
            "name",
        )
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
        "company": company,
        "courses": courses,
        "total_courses": total_courses,
        "active_courses": active_courses,
        "confirmed_courses": confirmed_courses,
        "cancelled_courses": cancelled_courses,
        "paused_courses": paused_courses,
        "completed_courses": completed_courses,
        "active_courses_list": active_courses_list,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_courses.html",
        context
    )


@login_required
def company_admin_all_courses_attendance(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    # ---------------------------------------------------------
    # COMPANY COURSES
    # ---------------------------------------------------------
    company_courses = Course.objects.filter(company=company)

    # ---------------------------------------------------------
    # SESSION LIFECYCLE
    #
    # Synchronize only Courses belonging to this company.
    # ClassSession remains responsible for lifecycle transitions.
    # ---------------------------------------------------------
    for company_course in company_courses.only("pk"):
        ClassSession.transition_past_sessions(course=company_course)

    # ---------------------------------------------------------
    # FILTERS
    # ---------------------------------------------------------
    now = timezone.now()

    attendance_session_statuses = [
        ClassSession.STATUS_SCHEDULED,
        ClassSession.STATUS_RESCHEDULED,
        ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
        ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
    ]

    selected_date = request.GET.get("date", "").strip()
    course_search = request.GET.get("course", "").strip()
    employee_search = request.GET.get("employee", "").strip()
    parsed_date = parse_date(selected_date) if selected_date else None

    # ---------------------------------------------------------
    # COMPANY SUMMARY
    # ---------------------------------------------------------
    total_company_courses_count = company_courses.count()
    active_company_courses_count = company_courses.filter(
        status="active"
    ).count()

    # ---------------------------------------------------------
    # ACTIVE ENROLLMENTS
    #
    # Used for current employee counts on non-completed Courses.
    # ---------------------------------------------------------
    enrollment_queryset = (
        CourseEnrollment.objects
        .filter(status=CourseEnrollment.STATUS_ACTIVE)
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
    # CLASS SESSIONS
    #
    # The queryset is deliberately filterable by date.
    # Attendance records are prefetched once and later aggregated
    # only for submitted ClassSessions.
    # ---------------------------------------------------------
    class_session_queryset = (
        ClassSession.objects
        .filter(status__in=attendance_session_statuses)
        .select_related("course")
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

    if parsed_date:
        class_session_queryset = class_session_queryset.filter(
            start_time__date=parsed_date
        )

    # ---------------------------------------------------------
    # FILTERABLE COURSE QUERYSET
    # ---------------------------------------------------------
    courses = (
        company_courses
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
        .annotate(
            status_priority=Case(
                When(status="active", then=Value(1)),
                When(status="confirmed", then=Value(2)),
                When(status="paused", then=Value(3)),
                When(status="completed", then=Value(4)),
                When(status="cancelled", then=Value(5)),
                default=Value(99),
                output_field=IntegerField(),
            )
        )
        .order_by(
            "status_priority",
            "name",
        )
    )

    if course_search:
        courses = courses.filter(
            Q(name__icontains=course_search)
            | Q(course_type__name__icontains=course_search)
        )

    if employee_search:
        employee_parts = employee_search.split()

        employee_query = (
            Q(enrollments__student__email__icontains=employee_search)
            | Q(enrollments__student__username__icontains=employee_search)
            | Q(enrollments__student__first_name__icontains=employee_search)
            | Q(enrollments__student__last_name__icontains=employee_search)
        )

        if len(employee_parts) >= 2:
            first_name_search = employee_parts[0]
            last_name_search = " ".join(employee_parts[1:])

            employee_query |= (
                Q(
                    enrollments__student__first_name__icontains=first_name_search
                )
                & Q(
                    enrollments__student__last_name__icontains=last_name_search
                )
            )

        courses = courses.filter(employee_query).distinct()

    if parsed_date:
        courses = courses.filter(
            class_sessions__status__in=attendance_session_statuses,
            class_sessions__start_time__date=parsed_date,
        ).distinct()

    # ---------------------------------------------------------
    # BUILD COURSE LIST
    #
    # Canonical lifecycle meaning comes from ClassSession.
    # Aggregation remains here because these values respect the
    # page's optional date/search filters.
    # ---------------------------------------------------------
    all_courses_list = []
    global_employee_ids = set()

    global_held_classes = 0
    global_pending_attendance_classes = 0
    global_submitted_classes = 0

    global_attended_count = 0
    global_missed_count = 0
    global_excused_count = 0

    for course in courses:
        active_enrollments = course.active_enrollments

        global_employee_ids.update(
            enrollment.student_id
            for enrollment in active_enrollments
        )

        class_sessions = course.attendance_class_sessions

        # -----------------------------------------------------
        # FILTER-SCOPED SESSION GROUPS
        #
        # ClassSession properties own lifecycle interpretation.
        # -----------------------------------------------------
        held_class_sessions = [
            session
            for session in class_sessions
            if session.is_held
        ]

        pending_attendance_sessions = [
            session
            for session in held_class_sessions
            if session.attendance_is_pending
        ]

        submitted_class_sessions = [
            session
            for session in held_class_sessions
            if session.attendance_is_submitted
        ]

        future_class_sessions = [
            session
            for session in class_sessions
            if session.status in {
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
            }
            and session.start_time >= now
        ]

        # -----------------------------------------------------
        # FILTER-SCOPED ATTENDANCE COUNTS
        #
        # Attendance owns the canonical final outcome statuses.
        # Only genuine outcomes from submitted lessons count.
        # -----------------------------------------------------
        attended_count = 0
        missed_count = 0
        excused_count = 0

        for class_session in submitted_class_sessions:
            final_attendance_records = [
                attendance
                for attendance in class_session.attendance_records.all()
                if attendance.status in Attendance.FINAL_OUTCOME_STATUSES
            ]

            attended_count += sum(
                attendance.status == Attendance.STATUS_ATTENDED
                for attendance in final_attendance_records
            )

            missed_count += sum(
                attendance.status == Attendance.STATUS_MISSED
                for attendance in final_attendance_records
            )

            excused_count += sum(
                attendance.status == Attendance.STATUS_EXCUSED
                for attendance in final_attendance_records
            )

        # -----------------------------------------------------
        # FILTER-SCOPED DELIVERY COUNTS
        #
        # These deliberately use the already-filtered session list
        # rather than whole-Course model totals.
        # -----------------------------------------------------
        held_classes_count = len(held_class_sessions)
        pending_submission_count = len(pending_attendance_sessions)
        submitted_classes_count = len(submitted_class_sessions)

        total_final_attendance_records = (
            attended_count
            + missed_count
            + excused_count
        )

        attendance_rate = (
            round(
                attended_count
                / total_final_attendance_records
                * 100
            )
            if total_final_attendance_records else 0
        )

        submission_rate = (
            round(
                submitted_classes_count
                / held_classes_count
                * 100
            )
            if held_classes_count else 0
        )

        # -----------------------------------------------------
        # DISPLAY-SPECIFIC SESSION SELECTION
        # -----------------------------------------------------
        last_class = max(
            held_class_sessions,
            key=lambda session: session.start_time,
            default=None,
        )

        next_class = min(
            future_class_sessions,
            key=lambda session: session.start_time,
            default=None,
        )

        # -----------------------------------------------------
        # EMPLOYEE COUNT
        #
        # For completed Courses there may no longer be active
        # enrollments, so use the final submitted lesson roster.
        # -----------------------------------------------------
        if course.status == "completed":
            last_submitted_class = max(
                submitted_class_sessions,
                key=lambda session: session.start_time,
                default=None,
            )

            course.employee_count = (
                last_submitted_class.attendance_records.count()
                if last_submitted_class
                else 0
            )
        else:
            course.employee_count = len(active_enrollments)

        # -----------------------------------------------------
        # TEMPLATE ATTRIBUTES
        #
        # These package the filtered data for the template.
        # They do not replace canonical model properties.
        # -----------------------------------------------------
        course.held_classes_count = held_classes_count
        course.pending_submission_count = pending_submission_count
        course.submitted_classes_count = submitted_classes_count
        course.submission_rate = submission_rate

        course.attended_count = attended_count
        course.missed_count = missed_count
        course.excused_count = excused_count
        course.attendance_rate = attendance_rate

        course.last_class = last_class
        course.next_class = next_class

        # Temporary compatibility alias.
        course.past_classes_count = held_classes_count

        all_courses_list.append(course)

        # -----------------------------------------------------
        # GLOBAL FILTERED TOTALS
        # -----------------------------------------------------
        global_held_classes += held_classes_count
        global_pending_attendance_classes += pending_submission_count
        global_submitted_classes += submitted_classes_count

        global_attended_count += attended_count
        global_missed_count += missed_count
        global_excused_count += excused_count

    # ---------------------------------------------------------
    # GLOBAL SUMMARY
    #
    # These are aggregates across the currently filtered Course
    # collection, so they correctly belong to this view.
    # ---------------------------------------------------------
    filtered_company_courses_count = len(all_courses_list)

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

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,

        "all_courses_list": all_courses_list,

        "filtered_company_courses_count": filtered_company_courses_count,
        "total_company_courses_count": total_company_courses_count,
        "active_company_courses_count": active_company_courses_count,
        "total_active_employees": len(global_employee_ids),

        "total_held_classes": global_held_classes,
        "total_pending_attendance_classes": global_pending_attendance_classes,
        "total_submitted_classes": global_submitted_classes,

        "global_attended_count": global_attended_count,
        "global_missed_count": global_missed_count,
        "global_excused_count": global_excused_count,

        "global_attendance_rate": global_attendance_rate,
        "global_missed_rate": global_missed_rate,
        "global_excused_rate": global_excused_rate,

        # Temporary compatibility alias.
        "total_past_classes": global_held_classes,

        "selected_date": selected_date,
        "course_search": course_search,
        "employee_search": employee_search,
    }
    
    return render(
        request,
        "profiles/company_admin/company_admin_all_courses_attendance.html",
        context,
    )



@login_required
def company_admin_course_details(request, course_id=None):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    # ---------------------------------------------------------
    # AVAILABLE COURSES
    # ---------------------------------------------------------
    available_courses = (
        Course.objects
        .filter(company=company)
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
    # - if the company already has courses, redirect to the
    #   first Course in selector order
    # - if the company has no courses, keep course=None and
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
                "profiles:company_admin_course_details",
                course_id=first_course.id,
            )

    # ---------------------------------------------------------
    # DEFAULT EMPTY-STATE VALUES
    #
    # These allow a company admin whose company has no courses
    # to access the complete Course Details interface safely.
    # ---------------------------------------------------------
    enrollments = CourseEnrollment.objects.none()
    sessions = ClassSession.objects.none()

    total_classes = 0
    held_classes_count = 0
    attendance_submitted_classes = 0
    remaining_classes = 0
    delivery_percentage = 0

    past_held_minutes = 0
    past_held_hours = Decimal("0.00")
    past_held_hours_display = format_minutes_duration(0)

    average_attendance = 0
    average_group_assessment_score = None
    average_group_assessment_percentage = 0

    formatted_timetable = []
    bcc_student_emails = ""

    # ---------------------------------------------------------
    # COURSE-SPECIFIC DATA
    # ---------------------------------------------------------
    if course:
        # -----------------------------------------------------
        # ENROLLMENTS
        # -----------------------------------------------------
        enrollments = (
            course.enrollments
            .select_related(
                "student",
                "student__profile",
            )
            .annotate(
                status_order=Case(
                    When(status="active", then=Value(1)),
                    When(status="paused", then=Value(2)),
                    When(status="completed", then=Value(3)),
                    When(status="cancelled", then=Value(4)),
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
        # GENERAL PROGRESS
        #
        # Held = physically delivered, regardless of whether
        # attendance has already been submitted.
        # -----------------------------------------------------
        held_classes = (
            course.class_sessions
            .filter(
                status__in=[
                    ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                    ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
                ]
            )
        )

        total_classes = course.total_sessions
        held_classes_count = held_classes.count()
        attendance_submitted_classes = (
            course.complete_attendance_submitted_sessions
        )
        remaining_classes = course.remaining_sessions
        delivery_percentage = course.delivery_percentage

        # -----------------------------------------------------
        # HOURS DELIVERED
        # -----------------------------------------------------
        past_held_minutes = get_session_minutes(
            held_classes
        )

        past_held_hours = (
            Decimal(past_held_minutes)
            / Decimal("60")
        ).quantize(
            Decimal("0.01")
        )

        past_held_hours_display = (
            format_minutes_duration(
                past_held_minutes
            )
        )

        # -----------------------------------------------------
        # AVERAGE COURSE ATTENDANCE
        #
        # Only sessions whose attendance has been submitted
        # contribute to learner attendance percentages.
        # -----------------------------------------------------
        attendance_percentages = [
            enrollment.attendance_percentage
            for enrollment in enrollments
            if enrollment.complete_attendance_submitted_classes > 0
        ]

        average_attendance = (
            round(
                sum(attendance_percentages)
                / len(attendance_percentages)
            )
            if attendance_percentages else 0
        )

        # -----------------------------------------------------
        # TIMETABLE
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

        # -----------------------------------------------------
        # AVERAGE GROUP SKILL ASSESSMENT
        # -----------------------------------------------------
        enrolled_student_ids = list(
            enrollments.values_list(
                "student_id",
                flat=True,
            )
        )

        skill_assessments = (
            StudentSkillAssessment.objects
            .filter(
                course=course,
                student_id__in=enrolled_student_ids,
            )
            .prefetch_related(
                "subskill_assessments"
            )
        )

        assessed_skill_scores = []

        for skill_assessment in skill_assessments:
            subskills = list(
                skill_assessment
                .subskill_assessments
                .all()
            )

            if not subskills:
                continue

            score = skill_assessment.average_score

            if score is not None:
                assessed_skill_scores.append(
                    score
                )

        average_group_assessment_score = (
            round(
                sum(assessed_skill_scores)
                / len(assessed_skill_scores),
                1,
            )
            if assessed_skill_scores else None
        )

        average_group_assessment_percentage = (
            round(
                (
                    average_group_assessment_score
                    / 10
                )
                * 100
            )
            if average_group_assessment_score is not None
            else 0
        )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,
        "course": course,
        "active_section": "overview",

        # Course selector
        "available_courses": available_courses,

        # Course learners / sessions
        "enrollments": enrollments,
        "sessions": sessions,

        # General Progress
        "total_classes": total_classes,
        "held_classes_count": held_classes_count,
        "attendance_submitted_classes": attendance_submitted_classes,
        "remaining_classes": remaining_classes,
        "delivery_percentage": delivery_percentage,

        # Compatibility with current template
        "past_held_classes": held_classes_count,

        # Hours delivered
        "past_held_minutes": past_held_minutes,
        "past_held_hours": past_held_hours,
        "past_held_hours_display": past_held_hours_display,

        # Attendance / assessment
        "average_attendance": average_attendance,
        "average_group_assessment_score": average_group_assessment_score,
        "average_group_assessment_percentage": average_group_assessment_percentage,

        # Timetable / group email
        "formatted_timetable": formatted_timetable,
        "bcc_student_emails": bcc_student_emails,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_course_details.html",
        context,
    )


@login_required
def company_admin_course_students_list(request, course_id=None):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    # Keep past scheduled/rescheduled sessions aligned with lifecycle status.
    ClassSession.transition_past_sessions()

    # ---------------------------------------------------------
    # AVAILABLE COURSES
    # ---------------------------------------------------------
    available_courses = (
        Course.objects
        .filter(company=company)
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
    # - if the company already has courses, redirect to the
    #   first Course in selector order
    # - if the company has no courses, keep course=None and
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
                "profiles:company_admin_course_students_list",
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
    # These allow a company admin whose company has no courses
    # to access the complete Enrollments interface safely.
    # ---------------------------------------------------------
    all_status_enrollments = CourseEnrollment.objects.none()
    all_status_enrollments_count = 0
    currently_active_enrollments_count = 0

    sessions = ClassSession.objects.none()

    total_classes = 0
    held_classes = 0
    attendance_pending_classes = 0
    attendance_submitted_classes = 0
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
        # ENROLLMENTS
        # -----------------------------------------------------
        active_course_enrollment = (
            CourseEnrollment.objects
            .filter(
                student_id=OuterRef("student_id"),
                status="active",
                course__status="active",
            )
        )

        all_status_enrollments = (
            course.enrollments
            .select_related(
                "student",
                "student__profile",
            )
            .annotate(
                sort_name=Lower(
                    Coalesce(
                        NullIf(
                            "student__first_name",
                            Value(""),
                        ),
                        "student__username",
                    )
                ),
                user_currently_enrolled=Exists(
                    active_course_enrollment
                ),
            )
        )

        all_status_enrollments_count = (
            all_status_enrollments.count()
        )

        currently_active_enrollments_count = (
            all_status_enrollments
            .filter(status="active")
            .count()
        )

        # -----------------------------------------------------
        # SORTING
        # -----------------------------------------------------
        if sort_by == "level":
            all_status_enrollments = (
                all_status_enrollments
                .order_by(
                    "student__profile__current_level",
                    "sort_name",
                    "student__last_name",
                )
            )
        else:
            all_status_enrollments = (
                all_status_enrollments
                .order_by(
                    "sort_name",
                    "student__last_name",
                )
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
        # AVERAGE ATTENDANCE
        #
        # Only enrollments with submitted attendance contribute.
        # -----------------------------------------------------
        attendance_percentages = [
            enrollment.attendance_percentage
            for enrollment in all_status_enrollments
            if enrollment.complete_attendance_submitted_classes > 0
        ]

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
        formatted_timetable = (
            build_formatted_timetable(
                course
            )
        )

        # -----------------------------------------------------
        # EMAIL ALL STUDENTS
        # -----------------------------------------------------
        student_emails = [
            enrollment.student.email
            for enrollment in all_status_enrollments
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
        "company": company,
        "course": course,
        "active_section": "enrollments",

        # Course selector
        "available_courses": available_courses,

        # Enrollments
        "all_status_enrollments": all_status_enrollments,
        "all_status_enrollments_count": all_status_enrollments_count,
        "currently_active_enrollments_count": currently_active_enrollments_count,

        # Sessions / sorting
        "sessions": sessions,
        "sort_by": sort_by,

        # General Progress
        "total_classes": total_classes,
        "held_classes": held_classes,
        "attendance_pending_classes": attendance_pending_classes,
        "attendance_submitted_classes": attendance_submitted_classes,
        "remaining_classes": remaining_classes,
        "delivery_percentage": delivery_percentage,

        # Attendance / timetable / email
        "average_attendance": average_attendance,
        "formatted_timetable": formatted_timetable,
        "bcc_student_emails": bcc_student_emails,

        # Form/display choices
        "level_choices": UserProfile.LEVEL_CHOICES,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_course_students_list.html",
        context,
    )



@login_required
def company_admin_course_attendance(request, course_id=None):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    # ---------------------------------------------------------
    # AVAILABLE COURSES
    # ---------------------------------------------------------
    available_courses = (
        Course.objects
        .filter(company=company)
        .annotate(
            status_order=Case(
                When(status="active", then=Value(1)),
                When(status="confirmed", then=Value(2)),
                When(status="paused", then=Value(3)),
                When(status="completed", then=Value(4)),
                When(status="cancelled", then=Value(5)),
                default=Value(99),
                output_field=IntegerField(),
            ),
            enrollment_count=Count("enrollments", distinct=True),
        )
        .select_related(
            "course_type",
            "company",
            "teacher",
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
    # - if the company already has courses, redirect to the
    #   first Course in selector order
    # - if the company has no courses, keep course=None and
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
                "profiles:company_admin_course_attendance",
                course_id=first_course.id,
            )

    # ---------------------------------------------------------
    # DEFAULT EMPTY-STATE VALUES
    #
    # These allow a company admin whose company has no courses
    # to access the complete Course Attendance interface safely.
    # ---------------------------------------------------------
    enrollments = CourseEnrollment.objects.none()
    submitted_class_sessions = ClassSession.objects.none()

    total_classes_held = 0
    held_attendance_pending_classes = 0
    attendance_submitted_classes = 0
    attendance_submission_percentage = 0
    average_attendance = 0

    # ---------------------------------------------------------
    # COURSE-SPECIFIC DATA
    # ---------------------------------------------------------
    if course:
        # -----------------------------------------------------
        # SYNCHRONIZE SELECTED COURSE
        #
        # Keep stale scheduled/rescheduled sessions aligned
        # with the lifecycle without scanning unrelated Courses.
        #
        # The final session transition may also complete the
        # Course and its active enrollments, so refresh the
        # Course afterwards.
        # -----------------------------------------------------
        ClassSession.transition_past_sessions(
            course=course
        )

        course.refresh_from_db()

        # -----------------------------------------------------
        # ENROLLMENTS
        #
        # Active and completed enrollments remain relevant to
        # the Course attendance overview.
        # -----------------------------------------------------
        enrollments = (
            course.enrollments
            .filter(
                status__in=[
                    CourseEnrollment.STATUS_ACTIVE,
                    CourseEnrollment.STATUS_COMPLETED,
                ]
            )
            .select_related(
                "student",
                "student__profile",
            )
        )

        # -----------------------------------------------------
        # SUBMITTED ATTENDANCE SESSIONS
        #
        # Only ClassSessions whose attendance workflow is
        # complete belong in this list.
        # -----------------------------------------------------
        submitted_class_sessions = (
            course.class_sessions
            .filter(
                status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            )
            .select_related(
                "course",
                "course__course_type",
                "course__teacher",
            )
            .prefetch_related(
                "attendance_records",
                "attendance_records__student",
                "attendance_records__student__profile",
            )
            .order_by("-start_time")
        )

        # -----------------------------------------------------
        # SESSION ATTENDANCE DISPLAY DATA
        #
        # ClassSession owns lesson lifecycle state.
        # Attendance owns the canonical genuine outcome
        # statuses.
        #
        # These values are attached only to package each
        # session for this particular page/table. They are not
        # canonical Course or CourseEnrollment calculations.
        # -----------------------------------------------------
        for class_session in submitted_class_sessions:
            attendance_records = [
                attendance
                for attendance in class_session.attendance_records.all()
                if attendance.status in Attendance.FINAL_OUTCOME_STATUSES
            ]

            attended_count = sum(
                attendance.status == Attendance.STATUS_ATTENDED
                for attendance in attendance_records
            )

            missed_count = sum(
                attendance.status == Attendance.STATUS_MISSED
                for attendance in attendance_records
            )

            excused_count = sum(
                attendance.status == Attendance.STATUS_EXCUSED
                for attendance in attendance_records
            )

            attendance_total = len(attendance_records)

            class_session.attended_count = attended_count
            class_session.missed_count = missed_count
            class_session.excused_count = excused_count
            class_session.attendance_total = attendance_total

            # Temporary display compatibility if the template
            # still expects registered_count.
            class_session.registered_count = attendance_total

            class_session.attendance_percentage = (
                round(
                    attended_count
                    / attendance_total
                    * 100
                )
                if attendance_total else 0
            )

            class_session.employee_search_text = " ".join(
                f"{attendance.student.get_full_name()} "
                f"{attendance.student.username} "
                f"{attendance.student.email}"
                for attendance in attendance_records
            )

        # -----------------------------------------------------
        # COURSE ATTENDANCE LIFECYCLE TOTALS
        #
        # Course owns all whole-course delivery/session counts.
        # -----------------------------------------------------
        total_classes_held = course.total_held_sessions

        held_attendance_pending_classes = (
            course.held_attendance_pending_sessions
        )

        attendance_submitted_classes = (
            course.complete_attendance_submitted_sessions
        )

        # -----------------------------------------------------
        # ATTENDANCE SUBMISSION %
        #
        # This is a page-specific ratio:
        # submitted attendance workflows / all lessons held.
        # -----------------------------------------------------
        attendance_submission_percentage = (
            round(
                attendance_submitted_classes
                / total_classes_held
                * 100
            )
            if total_classes_held else 0
        )

        # -----------------------------------------------------
        # COURSE AVERAGE ATTENDANCE
        #
        # CourseEnrollment owns each learner's submitted-
        # attendance population and attendance percentage.
        #
        # Retrieve attendance_metrics once per enrollment so
        # the view does not independently recount or
        # recalculate learner data.
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

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,
        "course": course,
        "active_section": "attendance",

        # Course selector
        "available_courses": available_courses,

        # Submitted attendance sessions
        "submitted_class_sessions": submitted_class_sessions,

        # Attendance lifecycle
        "total_classes_held": total_classes_held,
        "held_attendance_pending_classes": held_attendance_pending_classes,
        "attendance_submitted_classes": attendance_submitted_classes,
        "attendance_submission_percentage": attendance_submission_percentage,

        # Course attendance
        "average_attendance": average_attendance,
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

    if not company:
        return redirect("home")

    # ---------------------------------------------------------
    # CLASS SESSION
    #
    # This page represents FINAL submitted attendance only.
    #
    # ClassSession owns the lesson lifecycle, so only a session
    # explicitly marked complete_attendance_submitted belongs here.
    # ---------------------------------------------------------
    class_session = get_object_or_404(
        ClassSession.objects.select_related(
            "course",
            "course__course_type",
            "course__teacher",
        ),
        id=class_session_id,
        course__company=company,
        status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
    )

    # ---------------------------------------------------------
    # FINAL ATTENDANCE OUTCOMES
    #
    # Attendance owns the canonical definition of a genuine
    # finalized learner outcome:
    #
    # - attended
    # - missed
    # - excused
    #
    # pending and enrollment_paused are therefore excluded.
    # ---------------------------------------------------------
    attendances = (
        class_session.attendance_records
        .filter(
            status__in=Attendance.FINAL_OUTCOME_STATUSES
        )
        .select_related(
            "student",
            "student__profile",
        )
        .order_by(
            "student__first_name",
            "student__last_name",
            "student__username",
        )
    )

    # ---------------------------------------------------------
    # ATTENDANCE METRICS
    #
    # ClassSession currently does not expose group-level attendance
    # counts/rate, so calculate them once here from the canonical
    # finalized Attendance population.
    # ---------------------------------------------------------
    attendance_metrics = attendances.aggregate(
        total_count=Count("id"),
        attended_count=Count(
            "id",
            filter=Q(status=Attendance.STATUS_ATTENDED),
        ),
        missed_count=Count(
            "id",
            filter=Q(status=Attendance.STATUS_MISSED),
        ),
        excused_count=Count(
            "id",
            filter=Q(status=Attendance.STATUS_EXCUSED),
        ),
    )

    total_count = attendance_metrics["total_count"] or 0
    attended_count = attendance_metrics["attended_count"] or 0
    missed_count = attendance_metrics["missed_count"] or 0
    excused_count = attendance_metrics["excused_count"] or 0

    attendance_percentage = (
        round(attended_count / total_count * 100)
        if total_count else 0
    )    

    total_count = attendance_metrics["total_count"] or 0
    attended_count = attendance_metrics["attended_count"] or 0
    missed_count = attendance_metrics["missed_count"] or 0
    excused_count = attendance_metrics["excused_count"] or 0

    attendance_percentage = (
        round(attended_count / total_count * 100)
        if total_count else 0
    )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,
        "course": class_session.course,
        "class_session": class_session,
        "attendances": attendances,

        "total_count": total_count,
        "attended_count": attended_count,
        "missed_count": missed_count,
        "excused_count": excused_count,
        "attendance_percentage": attendance_percentage,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_course_attendance_detail.html",
        context,
    )



@login_required
def company_admin_student_detail(request, student_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    # ---------------------------------------------------------
    # EMPLOYEE
    # ---------------------------------------------------------
    student = get_object_or_404(
        User.objects.select_related("profile"),
        id=student_id,
        profile__company=company,
    )

    student_profile = student.profile

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # ALL ENROLLMENTS
    # ---------------------------------------------------------
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects
        .filter(
            student=student,
            course__company=company,
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
        enrollment = enrollments.first()

    # ---------------------------------------------------------
    # NO ENROLLMENTS
    #
    # Keep the normal employee Overview page accessible and
    # provide the same structural context with empty/default
    # values.
    # ---------------------------------------------------------
    if not enrollment:
        context = {
            "profile": profile,
            "company": company,
            "student": student,
            "student_profile": student_profile,
            "user_currently_enrolled": user_currently_enrolled,

            "enrollments": enrollments,
            "enrollment": None,
            "course": None,
            "level_choices": UserProfile.LEVEL_CHOICES,

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

            # General Progress
            "held_classes": 0,
            "attendance_pending_classes": 0,
            "attendance_submitted_classes": 0,
            "remaining_classes": 0,
            "total_classes": 0,
            "delivery_percentage": 0,

            # Assigned hours / delivery
            "total_hours": Decimal("0"),
            "total_hours_display": format_hours_duration(Decimal("0")),
            "held_hours": Decimal("0"),
            "held_hours_display": format_hours_duration(Decimal("0")),
            "remaining_hours": Decimal("0"),
            "remaining_hours_display": format_hours_duration(Decimal("0")),

            # Temporary compatibility aliases
            "completed_classes": 0,
            "completed_hours": Decimal("0"),
            "completed_hours_display": format_minutes_duration(0),

            # Skills
            "overall_average_score": None,
            "overall_skill_chart_data": {
                "labels": [],
                "datasets": [],
            },
            "chart_data": None,
            "skill_note_display": [],
        }

        return render(
            request,
            "profiles/company_admin/company_admin_student_detail.html",
            context,
        )

    # ---------------------------------------------------------
    # SELECTED COURSE
    # ---------------------------------------------------------
    course = enrollment.course

    # Keep lifecycle synchronization scoped to the selected Course.
    # The final transition may also complete the Course and its active
    # enrollments, so refresh the selected objects and enrollment flag.
    ClassSession.transition_past_sessions(course=course)
    course.refresh_from_db()
    enrollment.refresh_from_db()

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # SKILLS CHART
    # ---------------------------------------------------------
    chart_data = build_skill_progress_chart_data(
        student=student,
        course=course,
    )

    # ---------------------------------------------------------
    # FINAL ATTENDANCE
    #
    # CourseEnrollment owns the canonical submitted-attendance
    # population and all derived attendance metrics.
    # ---------------------------------------------------------
    attendances = enrollment.submitted_attendances
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
    # ---------------------------------------------------------
    submitted_minutes = enrollment.submitted_minutes
    submitted_hours = enrollment.submitted_hours
    submitted_hours_display = format_minutes_duration(submitted_minutes)

    attended_minutes = enrollment.attended_minutes
    attended_hours = enrollment.attended_hours
    attended_hours_display = format_minutes_duration(attended_minutes)

    # ---------------------------------------------------------
    # LEARNER GENERAL PROGRESS
    #
    # Held = attendance pending + attendance submitted.
    # ---------------------------------------------------------
    total_classes = enrollment.total_assigned_classes
    held_classes = enrollment.total_held_classes
    attendance_pending_classes = enrollment.held_attendance_pending_classes
    attendance_submitted_classes = enrollment.complete_attendance_submitted_classes
    remaining_classes = enrollment.remaining_classes
    delivery_percentage = enrollment.delivery_percentage

    # ---------------------------------------------------------
    # COURSE-LEVEL DELIVERY
    # ---------------------------------------------------------
    held_course_minutes = course.held_minutes
    held_course_hours_numeric = course.held_hours
    held_course_hours_display = format_minutes_duration(
        held_course_minutes
    )

    course_total_hours = course.total_hours or Decimal("0")
    course_total_minutes = course.total_minutes
    course_total_hours_display = format_minutes_duration(
        course_total_minutes
    )

    # ---------------------------------------------------------
    # ASSIGNED DELIVERY HOURS
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

    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]

    overall_skill_chart_data = (
        build_overall_skill_progress_chart_data(
            student=student,
            course=course,
        )
    )

    # ---------------------------------------------------------
    # TIMETABLE
    # ---------------------------------------------------------
    formatted_timetable = build_formatted_timetable(
        course
    )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,

        "student": student,
        "student_profile": student_profile,
        "user_currently_enrolled": user_currently_enrolled,

        "enrollments": enrollments,
        "enrollment": enrollment,
        "course": course,
        "level_choices": UserProfile.LEVEL_CHOICES,
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

        # Learner General Progress
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

        # IMPORTANT:
        # Existing attendance template expects completed_hours_display.
        # It must now mean submitted-attendance hours, NOT held hours.
        "completed_hours": submitted_hours,
        "completed_hours_display": submitted_hours_display,

        # Skills
        "chart_data": chart_data,
        "skill_note_display": skill_note_display,
        "overall_skill_chart_data": overall_skill_chart_data,
        "overall_average_score": overall_average_score,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_student_detail.html",
        context,
    )


@login_required
def company_admin_student_attendance_record(request, student_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    held_statuses = [
        ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
        ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
    ]

    # ---------------------------------------------------------
    # EMPLOYEE
    # ---------------------------------------------------------
    student = get_object_or_404(
        User.objects.select_related("profile"),
        id=student_id,
        profile__company=company,
    )

    student_profile = student.profile

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # ENROLLMENTS
    # ---------------------------------------------------------
    enrollments = order_enrollments_by_course_status(
        CourseEnrollment.objects
        .filter(
            student=student,
            course__company=company,
        )
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
    )

    selected_course_id = request.GET.get("course")

    if selected_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )
    else:
        enrollment = enrollments.first()

    # ---------------------------------------------------------
    # NO ENROLLMENTS
    # ---------------------------------------------------------
    if not enrollment:
        context = {
            "profile": profile,
            "company": company,
            "student": student,
            "student_profile": student_profile,
            "user_currently_enrolled": user_currently_enrolled,
            "enrollments": enrollments,
            "enrollment": None,
            "course": None,
            "level_choices": UserProfile.LEVEL_CHOICES,

            # Attendance
            "attended_count": 0,
            "missed_count": 0,
            "excused_count": 0,
            "total_absences": 0,
            "total_attendance_records": 0,
            "attendance_percentage": 0,

            # Attendance hours
            "attended_minutes": 0,
            "attended_hours": Decimal("0"),
            "attended_hours_display": format_minutes_duration(0),
            "submitted_minutes": 0,
            "submitted_hours": Decimal("0"),
            "submitted_hours_display": format_minutes_duration(0),

            # Delivery
            "held_classes": 0,
            "attendance_pending_classes": 0,
            "attendance_submitted_classes": 0,
            "course_held_classes": 0,
            "course_attendance_pending_classes": 0,
            "course_attendance_submitted_classes": 0,
            "remaining_classes": 0,
            "total_classes": 0,
            "delivery_percentage": 0,

            # Delivery hours
            "held_minutes": 0,
            "held_hours": Decimal("0"),
            "held_hours_display": format_minutes_duration(0),

            # Late enrollment
            "lessons_before_enrollment": 0,
            "show_enrollment_context": False,

            # History
            "recent_attendance": [],
            "recent_absences": [],

            # Temporary compatibility aliases
            "completed_classes": 0,
            "course_completed_classes": 0,
            "completed_hours_display": format_minutes_duration(0),
        }

        return render(
            request,
            "profiles/company_admin/company_admin_student_attendance_record.html",
            context,
        )

    course = enrollment.course

    # Keep lifecycle synchronization scoped to the selected Course.
    # The final transition may also complete the Course and its active
    # enrollments, so refresh the selected objects and enrollment flag.
    ClassSession.transition_past_sessions(course=course)
    course.refresh_from_db()
    enrollment.refresh_from_db()

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # SUBMITTED ATTENDANCE RECORDS
    #
    # CourseEnrollment owns the canonical submitted-attendance
    # population and all derived attendance metrics.
    # ---------------------------------------------------------
    attendances = enrollment.submitted_attendances
    attendance_metrics = enrollment.attendance_metrics

    recent_absences = attendances.filter(
        status__in=[
            Attendance.STATUS_MISSED,
            Attendance.STATUS_EXCUSED,
        ]
    )

    total_attendance_records = attendance_metrics[
        "total_submitted_attendance_records"
    ]
    attended_count = attendance_metrics["attended_classes"]
    missed_count = attendance_metrics["missed_classes"]
    excused_count = attendance_metrics["excused_classes"]
    total_absences = attendance_metrics["total_absences"]
    attendance_percentage = attendance_metrics["attendance_percentage"]

    # ---------------------------------------------------------
    # ATTENDANCE HOURS
    # ---------------------------------------------------------
    submitted_minutes = enrollment.submitted_minutes
    submitted_hours = enrollment.submitted_hours
    submitted_hours_display = format_minutes_duration(submitted_minutes)

    attended_minutes = enrollment.attended_minutes
    attended_hours = enrollment.attended_hours
    attended_hours_display = format_minutes_duration(attended_minutes)

    # ---------------------------------------------------------
    # EMPLOYEE-SPECIFIC GENERAL PROGRESS
    #
    # Held = attendance pending + attendance submitted.
    # ---------------------------------------------------------
    total_classes = enrollment.total_assigned_classes
    held_classes = enrollment.total_held_classes
    attendance_pending_classes = enrollment.held_attendance_pending_classes
    attendance_submitted_classes = enrollment.complete_attendance_submitted_classes
    remaining_classes = enrollment.remaining_classes
    delivery_percentage = enrollment.delivery_percentage

    # ---------------------------------------------------------
    # COURSE-WIDE DELIVERY
    # ---------------------------------------------------------
    course_held_classes = course.total_held_sessions
    course_attendance_pending_classes = course.held_attendance_pending_sessions
    course_attendance_submitted_classes = course.complete_attendance_submitted_sessions

    # ---------------------------------------------------------
    # LESSONS HELD BEFORE EMPLOYEE ENROLLED
    # ---------------------------------------------------------
    lessons_before_enrollment = (
        course.class_sessions
        .filter(
            status__in=held_statuses,
            end_time__lt=enrollment.enrolled_at,
        )
        .count()
        if enrollment.enrolled_at else 0
    )

    show_enrollment_context = lessons_before_enrollment > 0

    # ---------------------------------------------------------
    # HOURS DELIVERED TO THIS EMPLOYEE
    #
    # CourseEnrollment owns learner-level held delivery.
    # This remains separate from submitted attendance hours.
    # ---------------------------------------------------------
    held_minutes = enrollment.held_minutes
    held_hours = enrollment.held_hours
    held_hours_display = format_minutes_duration(held_minutes)

    # ---------------------------------------------------------
    # FULL ATTENDANCE HISTORY
    # ---------------------------------------------------------
    recent_attendance = attendances

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,

        "student": student,
        "student_profile": student_profile,
        "user_currently_enrolled": user_currently_enrolled,

        "enrollments": enrollments,
        "enrollment": enrollment,
        "course": course,
        "level_choices": UserProfile.LEVEL_CHOICES,

        # Attendance
        "attended_count": attended_count,
        "missed_count": missed_count,
        "excused_count": excused_count,
        "total_absences": total_absences,
        "total_attendance_records": total_attendance_records,
        "attendance_percentage": attendance_percentage,

        # Attendance hours
        "attended_minutes": attended_minutes,
        "attended_hours": attended_hours,
        "attended_hours_display": attended_hours_display,
        "submitted_minutes": submitted_minutes,
        "submitted_hours": submitted_hours,
        "submitted_hours_display": submitted_hours_display,

        # Employee delivery
        "held_classes": held_classes,
        "attendance_pending_classes": attendance_pending_classes,
        "attendance_submitted_classes": attendance_submitted_classes,
        "remaining_classes": remaining_classes,
        "total_classes": total_classes,
        "delivery_percentage": delivery_percentage,

        # Course-wide delivery
        "course_held_classes": course_held_classes,
        "course_attendance_pending_classes": course_attendance_pending_classes,
        "course_attendance_submitted_classes": course_attendance_submitted_classes,

        # Delivery hours
        "held_minutes": held_minutes,
        "held_hours": held_hours,
        "held_hours_display": held_hours_display,

        # Late enrollment
        "lessons_before_enrollment": lessons_before_enrollment,
        "show_enrollment_context": show_enrollment_context,

        # History
        "recent_attendance": recent_attendance,
        "recent_absences": recent_absences,

        # Temporary compatibility aliases
        "completed_classes": attendance_submitted_classes,
        "course_completed_classes": course_attendance_submitted_classes,

        # Existing templates using completed_hours_display should
        # receive submitted attendance hours, NOT all held hours.
        "completed_hours_display": submitted_hours_display,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_student_attendance_record.html",
        context,
    )



@login_required
def company_admin_student_skills_overview(request, student_id):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    # ---------------------------------------------------------
    # GET EMPLOYEE
    # ---------------------------------------------------------
    student = get_object_or_404(
        User.objects.select_related("profile"),
        id=student_id,
        profile__company=company,
    )

    student_profile = student.profile

    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
        course__status="active",
    ).exists()

    # ---------------------------------------------------------
    # GET ALL ENROLLMENTS FOR THIS EMPLOYEE
    # HElper in profiles/utils/enrollments.py
    # Historical courses remain accessible.
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
            course__company=company,
        )
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
    )

    # ---------------------------------------------------------
    # GET SELECTED COURSE FROM URL
    # Example:
    # /profiles/company-admin/employees/3/skills/?course=9
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")

    # ---------------------------------------------------------
    # DETERMINE SELECTED ENROLLMENT
    # ---------------------------------------------------------
    if selected_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )
    else:
        enrollment = enrollments.first()


    # ---------------------------------------------------------
    # NO ENROLLMENTS
    # ---------------------------------------------------------
    if not enrollment:
        _, skills = build_student_skill_cards(
            student=student,
            course=None,
            build_skill_note_display=build_skill_note_display,
        )
        context = {
            "profile": profile,
            "company": company,
            "student": student,
            "student_profile": student_profile,
            "user_currently_enrolled":
                user_currently_enrolled,
            "enrollments": enrollments,
            "enrollment": None,
            "course": None,
            "skills": skills,
            "academic_profile": getattr(
                student,
                "academic_profile",
                None,
            ),
            "chart_data": {
                "labels": [],
                "datasets": [],
            },
            "skill_note_display": [],
        }

        return render(
            request,
            "profiles/company_admin/"
            "company_admin_student_skills_overview.html",
            context,
        )

    # ---------------------------------------------------------
    # SELECTED COURSE
    # ---------------------------------------------------------
    course = enrollment.course

    # ---------------------------------------------------------
    # SHARED SKILL CARD DATA
    # Helper in FILE profiles/utils/skills.py
    # Helper shared w.all profile roles
    # Builds:
    # - all four skill cards
    # - all canonical subskills
    # - assessed / pending state
    # - assessed subskill count
    # - total subskill count
    # - current skill score
    # - grouped assessment categories
    #
    # The helper is explicitly scoped to:
    # student + selected course
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
    # DISPLAY-FRIENDLY NOTES
    # Only existing assessments can have notes.
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
    # CHART DATA
    #
    # Course status does not matter.
    # No assessments yet simply means an empty chart.
    # ---------------------------------------------------------
    chart_data = build_skill_progress_chart_data(
        student=student,
        course=course,
    )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,
        "student": student,
        "student_profile": student_profile,
        "user_currently_enrolled":
            user_currently_enrolled,
        # Full enrollment list for selector
        "enrollments": enrollments,
        # Selected enrollment/course
        "enrollment": enrollment,
        "course": course,
        # Shared skill-card structure
        "skills": skills,
        # Academic profile
        "academic_profile": academic_profile,
        # Chart
        "chart_data": chart_data,
        # Notes
        "skill_note_display":
            skill_note_display,
    }

    return render(
        request,
        "profiles/company_admin/"
        "company_admin_student_skills_overview.html",
        context,
    )



@login_required
def company_admin_student_needs_analysis(request, student_id):
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    # ---------------------------------------------------------
    # STUDENT / COMPANY OWNERSHIP
    # ---------------------------------------------------------
    student = get_object_or_404(
        User.objects.select_related("profile"),
        id=student_id,
        profile__company=company,
    )

    student_profile = student.profile
    is_self = student.pk == request.user.pk

    # ---------------------------------------------------------
    # AVAILABLE ENROLLMENTS
    #
    # Self: own enrollments, including personal Courses.
    # Employee: only Courses belonging to this company.
    # Historical enrollments remain accessible.
    # ---------------------------------------------------------
    enrollments = CourseEnrollment.objects.filter(student=student)

    if not is_self:
        enrollments = enrollments.filter(course__company=company)

    enrollments = (
        enrollments
        .select_related("course", "course__course_type", "course__teacher")
        .order_by("course__name")
    )

    # ---------------------------------------------------------
    # SELECTED COURSE / ENROLLMENT
    # ---------------------------------------------------------
    course_id = request.GET.get("course")

    if course_id:
        enrollment = get_object_or_404(enrollments, course_id=course_id)
    else:
        enrollment = enrollments.first()

    course = enrollment.course if enrollment else None

    # ---------------------------------------------------------
    # CURRENT ENROLLMENT STATUS
    #
    # Used by the shared student details header.
    # ---------------------------------------------------------
    active_enrollments = CourseEnrollment.objects.filter(
        student=student,
        status=CourseEnrollment.STATUS_ACTIVE,
        course__status="active",
    )

    if not is_self:
        active_enrollments = active_enrollments.filter(
            course__company=company,
        )

    user_currently_enrolled = active_enrollments.exists()

    # =========================================================
    # COMPANY ADMIN VIEWING AN EMPLOYEE
    #
    # STATUS ONLY — NO QUESTIONNAIRE ACCESS
    # =========================================================
    if not is_self:

        # Company Admins cannot submit or modify an employee's
        # questionnaire, including through manually crafted POSTs.
        if request.method != "GET":
            return HttpResponseForbidden(
                "You cannot modify another learner's Learning Needs."
            )

        needs_status = None

        if enrollment:
            # Only determine whether the questionnaire was submitted.
            # REVIEWED also means the learner has submitted it.
            #
            # No questionnaire object, answers, free-text responses
            # or confidence ratings are retrieved.
            needs_submitted = StudentNeedsAnalysis.objects.filter(
                enrollment_id=enrollment.id,
                status__in=[
                    StudentNeedsAnalysis.Status.SUBMITTED,
                    StudentNeedsAnalysis.Status.REVIEWED,
                ],
            ).exists()

            needs_status = (
                "submitted"
                if needs_submitted
                else "pending"
            )

        context = {
            "profile": profile,
            "company": company,
            "student": student,
            "student_profile": student_profile,
            "course": course,
            "enrollment": enrollment,
            "enrollments": enrollments,
            "is_self": False,
            "needs_status": needs_status,
            "user_currently_enrolled": user_currently_enrolled,
            "active_section": "needs_analysis",
        }

        return render(
            request,
            "profiles/company_admin/company_admin_student_needs_analysis.html",
            context,
        )

    # =========================================================
    # COMPANY ADMIN VIEWING THEIR OWN LEARNER RECORD
    #
    # Full access to their own questionnaire.
    # Existing learner submission workflow preserved.
    # =========================================================

    # ---------------------------------------------------------
    # DEFAULT EMPTY-STATE VALUES
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
        needs_analysis, _ = StudentNeedsAnalysis.objects.get_or_create(
            enrollment=enrollment,
        )

        # -----------------------------------------------------
        # EDIT PERMISSION
        #
        # Own record + active enrollment + pending questionnaire.
        # Submitted/reviewed responses remain read-only.
        # -----------------------------------------------------
        can_edit = (
            enrollment.status == CourseEnrollment.STATUS_ACTIVE
            and needs_analysis.status == StudentNeedsAnalysis.Status.PENDING
        )

        # -----------------------------------------------------
        # FORM INITIAL DATA
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
            if not can_edit:
                return HttpResponseForbidden(
                    "This Learning Needs questionnaire cannot be edited."
                )

            form = StudentNeedsAnalysisForm(request.POST)

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

                needs_analysis.status = StudentNeedsAnalysis.Status.SUBMITTED
                needs_analysis.submitted_at = timezone.now()

                needs_analysis.save()

                return redirect(
                    f"{request.path}?course={course.id}"
                )

        else:
            form = StudentNeedsAnalysisForm(initial=form_initial)

        # -----------------------------------------------------
        # HUMAN-READABLE DISPLAY VALUES — OWN RECORD ONLY
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
    # ---------------------------------------------------------
    elif (
        request.method == "POST"
        and request.POST.get("action") == "submit_needs_analysis"
    ):
        return redirect(request.path)

    # ---------------------------------------------------------
    # OWN LEARNER RECORD CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,
        "student": student,
        "student_profile": student_profile,

        "course": course,
        "enrollment": enrollment,
        "enrollments": enrollments,

        "needs_analysis": needs_analysis,
        "form": form,

        "is_self": True,
        "can_edit": can_edit,
        "can_review": False,

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

        "user_currently_enrolled": user_currently_enrolled,
        "active_section": "needs_analysis",
    }

    return render(
        request,
        "profiles/company_admin/company_admin_student_needs_analysis.html",
        context,
    )


@login_required
def company_admin_student_teacher_notes(request, student_id):
    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")

    # ---------------------------------------------------------
    # GET EMPLOYEE
    # ---------------------------------------------------------
    student = get_object_or_404(
        User.objects.select_related("profile"),
        id=student_id,
        profile__company=company,
    )

    student_profile = student.profile

    # ---------------------------------------------------------
    # CURRENT ENROLLMENT STATUS
    #
    # Independent of the selected Course.
    # Used by the shared student details header.
    # ---------------------------------------------------------
    user_currently_enrolled = CourseEnrollment.objects.filter(
        student=student,
        status="active",
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
        .filter(
            student=student,
            course__company=company,
        )
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
    # /profiles/company-admin/employees/3/assessment/?course=9
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")

    # ---------------------------------------------------------
    # DETERMINE SELECTED ENROLLMENT
    # ---------------------------------------------------------
    if selected_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )
    else:
        enrollment = enrollments.first()

    # ---------------------------------------------------------
    # NO ENROLLMENTS
    #
    # Keep the normal Assessment page accessible with empty
    # data when the employee has never been enrolled.
    # ---------------------------------------------------------
    if not enrollment:
        context = {
            "profile": profile,
            "company": company,

            "student": student,
            "student_profile": student_profile,
            "user_currently_enrolled": user_currently_enrolled,

            # Course selector
            "enrollments": enrollments,

            # Temporary compatibility alias
            "active_enrollments": enrollments,

            # No selected enrollment / course
            "enrollment": None,
            "course": None,

            # Assessment
            "skills": [],
            "skill_note_display": [],
        }

        return render(
            request,
            "profiles/company_admin/company_admin_student_teacher_notes.html",
            context,
        )

    # ---------------------------------------------------------
    # SELECTED COURSE
    # ---------------------------------------------------------
    course = enrollment.course

    # ---------------------------------------------------------
    # SKILL ASSESSMENTS
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
    # DISPLAY-FRIENDLY SKILL NOTES
    # ---------------------------------------------------------
    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]

    # ---------------------------------------------------------
    # SKILLS
    #
    # Original behaviour retained.
    # ---------------------------------------------------------
    skills = []

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,

        "student": student,
        "student_profile": student_profile,
        "user_currently_enrolled": user_currently_enrolled,

        # Course selector
        "enrollments": enrollments,

        # Temporary compatibility alias
        "active_enrollments": enrollments,

        # Selected enrollment / course
        "enrollment": enrollment,
        "course": course,

        # Assessment
        "skills": skills,
        "skill_note_display": skill_note_display,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_student_teacher_notes.html",
        context,
    )



@login_required
def company_admin_classes_list(request):
    '''
    Displays list of classes (past & upcoming)
     of all company courses status=active
    '''
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

        # ---------------------------------------------------------
        # UI GROUP
        #
        # Upcoming:
        # scheduled/rescheduled sessions still in the future.
        #
        # Past:
        # class held, regardless of whether attendance has
        # already been submitted.
        # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # DATE FILTERS
        # ---------------------------------------------------------
        session.is_today = session_date == today

        session.is_this_week = (
            start_of_week <= session_date <= end_of_week
        )

        session.is_this_month = (
            session_date.year == today.year
            and session_date.month == today.month
        )
        # ---------------------------------------------------------
        # SUBMISSION STATUS 
        # ---------------------------------------------------------
        session.attendance_submitted = (
            session.status == ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
        )

        # ---------------------------------------------------------
        # COUNTS
        # ---------------------------------------------------------
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
        "profile": profile,
        "company": company,
        "sessions": sessions,
        "now": now,
        "class_filter_counts": class_filter_counts,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_classes_list.html",
        context,
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

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN or not profile.company:
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
            course__company=profile.company,
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
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

    bank_holidays = BankHoliday.objects.filter(is_active=True).order_by("start_date")

    # FullCalendar visible range.
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

        teacher = session.course.teacher
        teacher_name = (
            teacher.get_full_name() or teacher.email
            if teacher
            else "Not assigned"
        )

        # Temporal state is separate from lifecycle state.
        is_past = (
            session.end_time <= now
            if session.end_time
            else session.start_time < now
        )

        # Historical held sessions remain visible but are not joinable.
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
            "extendedProps": {"type": "bank_holiday"},
        }

        if holiday.end_date:
            event["end"] = (holiday.end_date + timedelta(days=1)).isoformat()

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

    # ---------------------------------------------------------
    # SORT OPTION
    # ---------------------------------------------------------
    sort_by = request.GET.get("sort", "status")

    if sort_by not in ["status", "name", "level"]:
        sort_by = "status"


    # ---------------------------------------------------------
    # ACTIVE ENROLLED COMPANY ADMINS
    #
    # A Company Admin remains a Company Admin, but if they also
    # have an active CourseEnrollment in one of their company's
    # courses, they are also treated as a training participant.
    # ---------------------------------------------------------
    active_company_admin_ids = (
        CourseEnrollment.objects
        .filter(
            course__company=company,
            student__profile__company=company,
            student__profile__role=UserProfile.ROLE_COMPANY_ADMIN,
            status=CourseEnrollment.STATUS_ACTIVE,
        )
        .values_list("student_id", flat=True)
    )

    # ---------------------------------------------------------
    # ALL COMPANY EMPLOYEES
    #
    # Employees are now retrieved independently from their
    # course enrollments, so they remain visible even when
    # courses are completed / paused / cancelled.
    # ---------------------------------------------------------
    employee_profiles = (
        UserProfile.objects
        .filter(company=company)
        .filter(
            Q(role=UserProfile.ROLE_EMPLOYEE)
            | Q(
                role=UserProfile.ROLE_COMPANY_ADMIN,
                user_id__in=active_company_admin_ids,
            )
        )
        .select_related("user")
        .order_by(
            "user__first_name",
            "user__last_name",
            "user__email",
        )
)
    # ---------------------------------------------------------
    # ALL COMPANY ENROLLMENTS
    # ---------------------------------------------------------
    enrollments = (
        CourseEnrollment.objects
        .filter(
            course__company=company,
            student__profile__company=company,
        )
        .filter(
            Q(student__profile__role=UserProfile.ROLE_EMPLOYEE)
            | Q(student_id__in=active_company_admin_ids)
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

    # ---------------------------------------------------------
    # GROUP ENROLLMENTS BY EMPLOYEE
    # ---------------------------------------------------------
    enrollments_by_student = {}

    for enrollment in enrollments:
        student_id = enrollment.student_id

        if student_id not in enrollments_by_student:
            enrollments_by_student[student_id] = []

        enrollments_by_student[student_id].append(enrollment)

    # ---------------------------------------------------------
    # ENROLLMENT STATUS PRIORITY
    #
    # If an employee belongs to several courses, show the
    # highest-priority current enrollment state.
    # ---------------------------------------------------------
    status_order = {
        "active": 1,
        "paused": 2,
        "completed": 3,
        "cancelled": 4,
        "unenrolled": 5,
    }

    # ---------------------------------------------------------
    # BUILD EMPLOYEE LIST
    # ---------------------------------------------------------
    employees = []

    for employee_profile in employee_profiles:
        student = employee_profile.user

        employee_enrollments = enrollments_by_student.get(
            student.id,
            [],
        )

        courses = [
            enrollment.course
            for enrollment in employee_enrollments
        ]

        if employee_enrollments:
            enrollment_status = min(
                (
                    enrollment.status
                    for enrollment in employee_enrollments
                ),
                key=lambda status: status_order.get(status, 999),
            )
        else:
            enrollment_status = "unenrolled"

        employees.append(
            {
                "student": student,
                "profile": employee_profile,
                "enrollments": employee_enrollments,
                "courses": courses,
                "enrollment_status": enrollment_status,
            }
        )


    # CALCULATE EMPLOYEES BY STATUS
    active_employees = sum(
        1
        for employee in employees
        if employee["enrollment_status"] == "active"
    )
    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def employee_display_name(employee):
        student = employee["student"]

        full_name = student.get_full_name().strip()

        if full_name:
            return full_name.lower()

        return student.username.lower()

    # ---------------------------------------------------------
    # SORT EMPLOYEES
    # ---------------------------------------------------------
    if sort_by == "level":

        level_order = {
            "A1": 1,
            "A2": 2,
            "B1.1": 3,
            "B1.2": 4,
            "B2.1": 5,
            "B2.2": 6,
            "C1.1": 7,
            "C1.2": 8,
            "C2.1": 9,
            "C2.2": 10,
        }

        employees.sort(
            key=lambda employee: (
                level_order.get(
                    employee["profile"].current_level,
                    999,
                ),
                employee_display_name(employee),
            )
        )

    elif sort_by == "name":

        employees.sort(
            key=employee_display_name
        )

    else:
        # Default:
        # active → paused → completed → cancelled → unenrolled
        # then alphabetical within each status
        employees.sort(
            key=lambda employee: (
                status_order.get(
                    employee["enrollment_status"],
                    999,
                ),
                employee_display_name(employee),
            )
        )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,
        "employees": employees,
        "active_company_admin_ids": active_company_admin_ids,
        "total_employees": len(employees),

        "active_employees": active_employees,    

        "level_choices": UserProfile.LEVEL_CHOICES,
        "sort_by": sort_by,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_employees_list.html",
        context,
    )



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

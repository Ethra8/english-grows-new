from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.db.models import Count, Q, Prefetch, Value, Case, When, Value, IntegerField, F, DateField

from django.db.models.functions import Coalesce, NullIf, Lower

from django.http import JsonResponse

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

from .models import UserProfile, TeacherProfile, StudentAcademicProfile, StudentAcademicProfile, StudentSkillAssessment, StudentSubSkillAssessment, SUBSKILLS, StudentSkillAssessmentSnapshot
from .forms import UserProfileForm, TeacherProfileForm, StudentAcademicProfileForm, StudentSkillAssessmentForm, StudentSubSkillAssessmentFormSet
from courses.models import Course, CourseEnrollment, ClassSession, BankHoliday, Attendance


User = get_user_model()


# =========================================================
# SHARED SKILLS CHART CONFIGURATION
# =========================================================
# Keep the same skill colors everywhere the progress chart is used.
# Dictionary order also controls the dataset / legend order.
SKILL_CHART_COLORS = {
    "Listening": "#4E2496",
    "Reading": "#E1752D",
    "Speaking": "#f5be58",
    "Writing": "#0ea5b7",
}

# =========================================================
# CALENDAR EVENT HELPERS
# =========================================================

def get_calendar_meeting_link(session):
    """
    Return the meeting link available for a ClassSession.

    Prefer the session-specific link.

    Fall back to the Course meeting link when the Course model
    provides one.
    """

    if session.meeting_link:
        return session.meeting_link

    return getattr(
        session.course,
        "meeting_link",
        "",
    ) or ""




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
@login_required
def my_course(request):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    # ---------------------------------------------------------
    # ALL ENROLLMENTS
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
    enrollments = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
        .annotate(
            status_order=Case(
                When(course__status="active", then=Value(1)),
                When(course__status="confirmed", then=Value(2)),
                When(course__status="paused", then=Value(3)),
                When(course__status="completed", then=Value(4)),
                When(course__status="cancelled", then=Value(5)),
                default=Value(99),
                output_field=IntegerField(),
            ),

            completed_date_order=Case(
                When(
                    course__status="completed",
                    then=F("course__end_date"),
                ),
                default=Value(None),
                output_field=DateField(),
            ),
        )
        .order_by(
            "status_order",
            "course__name",
            "-completed_date_order",
        )
    )

    # ---------------------------------------------------------
    # GET SELECTED COURSE FROM URL
    #
    # Example:
    # /profiles/student/course-details-page/?course=4
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")

    # ---------------------------------------------------------
    # DETERMINE WHICH ENROLLMENT / COURSE TO DISPLAY
    # ---------------------------------------------------------
    if selected_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )
    else:
        enrollment = enrollments.first()

    # ---------------------------------------------------------
    # SELECTED COURSE
    # ---------------------------------------------------------
    course = (
        enrollment.course
        if enrollment
        else None
    )

    enrollment_status = (
        enrollment.status
        if enrollment
        else None
    )

    # ---------------------------------------------------------
    # TIMETABLE
    # Must come from the SELECTED course.
    # ---------------------------------------------------------
    timetable_slots = None

    if enrollment:
        timetable_slots = (
            course.timetable_slots
            .all()
            .order_by(
                "day_of_week",
                "start_time",
            )
        )

    # ---------------------------------------------------------
    # NEXT CLASS
    #
    # Must come from the SELECTED course.
    #
    # For completed/cancelled courses this will naturally
    # return None because there should be no future scheduled
    # sessions.
    # ---------------------------------------------------------
    next_class = None

    if enrollment:
        next_class = (
            ClassSession.objects
            .filter(
                course=course,
                start_time__gte=timezone.now(),
                status__in=[
                    ClassSession.STATUS_SCHEDULED,
                    ClassSession.STATUS_RESCHEDULED,
                ],
            )
            .order_by("start_time")
            .first()
        )

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,

        # ALL enrollments -> course selector
        "enrollments": enrollments,

        # ONE selected enrollment/course -> page content
        "enrollment": enrollment,
        "course": course,

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
    """
    Calendar events for employee / individual learner profiles.

    Event actions exposed to calendar.js:

    - meeting_link:
        Join class when available.

    - group_details_url:
        Fallback action when no meeting link exists.
        Opens the learner's course page.
    """

    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role not in [
        UserProfile.ROLE_EMPLOYEE,
        UserProfile.ROLE_INDIVIDUAL,
    ]:
        return JsonResponse(
            [],
            safe=False,
        )

    start = request.GET.get("start")
    end = request.GET.get("end")

    active_course_ids = (
        CourseEnrollment.objects
        .filter(
            student=request.user,
            status="active",
            course__status="active",
        )
        .values_list(
            "course_id",
            flat=True,
        )
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
        .select_related(
            "course",
        )
        .order_by(
            "start_time"
        )
    )

    bank_holidays = (
        BankHoliday.objects
        .filter(
            is_active=True,
        )
        .order_by(
            "start_date"
        )
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

    events = []

    for session in sessions:

        events.append({
            "id": session.id,
            "title": session.title,
            "start": session.start_time.isoformat(),
            "end": (
                session.end_time.isoformat()
                if session.end_time
                else None
            ),

            "extendedProps": {
                "type": "class_session",

                "course":
                    session.course.name,

                "class_number":
                    session.class_number,

                "meeting_link": get_calendar_meeting_link(session),

                # This becomes the Group Details fallback
                # in calendar.js when no meeting link exists.
                
                "group_details_url": (
                    f"{reverse('profiles:my_course')}"
                    f"?course={session.course.id}"
                ),
            },
        })

    for holiday in bank_holidays:

        event = {
            "id":
                f"holiday-{holiday.id}",

            "title":
                holiday.title,

            "start":
                holiday.start_date.isoformat(),

            "allDay":
                True,

            "display":
                "block",

            "className":
                "bank-holiday-event",

            "extendedProps": {
                "type":
                    "bank_holiday",
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


    # ---------------------------------------------------------
    # ALL ENROLLMENTS
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
    enrollments = (
        CourseEnrollment.objects
        .filter(
            student=student,
        )
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
        .annotate(
            status_order=Case(
                When(
                    course__status="active",
                    then=Value(1),
                ),
                When(
                    course__status="confirmed",
                    then=Value(2),
                ),
                When(
                    course__status="paused",
                    then=Value(3),
                ),
                When(
                    course__status="completed",
                    then=Value(4),
                ),
                When(
                    course__status="cancelled",
                    then=Value(5),
                ),
                default=Value(99),
                output_field=IntegerField(),
            ),

            completed_date_order=Case(
                When(
                    course__status="completed",
                    then=F("course__end_date"),
                ),
                default=Value(None),
                output_field=DateField(),
            ),
        )
        .order_by(
            "status_order",
            "course__name",
            "-completed_date_order",
        )
    )


    # ---------------------------------------------------------
    # GET SELECTED COURSE FROM URL
    #
    # Example:
    # /profiles/student/my_learning_progress/?course=4
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")


    # ---------------------------------------------------------
    # COURSE SELECTED IN URL
    # ---------------------------------------------------------
    if selected_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )


    # ---------------------------------------------------------
    # NO COURSE SELECTED IN URL
    # ---------------------------------------------------------
    else:
        # Because the queryset is already ordered by lifecycle
        # priority, this naturally prefers:
        #
        # active -> confirmed -> paused -> completed -> cancelled
        enrollment = enrollments.first()

        # If a default course exists, redirect to the canonical
        # URL so the currently displayed course is explicit.
        if enrollment:
            return redirect(
                f"{request.path}?course={enrollment.course_id}"
            )


    # ---------------------------------------------------------
    # NO ENROLLMENTS
    # ---------------------------------------------------------
    if not enrollment:
        return render(
            request,
            "profiles/student/my_learning_progress.html",
            {
                "student": student,
                "student_profile": student_profile,

                # Full queryset for selector
                "enrollments": enrollments,

                # No selected enrollment/course
                "enrollment": None,
                "course": None,

                # Skills
                "overall_skill_chart_data": {
                    "labels": [],
                    "datasets": [],
                },
                "overall_average_score": None,

                # Attendance
                "attended_count": 0,
                "missed_count": 0,
                "excused_count": 0,
                "total_attendance_records": 0,
                "attendance_percentage": 0,
                "recent_attendance": [],

                # Progress
                "completed_classes": 0,
                "remaining_classes": 0,
                "total_classes": 0,
                "completion_percentage": 0,
            },
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
    # Calculate the learner's CURRENT overall skill score
    # for the selected course.
    #
    # Each StudentSkillAssessment already exposes:
    #
    #     assessment.average_score
    #
    # on a 0-10 scale.
    #
    # The overall score is therefore:
    #
    #     Speaking
    #   + Reading
    #   + Writing
    #   + Listening
    #   ----------------
    #          4
    #
    # IMPORTANT:
    # Only display an overall score when all four skills have
    # a valid current score. This avoids presenting a misleading
    # "overall" average based on only one, two or three skills.
    # ---------------------------------------------------------
    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related(
            "subskill_assessments",
        )
    )


    current_skill_scores = []

    for assessment in skill_assessments:

        score = assessment.average_score

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
    # ATTENDANCE
    #
    # Historical course status does not matter.
    # We are explicitly retrieving records for the selected
    # student + selected course.
    # ---------------------------------------------------------
    attendances = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course,
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
        .order_by(
            "-class_session__start_time"
        )
    )


    # ---------------------------------------------------------
    # ATTENDANCE COUNTS
    # ---------------------------------------------------------
    attended_count = attendances.filter(
        status=Attendance.STATUS_ATTENDED
    ).count()

    missed_count = attendances.filter(
        status=Attendance.STATUS_MISSED
    ).count()

    excused_count = attendances.filter(
        status=Attendance.STATUS_EXCUSED
    ).count()

    total_attendance_records = (
        attended_count
        + missed_count
        + excused_count
    )


    # ---------------------------------------------------------
    # ATTENDED HOURS
    #
    # Calculate the actual duration of every class the learner
    # attended. This correctly supports sessions with different
    # durations, including a shorter final class.
    # ---------------------------------------------------------
    attended_minutes = 0

    for attendance in attendances:
        if (
            attendance.status == Attendance.STATUS_ATTENDED
            and attendance.class_session.start_time
            and attendance.class_session.end_time
        ):
            session_duration = (
                attendance.class_session.end_time
                - attendance.class_session.start_time
            )

            attended_minutes += round(
                session_duration.total_seconds() / 60
            )


    # Decimal version, useful if you ever need calculations.
    attended_hours = attended_minutes / 60


    # Human-friendly display:
    # 90 minutes  -> 1h30
    # 120 minutes -> 2h
    attended_whole_hours, attended_remaining_minutes = divmod(
        attended_minutes,
        60,
    )

    if attended_remaining_minutes:
        attended_hours_display = (
            f"{attended_whole_hours}h"
            f"{attended_remaining_minutes:02d}"
        )
    else:
        attended_hours_display = (
            f"{attended_whole_hours}h"
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
            status=ClassSession.STATUS_COMPLETED,
        )
    )

    completed_minutes = 0

    for class_session in completed_course_sessions:
        if (
            class_session.start_time
            and class_session.end_time
        ):
            session_duration = (
                class_session.end_time
                - class_session.start_time
            )

            completed_minutes += round(
                session_duration.total_seconds() / 60
            )


    # Numeric version if needed elsewhere.
    completed_hours = completed_minutes / 60


    # Human-friendly display.
    completed_whole_hours, completed_remaining_minutes = divmod(
        completed_minutes,
        60,
    )

    if completed_remaining_minutes:
        completed_hours_display = (
            f"{completed_whole_hours}h"
            f"{completed_remaining_minutes:02d}"
        )
    else:
        completed_hours_display = (
            f"{completed_whole_hours}h"
        )


    # ---------------------------------------------------------
    # TOTAL COURSE HOURS
    # ---------------------------------------------------------
    total_hours = course.total_hours or 0

    total_minutes = round(
        float(total_hours) * 60
    )

    total_whole_hours, total_remaining_minutes = divmod(
        total_minutes,
        60,
    )

    if total_remaining_minutes:
        total_hours_display = (
            f"{total_whole_hours}h"
            f"{total_remaining_minutes:02d}"
        )
    else:
        total_hours_display = (
            f"{total_whole_hours}h"
        )


    # ---------------------------------------------------------
    # ATTENDANCE %
    # ---------------------------------------------------------
    attendance_percentage = (
        round(
            attended_count
            / total_attendance_records
            * 100
        )
        if total_attendance_records > 0
        else 0
    )


    # ---------------------------------------------------------
    # COURSE PROGRESS
    #
    # Use the selected enrollment rather than generic course
    # totals, so progress reflects the sessions actually
    # assigned to this learner.
    # ---------------------------------------------------------
    completed_classes = (
        enrollment.total_completed_classes
    )

    total_classes = (
        enrollment.total_assigned_classes
    )

    remaining_classes = (
        enrollment.upcoming_classes
    )


    # ---------------------------------------------------------
    # COMPLETION %
    # ---------------------------------------------------------
    completion_percentage = (
        round(
            (completed_classes / total_classes) * 100
        )
        if total_classes > 0
        else 0
    )


    # ---------------------------------------------------------
    # RECENT ATTENDANCE
    # ---------------------------------------------------------
    recent_attendance = (
        attendances
        .order_by(
            "-class_session__start_time"
        )[:5]
    )


    # ---------------------------------------------------------
    # COURSE TIMETABLE
    # ---------------------------------------------------------
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
            "days": " / ".join(days),
            "start": start,
            "end": end,
        })


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "student": student,
        "student_profile": student_profile,

        # ALL enrollments -> selector
        "enrollments": enrollments,

        # ONE selected enrollment/course
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
        "total_hours": total_hours,
        "total_hours_display": total_hours_display,

        # Completed course hours
        "completed_minutes": completed_minutes,
        "completed_hours": completed_hours,
        "completed_hours_display": completed_hours_display,

        # Progress
        "completed_classes": completed_classes,
        "remaining_classes": remaining_classes,
        "total_classes": total_classes,
        "completion_percentage": completion_percentage,

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

    student = request.user
    student_profile = profile


    # ---------------------------------------------------------
    # ALL ENROLLMENTS
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
    enrollments = (
        CourseEnrollment.objects
        .filter(
            student=student,
        )
        .select_related(
            "course",
            "course__course_type",
            "course__company",
            "course__teacher",
        )
        .annotate(
            status_order=Case(
                When(
                    course__status="active",
                    then=Value(1),
                ),
                When(
                    course__status="confirmed",
                    then=Value(2),
                ),
                When(
                    course__status="paused",
                    then=Value(3),
                ),
                When(
                    course__status="completed",
                    then=Value(4),
                ),
                When(
                    course__status="cancelled",
                    then=Value(5),
                ),
                default=Value(99),
                output_field=IntegerField(),
            ),

            completed_date_order=Case(
                When(
                    course__status="completed",
                    then=F("course__end_date"),
                ),
                default=Value(None),
                output_field=DateField(),
            ),
        )
        .order_by(
            "status_order",
            "course__name",
            "-completed_date_order",
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
                "course": None,

                # Course selector
                "enrollments": enrollments,

                # No selected enrollment
                "enrollment": None,

                # Attendance
                "recent_attendance": [],
                "recent_absences": [],
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
            class_session__status=ClassSession.STATUS_COMPLETED,
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
        .order_by(
            "-class_session__start_time"
        )
    )


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,

        # Shared student header
        "student": student,
        "student_profile": student_profile,
        "course": course,

        # ALL enrollments -> course selector
        "enrollments": enrollments,

        # ONE selected enrollment -> page content
        "enrollment": enrollment,

        # Attendance
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
    # ALL ENROLLMENTS
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
    enrollments = (
        CourseEnrollment.objects
        .filter(
            student=student,
        )
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
        .annotate(
            status_order=Case(
                When(
                    course__status="active",
                    then=Value(1),
                ),
                When(
                    course__status="confirmed",
                    then=Value(2),
                ),
                When(
                    course__status="paused",
                    then=Value(3),
                ),
                When(
                    course__status="completed",
                    then=Value(4),
                ),
                When(
                    course__status="cancelled",
                    then=Value(5),
                ),
                default=Value(99),
                output_field=IntegerField(),
            ),

            completed_date_order=Case(
                When(
                    course__status="completed",
                    then=F("course__end_date"),
                ),
                default=Value(None),
                output_field=DateField(),
            ),
        )
        .order_by(
            "status_order",
            "course__name",
            "-completed_date_order",
        )
    )


    # ---------------------------------------------------------
    # SELECTED COURSE
    #
    # Example:
    # /profiles/student/my_skills/?course=4
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")


    # ---------------------------------------------------------
    # COURSE SELECTED IN URL
    # ---------------------------------------------------------
    if selected_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )


    # ---------------------------------------------------------
    # NO COURSE SELECTED
    # ---------------------------------------------------------
    else:
        # Because enrollments is already ordered by status
        # priority, the default naturally prefers:
        #
        # active -> confirmed -> paused -> completed -> cancelled
        enrollment = enrollments.first()

        # Make the selected/default course explicit in the URL.
        #
        # /my_skills/
        #
        # becomes:
        #
        # /my_skills/?course=4
        if enrollment:
            return redirect(
                f"{request.path}?course={enrollment.course_id}"
            )


    # ---------------------------------------------------------
    # NO ENROLLMENTS
    # ---------------------------------------------------------
    if not enrollment:
        return render(
            request,
            "profiles/student/my_skills.html",
            {
                "student": student,
                "student_profile": student_profile,

                # Full queryset for selector
                "enrollments": enrollments,

                # No selected enrollment/course
                "enrollment": None,
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
    course = enrollment.course


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
    # SKILL ASSESSMENTS
    #
    # IMPORTANT:
    # Learner-facing views only READ existing assessments.
    # They do not create or modify assessment records.
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
    # SKILL NOTES DISPLAY
    # ---------------------------------------------------------
    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]


    # ---------------------------------------------------------
    # BUILD ALL 4 SKILL CARDS
    # ---------------------------------------------------------

    assessments_by_skill = {
        assessment.skill: assessment
        for assessment in skill_assessments
    }

    skill_areas = [
        ("listening", "Listening"),
        ("reading", "Reading"),
        ("speaking", "Speaking"),
        ("writing", "Writing"),
    ]

    skills = []

    for skill_value, skill_name in skill_areas:

        assessment = assessments_by_skill.get(skill_value)

        if assessment:

            note_display = build_skill_note_display(assessment)

            skills.append({
                "assessment": assessment,
                "assessment_id": assessment.id,
                "skill_value": skill_value,
                "name": skill_name,
                "icon": skill_icons.get(skill_value),
                "score": assessment.average_score,
                "subskills": assessment.subskill_assessments.all(),
                "strengths": note_display["strengths"],
                "confident": note_display["confident"],
                "required_standard": note_display["required_standard"],
                "developing": note_display["developing"],
                "needs_work": note_display["needs_work"],
            })

        else:

            skills.append({
                "assessment": None,
                "assessment_id": None,
                "skill_value": skill_value,
                "name": skill_name,
                "icon": skill_icons.get(skill_value),
                "score": None,
                "subskills": [],
                "strengths": [],
                "confident": [],
                "required_standard": [],
                "developing": [],
                "needs_work": [],
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
    #
    # Historical course status does not matter.
    # Data is explicitly scoped to selected student + course.
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

        # ALL enrollments -> course selector
        "enrollments": enrollments,

        # ONE selected enrollment -> current page
        "enrollment": enrollment,

        # Selected course
        "course": course,

        "skills": skills,
        "academic_profile": academic_profile,

        # Normal Python object because template uses json_script.
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
    end_of_month_date = today.replace(day=last_day_of_month)

    start_of_month = timezone.make_aware(
        datetime.combine(start_of_month_date, time.min)
    )
    end_of_month = timezone.make_aware(
        datetime.combine(end_of_month_date, time.max)
    )


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
                ClassSession.STATUS_COMPLETED,
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
    # WEEKLY / MONTHLY SESSIONS
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # HELPER
    # ---------------------------------------------------------

    def get_percentage(value, total):
        if total == 0:
            return 0

        return round((value / total) * 100)


    # =========================================================
    # WEEKLY DATA
    # =========================================================

    total_weekly_sessions = weekly_sessions.count()

    # A class is considered HELD when its end time has passed.
    held_weekly_sessions = weekly_sessions.filter(
        end_time__lt=now,
    ).count()

    upcoming_weekly_sessions = weekly_sessions.filter(
        start_time__gte=now,
    ).count()

    held_weekly_percentage = get_percentage(
        held_weekly_sessions,
        total_weekly_sessions,
    )


    # ---------------------------------------------------------
    # WEEKLY ATTENDANCE SUBMISSION
    # ---------------------------------------------------------

    weekly_held_sessions = weekly_sessions.filter(
        end_time__lt=now,
    )

    weekly_attendance_submitted_sessions = (
        weekly_held_sessions
        .filter(
            attendance_records__status__in=[
                Attendance.STATUS_ATTENDED,
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ]
        )
        .distinct()
        .count()
    )

    weekly_attendance_pending_sessions = max(
        held_weekly_sessions
        - weekly_attendance_submitted_sessions,
        0,
    )


    # ---------------------------------------------------------
    # WEEKLY ATTENDANCE RATE
    # ---------------------------------------------------------

    weekly_attendance_records = Attendance.objects.filter(
        class_session__course__teacher=request.user,
        class_session__course__status="active",
        class_session__start_time__gte=start_of_week,
        class_session__start_time__lte=end_of_week,
        class_session__end_time__lt=now,
        status__in=[
            Attendance.STATUS_ATTENDED,
            Attendance.STATUS_MISSED,
            Attendance.STATUS_EXCUSED,
        ],
    )

    weekly_total_attendance_records = (
        weekly_attendance_records.count()
    )

    weekly_attended_records = (
        weekly_attendance_records
        .filter(status=Attendance.STATUS_ATTENDED)
        .count()
    )

    weekly_attendance_rate = get_percentage(
        weekly_attended_records,
        weekly_total_attendance_records,
    )


    # =========================================================
    # MONTHLY DATA
    # =========================================================

    total_monthly_sessions = monthly_sessions.count()

    held_monthly_sessions = monthly_sessions.filter(
        end_time__lt=now,
    ).count()

    upcoming_monthly_sessions = monthly_sessions.filter(
        start_time__gte=now,
    ).count()

    held_monthly_percentage = get_percentage(
        held_monthly_sessions,
        total_monthly_sessions,
    )


    # ---------------------------------------------------------
    # MONTHLY ATTENDANCE SUBMISSION
    # ---------------------------------------------------------

    monthly_held_sessions = monthly_sessions.filter(
        end_time__lt=now,
    )

    monthly_attendance_submitted_sessions = (
        monthly_held_sessions
        .filter(
            attendance_records__status__in=[
                Attendance.STATUS_ATTENDED,
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ]
        )
        .distinct()
        .count()
    )

    monthly_attendance_pending_sessions = max(
        held_monthly_sessions
        - monthly_attendance_submitted_sessions,
        0,
    )


    # ---------------------------------------------------------
    # MONTHLY ATTENDANCE RATE
    # ---------------------------------------------------------

    monthly_attendance_records = Attendance.objects.filter(
        class_session__course__teacher=request.user,
        class_session__course__status="active",
        class_session__start_time__gte=start_of_month,
        class_session__start_time__lte=end_of_month,
        class_session__end_time__lt=now,
        status__in=[
            Attendance.STATUS_ATTENDED,
            Attendance.STATUS_MISSED,
            Attendance.STATUS_EXCUSED,
        ],
    )

    monthly_total_attendance_records = (
        monthly_attendance_records.count()
    )

    monthly_attended_records = (
        monthly_attendance_records
        .filter(status=Attendance.STATUS_ATTENDED)
        .count()
    )

    monthly_attendance_rate = get_percentage(
        monthly_attended_records,
        monthly_total_attendance_records,
    )


    # =========================================================
    # GENERAL DATA
    # =========================================================

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
    # ---------------------------------------------------------

    attendance_records = Attendance.objects.filter(
        class_session__course__teacher=request.user,
        class_session__course__status="active",
        class_session__end_time__lt=now,
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


    # =========================================================
    # CONTEXT
    # =========================================================

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
        "total_weekly_sessions": total_weekly_sessions,
        "held_weekly_sessions": held_weekly_sessions,
        "held_weekly_percentage": held_weekly_percentage,
        "upcoming_weekly_sessions": upcoming_weekly_sessions,

        "weekly_attendance_submitted_sessions":
            weekly_attendance_submitted_sessions,

        "weekly_attendance_pending_sessions":
            weekly_attendance_pending_sessions,

        "weekly_attendance_rate":
            weekly_attendance_rate,

        # Monthly
        "total_monthly_sessions": total_monthly_sessions,
        "held_monthly_sessions": held_monthly_sessions,
        "held_monthly_percentage": held_monthly_percentage,
        "upcoming_monthly_sessions": upcoming_monthly_sessions,

        "monthly_attendance_submitted_sessions":
            monthly_attendance_submitted_sessions,

        "monthly_attendance_pending_sessions":
            monthly_attendance_pending_sessions,

        "monthly_attendance_rate":
            monthly_attendance_rate,
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
        # TIME-BASED CLASSIFICATION
        # --------------------------------------------------

        is_upcoming = session.start_time > now
        is_past = session.start_time <= now

        # Keep these only if the template uses them
        session.is_upcoming = is_upcoming

        # --------------------------------------------------
        # WORKFLOW STATUS
        # --------------------------------------------------

        session.is_completed = (
            session.status == ClassSession.STATUS_COMPLETED
        )

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
        # FRONT-END STATUS GROUP
        # --------------------------------------------------

        if is_past:
            session.class_status_group = "past"
        else:
            session.class_status_group = "upcoming"

        # --------------------------------------------------
        # UPCOMING COUNTS
        # --------------------------------------------------

        if is_upcoming:
            class_filter_counts["upcoming"]["all"] += 1

            if session.is_today:
                class_filter_counts["upcoming"]["today"] += 1

            if session.is_this_week:
                class_filter_counts["upcoming"]["weekly"] += 1

            if session.is_this_month:
                class_filter_counts["upcoming"]["monthly"] += 1

        # --------------------------------------------------
        # PAST COUNTS
        # --------------------------------------------------

        if is_past:
            class_filter_counts["past"]["all"] += 1

            if session.is_today:
                class_filter_counts["past"]["today"] += 1

            if session.is_this_week:
                class_filter_counts["past"]["weekly"] += 1

            if session.is_this_month:
                class_filter_counts["past"]["monthly"] += 1


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
def teacher_course_details(request, course_id):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != UserProfile.ROLE_TEACHER:
        return redirect("home")


    # ---------------------------------------------------------
    # COURSE
    #
    # Course remains accessible regardless of status,
    # provided it belongs to this teacher.
    # ---------------------------------------------------------
    course = get_object_or_404(
        Course,
        id=course_id,
        teacher=request.user,
    )


    # ---------------------------------------------------------
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
    # ---------------------------------------------------------
    enrollments = (
        course.enrollments
        .select_related(
            "student",
            "student__profile",
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
        .order_by(
            "status_order",
            "student__first_name",
            "student__last_name",
            "student__username",
        )
    )


    # ---------------------------------------------------------
    # CLASS SESSIONS
    # ---------------------------------------------------------
    sessions = (
        course.class_sessions
        .all()
        .order_by("start_time")
    )


    # ---------------------------------------------------------
    # COURSE PROGRESS
    # ---------------------------------------------------------
    total_classes = course.total_sessions
    completed_classes = course.completed_sessions
    remaining_classes = course.remaining_sessions
    completion_percentage = course.completion_percentage


    # ---------------------------------------------------------
    # AVERAGE COURSE ATTENDANCE
    # ---------------------------------------------------------
    attendance_percentages = []

    for enrollment in enrollments:
        total_completed = enrollment.total_completed_classes

        if total_completed > 0:
            attendance_percentages.append(
                (
                    enrollment.classes_attended
                    / total_completed
                ) * 100
            )

    if attendance_percentages:
        average_attendance = round(
            sum(attendance_percentages)
            / len(attendance_percentages)
        )
    else:
        average_attendance = 0


    # ---------------------------------------------------------
    # COURSE TIMETABLE
    # ---------------------------------------------------------
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
            "days": " / ".join(days),
            "start": start,
            "end": end,
        })


    # ---------------------------------------------------------
    # GROUP EMAIL LIST
    # ---------------------------------------------------------
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
        context,
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
def teacher_attendance_detail(request, session_id):
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
        "profiles/teacher/teacher_attendance_detail.html",
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

    # ---------------------------------------------------------
    # COURSE TIMETABLE
    # ---------------------------------------------------------

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
            "days": " / ".join(days),
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
    """
    Build skill progress chart data from detailed assessment snapshots.

    Multiple subskill changes can create multiple snapshots for the
    same skill on the same day.

    For the chart's daily point, use the LAST snapshot recorded for
    that skill on that date. This ensures the latest graph point
    matches the current skill-card score.
    """

    snapshots = (
        StudentSkillAssessmentSnapshot.objects
        .filter(
            skill_assessment__student=student,
            skill_assessment__course=course,
        )
        .select_related(
            "skill_assessment",
        )
        .order_by(
            "recorded_at",
        )
    )

    # ---------------------------------------------------------
    # GROUP SNAPSHOTS BY DATE + SKILL
    #
    # Because snapshots are ordered chronologically, assigning
    # repeatedly to the same date/skill automatically leaves us
    # with the LAST snapshot for that day.
    # ---------------------------------------------------------
    daily_scores = {}

    for snapshot in snapshots:
        date = timezone.localtime(
            snapshot.recorded_at
        ).date()

        skill = snapshot.skill_assessment.skill

        daily_scores.setdefault(date, {})

        daily_scores[date][skill] = snapshot.score


    # ---------------------------------------------------------
    # CHART DATES
    # ---------------------------------------------------------
    chart_dates = sorted(daily_scores.keys())

    chart_labels = [
        date.strftime("%d/%m/%y")
        for date in chart_dates
    ]


    # ---------------------------------------------------------
    # DATASETS
    # ---------------------------------------------------------
    datasets = []

    for skill_name, color in SKILL_CHART_COLORS.items():

        skill_value = skill_name.lower()

        values = []

        for date in chart_dates:
            score = daily_scores.get(
                date,
                {},
            ).get(
                skill_value,
            )

            values.append(
                float(score)
                if score is not None
                else None
            )

        datasets.append({
            "label": skill_name,
            "data": values,
            "borderColor": color,
            "backgroundColor": color,
            "tension": 0.2,
        })


    return {
        "labels": chart_labels,
        "datasets": datasets,
    }


from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone


def build_overall_skill_progress_chart_data(student, course):
    """
    Build one overall skill-development score per assessment date.

    Each point represents the average of the latest known scores
    for all four skills on that date.

    Rules:
    - Uses existing term snapshots as historical baseline.
    - Uses detailed assessment snapshots for newer changes.
    - If a skill is assessed several times on the same day,
      only its LAST score that day is used.
    - A chart point is created only once all four skills have
      an available assessment score.
    """

    skill_names = {
        "listening",
        "reading",
        "speaking",
        "writing",
    }

    # ---------------------------------------------------------
    # DETAILED ASSESSMENT SNAPSHOTS
    # ---------------------------------------------------------
    assessment_snapshots = (
        StudentSkillAssessmentSnapshot.objects
        .filter(
            skill_assessment__student=student,
            skill_assessment__course=course,
        )
        .select_related("skill_assessment")
        .order_by("recorded_at")
    )


    # ---------------------------------------------------------
    # COLLECT ALL CHANGES BY DATE
    #
    # {
    #     date: {
    #         "listening": Decimal(...),
    #         "reading": Decimal(...),
    #         ...
    #     }
    # }
    # ---------------------------------------------------------
    daily_changes = {}

    # New detailed assessment history
    #
    # These are processed second, so they take precedence
    # over a term snapshot on the same date.
    for snapshot in assessment_snapshots:
        date = timezone.localtime(
            snapshot.recorded_at
        ).date()

        skill = snapshot.skill_assessment.skill

        daily_changes.setdefault(date, {})

        # Because queryset is chronological, the last
        # snapshot for this skill/date wins.
        daily_changes[date][skill] = snapshot.score


    if not daily_changes:
        return {
            "labels": [],
            "datasets": [],
        }


    # ---------------------------------------------------------
    # WALK THROUGH HISTORY
    #
    # Carry forward the latest known value for every skill.
    # ---------------------------------------------------------
    latest_scores = {}

    chart_labels = []
    overall_scores = []


    for date in sorted(daily_changes.keys()):

        # Apply all assessment changes made on this date.
        for skill, score in daily_changes[date].items():
            latest_scores[skill] = score


        # -----------------------------------------------------
        # ONLY CREATE A POINT WHEN ALL 4 SKILLS HAVE
        # ACTUALLY BEEN ASSESSED.
        # -----------------------------------------------------
        if not skill_names.issubset(latest_scores.keys()):
            continue


        total = sum(
            (
                latest_scores[skill]
                for skill in skill_names
            ),
            Decimal("0"),
        )

        average = (
            total / Decimal("4")
        ).quantize(
            Decimal("0.1"),
            rounding=ROUND_HALF_UP,
        )


        chart_labels.append(
            date.strftime("%d/%m/%y")
        )

        overall_scores.append(
            float(average)
        )


    return {
        "labels": chart_labels,

        "datasets": [
            {
                "label": "Overall Skills",
                "data": overall_scores,

                # I'd use ONE brand colour here,
                # not one of the individual skill colours.
                "borderColor": "#007A7D",
                "backgroundColor": "#007A7D",

                "tension": 0.2,
            }
        ],
    }



# Helper to display Teacher notes (+ future automated reports ???)
def build_skill_note_display(skill_assessment):
    subskills = skill_assessment.subskill_assessments.all()

    return {
        "skill": skill_assessment.get_skill_display(),
        "score": skill_assessment.average_score,

        "strengths": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating == "strong"
        ],

        "confident": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating == "confident"
        ],

        "required_standard": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating == "required_standard"
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

    # Explicit learner account status.
    #
    # This is User.is_active and is completely independent
    # from CourseEnrollment.status and Course.status.
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
    enrollments = (
        CourseEnrollment.objects
        .filter(
            student=student,
            course__teacher=request.user,
        )
        .select_related(
            "student",
            "student__profile",
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
        .annotate(
            status_order=Case(
                When(
                    course__status="active",
                    then=Value(1),
                ),
                When(
                    course__status="confirmed",
                    then=Value(2),
                ),
                When(
                    course__status="paused",
                    then=Value(3),
                ),
                When(
                    course__status="completed",
                    then=Value(4),
                ),
                When(
                    course__status="cancelled",
                    then=Value(5),
                ),
                default=Value(99),
                output_field=IntegerField(),
            ),

            completed_date_order=Case(
                When(
                    course__status="completed",
                    then=F("course__end_date"),
                ),
                default=Value(None),
                output_field=DateField(),
            ),
        )
        .order_by(
            "status_order",
            "course__name",
            "-completed_date_order",
        )
    )


    # ---------------------------------------------------------
    # SELECTED COURSE FROM QUERY STRING
    #
    # Example:
    #
    # ?course=8
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")


    if selected_course_id:

        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )

    else:

        enrollment = original_enrollment


    # ---------------------------------------------------------
    # CURRENT COURSE
    # ---------------------------------------------------------
    course = enrollment.course


    # ---------------------------------------------------------
    # ATTENDANCE
    # ---------------------------------------------------------
    attendances = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course,
            status__in=[
                Attendance.STATUS_ATTENDED,
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ],
        )
        .select_related(
            "class_session"
        )
        .order_by(
            "-class_session__start_time"
        )
    )


    # ---------------------------------------------------------
    # ATTENDANCE COUNTS
    # ---------------------------------------------------------
    total_attendance_records = (
        attendances.count()
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
    # ---------------------------------------------------------
    completed_classes = (
        enrollment.total_completed_classes
    )

    total_classes = (
        enrollment.total_assigned_classes
    )

    remaining_classes = (
        enrollment.upcoming_classes
    )


    # ---------------------------------------------------------
    # ATTENDANCE %
    #
    # Based on submitted attendance records only.
    # ---------------------------------------------------------
    attendance_percentage = (
        round(
            (
                attended_count
                / total_attendance_records
            )
            * 100
        )
        if total_attendance_records > 0
        else 0
    )


    # ---------------------------------------------------------
    # COMPLETION %
    # ---------------------------------------------------------
    completion_percentage = (
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
    # ATTENDED HOURS
    #
    # Actual duration of classes the learner attended.
    # ---------------------------------------------------------
    attended_minutes = 0

    for attendance in attendances:

        if (
            attendance.status == Attendance.STATUS_ATTENDED
            and attendance.class_session.start_time
            and attendance.class_session.end_time
        ):
            session_duration = (
                attendance.class_session.end_time
                - attendance.class_session.start_time
            )

            attended_minutes += round(
                session_duration.total_seconds()
                / 60
            )


    attended_hours = (
        attended_minutes / 60
    )


    attended_whole_hours, attended_remaining_minutes = divmod(
        attended_minutes,
        60,
    )

    if attended_remaining_minutes:

        attended_hours_display = (
            f"{attended_whole_hours}h"
            f"{attended_remaining_minutes:02d}"
        )

    else:

        attended_hours_display = (
            f"{attended_whole_hours}h"
        )


    # ---------------------------------------------------------
    # COMPLETED COURSE HOURS
    #
    # Total duration of all completed sessions for the course,
    # regardless of attendance status.
    # ---------------------------------------------------------
    completed_course_sessions = (
        course.class_sessions
        .filter(
            status=ClassSession.STATUS_COMPLETED,
        )
    )


    completed_minutes = 0

    for class_session in completed_course_sessions:

        if (
            class_session.start_time
            and class_session.end_time
        ):
            session_duration = (
                class_session.end_time
                - class_session.start_time
            )

            completed_minutes += round(
                session_duration.total_seconds()
                / 60
            )


    completed_hours = (
        completed_minutes / 60
    )


    completed_whole_hours, completed_remaining_minutes = divmod(
        completed_minutes,
        60,
    )

    if completed_remaining_minutes:

        completed_hours_display = (
            f"{completed_whole_hours}h"
            f"{completed_remaining_minutes:02d}"
        )

    else:

        completed_hours_display = (
            f"{completed_whole_hours}h"
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


    total_whole_hours, total_remaining_minutes = divmod(
        total_minutes,
        60,
    )


    if total_remaining_minutes:

        total_hours_display = (
            f"{total_whole_hours}h"
            f"{total_remaining_minutes:02d}"
        )

    else:

        total_hours_display = (
            f"{total_whole_hours}h"
        )


    # ---------------------------------------------------------
    # RECENT ATTENDANCE
    # ---------------------------------------------------------
    recent_attendance = (
        attendances[:5]
    )


    # ---------------------------------------------------------
    # CURRENT SKILL ASSESSMENTS
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
        .order_by(
            "skill"
        )
    )


    # ---------------------------------------------------------
    # CURRENT OVERALL SKILLS AVERAGE
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
    # OVERALL SKILLS PROGRESS GRAPH
    # ---------------------------------------------------------
    overall_skill_chart_data = (
        build_overall_skill_progress_chart_data(
            student=student,
            course=course,
        )
    )


    # ---------------------------------------------------------
    # COURSE TIMETABLE
    #
    # Groups slots sharing the same start/end time.
    # ---------------------------------------------------------
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
            "days": " / ".join(days),
            "start": start,
            "end": end,
        })


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {

        # Student
        "student": student,
        "student_profile": student_profile,

        # Explicit Django User.is_active value
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

        # Completed course hours
        "completed_minutes": completed_minutes,
        "completed_hours": completed_hours,
        "completed_hours_display": completed_hours_display,

        # Total course hours
        "total_hours": total_hours,
        "total_hours_display": total_hours_display,

        # Course progress
        "completed_classes": completed_classes,
        "remaining_classes": remaining_classes,
        "total_classes": total_classes,
        "completion_percentage": completion_percentage,

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
    enrollments = (
        CourseEnrollment.objects
        .filter(
            student=student,
            course__teacher=request.user,
        )
        .select_related(
            "student",
            "student__profile",
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
        .annotate(
            status_order=Case(
                When(
                    course__status="active",
                    then=Value(1),
                ),
                When(
                    course__status="confirmed",
                    then=Value(2),
                ),
                When(
                    course__status="paused",
                    then=Value(3),
                ),
                When(
                    course__status="completed",
                    then=Value(4),
                ),
                When(
                    course__status="cancelled",
                    then=Value(5),
                ),
                default=Value(99),
                output_field=IntegerField(),
            ),

            completed_date_order=Case(
                When(
                    course__status="completed",
                    then=F("course__end_date"),
                ),
                default=Value(None),
                output_field=DateField(),
            ),
        )
        .order_by(
            "status_order",
            "course__name",
            "-completed_date_order",
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
        enrollment.total_completed_classes
    )

    total_classes = (
        enrollment.total_assigned_classes
    )

    remaining_classes = (
        enrollment.upcoming_classes
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
    completion_percentage = (
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
                status=ClassSession.STATUS_COMPLETED,
                start_time__lt=enrollment.enrolled_at,
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
    attended_minutes = 0

    for attendance in attendances:

        if (
            attendance.status == Attendance.STATUS_ATTENDED
            and attendance.class_session.start_time
            and attendance.class_session.end_time
        ):

            session_duration = (
                attendance.class_session.end_time
                - attendance.class_session.start_time
            )

            attended_minutes += round(
                session_duration.total_seconds()
                / 60
            )


    attended_hours = (
        attended_minutes / 60
    )


    attended_whole_hours, attended_remaining_minutes = divmod(
        attended_minutes,
        60,
    )


    if attended_remaining_minutes:

        attended_hours_display = (
            f"{attended_whole_hours}h"
            f"{attended_remaining_minutes:02d}"
        )

    else:

        attended_hours_display = (
            f"{attended_whole_hours}h"
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
            status=ClassSession.STATUS_COMPLETED,
        )
    )


    completed_minutes = 0

    for class_session in completed_course_sessions:

        if (
            class_session.start_time
            and class_session.end_time
        ):

            session_duration = (
                class_session.end_time
                - class_session.start_time
            )

            completed_minutes += round(
                session_duration.total_seconds()
                / 60
            )


    completed_hours = (
        completed_minutes / 60
    )


    completed_whole_hours, completed_remaining_minutes = divmod(
        completed_minutes,
        60,
    )


    if completed_remaining_minutes:

        completed_hours_display = (
            f"{completed_whole_hours}h"
            f"{completed_remaining_minutes:02d}"
        )

    else:

        completed_hours_display = (
            f"{completed_whole_hours}h"
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


    total_whole_hours, total_remaining_minutes = divmod(
        total_minutes,
        60,
    )


    if total_remaining_minutes:

        total_hours_display = (
            f"{total_whole_hours}h"
            f"{total_remaining_minutes:02d}"
        )

    else:

        total_hours_display = (
            f"{total_whole_hours}h"
        )


    # ---------------------------------------------------------
    # COURSE TIMETABLE
    #
    # Not currently displayed in the attendance body you
    # supplied, but kept available because the learner header /
    # shared course components may use it.
    # ---------------------------------------------------------
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
            "days": " / ".join(days),
            "start": start,
            "end": end,
        })


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

        # Explicit learner account status.
        #
        # This is User.is_active and is completely independent
        # from CourseEnrollment.status and Course.status.
        "student_is_active": student_is_active,

        # -----------------------------------------------------
        # COURSE SELECTOR
        # -----------------------------------------------------
        "enrollments": enrollments,

        "course": course,
        "enrollment": enrollment,


        # -----------------------------------------------------
        # COURSE / TIMETABLE
        # -----------------------------------------------------
        "formatted_timetable": (
            formatted_timetable
        ),


        # -----------------------------------------------------
        # ATTENDANCE
        # -----------------------------------------------------
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

        "completion_percentage": (
            completion_percentage
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
    enrollments = (
        CourseEnrollment.objects
        .filter(
            student=student,
            course__teacher=request.user,
        )
        .select_related(
            "student",
            "student__profile",
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
        .annotate(
            status_order=Case(
                When(
                    course__status="active",
                    then=Value(1),
                ),
                When(
                    course__status="confirmed",
                    then=Value(2),
                ),
                When(
                    course__status="paused",
                    then=Value(3),
                ),
                When(
                    course__status="completed",
                    then=Value(4),
                ),
                When(
                    course__status="cancelled",
                    then=Value(5),
                ),
                default=Value(99),
                output_field=IntegerField(),
            ),

            completed_date_order=Case(
                When(
                    course__status="completed",
                    then=F("course__end_date"),
                ),
                default=Value(None),
                output_field=DateField(),
            ),
        )
        .order_by(
            "status_order",
            "course__name",
            "-completed_date_order",
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
    # SKILL ICONS
    # ---------------------------------------------------------
    skill_icons = {
        "speaking": "fa-solid fa-microphone",
        "reading": "fa-solid fa-book-open",
        "writing": "fa-solid fa-pen",
        "listening": "fa-solid fa-headphones",
    }


    # ---------------------------------------------------------
    # ENSURE ALL PREDEFINED SKILLS / SUBSKILLS EXIST
    #
    # Important:
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
    # SKILL ASSESSMENTS
    # ---------------------------------------------------------
    skill_assessments = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .prefetch_related(
            "subskill_assessments",
        )
        .order_by(
            "skill"
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
    # BUILD SKILL CARDS
    #
    # Same structure as learner Skills page,
    # but assessment_id is retained so teacher can edit.
    # ---------------------------------------------------------
    skills = []

    for assessment in skill_assessments:

        note_display = (
            build_skill_note_display(
                assessment
            )
        )

        # Only genuinely assessed subskills.
        assessed_subskills = (
            assessment.subskill_assessments
            .exclude(
                rating__isnull=True
            )
            .exclude(
                rating=""
            )
        )


        skills.append({
            "assessment": assessment,

            # Needed by Edit Skill button
            "assessment_id": assessment.id,

            "skill_value": assessment.skill,

            "name": (
                assessment.get_skill_display()
            ),

            "icon": skill_icons.get(
                assessment.skill,
                "fa-solid fa-chart-simple",
            ),

            # Overall assessment /10
            "score": assessment.average_score,

            "teacher_notes": (
                assessment.teacher_notes
            ),

            # Use only genuinely assessed subskills
            "subskills": assessed_subskills,

            # Grouped assessment categories
            "strengths": note_display["strengths"],
            "confident": note_display["confident"],
            "required_standard": (
                note_display["required_standard"]
            ),
            "developing": note_display["developing"],
            "needs_work": note_display["needs_work"],
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
        .order_by(
            "skill"
        )
    )


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

        "student_is_active": student_is_active,
        # Course selector
        "enrollments": enrollments,

        # Current selected course / enrollment
        "course": course,
        "enrollment": enrollment,

        # Skills
        "skills": skills,
        "skill_assessments": skill_assessments,
        "skill_notes": skill_notes,
        "skill_note_display": skill_note_display,

        # Overall current score
        "overall_average_score": overall_average_score,

        # Graphs
        "chart_data": chart_data,
        "overall_skill_chart_data": overall_skill_chart_data,

        # Academic profile
        "academic_profile": academic_profile,

        # Level choices
        "level_choices": UserProfile.LEVEL_CHOICES,
    }


    # ---------------------------------------------------------
    # RENDER
    # ---------------------------------------------------------
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
        .select_related(
            "student",
            "course",
        )
        .prefetch_related(
            "subskill_assessments",
        ),
        id=skill_assessment_id,
        course__teacher=request.user,
    )

    skill = StudentSkillAssessment.SKILL_AREA_CHOICES


    # ---------------------------------------------------------
    # POST
    # ---------------------------------------------------------
    if request.method == "POST":

        form = StudentSkillAssessmentForm(
            request.POST,
            instance=skill_assessment,
        )

        formset = StudentSubSkillAssessmentFormSet(
            request.POST,
            instance=skill_assessment,
        )


        # -----------------------------------------------------
        # VALID FORMS
        # -----------------------------------------------------
        if form.is_valid() and formset.is_valid():

            # -------------------------------------------------
            # SAVE GENERAL SKILL FORM
            #
            # Currently this saves teacher_notes.
            # -------------------------------------------------
            form.save()


            # -------------------------------------------------
            # SAVE SUBSKILL RATINGS
            #
            # IMPORTANT:
            #
            # Each StudentSubSkillAssessment is saved through
            # its own model save() method.
            #
            # That model method:
            # - checks whether the rating genuinely changed
            # - ignores unrated subskills
            # - recalculates the overall skill average
            # - creates a StudentSkillAssessmentSnapshot
            #   when a real rating is added or changed
            #
            # Therefore NO snapshot creation is needed here.
            # -------------------------------------------------
            formset.save()


            # -------------------------------------------------
            # CLEAR PREFETCH CACHE
            #
            # skill_assessment was loaded with:
            #
            #     prefetch_related("subskill_assessments")
            #
            # After formset.save(), that cached queryset may
            # still contain the old values.
            #
            # Clearing the cache ensures the newly saved
            # ratings are used below.
            # -------------------------------------------------
            if hasattr(
                skill_assessment,
                "_prefetched_objects_cache",
            ):
                skill_assessment._prefetched_objects_cache = {}


            # -------------------------------------------------
            # REGENERATE TEACHER NOTES
            #
            # Uses the latest saved subskill ratings.
            # -------------------------------------------------
            skill_assessment.teacher_notes = (
                skill_assessment.generate_teacher_notes()
            )


            # -------------------------------------------------
            # SAVE GENERATED NOTES
            #
            # Do NOT create a snapshot here.
            #
            # Snapshot creation belongs to:
            #
            # StudentSubSkillAssessment.save()
            #
            # because the snapshot represents an actual
            # subskill assessment change.
            # -------------------------------------------------
            skill_assessment.save(
                update_fields=[
                    "teacher_notes",
                    "updated_at",
                ]
            )


            # -------------------------------------------------
            # IMPORTANT:
            # NO StudentSkillTermSnapshot HERE
            #
            # StudentSkillTermSnapshot is reserved for formal
            # term assessments only.
            #
            # Ordinary teacher changes are stored as:
            #
            # StudentSkillAssessmentSnapshot
            #
            # via StudentSubSkillAssessment.save().
            # -------------------------------------------------


            # -------------------------------------------------
            # GET COURSE ENROLLMENT
            #
            # Needed for redirect back to the teacher's
            # student skills overview.
            # -------------------------------------------------
            enrollment = get_object_or_404(
                CourseEnrollment,
                student=skill_assessment.student,
                course=skill_assessment.course,
            )


            # -------------------------------------------------
            # REDIRECT
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

        form = StudentSkillAssessmentForm(
            instance=skill_assessment,
        )

        formset = StudentSubSkillAssessmentFormSet(
            instance=skill_assessment,
        )


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "skill_assessment": skill_assessment,
        "form": form,
        "formset": formset,
        "skill": skill,
    }


    # ---------------------------------------------------------
    # RENDER
    # ---------------------------------------------------------
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

    # Django User account status
    student_is_active = student.is_active

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
        # Django User account status
        "student_is_active": student_is_active,

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
    """
    Calendar events for teacher profiles.

    Teacher action:

    - meeting link exists
        -> Join class

    - no meeting link
        -> Group details
    """

    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if profile.role != UserProfile.ROLE_TEACHER:
        return JsonResponse(
            [],
            safe=False,
        )

    start = request.GET.get("start")
    end = request.GET.get("end")

    sessions = (
        ClassSession.objects
        .filter(
            course__teacher=request.user,
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
                ClassSession.STATUS_COMPLETED,
            ],
        )
        .select_related(
            "course",
        )
        .order_by(
            "start_time"
        )
    )

    bank_holidays = (
        BankHoliday.objects
        .filter(
            is_active=True,
        )
        .order_by(
            "start_date"
        )
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

    events = []

    for session in sessions:

        status_class = ""

        if session.course.status == "confirmed":
            status_class = (
                "course-confirmed-event"
            )

        elif session.course.status == "paused":
            status_class = (
                "course-paused-event"
            )

        elif session.course.status == "cancelled":
            status_class = (
                "course-cancelled-event"
            )

        events.append({
            "id":
                session.id,

            "title":
                session.title,

            "start":
                session.start_time.isoformat(),

            "end": (
                session.end_time.isoformat()
                if session.end_time
                else None
            ),

            "className":
                status_class,

            "extendedProps": {
                "type":
                    "class_session",

                "course":
                    session.course.name,

                "course_status":
                    session.course.status,

                "class_number":
                    session.class_number,

                "meeting_link": get_calendar_meeting_link(session),

                "group_details_url":
                    reverse(
                        "profiles:teacher_course_details",
                        args=[
                            session.course.id
                        ],
                    ),
            },
        })

    for holiday in bank_holidays:

        event = {
            "id":
                f"holiday-{holiday.id}",

            "title":
                holiday.title,

            "start":
                holiday.start_date.isoformat(),

            "allDay":
                True,

            "display":
                "block",

            "className":
                "bank-holiday-event",

            "extendedProps": {
                "type":
                    "bank_holiday",
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
            "pending_sessions": pending_sessions,
            "rescheduled_sessions": rescheduled_sessions,
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
            Session is already held AND every attendance
            record attached to that session has been resolved.

        Attendance rate:
            Attended / all resolved attendance records.
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


            # Attendance submission only matters
            # after the class has actually happened.
            if session.end_time >= now:
                continue


            attendance_records = list(
                session.attendance_records.all()
            )

            # No attendance rows means attendance
            # cannot be considered submitted.
            if not attendance_records:
                continue


            resolved_records = [
                attendance
                for attendance in attendance_records
                if attendance.status in resolved_attendance_statuses
            ]


            # -----------------------------
            # ATTENDANCE SUBMITTED
            # -----------------------------

            if len(resolved_records) == len(attendance_records):
                attendance_submitted_sessions += 1


            # -----------------------------
            # ATTENDANCE RATE
            # -----------------------------

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
                ClassSession.STATUS_COMPLETED,
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
                ClassSession.STATUS_COMPLETED,
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
    # Only resolved records belonging to classes that
    # have actually finished are included.
    # ---------------------------------------------------------

    attendance_records = (
        Attendance.objects
        .filter(
            class_session__course__company=company,
            class_session__course__status="active",
            class_session__end_time__lt=now,
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

    all_courses_list = []
    active_courses_list = []

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
            # ULifecycle: attendance is considered submitted
            # only when the lesson itself has been marked as completed.
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

        all_courses_list.append(course)

        if course.status == "active":
            active_courses_list.append(course)

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
        "all_courses_list": all_courses_list,
        "active_courses_list": active_courses_list,

        # Global summary.
        "total_courses_count": len(all_courses_list),
        "active_courses_count": len(active_courses_list),

        "total_active_employees": len(global_employee_ids),
        
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
    # AVAILABLE COURSES FOR SELECTOR
    #
    # Show ALL company courses regardless of status.
    # Order:
    # active -> confirmed -> paused -> completed -> cancelled
    # ---------------------------------------------------------
    available_courses = (
        Course.objects
        .filter(
            company=company,
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
        )
        .order_by(
            "status_order",
            "name",
        )
    )


    # ---------------------------------------------------------
    # COURSE
    #
    # Course remains accessible regardless of status:
    # active, confirmed, paused, completed or cancelled.
    # ---------------------------------------------------------
    course = get_object_or_404(
        available_courses,
        id=course_id,
    )
    # ---------------------------------------------------------
    # ALL ENROLLMENTS
    #
    # Keep all enrollment records available so historical
    # course/student information remains accessible regardless
    # of enrollment status.
    # ---------------------------------------------------------
    enrollments = (
        course.enrollments
        .select_related(
            "student",
            "student__profile",
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
        .order_by(
            "status_order",
            "student__first_name",
            "student__last_name",
            "student__username",
        )
    )


    # ---------------------------------------------------------
    # CLASS SESSIONS
    # ---------------------------------------------------------
    sessions = (
        course.class_sessions
        .all()
        .order_by("start_time")
    )


    # ---------------------------------------------------------
    # COURSE PROGRESS
    # ---------------------------------------------------------
    total_classes = course.total_sessions

    # Completed classes refers to manually take attendance
    # and mark class as complete
    completed_classes = course.completed_sessions

    remaining_classes = course.remaining_sessions

    now = timezone.now()

    completion_percentage = course.completion_percentage

    # CLASSES IN THE PAST, 
    # regardless if attendance has been submitted or not
    held_classes = (
        course.class_sessions
        .filter(
            end_time__lt=now,
        )
        .exclude(
            status=ClassSession.STATUS_PENDING_RESCHEDULE,
        )
    )

    past_held_classes = held_classes.count()


    # ---------------------------------------------------------
    # COMPLETED HOURS
    #
    # IMPORTANT:
    # For this Company Admin overview, completed hours are
    # schedule/time-based rather than Attendance-based.
    #
    # A lesson counts toward completed hours when:
    # - its current end_time is in the past
    # - it is NOT pending reschedule
    #
    # Attendance records are deliberately NOT used here.
    #
    # Using the actual session start/end times also means a
    # shorter final lesson is counted correctly.
    # ---------------------------------------------------------

    past_completed_hour_sessions = (
        course.class_sessions
        .filter(
            end_time__lt=now,
        )
        .exclude(
            status=ClassSession.STATUS_PENDING_RESCHEDULE,
        )
    )

    past_held_hours = Decimal("0.00")

    for session in past_completed_hour_sessions:
        duration = session.end_time - session.start_time

        duration_hours = (
            Decimal(str(duration.total_seconds()))
            / Decimal("3600")
        )

        past_held_hours += duration_hours

    past_held_hours = past_held_hours.quantize(
        Decimal("0.01")
    )

    # ---------------------------------------------------------
    # AVERAGE COURSE ATTENDANCE
    # ---------------------------------------------------------
    attendance_percentages = []

    for enrollment in enrollments:
        total_completed = enrollment.total_completed_classes

        if total_completed > 0:
            student_attendance_percentage = (
                enrollment.classes_attended
                / total_completed
            ) * 100

            attendance_percentages.append(
                student_attendance_percentage
            )

    if attendance_percentages:
        average_attendance = round(
            sum(attendance_percentages)
            / len(attendance_percentages)
        )
    else:
        average_attendance = 0


    # ---------------------------------------------------------
    # TIMETABLE DISPLAY
    # ---------------------------------------------------------
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
            "days": " / ".join(days),
            "start": start,
            "end": end,
        })


    # ---------------------------------------------------------
    # EMAIL LIST
    # ---------------------------------------------------------
    student_emails = [
        enrollment.student.email
        for enrollment in enrollments
        if enrollment.student.email
    ]

    bcc_student_emails = ",".join(
        student_emails
    )

    # ---------------------------------------------------------
    # AVERAGE GROUP SKILL ASSESSMENT
    #
    # Calculate the average score across all assessed
    # StudentSkillAssessment records belonging to learners
    # enrolled in this course.
    #
    # Important:
    # - only learners enrolled in this course are included
    # - only skill assessments with at least one subskill
    #   assessment are considered
    # - scores are based on StudentSkillAssessment.average_score
    #   which is on a 0–10 scale
    # ---------------------------------------------------------

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
            "subskill_assessments",
        )
    )

    assessed_skill_scores = []

    for skill_assessment in skill_assessments:

        subskills = list(
            skill_assessment.subskill_assessments.all()
        )

        if not subskills:
            continue

        score = skill_assessment.average_score

        if score is not None:
            assessed_skill_scores.append(score)


    if assessed_skill_scores:
        average_group_assessment_score = round(
            sum(assessed_skill_scores)
            / len(assessed_skill_scores),
            1,
        )
    else:
        average_group_assessment_score = None


    if average_group_assessment_score is not None:
        average_group_assessment_percentage = round(
            (average_group_assessment_score / 10) * 100
        )
    else:
        average_group_assessment_percentage = 0


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,
        "course": course,
        # All company courses for selector
        "available_courses": available_courses,
        # Enrollments belonging to selected course
        "enrollments": enrollments,
        "sessions": sessions,

        "total_classes": total_classes,

        "past_held_classes": past_held_classes,     
        # manually set attendance and class as status='complete'
        "completed_classes": completed_classes,
        "remaining_classes": remaining_classes,

        "average_group_assessment_score": average_group_assessment_score,
        "past_held_hours": past_held_hours,
        "completion_percentage": completion_percentage,

        "average_attendance": average_attendance,

        "average_group_assessment_percentage": average_group_assessment_percentage, 
        
        "formatted_timetable": formatted_timetable,
        "bcc_student_emails": bcc_student_emails,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_course_details.html",
        context,
    )



@login_required
def company_admin_course_students_list(request, course_id):
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
    # AVAILABLE COURSES FOR SELECTOR
    #
    # Show ALL company courses regardless of status.
    #
    # Order:
    # active
    # confirmed
    # paused
    # completed
    # cancelled
    # ---------------------------------------------------------
    available_courses = (
        Course.objects
        .filter(
            company=company,
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
        )
        .order_by(
            "status_order",
            "name",
        )
    )


    # ---------------------------------------------------------
    # CURRENT COURSE
    #
    # The requested course must:
    # - belong to the company admin's company
    # - exist in the available course queryset
    #
    # Course remains accessible regardless of status.
    # ---------------------------------------------------------
    course = get_object_or_404(
        available_courses,
        id=course_id,
    )


    # ---------------------------------------------------------
    # ENROLLMENTS
    #
    # All enrollments belonging to the currently selected
    # course are displayed, regardless of enrollment status.
    # ---------------------------------------------------------
    enrollments = (
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
            )
        )
    )


    # ---------------------------------------------------------
    # SORTING
    # ---------------------------------------------------------
    sort_by = request.GET.get(
        "sort",
        "name",
    )

    if sort_by == "level":
        enrollments = enrollments.order_by(
            "student__profile__current_level",
            "sort_name",
            "student__last_name",
        )

    else:
        # Default: Name A-Z
        sort_by = "name"

        enrollments = enrollments.order_by(
            "sort_name",
            "student__last_name",
        )


    # ---------------------------------------------------------
    # COURSE SESSIONS
    # ---------------------------------------------------------
    sessions = (
        course.class_sessions
        .all()
        .order_by("start_time")
    )


    # ---------------------------------------------------------
    # COURSE PROGRESS
    #
    # Uses the status-based Course properties established
    # in the new business logic.
    # ---------------------------------------------------------
    total_classes = course.total_sessions
    completed_classes = course.completed_sessions
    remaining_classes = course.remaining_sessions
    completion_percentage = course.completion_percentage


    # ---------------------------------------------------------
    # AVERAGE ATTENDANCE
    # ---------------------------------------------------------
    attendance_percentages = []

    for enrollment in enrollments:
        total_completed = enrollment.total_completed_classes

        if total_completed > 0:
            attendance_percentage = (
                enrollment.classes_attended
                / total_completed
            ) * 100

            attendance_percentages.append(
                attendance_percentage
            )

    average_attendance = 0

    if attendance_percentages:
        average_attendance = round(
            sum(attendance_percentages)
            / len(attendance_percentages)
        )


    # ---------------------------------------------------------
    # COURSE TIMETABLE
    # ---------------------------------------------------------
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
            "days": " / ".join(days),
            "start": start,
            "end": end,
        })


    # ---------------------------------------------------------
    # EMAIL ALL STUDENTS
    # ---------------------------------------------------------
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
        "company": company,

        # Current selected course
        "course": course,

        # All company courses for course selector
        "available_courses": available_courses,

        # Current course data
        "enrollments": enrollments,
        "sessions": sessions,
        "sort_by": sort_by,

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
        context,
    )



@login_required
def company_admin_course_attendance(request, course_id):
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
    # AVAILABLE COURSES FOR SELECTOR
    #
    # Show ALL company courses regardless of status.
    #
    # Order:
    # active
    # confirmed
    # paused
    # completed
    # cancelled
    # ---------------------------------------------------------
    available_courses = (
        Course.objects
        .filter(
            company=company,
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
            ),
            enrollment_count=Count(
                "enrollments",
                distinct=True,
            ),
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
    # Course remains accessible regardless of status.
    # ---------------------------------------------------------
    course = get_object_or_404(
        available_courses,
        id=course_id,
    )


    # ---------------------------------------------------------
    # ENROLLMENTS
    #
    # Include students who are currently enrolled
    # and students whose enrollment was completed
    # when the course finished.
    # ---------------------------------------------------------
    enrollments = (
        course.enrollments
        .select_related(
            "student",
            "student__profile",
        )
        .filter(
            status__in=[
                "active",
                "completed",
            ]
        )
    )


    # ---------------------------------------------------------
    # COMPLETED CLASS SESSIONS
    # ---------------------------------------------------------
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
        .prefetch_related(
            "attendance_records",
            "attendance_records__student",
            "attendance_records__student__profile",
        )
        .order_by("-start_time")
    )


    submitted_class_sessions = []


    # ---------------------------------------------------------
    # SESSION-LEVEL ATTENDANCE
    # ---------------------------------------------------------
    for class_session in class_sessions:

        # Attendance records already belong to this specific
        # ClassSession, so they represent the students who were
        # assigned to that lesson.
        attendance_records = list(
            class_session.attendance_records.all()
        )

        has_records = bool(attendance_records)

        has_scheduled_records = any(
            attendance.status == Attendance.STATUS_SCHEDULED
            for attendance in attendance_records
        )

        # Attendance is considered submitted only when:
        #
        # 1. Attendance records exist
        # 2. none remain status="scheduled"
        #
        # Valid final Attendance states:
        # attended
        # missed
        # excused
        # -----------------------------------------------------
        if has_records and not has_scheduled_records:

            class_session.attendance_filter_status = "completed"


            # -------------------------------------------------
            # COUNTS FOR THIS SESSION
            # -------------------------------------------------
            attended_count = sum(
                1
                for attendance in attendance_records
                if attendance.status == Attendance.STATUS_ATTENDED
            )

            missed_count = sum(
                1
                for attendance in attendance_records
                if attendance.status == Attendance.STATUS_MISSED
            )

            excused_count = sum(
                1
                for attendance in attendance_records
                if attendance.status == Attendance.STATUS_EXCUSED
            )


            # -------------------------------------------------
            # NUMBER OF LEARNERS ASSIGNED TO THIS SESSION
            #
            # Use Attendance records rather than the Course's
            # current enrollment count because learners may
            # have joined the Course later.
            # -------------------------------------------------
            registered_count = len(
                attendance_records
            )


            # -------------------------------------------------
            # FINAL ATTENDANCE RECORDS
            # -------------------------------------------------
            attendance_total = (
                attended_count
                + missed_count
                + excused_count
            )


            # -------------------------------------------------
            # ATTENDANCE % FOR THIS SESSION
            # -------------------------------------------------
            if attendance_total > 0:
                class_session.attendance_percentage = round(
                    (
                        attended_count
                        / attendance_total
                    ) * 100
                )
            else:
                class_session.attendance_percentage = 0


            # -------------------------------------------------
            # TEMPORARY DISPLAY VALUES
            #
            # These are attached only for the current request.
            # They are NOT saved to the database.
            # -------------------------------------------------
            class_session.attended_count = attended_count
            class_session.missed_count = missed_count
            class_session.excused_count = excused_count
            class_session.registered_count = registered_count
            class_session.attendance_total = attendance_total


            # -------------------------------------------------
            # EMPLOYEE SEARCH TEXT
            # -------------------------------------------------
            class_session.employee_search_text = " ".join(
                [
                    (
                        f"{attendance.student.get_full_name()} "
                        f"{attendance.student.username} "
                        f"{attendance.student.email}"
                    )
                    for attendance in attendance_records
                ]
            )


            submitted_class_sessions.append(
                class_session
            )


    # ---------------------------------------------------------
    # COURSE-LEVEL TOTALS
    # ---------------------------------------------------------
    total_classes = course.total_sessions
    completed_classes = course.completed_sessions


    # ---------------------------------------------------------
    # COURSE AVERAGE ATTENDANCE
    # ---------------------------------------------------------
    attendance_percentages = []

    for enrollment in enrollments:
        total_completed = enrollment.total_completed_classes

        if total_completed > 0:
            student_attendance_percentage = (
                enrollment.classes_attended
                / total_completed
            ) * 100

            attendance_percentages.append(
                student_attendance_percentage
            )


    if attendance_percentages:
        average_attendance = round(
            sum(attendance_percentages)
            / len(attendance_percentages)
        )
    else:
        average_attendance = 0


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,

        # Currently selected course
        "course": course,

        # All company courses for selector
        "available_courses": available_courses,

        "submitted_class_sessions": submitted_class_sessions,

        "submitted_class_sessions_count": len(
            submitted_class_sessions
        ),

        "total_classes": total_classes,
        "completed_classes": completed_classes,

        "average_attendance": average_attendance,
    }


    return render(
        request,
        "profiles/company_admin/"
        "company_admin_course_attendance.html",
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
def company_admin_student_detail(request, student_id):
    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("home")

    company = profile.company

    if not company:
        return redirect("home")


    # ---------------------------------------------------------
    # GET EMPLOYEE
    #
    # The employee must belong to the same company as the
    # logged-in company admin.
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
    #
    # Course lifecycle order:
    # 1. Active
    # 2. Confirmed
    # 3. Paused
    # 4. Completed
    # 5. Cancelled
    # ---------------------------------------------------------
    enrollments = (
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
            "student",
            "student__profile",
        )
        .annotate(
            status_order=Case(
                When(
                    course__status="active",
                    then=Value(1),
                ),
                When(
                    course__status="confirmed",
                    then=Value(2),
                ),
                When(
                    course__status="paused",
                    then=Value(3),
                ),
                When(
                    course__status="completed",
                    then=Value(4),
                ),
                When(
                    course__status="cancelled",
                    then=Value(5),
                ),
                default=Value(99),
                output_field=IntegerField(),
            ),

            completed_date_order=Case(
                When(
                    course__status="completed",
                    then=F("course__end_date"),
                ),
                default=Value(None),
                output_field=DateField(),
            ),
        )
        .order_by(
            "status_order",
            "course__name",
            "-completed_date_order",
        )
    )


    # ---------------------------------------------------------
    # GET SELECTED COURSE FROM URL
    #
    # Example:
    #
    # /profiles/company-admin/employees/3/?course=5
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")


    # ---------------------------------------------------------
    # DETERMINE SELECTED ENROLLMENT / COURSE
    # ---------------------------------------------------------
    if selected_course_id:
        enrollment = get_object_or_404(
            enrollments,
            course_id=selected_course_id,
        )

    else:
        enrollment = enrollments.first()


    # ---------------------------------------------------------
    # EMPLOYEE HAS NO ENROLLMENTS
    #
    # Keep the employee profile accessible, but without
    # course-specific progress data.
    # ---------------------------------------------------------
    if not enrollment:
        context = {
            "profile": profile,
            "company": company,

            "student": student,
            "student_profile": student_profile,

            "enrollments": enrollments,
            "enrollment": None,
            "course": None,

            "level_choices": UserProfile.LEVEL_CHOICES,

            # Attendance
            "attended_count": 0,
            "missed_count": 0,
            "excused_count": 0,
            "total_attendance_records": 0,
            "attendance_percentage": 0,

            # Progress
            "completed_classes": 0,
            "remaining_classes": 0,
            "total_classes": 0,
            "completion_percentage": 0,

            # Hours
            "total_hours_display": format_hours_duration(
                Decimal("0")
            ),
            "completed_hours_display": format_hours_duration(
                Decimal("0")
            ),
            "remaining_hours_display": format_hours_duration(
                Decimal("0")
            ),

            # Skills
            "overall_average_score": None,
            "overall_skill_chart_data": {
                "labels": [],
                "datasets": [],
            },

            # Additional data
            "recent_attendance": [],
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


    # ---------------------------------------------------------
    # SKILLS CHART
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
            status__in=[
                Attendance.STATUS_ATTENDED,
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ],
        )
        .select_related(
            "class_session"
        )
        .order_by(
            "-class_session__start_time"
        )
    )


    # ---------------------------------------------------------
    # ATTENDANCE COUNTS
    # ---------------------------------------------------------
    total_attendance_records = (
        attendances.count()
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
    # Progress is based on the ClassSessions actually assigned
    # to this enrollment.
    # ---------------------------------------------------------
    completed_classes = (
        enrollment.total_completed_classes
    )

    total_classes = (
        enrollment.total_assigned_classes
    )

    remaining_classes = (
        enrollment.upcoming_classes
    )


    # ---------------------------------------------------------
    # ATTENDED HOURS
    # ---------------------------------------------------------
    attended_minutes = 0

    for attendance in attendances:

        if (
            attendance.status == Attendance.STATUS_ATTENDED
            and attendance.class_session.start_time
            and attendance.class_session.end_time
        ):
            session_duration = (
                attendance.class_session.end_time
                - attendance.class_session.start_time
            )

            attended_minutes += round(
                session_duration.total_seconds()
                / 60
            )


    attended_hours = (
        attended_minutes / 60
    )


    attended_whole_hours, attended_remaining_minutes = divmod(
        attended_minutes,
        60,
    )

    if attended_remaining_minutes:
        attended_hours_display = (
            f"{attended_whole_hours}h"
            f"{attended_remaining_minutes:02d}"
        )

    else:
        attended_hours_display = (
            f"{attended_whole_hours}h"
        )


    # ---------------------------------------------------------
    # COMPLETED COURSE HOURS
    #
    # Total duration of all completed sessions in the course,
    # regardless of this employee's attendance.
    # ---------------------------------------------------------
    completed_course_sessions = (
        course.class_sessions
        .filter(
            status=ClassSession.STATUS_COMPLETED,
        )
    )

    completed_minutes = 0

    for class_session in completed_course_sessions:

        if (
            class_session.start_time
            and class_session.end_time
        ):
            session_duration = (
                class_session.end_time
                - class_session.start_time
            )

            completed_minutes += round(
                session_duration.total_seconds()
                / 60
            )


    completed_hours_numeric = (
        completed_minutes / 60
    )


    completed_whole_hours, completed_remaining_minutes = divmod(
        completed_minutes,
        60,
    )

    if completed_remaining_minutes:
        completed_course_hours_display = (
            f"{completed_whole_hours}h"
            f"{completed_remaining_minutes:02d}"
        )

    else:
        completed_course_hours_display = (
            f"{completed_whole_hours}h"
        )


    # ---------------------------------------------------------
    # COURSE TOTAL HOURS
    #
    # Original Course.total_hours value.
    # ---------------------------------------------------------
    course_total_hours = (
        course.total_hours or 0
    )

    course_total_minutes = round(
        float(course_total_hours) * 60
    )

    course_total_whole_hours, course_total_remaining_minutes = divmod(
        course_total_minutes,
        60,
    )

    if course_total_remaining_minutes:
        course_total_hours_display = (
            f"{course_total_whole_hours}h"
            f"{course_total_remaining_minutes:02d}"
        )

    else:
        course_total_hours_display = (
            f"{course_total_whole_hours}h"
        )


    # ---------------------------------------------------------
    # COMPLETED ASSIGNED HOURS
    #
    # Based specifically on sessions eligible for this
    # employee/enrollment.
    # ---------------------------------------------------------
    completed_session_list = list(
        enrollment.eligible_sessions.filter(
            status=ClassSession.STATUS_COMPLETED
        )
    )

    completed_hours = sum(
        (
            Decimal(
                str(
                    (
                        session.end_time
                        - session.start_time
                    ).total_seconds()
                )
            )
            / Decimal("3600")

            for session in completed_session_list
        ),
        Decimal("0"),
    )


    # ---------------------------------------------------------
    # TOTAL ASSIGNED HOURS
    # ---------------------------------------------------------
    assigned_session_list = list(
        enrollment.eligible_sessions
    )

    total_hours = sum(
        (
            Decimal(
                str(
                    (
                        session.end_time
                        - session.start_time
                    ).total_seconds()
                )
            )
            / Decimal("3600")

            for session in assigned_session_list
        ),
        Decimal("0"),
    )


    # ---------------------------------------------------------
    # REMAINING HOURS
    # ---------------------------------------------------------
    remaining_hours = max(
        total_hours - completed_hours,
        Decimal("0"),
    )


    # ---------------------------------------------------------
    # FORMAT ASSIGNED HOURS FOR DISPLAY
    # ---------------------------------------------------------
    completed_hours_display = (
        format_hours_duration(
            completed_hours
        )
    )

    remaining_hours_display = (
        format_hours_duration(
            remaining_hours
        )
    )

    total_hours_display = (
        format_hours_duration(
            total_hours
        )
    )


    # ---------------------------------------------------------
    # ATTENDANCE %
    # ---------------------------------------------------------
    attendance_percentage = (
        enrollment.attendance_percentage
    )


    # ---------------------------------------------------------
    # COMPLETION %
    # ---------------------------------------------------------
    completion_percentage = (
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
    # RECENT ATTENDANCE
    # ---------------------------------------------------------
    recent_attendance = (
        attendances[:5]
    )


    # ---------------------------------------------------------
    # SKILL ASSESSMENTS
    #
    # These are the CURRENT skill assessments for this
    # employee + selected course.
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
        .order_by(
            "skill"
        )
    )


    # ---------------------------------------------------------
    # CURRENT OVERALL SKILLS AVERAGE
    #
    # Each StudentSkillAssessment.average_score already
    # provides the current score for that skill on a 0-10
    # scale.
    #
    # An overall score is only shown once all four skills
    # have a valid score.
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
    # SKILL NOTES
    # ---------------------------------------------------------
    skill_note_display = [
        build_skill_note_display(
            skill_assessment
        )
        for skill_assessment in skill_assessments
    ]


    # ---------------------------------------------------------
    # OVERALL SKILLS PROGRESS GRAPH
    # ---------------------------------------------------------
    overall_skill_chart_data = (
        build_overall_skill_progress_chart_data(
            student=student,
            course=course,
        )
    )


    # ---------------------------------------------------------
    # COURSE TIMETABLE
    # ---------------------------------------------------------
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
            "days": " / ".join(days),
            "start": start,
            "end": end,
        })


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,

        # Employee
        "student": student,
        "student_profile": student_profile,

        "user_currently_enrolled": user_currently_enrolled,
        # Course selector
        "enrollments": enrollments,

        # Currently selected course
        "enrollment": enrollment,
        "course": course,

        "level_choices": UserProfile.LEVEL_CHOICES,

        # Timetable
        "formatted_timetable": formatted_timetable,

        # Attendance
        "attended_count": attended_count,
        "missed_count": missed_count,
        "excused_count": excused_count,
        "total_attendance_records": total_attendance_records,
        "attendance_percentage": attendance_percentage,

        # Attendance hours
        "attended_minutes": attended_minutes,
        "attended_hours": attended_hours,
        "attended_hours_display": attended_hours_display,

        # Original course-hour information
        "course_total_hours": course_total_hours,
        "course_total_hours_display": course_total_hours_display,

        # Completed course session hours
        "completed_minutes": completed_minutes,
        "completed_hours_numeric": completed_hours_numeric,
        "completed_course_hours_display": completed_course_hours_display,

        # Progress
        "completed_classes": completed_classes,
        "remaining_classes": remaining_classes,
        "total_classes": total_classes,
        "completion_percentage": completion_percentage,

        # Assigned enrollment hours
        "total_hours": total_hours,
        "total_hours_display": total_hours_display,
        "completed_hours": completed_hours,
        "completed_hours_display": completed_hours_display,
        "remaining_hours": remaining_hours,
        "remaining_hours_display": remaining_hours_display,

        # Attendance history
        "recent_attendance": recent_attendance,

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
    # GET ALL ENROLLMENTS FOR THIS EMPLOYEE
    # ---------------------------------------------------------
    enrollments = (
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
            "student",
            "student__profile",
        )
        .annotate(
            status_order=Case(
                When(course__status="active", then=Value(1)),
                When(course__status="confirmed", then=Value(2)),
                When(course__status="paused", then=Value(3)),
                When(course__status="completed", then=Value(4)),
                When(course__status="cancelled", then=Value(5)),
                default=Value(99),
                output_field=IntegerField(),
            ),

            completed_date_order=Case(
                When(
                    course__status="completed",
                    then=F("course__end_date"),
                ),
                default=Value(None),
                output_field=DateField(),
            ),
        )
        .order_by(
            "status_order",
            "course__name",
            "-completed_date_order",
        )
    )


    # ---------------------------------------------------------
    # GET SELECTED COURSE FROM URL
    # ---------------------------------------------------------
    selected_course_id = request.GET.get("course")


    # ---------------------------------------------------------
    # DETERMINE SELECTED ENROLLMENT / COURSE
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
        context = {
            "profile": profile,
            "company": company,

            # Employee
            "student": student,
            "student_profile": student_profile,

            # Course selector
            "enrollments": enrollments,

            # No selected course
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

            # Progress
            "completed_classes": 0,
            "course_completed_classes": 0,
            "remaining_classes": 0,
            "total_classes": 0,
            "completion_percentage": 0,

            # Late enrollment context
            "lessons_before_enrollment": 0,
            "show_enrollment_context": False,

            # Attendance history
            "recent_attendance": [],
            "recent_absences": [],
        }

        return render(
            request,
            "profiles/company_admin/"
            "company_admin_student_attendance_record.html",
            context,
        )


    # ---------------------------------------------------------
    # SELECTED COURSE
    # ---------------------------------------------------------
    course = enrollment.course


    # ---------------------------------------------------------
    # ATTENDANCE RECORDS
    #
    # Retrieve all submitted attendance records for this
    # employee + selected course.
    # ---------------------------------------------------------
    attendances = (
        Attendance.objects
        .filter(
            student=student,
            class_session__course=course,
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
        .order_by(
            "-class_session__start_time"
        )
    )


    # ---------------------------------------------------------
    # ABSENCE RECORDS
    #
    # Only missed + excused attendance records are needed
    # for the Absence Record accordion.
    # ---------------------------------------------------------
    recent_absences = (
        attendances
        .filter(
            status__in=[
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ]
        )
    )


    # ---------------------------------------------------------
    # ATTENDANCE COUNTS
    # ---------------------------------------------------------
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

    total_absences = missed_count + excused_count


    # ---------------------------------------------------------
    # EMPLOYEE-SPECIFIC COMPLETED CLASSES
    # ---------------------------------------------------------
    completed_classes = (
        enrollment.total_completed_classes
    )


    # ---------------------------------------------------------
    # COURSE-WIDE COMPLETED CLASSES
    # ---------------------------------------------------------
    course_completed_classes = (
        ClassSession.objects
        .filter(
            course=course,
            end_time__lt=timezone.now(),
        )
        .exclude(
            status="cancelled",
        )
        .count()
    )


    # ---------------------------------------------------------
    # LESSONS BEFORE EMPLOYEE ENROLLMENT
    # ---------------------------------------------------------
    lessons_before_enrollment = (
        ClassSession.objects
        .filter(
            course=course,
            end_time__lt=enrollment.enrolled_at,
        )
        .exclude(
            status="cancelled",
        )
        .count()
    )


    # ---------------------------------------------------------
    # SHOW LATE-ENROLLMENT CONTEXT?
    # ---------------------------------------------------------
    show_enrollment_context = (
        lessons_before_enrollment > 0
    )


    # ---------------------------------------------------------
    # TOTAL / REMAINING CLASSES
    # ---------------------------------------------------------
    total_classes = (
        enrollment.total_assigned_classes
    )

    remaining_classes = (
        enrollment.upcoming_classes
    )


    # ---------------------------------------------------------
    # ATTENDANCE %
    # ---------------------------------------------------------
    attendance_percentage = (
        enrollment.attendance_percentage
    )


    # ---------------------------------------------------------
    # COMPLETION %
    # ---------------------------------------------------------
    completion_percentage = (
        round(
            (completed_classes / total_classes) * 100
        )
        if total_classes > 0
        else 0
    )


    # ---------------------------------------------------------
    # ATTENDED HOURS
    #
    # Actual duration of the sessions this employee attended.
    # ---------------------------------------------------------
    attended_minutes = 0

    for attendance in attendances:

        if (
            attendance.status == Attendance.STATUS_ATTENDED
            and attendance.class_session.start_time
            and attendance.class_session.end_time
        ):
            session_duration = (
                attendance.class_session.end_time
                - attendance.class_session.start_time
            )

            attended_minutes += round(
                session_duration.total_seconds() / 60
            )


    attended_hours = (
        attended_minutes / 60
    )


    attended_whole_hours, attended_remaining_minutes = divmod(
        attended_minutes,
        60,
    )


    if attended_remaining_minutes:
        attended_hours_display = (
            f"{attended_whole_hours}h"
            f"{attended_remaining_minutes:02d}"
        )
    else:
        attended_hours_display = (
            f"{attended_whole_hours}h"
        )


    # ---------------------------------------------------------
    # COMPLETED HOURS SINCE ENROLLMENT
    #
    # Total duration of completed sessions that belong to this
    # employee's enrollment context.
    #
    # This excludes lessons completed before the employee joined,
    # so the denominator matches the attendance context shown
    # elsewhere in the card.
    # ---------------------------------------------------------
    completed_minutes = 0

    completed_attendance_records = (
        attendances
        .filter(
            class_session__status=ClassSession.STATUS_COMPLETED,
        )
    )


    for attendance in completed_attendance_records:

        class_session = attendance.class_session

        if (
            class_session.start_time
            and class_session.end_time
        ):
            session_duration = (
                class_session.end_time
                - class_session.start_time
            )

            completed_minutes += round(
                session_duration.total_seconds() / 60
            )


    completed_hours = (
        completed_minutes / 60
    )


    completed_whole_hours, completed_remaining_minutes = divmod(
        completed_minutes,
        60,
    )


    if completed_remaining_minutes:
        completed_hours_display = (
            f"{completed_whole_hours}h"
            f"{completed_remaining_minutes:02d}"
        )
    else:
        completed_hours_display = (
            f"{completed_whole_hours}h"
        )

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

        # Employee
        "student": student,
        "student_profile": student_profile,

        # All enrollments -> course selector
        "enrollments": enrollments,

        # Selected enrollment/course
        "enrollment": enrollment,
        "course": course,

        "level_choices": UserProfile.LEVEL_CHOICES,

        # Attendance - Classes
        "attended_count": attended_count,
        "missed_count": missed_count,
        "excused_count": excused_count,
        "total_absences": total_absences,
        "total_attendance_records": total_attendance_records,
        "attendance_percentage": attendance_percentage,

        # Attended Hours
        "attended_hours_display": attended_hours_display,
        "completed_hours_display": completed_hours_display,

        # Progress
        "completed_classes": completed_classes,
        "course_completed_classes": course_completed_classes,
        "remaining_classes": remaining_classes,
        "total_classes": total_classes,
        "completion_percentage": completion_percentage,

        # Late enrollment context
        "lessons_before_enrollment": lessons_before_enrollment,
        "show_enrollment_context": show_enrollment_context,

        # Attendance / absence records
        "recent_attendance": recent_attendance,
        "recent_absences": recent_absences,
    }

    return render(
        request,
        "profiles/company_admin/"
        "company_admin_student_attendance_record.html",
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


    # ---------------------------------------------------------
    # GET ALL ENROLLMENTS FOR THIS EMPLOYEE
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

    enrollments = (
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
        .annotate(
            status_order=Case(
                When(
                    course__status="active",
                    then=Value(1),
                ),
                When(
                    course__status="confirmed",
                    then=Value(2),
                ),
                When(
                    course__status="paused",
                    then=Value(3),
                ),
                When(
                    course__status="completed",
                    then=Value(4),
                ),
                When(
                    course__status="cancelled",
                    then=Value(5),
                ),
                default=Value(99),
                output_field=IntegerField(),
            ),

            completed_date_order=Case(
                When(
                    course__status="completed",
                    then=F("course__end_date"),
                ),
                default=Value(None),
                output_field=DateField(),
            ),
        )
        .order_by(
            "status_order",
            "course__name",
            "-completed_date_order",
        )
    )


    # ---------------------------------------------------------
    # GET SELECTED COURSE FROM URL
    #
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
        context = {
            "profile": profile,
            "company": company,

            "student": student,
            "student_profile": student_profile,

            "enrollments": enrollments,
            "enrollment": None,
            "course": None,

            "skills": [],

            "academic_profile": getattr(
                student,
                "academic_profile",
                None,
            ),

            "chart_data": {
                "labels": [],
                "datasets": [],
            },

            "skill_notes": [],
            "skill_note_display": [],
        }

        return render(
            request,
            "profiles/company_admin/company_admin_student_skills_overview.html",
            context,
        )


    # ---------------------------------------------------------
    # SELECTED COURSE
    # ---------------------------------------------------------

    course = enrollment.course


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
    # EXISTING SKILL ASSESSMENTS
    #
    # IMPORTANT:
    # This may legitimately be empty for a confirmed/new course.
    # We do NOT create assessments here.
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
    # DISPLAY-FRIENDLY NOTES
    #
    # Only existing assessments can have notes.
    # ---------------------------------------------------------

    skill_note_display = [
        build_skill_note_display(skill_assessment)
        for skill_assessment in skill_assessments
    ]


    # ---------------------------------------------------------
    # BUILD ALL FOUR SKILL CARDS
    #
    # This is the important change.
    #
    # Even if no assessment exists yet, Listening, Reading,
    # Speaking and Writing are still added to `skills`.
    # ---------------------------------------------------------

    assessments_by_skill = {
        assessment.skill: assessment
        for assessment in skill_assessments
    }

    skill_areas = [
        ("listening", "Listening"),
        ("reading", "Reading"),
        ("speaking", "Speaking"),
        ("writing", "Writing"),
    ]

    skills = []

    for skill_value, skill_name in skill_areas:

        assessment = assessments_by_skill.get(skill_value)

        # -----------------------------------------------------
        # ASSESSMENT EXISTS
        # -----------------------------------------------------

        if assessment:

            note_display = build_skill_note_display(
                assessment
            )

            skills.append({
                "assessment": assessment,
                "assessment_id": assessment.id,
                "skill_value": skill_value,
                "name": skill_name,

                "icon": skill_icons.get(
                    skill_value,
                    "fa-solid fa-chart-simple",
                ),

                "score": assessment.average_score,

                "teacher_notes": assessment.teacher_notes,

                "subskills": (
                    assessment
                    .subskill_assessments
                    .all()
                ),

                "strengths": note_display["strengths"],
                "confident": note_display["confident"],
                "required_standard": note_display["required_standard"],
                "developing": note_display["developing"],
                "needs_work": note_display["needs_work"],
            })


        # -----------------------------------------------------
        # NO ASSESSMENT YET
        #
        # Still build the card so the UI can show:
        #
        # Listening      —/10
        # 0 subskills assessed yet
        # -----------------------------------------------------

        else:

            skills.append({
                "assessment": None,
                "assessment_id": None,
                "skill_value": skill_value,
                "name": skill_name,

                "icon": skill_icons.get(
                    skill_value,
                    "fa-solid fa-chart-simple",
                ),

                "score": None,
                "teacher_notes": "",

                "subskills": [],

                "strengths": [],
                "confident": [],
                "required_standard": [],
                "developing": [],
                "needs_work": [],
            })


    # ---------------------------------------------------------
    # SKILL NOTES
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

        # Full enrollment list for selector
        "enrollments": enrollments,

        # Selected enrollment/course
        "enrollment": enrollment,
        "course": course,

        # Always contains all four skill cards
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
    # GET ACTIVE ENROLLMENTS
    #
    # Used for the course selector and to ensure the employee
    # belongs to one of this company's active courses.
    # ---------------------------------------------------------
    active_enrollments = (
        CourseEnrollment.objects
        .filter(
            student=student,
            status="active",
            course__status="active",
            course__company=company,
        )
        .select_related(
            "course",
            "course__teacher",
            "course__course_type",
            "course__company",
        )
        .order_by("course__name")
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
            active_enrollments,
            course_id=selected_course_id,
        )
    else:
        enrollment = active_enrollments.first()


    # ---------------------------------------------------------
    # NO ACTIVE ENROLLMENT
    # ---------------------------------------------------------
    if not enrollment:
        context = {
            "profile": profile,
            "company": company,

            "student": student,
            "student_profile": student_profile,

            "active_enrollments": active_enrollments,
            "enrollment": None,
            "course": None,

            "skills": [],
            "skill_notes": [],
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
    # Your original view passed an empty list, so this remains
    # unchanged unless the template actually needs skill data.
    # ---------------------------------------------------------
    skills = []


    # ---------------------------------------------------------
    # TEACHER NOTES
    # ---------------------------------------------------------
    skill_notes = (
        StudentSkillAssessment.objects
        .filter(
            student=student,
            course=course,
        )
        .exclude(teacher_notes="")
        .order_by("skill")
    )


    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------
    context = {
        "profile": profile,
        "company": company,

        "student": student,
        "student_profile": student_profile,

        # Course selector
        "active_enrollments": active_enrollments,

        # Selected enrollment / course
        "enrollment": enrollment,
        "course": course,

        "skills": skills,
        "skill_notes": skill_notes,
        "skill_note_display": skill_note_display,
    }

    return render(
        request,
        "profiles/company_admin/company_admin_student_teacher_notes.html",
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
                "meeting_link": get_calendar_meeting_link(session),
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

    # ---------------------------------------------------------
    # SORT OPTION
    # ---------------------------------------------------------
    sort_by = request.GET.get("sort", "status")

    if sort_by not in ["status", "name", "level"]:
        sort_by = "status"

    # ---------------------------------------------------------
    # ALL COMPANY EMPLOYEES
    #
    # Employees are now retrieved independently from their
    # course enrollments, so they remain visible even when
    # courses are completed / paused / cancelled.
    # ---------------------------------------------------------
    employee_profiles = (
        UserProfile.objects
        .filter(
            company=company,
            role=UserProfile.ROLE_EMPLOYEE,
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
            student__profile__role=UserProfile.ROLE_EMPLOYEE,
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

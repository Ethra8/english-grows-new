
from courses.models import CourseEnrollment


# ---------------------------------------------------------
# ENROLMENT AND COURSE LIFECYCLE
# ---------------------------------------------------------

ONGOING_ENROLLMENT_STATUSES = {
    CourseEnrollment.STATUS_ACTIVE,
    CourseEnrollment.STATUS_PAUSED,
}

TERMINAL_ENROLLMENT_STATUSES = {
    CourseEnrollment.STATUS_COMPLETED,
    CourseEnrollment.STATUS_ENDED_WITHOUT_COMPLETION,
    CourseEnrollment.STATUS_CANCELLED,
}

ONGOING_COURSE_STATUSES = {"confirmed", "active", "paused"}
TERMINAL_COURSE_STATUSES = {"completed", "cancelled"}
KNOWN_COURSE_STATUSES = ONGOING_COURSE_STATUSES | TERMINAL_COURSE_STATUSES


# ---------------------------------------------------------
# RETENTION PERIODS
# ---------------------------------------------------------

def add_calendar_years(value, years):
    """Add calendar years, accounting for leap-day dates."""
    try:
        return value.replace(year=value.year + years)
    except ValueError:
        return value.replace(year=value.year + years, day=28)


def add_24_months(value):
    """Add 24 calendar months for never-enrolled individual learners."""
    return add_calendar_years(value, 2)


def add_36_months(value):
    """Add 36 calendar months for previously enrolled learners."""
    return add_calendar_years(value, 3)


# ---------------------------------------------------------
# LEARNER RETENTION CALCULATOR
# ---------------------------------------------------------

def get_learner_retention_snapshot(user):
    """
    Calculate a learner's potential account-retention deadline.

    Business rules:
    - An ongoing enrolment prevents expiry, regardless of login activity.
    - Never-enrolled individual learners: 24 months from registration,
      reset by a subsequent successful login.
    - Employees without enrolment history require company onboarding review.
    - The most recent enrolment end starts the 36-month period.
    - Only a successful login AFTER that end date restarts the period.
    - Missing or inconsistent historical records require review.
    - Teachers and company administrators are out of scope.

    Placement-test records follow their own retention policy independently
    of the learner account lifecycle.

    Read-only: never modifies records, closes accounts or deletes data.

    A calculated deadline is not authorisation to delete an account.
    """

    result = {
        "status": "needs_review",
        "latest_enrollment_end_at": None,
        "reference_at": None,
        "potential_expiry_at": None,
    }

    # ---------------------------------------------------------
    # 1. VERIFY USER ROLE
    # ---------------------------------------------------------

    profile = getattr(user, "profile", None)

    if profile is None:
        return result

    if profile.role not in {
        profile.ROLE_INDIVIDUAL_LEARNER,
        profile.ROLE_EMPLOYEE,
    }:
        return {**result, "status": "out_of_scope"}

    # ---------------------------------------------------------
    # 2. RETRIEVE ALL ENROLMENTS
    # ---------------------------------------------------------

    enrollments = list(
        CourseEnrollment.objects
        .filter(student=user)
        .select_related("course")
    )

    # ---------------------------------------------------------
    # 3. ACCOUNTS WITHOUT ENROLMENT HISTORY
    # ---------------------------------------------------------

    if not enrollments:
        # Employees may be awaiting company-managed onboarding
        # or course assignment without ever accessing the platform.
        if profile.role == profile.ROLE_EMPLOYEE:
            return {**result, "status": "company_onboarding_review"}

        # Individual learners: registration starts the 24-month period.
        reference_at = user.date_joined

        # Only a successful login after registration resets the period.
        if user.last_login and user.last_login > reference_at:
            reference_at = user.last_login

        return {
            "status": "never_enrolled",
            "latest_enrollment_end_at": None,
            "reference_at": reference_at,
            "potential_expiry_at": add_24_months(reference_at),
        }

    # ---------------------------------------------------------
    # 4. ONGOING TRAINING ALWAYS PREVENTS EXPIRY
    # ---------------------------------------------------------

    if any(
        enrollment.status in ONGOING_ENROLLMENT_STATUSES
        and enrollment.course.status in ONGOING_COURSE_STATUSES
        for enrollment in enrollments
    ):
        return {**result, "status": "ongoing_enrollment"}

    # ---------------------------------------------------------
    # 5. VALIDATE HISTORICAL RECORDS
    # ---------------------------------------------------------

    if any(
        enrollment.status not in TERMINAL_ENROLLMENT_STATUSES
        or enrollment.course.status not in KNOWN_COURSE_STATUSES
        or enrollment.ended_at is None
        for enrollment in enrollments
    ):
        return result

    # ---------------------------------------------------------
    # 6. MOST RECENT ENROLMENT END
    # ---------------------------------------------------------

    # The end of the most recent training relationship is always
    # the INITIAL reference date, regardless of previous logins.
    latest_end = max(
        enrollment.ended_at
        for enrollment in enrollments
    )

    reference_at = latest_end

    # ---------------------------------------------------------
    # 7. SUBSEQUENT AUTHENTICATED LOGIN
    # ---------------------------------------------------------

    # A login only extends retention if it occurred AFTER the
    # most recent enrolment ended.
    #
    # Logins before or during training do not affect the
    # post-training retention period.
    #
    # Learners who never log in are not penalised.

    if user.last_login and user.last_login > latest_end:
        reference_at = user.last_login

    # ---------------------------------------------------------
    # 8. CALCULATE POTENTIAL RETENTION DEADLINE
    # ---------------------------------------------------------

    return {
        "status": "calculable",
        "latest_enrollment_end_at": latest_end,
        "reference_at": reference_at,
        "potential_expiry_at": add_36_months(reference_at),
    }

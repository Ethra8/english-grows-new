
from datetime import datetime, timezone as dt_timezone

from django.contrib.auth import get_user_model
from django.test import TestCase

from courses.models import Course, CourseEnrollment, CourseType
from profiles.models import UserProfile
from profiles.utils.learner_account_retention import get_learner_retention_snapshot


class LearnerAccountRetentionTests(TestCase):
    """Test the read-only learner account-retention calculator."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user = User.objects.create_user(
            username="retention_learner",
            email="retention@example.com",
            password="test-password",
        )

        cls.profile, _ = UserProfile.objects.get_or_create(user=cls.user)
        cls.profile.role = UserProfile.ROLE_INDIVIDUAL_LEARNER
        cls.profile.save(update_fields=["role"])

        cls.course_type = CourseType.objects.create(
            name="Retention Test Course Type",
            is_for_individual=True,
        )

        cls.course = Course.objects.create(
            name="Retention Test Course",
            course_type=cls.course_type,
            status="confirmed",
        )

        cls.enrollment = CourseEnrollment.objects.create(
            student=cls.user,
            course=cls.course,
            status=CourseEnrollment.STATUS_ACTIVE,
        )

    def set_ended_enrollment(
        self,
        ended_at,
        status=CourseEnrollment.STATUS_COMPLETED,
        course_status="completed",
    ):
        """Prepare a historical enrolment without triggering lifecycle side effects."""
        CourseEnrollment.objects.filter(pk=self.enrollment.pk).update(
            status=status,
            ended_at=ended_at,
        )
        Course.objects.filter(pk=self.course.pk).update(status=course_status)

    # ---------------------------------------------------------
    # ONGOING TRAINING PROTECTS THE ACCOUNT
    # ---------------------------------------------------------

    def test_active_enrollment_prevents_expiry_without_login(self):
        self.assertIsNone(self.user.last_login)

        result = get_learner_retention_snapshot(self.user)

        self.assertEqual(result["status"], "ongoing_enrollment")
        self.assertIsNone(result["reference_at"])
        self.assertIsNone(result["potential_expiry_at"])

    def test_paused_enrollment_prevents_expiry_without_login(self):
        CourseEnrollment.objects.filter(pk=self.enrollment.pk).update(
            status=CourseEnrollment.STATUS_PAUSED,
        )

        result = get_learner_retention_snapshot(self.user)

        self.assertEqual(result["status"], "ongoing_enrollment")
        self.assertIsNone(result["potential_expiry_at"])

    # ---------------------------------------------------------
    # COURSE COMPLETION STARTS THE 36-MONTH RETENTION PERIOD
    # ---------------------------------------------------------

    def test_completed_course_without_login_starts_retention(self):
        """A learner may complete training through Teams/Zoom without logging in."""
        ended_at = datetime(2024, 6, 30, 12, 0, tzinfo=dt_timezone.utc)
        self.set_ended_enrollment(ended_at)

        result = get_learner_retention_snapshot(self.user)

        self.assertEqual(result["status"], "calculable")
        self.assertEqual(result["latest_enrollment_end_at"], ended_at)
        self.assertEqual(result["reference_at"], ended_at)
        self.assertEqual(
            result["potential_expiry_at"],
            datetime(2027, 6, 30, 12, 0, tzinfo=dt_timezone.utc),
        )

    def test_login_before_course_completion_does_not_extend_retention(self):
        ended_at = datetime(2024, 6, 30, 12, 0, tzinfo=dt_timezone.utc)
        earlier_login = datetime(2024, 3, 15, 10, 0, tzinfo=dt_timezone.utc)

        self.set_ended_enrollment(ended_at)
        type(self.user).objects.filter(pk=self.user.pk).update(
            last_login=earlier_login,
        )
        self.user.refresh_from_db()

        result = get_learner_retention_snapshot(self.user)

        self.assertEqual(result["reference_at"], ended_at)
        self.assertEqual(
            result["potential_expiry_at"],
            datetime(2027, 6, 30, 12, 0, tzinfo=dt_timezone.utc),
        )

    def test_login_after_course_completion_extends_retention(self):
        ended_at = datetime(2024, 6, 30, 12, 0, tzinfo=dt_timezone.utc)
        later_login = datetime(2025, 2, 10, 9, 0, tzinfo=dt_timezone.utc)

        self.set_ended_enrollment(ended_at)
        type(self.user).objects.filter(pk=self.user.pk).update(
            last_login=later_login,
        )
        self.user.refresh_from_db()

        result = get_learner_retention_snapshot(self.user)

        self.assertEqual(result["latest_enrollment_end_at"], ended_at)
        self.assertEqual(result["reference_at"], later_login)
        self.assertEqual(
            result["potential_expiry_at"],
            datetime(2028, 2, 10, 9, 0, tzinfo=dt_timezone.utc),
        )

    def test_login_at_exact_completion_time_does_not_reset_reference(self):
        ended_at = datetime(2024, 6, 30, 12, 0, tzinfo=dt_timezone.utc)

        self.set_ended_enrollment(ended_at)
        type(self.user).objects.filter(pk=self.user.pk).update(
            last_login=ended_at,
        )
        self.user.refresh_from_db()

        result = get_learner_retention_snapshot(self.user)

        self.assertEqual(result["reference_at"], ended_at)

    # ---------------------------------------------------------
    # MULTIPLE COURSES
    # ---------------------------------------------------------

    def test_most_recent_enrollment_end_takes_precedence(self):
        first_end = datetime(2023, 6, 30, 12, 0, tzinfo=dt_timezone.utc)
        later_login = datetime(2023, 9, 15, 9, 0, tzinfo=dt_timezone.utc)
        second_end = datetime(2024, 6, 30, 12, 0, tzinfo=dt_timezone.utc)

        self.set_ended_enrollment(first_end)
        type(self.user).objects.filter(pk=self.user.pk).update(
            last_login=later_login,
        )
        self.user.refresh_from_db()

        second_course = Course.objects.create(
            name="Second Retention Test Course",
            course_type=self.course_type,
            status="confirmed",
        )
        Course.objects.filter(pk=second_course.pk).update(status="completed")

        second_enrollment = CourseEnrollment.objects.create(
            student=self.user,
            course=second_course,
            status=CourseEnrollment.STATUS_ACTIVE,
        )
        CourseEnrollment.objects.filter(pk=second_enrollment.pk).update(
            status=CourseEnrollment.STATUS_COMPLETED,
            ended_at=second_end,
        )

        result = get_learner_retention_snapshot(self.user)

        # A login after the first course but before the second course ended
        # must not override the most recent training relationship.
        self.assertEqual(result["latest_enrollment_end_at"], second_end)
        self.assertEqual(result["reference_at"], second_end)
        self.assertEqual(
            result["potential_expiry_at"],
            datetime(2027, 6, 30, 12, 0, tzinfo=dt_timezone.utc),
        )

    # ---------------------------------------------------------
    # OTHER TERMINAL ENROLMENT STATUSES
    # ---------------------------------------------------------

    def test_other_terminal_enrollment_statuses_are_calculable(self):
        ended_at = datetime(2024, 6, 30, 12, 0, tzinfo=dt_timezone.utc)

        scenarios = (
            (CourseEnrollment.STATUS_ENDED_WITHOUT_COMPLETION, "completed"),
            (CourseEnrollment.STATUS_CANCELLED, "cancelled"),
        )

        for enrollment_status, course_status in scenarios:
            with self.subTest(enrollment_status=enrollment_status):
                self.set_ended_enrollment(
                    ended_at,
                    status=enrollment_status,
                    course_status=course_status,
                )

                result = get_learner_retention_snapshot(self.user)

                self.assertEqual(result["status"], "calculable")
                self.assertEqual(result["reference_at"], ended_at)

    # ---------------------------------------------------------
    # HISTORICAL DATA SAFEGUARDS
    # ---------------------------------------------------------

    def test_missing_historical_end_date_requires_review(self):
        self.set_ended_enrollment(None)

        result = get_learner_retention_snapshot(self.user)

        self.assertEqual(result["status"], "needs_review")
        self.assertIsNone(result["potential_expiry_at"])

    def test_terminal_course_with_ongoing_enrollment_requires_review(self):
        for enrollment_status in (
            CourseEnrollment.STATUS_ACTIVE,
            CourseEnrollment.STATUS_PAUSED,
        ):
            with self.subTest(enrollment_status=enrollment_status):
                CourseEnrollment.objects.filter(pk=self.enrollment.pk).update(
                    status=enrollment_status,
                    ended_at=None,
                )
                Course.objects.filter(pk=self.course.pk).update(status="completed")

                result = get_learner_retention_snapshot(self.user)

                self.assertEqual(result["status"], "needs_review")
                self.assertIsNone(result["potential_expiry_at"])

    # ---------------------------------------------------------
    # NEVER-ENROLLED INDIVIDUAL LEARNERS — 24 MONTHS
    # ---------------------------------------------------------

    def test_never_enrolled_account_uses_registration_date(self):
        self.enrollment.delete()

        joined_at = datetime(2024, 10, 1, 12, 0, tzinfo=dt_timezone.utc)

        type(self.user).objects.filter(pk=self.user.pk).update(
            date_joined=joined_at,
            last_login=None,
        )
        self.user.refresh_from_db()

        result = get_learner_retention_snapshot(self.user)

        self.assertEqual(result["status"], "never_enrolled")
        self.assertIsNone(result["latest_enrollment_end_at"])
        self.assertEqual(result["reference_at"], joined_at)
        self.assertEqual(
            result["potential_expiry_at"],
            datetime(2026, 10, 1, 12, 0, tzinfo=dt_timezone.utc),
        )

    def test_never_enrolled_login_restarts_24_month_period(self):
        self.enrollment.delete()

        joined_at = datetime(2024, 10, 1, 12, 0, tzinfo=dt_timezone.utc)
        later_login = datetime(2025, 9, 15, 9, 0, tzinfo=dt_timezone.utc)

        type(self.user).objects.filter(pk=self.user.pk).update(
            date_joined=joined_at,
            last_login=later_login,
        )
        self.user.refresh_from_db()

        result = get_learner_retention_snapshot(self.user)

        self.assertEqual(result["status"], "never_enrolled")
        self.assertIsNone(result["latest_enrollment_end_at"])
        self.assertEqual(result["reference_at"], later_login)
        self.assertEqual(
            result["potential_expiry_at"],
            datetime(2027, 9, 15, 9, 0, tzinfo=dt_timezone.utc),
        )

    def test_never_enrolled_leap_day_registration(self):
        self.enrollment.delete()

        joined_at = datetime(2024, 2, 29, 12, 0, tzinfo=dt_timezone.utc)

        type(self.user).objects.filter(pk=self.user.pk).update(
            date_joined=joined_at,
            last_login=None,
        )
        self.user.refresh_from_db()

        result = get_learner_retention_snapshot(self.user)

        self.assertEqual(result["status"], "never_enrolled")
        self.assertEqual(
            result["potential_expiry_at"],
            datetime(2026, 2, 28, 12, 0, tzinfo=dt_timezone.utc),
        )

    # ---------------------------------------------------------
    # USER ROLES AND COMPANY ONBOARDING
    # ---------------------------------------------------------

    def test_teacher_and_company_admin_are_out_of_scope(self):
        for role in (
            UserProfile.ROLE_TEACHER,
            UserProfile.ROLE_COMPANY_ADMIN,
        ):
            with self.subTest(role=role):
                # Update the role directly in the test database.
                UserProfile.objects.filter(user=self.user).update(role=role)

                # Retrieve a fresh User to avoid cached profile information.
                fresh_user = get_user_model().objects.get(pk=self.user.pk)

                result = get_learner_retention_snapshot(fresh_user)

                self.assertEqual(result["status"], "out_of_scope")
                self.assertIsNone(result["potential_expiry_at"])

    def test_employee_without_enrollment_requires_onboarding_review(self):
        # Simulate an employee whose account exists before course assignment.
        self.enrollment.delete()

        UserProfile.objects.filter(user=self.user).update(
            role=UserProfile.ROLE_EMPLOYEE,
        )

        # Retrieve a fresh User to avoid a cached profile relationship.
        fresh_user = get_user_model().objects.get(pk=self.user.pk)

        result = get_learner_retention_snapshot(fresh_user)

        self.assertEqual(result["status"], "company_onboarding_review")
        self.assertIsNone(result["latest_enrollment_end_at"])
        self.assertIsNone(result["reference_at"])
        self.assertIsNone(result["potential_expiry_at"])

    # ---------------------------------------------------------
    # CALENDAR ACCURACY — 36 MONTHS
    # ---------------------------------------------------------

    def test_leap_day_is_handled_correctly(self):
        ended_at = datetime(2024, 2, 29, 12, 0, tzinfo=dt_timezone.utc)
        self.set_ended_enrollment(ended_at)

        result = get_learner_retention_snapshot(self.user)

        self.assertEqual(
            result["potential_expiry_at"],
            datetime(2027, 2, 28, 12, 0, tzinfo=dt_timezone.utc),
        )

    # ---------------------------------------------------------
    # READ-ONLY GUARANTEE
    # ---------------------------------------------------------

    def test_calculator_does_not_modify_database_records(self):
        ended_at = datetime(2024, 6, 30, 12, 0, tzinfo=dt_timezone.utc)
        self.set_ended_enrollment(ended_at)

        get_learner_retention_snapshot(self.user)

        self.enrollment.refresh_from_db()
        self.course.refresh_from_db()

        self.assertEqual(
            self.enrollment.status,
            CourseEnrollment.STATUS_COMPLETED,
        )
        self.assertEqual(self.enrollment.ended_at, ended_at)
        self.assertEqual(self.course.status, "completed")

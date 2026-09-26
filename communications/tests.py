from io import StringIO

from django.core.management import call_command
from datetime import date, datetime, time, timedelta, timezone as dt_timezone
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.utils import timezone

from communications.models import EmailTemplate, LearnerAccountClosureNotice
from communications.services import send_learner_account_closure_notice
from courses.models import Course, CourseEnrollment, CourseType
from profiles.models import UserProfile


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    SITE_URL="https://www.englishgrows.com",
    TIME_ZONE="Europe/Madrid",
)
class LearnerAccountClosureNoticeTests(TestCase):
    """Test closure notices without sending emails outside Django."""

    TODAY = date(2026, 9, 25)
    NOW = datetime(2026, 9, 25, 10, 0, tzinfo=dt_timezone.utc)

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.user = User.objects.create_user(
            username="closure_learner",
            email="emma@example.com",
            first_name="Emma",
            password="test-password",
        )

        profile, _ = UserProfile.objects.get_or_create(user=cls.user)
        profile.role = UserProfile.ROLE_INDIVIDUAL_LEARNER
        profile.save(update_fields=["role"])

        cls.email_template = EmailTemplate.objects.create(
            name="Learner Account Closure Notice",
            subject="Your English Grows account — 30-day closure notice",
            heading="Keep your English Grows account active",
            body_html=(
                "<p>Hi {{ first_name }},</p>"
                "<p>Closure: {{ closure_date }}</p>"
                "<p>[[CTA]]</p>"
            ),
            body_text=(
                "Hi {{ first_name }}.\n"
                "Closure: {{ closure_date }}\n"
                "[[CTA]]"
            ),
            is_active=True,
        )

    def setUp(self):
        date_patcher = patch(
            "communications.services.timezone.localdate",
            return_value=self.TODAY,
        )
        date_patcher.start()
        self.addCleanup(date_patcher.stop)

        time_patcher = patch(
            "communications.services.timezone.now",
            return_value=self.NOW,
        )
        time_patcher.start()
        self.addCleanup(time_patcher.stop)

    def set_registration_date(self, year, month, day):
        """Prepare a never-enrolled learner with no subsequent login."""
        joined_at = datetime(
            year, month, day, 12, 0,
            tzinfo=dt_timezone.utc,
        )

        get_user_model().objects.filter(pk=self.user.pk).update(
            date_joined=joined_at,
            last_login=None,
        )

        return joined_at

    def create_enrollment(
        self,
        status=CourseEnrollment.STATUS_ACTIVE,
        course_status="confirmed",
        ended_at=None,
    ):
        """Create an enrolment and prepare its lifecycle state."""
        course_type = CourseType.objects.create(
            name="Closure Notice Test Course Type",
            is_for_individual=True,
        )

        course = Course.objects.create(
            name="Closure Notice Test Course",
            course_type=course_type,
            status="confirmed",
        )

        enrollment = CourseEnrollment.objects.create(
            student=self.user,
            course=course,
            status=CourseEnrollment.STATUS_ACTIVE,
        )

        # Set historical states without invoking lifecycle side effects.
        CourseEnrollment.objects.filter(pk=enrollment.pk).update(
            status=status,
            ended_at=ended_at,
        )
        Course.objects.filter(pk=course.pk).update(status=course_status)

        return enrollment

    # ---------------------------------------------------------
    # NOTIFICATION WINDOW
    # ---------------------------------------------------------

    def test_sends_at_30_day_boundary_with_branded_cta(self):
        # Registration: 25 October 2024.
        # Expiry: 25 October 2026, exactly 30 days from TODAY.
        reference_at = self.set_registration_date(2024, 10, 25)

        sent = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(sent, 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            self.email_template.key,
            "learner_account_closure_notice",
        )

        notice = LearnerAccountClosureNotice.objects.get(user=self.user)

        self.assertEqual(notice.status, LearnerAccountClosureNotice.STATUS_SENT)
        self.assertEqual(notice.reference_at, reference_at)
        self.assertEqual(
            notice.potential_expiry_at,
            datetime(2026, 10, 25, 12, 0, tzinfo=dt_timezone.utc),
        )
        self.assertEqual(notice.recipient_email, "emma@example.com")
        self.assertIsNotNone(notice.sent_at)

        email = mail.outbox[0]
        html = email.alternatives[0][0]
        login_url = "https://www.englishgrows.com/accounts/login/"

        self.assertEqual(email.to, ["emma@example.com"])
        self.assertEqual(
            email.subject,
            "Your English Grows account — 30-day closure notice",
        )

        # Database template variables and CKEditor CTA are rendered.
        self.assertIn("Hi Emma", html)
        self.assertIn("25 October 2026", html)
        self.assertIn("Keep your English Grows account active", html)
        self.assertIn(f'href="{login_url}"', html)
        self.assertIn("Sign in to my account", html)
        self.assertNotIn("[[CTA]]", html)

        # The plain-text alternative also includes the login link.
        self.assertIn("Hi Emma", email.body)
        self.assertIn("Sign in to my account", email.body)
        self.assertIn(login_url, email.body)
        self.assertNotIn("[[CTA]]", email.body)

    def test_recovers_notice_one_day_before_original_deadline(self):
        self.set_registration_date(2024, 9, 26)

        sent = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(sent, 1)
        self.assertEqual(len(mail.outbox), 1)

        notice = LearnerAccountClosureNotice.objects.get(user=self.user)

        self.assertEqual(notice.status, LearnerAccountClosureNotice.STATUS_SENT)
        self.assertEqual(
            notice.potential_expiry_at,
            datetime(2026, 9, 26, 12, 0, tzinfo=dt_timezone.utc),
        )
        local_closure = timezone.localtime(
            notice.effective_closure_at,
            timezone.get_default_timezone(),
        )

        self.assertEqual(local_closure.date(), date(2026, 10, 25))
        self.assertEqual(local_closure.time(), time(23, 59))
        self.assertGreaterEqual(
            notice.effective_closure_at,
            notice.potential_expiry_at,
        )

        html = mail.outbox[0].alternatives[0][0]
        self.assertIn("25 October 2026", html)

    def test_does_not_send_31_days_before_deadline(self):
        self.set_registration_date(2024, 10, 26)

        sent = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(sent, 0)
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(LearnerAccountClosureNotice.objects.exists())

    def test_recovers_notice_on_original_deadline(self):
        self.set_registration_date(2024, 9, 25)

        sent = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(sent, 1)
        self.assertEqual(len(mail.outbox), 1)

        notice = LearnerAccountClosureNotice.objects.get(user=self.user)

        self.assertEqual(notice.potential_expiry_at.date(), self.TODAY)
        self.assertEqual(notice.status, LearnerAccountClosureNotice.STATUS_SENT)

        local_closure = timezone.localtime(
            notice.effective_closure_at,
            timezone.get_default_timezone(),
        )

        self.assertEqual(local_closure.date(), date(2026, 10, 25))
        self.assertEqual(local_closure.time(), time(23, 59))
        self.assertGreaterEqual(
            notice.effective_closure_at,
            notice.sent_at + timedelta(days=30),
        )

    def test_recovers_notice_after_original_deadline(self):
        self.set_registration_date(2024, 9, 24)

        sent = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(sent, 1)
        self.assertEqual(len(mail.outbox), 1)

        notice = LearnerAccountClosureNotice.objects.get(user=self.user)

        self.assertEqual(
            notice.potential_expiry_at.date(),
            date(2026, 9, 24),
        )
        self.assertEqual(notice.status, LearnerAccountClosureNotice.STATUS_SENT)
        self.assertGreaterEqual(
            notice.effective_closure_at,
            notice.sent_at + timedelta(days=30),
        )
    # ---------------------------------------------------------
    # DUPLICATE PREVENTION AND CHANGED RETENTION PERIODS
    # ---------------------------------------------------------

    def test_repeated_calls_send_only_one_notice(self):
        self.set_registration_date(2024, 10, 25)

        first_result = send_learner_account_closure_notice(self.user.pk)
        second_result = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(first_result, 1)
        self.assertEqual(second_result, 0)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(LearnerAccountClosureNotice.objects.count(), 1)

    def test_subsequent_login_changes_retention_period(self):
        self.set_registration_date(2024, 10, 25)

        self.assertEqual(
            send_learner_account_closure_notice(self.user.pk),
            1,
        )

        # The learner signs in after receiving the notice.
        later_login = datetime(
            2026, 9, 25, 15, 0,
            tzinfo=dt_timezone.utc,
        )

        get_user_model().objects.filter(pk=self.user.pk).update(
            last_login=later_login,
        )

        # The new expiry is in September 2028, outside the notice window.
        sent = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(sent, 0)
        self.assertEqual(len(mail.outbox), 1)

        # The original notice remains as historical evidence.
        self.assertEqual(LearnerAccountClosureNotice.objects.count(), 1)

    # ---------------------------------------------------------
    # PREVIOUSLY ENROLLED LEARNERS — 36 MONTHS
    # ---------------------------------------------------------

    def test_former_learner_uses_36_month_deadline(self):
        ended_at = datetime(
            2023, 10, 25, 12, 0,
            tzinfo=dt_timezone.utc,
        )

        self.create_enrollment(
            status=CourseEnrollment.STATUS_COMPLETED,
            course_status="completed",
            ended_at=ended_at,
        )

        sent = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(sent, 1)
        self.assertEqual(len(mail.outbox), 1)

        notice = LearnerAccountClosureNotice.objects.get(user=self.user)

        self.assertEqual(notice.reference_at, ended_at)
        self.assertEqual(
            notice.potential_expiry_at,
            datetime(2026, 10, 25, 12, 0, tzinfo=dt_timezone.utc),
        )

    # ---------------------------------------------------------
    # PROTECTED ACCOUNTS
    # ---------------------------------------------------------

    def test_ongoing_enrollment_prevents_notification(self):
        enrollment = self.create_enrollment()

        for status in (
            CourseEnrollment.STATUS_ACTIVE,
            CourseEnrollment.STATUS_PAUSED,
        ):
            with self.subTest(status=status):
                CourseEnrollment.objects.filter(pk=enrollment.pk).update(
                    status=status,
                )

                sent = send_learner_account_closure_notice(self.user.pk)

                self.assertEqual(sent, 0)
                self.assertEqual(len(mail.outbox), 0)
                self.assertFalse(LearnerAccountClosureNotice.objects.exists())

    def test_employee_awaiting_onboarding_receives_no_notice(self):
        self.set_registration_date(2024, 10, 25)

        UserProfile.objects.filter(user=self.user).update(
            role=UserProfile.ROLE_EMPLOYEE,
        )

        sent = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(sent, 0)
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(LearnerAccountClosureNotice.objects.exists())

    def test_inconsistent_historical_records_prevent_notification(self):
        self.create_enrollment(
            status=CourseEnrollment.STATUS_COMPLETED,
            course_status="completed",
            ended_at=None,
        )

        sent = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(sent, 0)
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(LearnerAccountClosureNotice.objects.exists())

    def test_teacher_and_company_admin_receive_no_notice(self):
        self.set_registration_date(2024, 10, 25)

        for role in (
            UserProfile.ROLE_TEACHER,
            UserProfile.ROLE_COMPANY_ADMIN,
        ):
            with self.subTest(role=role):
                UserProfile.objects.filter(user=self.user).update(role=role)

                sent = send_learner_account_closure_notice(self.user.pk)

                self.assertEqual(sent, 0)
                self.assertEqual(len(mail.outbox), 0)
                self.assertFalse(LearnerAccountClosureNotice.objects.exists())

    def test_inactive_user_or_missing_email_receives_no_notice(self):
        self.set_registration_date(2024, 10, 25)

        User = get_user_model()

        # Inactive account.
        User.objects.filter(pk=self.user.pk).update(is_active=False)

        self.assertEqual(
            send_learner_account_closure_notice(self.user.pk),
            0,
        )

        # Active account without an email address.
        User.objects.filter(pk=self.user.pk).update(
            is_active=True,
            email="",
        )

        self.assertEqual(
            send_learner_account_closure_notice(self.user.pk),
            0,
        )

        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(LearnerAccountClosureNotice.objects.exists())

    # ---------------------------------------------------------
    # FAILURE HANDLING
    # ---------------------------------------------------------

    def test_failed_send_is_recorded_without_automatic_retry(self):
        self.set_registration_date(2024, 10, 25)

        with patch(
            "communications.services.send_template_email",
            side_effect=RuntimeError("Simulated email failure"),
        ) as mocked_sender:
            with self.assertLogs("communications.services", level="ERROR"):
                first_result = send_learner_account_closure_notice(self.user.pk)

            second_result = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(first_result, 0)
        self.assertEqual(second_result, 0)
        self.assertEqual(mocked_sender.call_count, 1)
        self.assertEqual(len(mail.outbox), 0)

        notice = LearnerAccountClosureNotice.objects.get(user=self.user)

        self.assertEqual(notice.status, LearnerAccountClosureNotice.STATUS_FAILED)
        self.assertIsNone(notice.sent_at)

    def test_inactive_email_template_records_failed_attempt(self):
        self.set_registration_date(2024, 10, 25)

        EmailTemplate.objects.filter(pk=self.email_template.pk).update(
            is_active=False,
        )

        with self.assertLogs("communications.services", level="ERROR"):
            sent = send_learner_account_closure_notice(self.user.pk)

        self.assertEqual(sent, 0)
        self.assertEqual(len(mail.outbox), 0)

        notice = LearnerAccountClosureNotice.objects.get(user=self.user)

        self.assertEqual(notice.status, LearnerAccountClosureNotice.STATUS_FAILED)
        self.assertIsNone(notice.sent_at)


    # ---------------------------------------------------------
    # MANAGEMENT COMMAND — READ-ONLY PREVIEW
    # ---------------------------------------------------------

    def test_preview_identifies_eligible_learner_without_sending(self):
        self.set_registration_date(2024, 10, 25)
        output = StringIO()

        call_command("process_learner_closure_notices", stdout=output)

        self.assertIn("Eligible accounts: 1", output.getvalue())
        self.assertIn("Ready for notification: 1", output.getvalue())
        self.assertIn("Days remaining: 30", output.getvalue())
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(LearnerAccountClosureNotice.objects.exists())

    def test_preview_excludes_learner_outside_notification_window(self):
        self.set_registration_date(2024, 10, 26)
        output = StringIO()

        call_command("process_learner_closure_notices", stdout=output)

        self.assertIn("Eligible accounts: 0", output.getvalue())
        self.assertIn("Ready for notification: 0", output.getvalue())
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(LearnerAccountClosureNotice.objects.exists())

    def test_preview_identifies_previously_recorded_notice(self):
        reference_at = self.set_registration_date(2024, 10, 25)

        LearnerAccountClosureNotice.objects.create(
            user=self.user,
            reference_at=reference_at,
            potential_expiry_at=datetime(
                2026, 10, 25, 12, 0,
                tzinfo=dt_timezone.utc,
            ),
            recipient_email=self.user.email,
            status=LearnerAccountClosureNotice.STATUS_SENT,
        )

        output = StringIO()

        call_command("process_learner_closure_notices", stdout=output)

        self.assertIn("Eligible accounts: 1", output.getvalue())
        self.assertIn("Previously recorded: 1", output.getvalue())
        self.assertIn("Ready for notification: 0", output.getvalue())
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(LearnerAccountClosureNotice.objects.count(), 1)

    def test_preview_excludes_ongoing_enrollment(self):
        self.set_registration_date(2024, 10, 25)
        self.create_enrollment()
        output = StringIO()

        call_command("process_learner_closure_notices", stdout=output)

        self.assertIn("Eligible accounts: 0", output.getvalue())
        self.assertIn("Ready for notification: 0", output.getvalue())
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(LearnerAccountClosureNotice.objects.exists())

    def test_preview_excludes_employee_awaiting_onboarding(self):
        self.set_registration_date(2024, 10, 25)

        UserProfile.objects.filter(user=self.user).update(
            role=UserProfile.ROLE_EMPLOYEE,
        )

        output = StringIO()

        call_command("process_learner_closure_notices", stdout=output)

        self.assertIn("Eligible accounts: 0", output.getvalue())
        self.assertIn("Ready for notification: 0", output.getvalue())
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(LearnerAccountClosureNotice.objects.exists())


    # ---------------------------------------------------------
    # MANAGEMENT COMMAND — EXPLICIT SENDING MODE
    # ---------------------------------------------------------

    def test_send_option_sends_eligible_notice(self):
        self.set_registration_date(2024, 10, 25)
        output = StringIO()

        call_command(
            "process_learner_closure_notices",
            "--send",
            stdout=output,
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Emails sent: 1", output.getvalue())
        self.assertIn("Not sent: 0", output.getvalue())

        notice = LearnerAccountClosureNotice.objects.get(user=self.user)

        self.assertEqual(
            notice.status,
            LearnerAccountClosureNotice.STATUS_SENT,
        )
        self.assertIsNotNone(notice.sent_at)
        self.assertEqual(notice.recipient_email, "emma@example.com")

    def test_send_option_prevents_duplicate_notifications(self):
        self.set_registration_date(2024, 10, 25)

        call_command(
            "process_learner_closure_notices",
            "--send",
            stdout=StringIO(),
        )

        second_output = StringIO()

        call_command(
            "process_learner_closure_notices",
            "--send",
            stdout=second_output,
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(LearnerAccountClosureNotice.objects.count(), 1)
        self.assertIn("Previously recorded: 1", second_output.getvalue())
        self.assertIn("Emails sent: 0", second_output.getvalue())

    def test_send_option_records_failure_without_retry(self):
        self.set_registration_date(2024, 10, 25)

        with patch(
            "communications.services.send_template_email",
            side_effect=RuntimeError("Simulated email failure"),
        ) as mocked_sender:
            with self.assertLogs("communications.services", level="ERROR"):
                call_command(
                    "process_learner_closure_notices",
                    "--send",
                    stdout=StringIO(),
                )

            # A second execution must not retry an uncertain delivery.
            call_command(
                "process_learner_closure_notices",
                "--send",
                stdout=StringIO(),
            )

        self.assertEqual(mocked_sender.call_count, 1)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(LearnerAccountClosureNotice.objects.count(), 1)

        notice = LearnerAccountClosureNotice.objects.get(user=self.user)

        self.assertEqual(
            notice.status,
            LearnerAccountClosureNotice.STATUS_FAILED,
        )
        self.assertIsNone(notice.sent_at)

    def test_send_option_excludes_ongoing_enrollment(self):
        self.set_registration_date(2024, 10, 25)
        self.create_enrollment()
        output = StringIO()

        call_command(
            "process_learner_closure_notices",
            "--send",
            stdout=output,
        )

        self.assertIn("Eligible accounts: 0", output.getvalue())
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(LearnerAccountClosureNotice.objects.exists())

    def test_send_option_excludes_employee_awaiting_onboarding(self):
        self.set_registration_date(2024, 10, 25)

        UserProfile.objects.filter(user=self.user).update(
            role=UserProfile.ROLE_EMPLOYEE,
        )

        output = StringIO()

        call_command(
            "process_learner_closure_notices",
            "--send",
            stdout=output,
        )

        self.assertIn("Eligible accounts: 0", output.getvalue())
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(LearnerAccountClosureNotice.objects.exists())



    # ---------------------------------------------------------
    # MANAGEMENT COMMAND — MISSED NOTIFICATION RECOVERY
    # ---------------------------------------------------------

    def test_preview_identifies_missed_notice_without_sending(self):
        # Original deadline: 20 September 2026.
        # Test date: 25 September 2026, five days overdue.
        self.set_registration_date(2024, 9, 20)
        output = StringIO()

        call_command("process_learner_closure_notices", stdout=output)

        self.assertIn("Eligible accounts: 1", output.getvalue())
        self.assertIn("Ready for notification: 1", output.getvalue())
        self.assertIn("Recovery candidates: 1", output.getvalue())
        self.assertIn("Timing: RECOVERY", output.getvalue())
        self.assertIn("Original deadline: 2026-09-20", output.getvalue())
        self.assertIn("Days remaining: -5", output.getvalue())

        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(LearnerAccountClosureNotice.objects.exists())

    def test_send_option_recovers_missed_notice_and_prevents_duplicates(self):
        self.set_registration_date(2024, 9, 20)
        output = StringIO()

        call_command(
            "process_learner_closure_notices",
            "--send",
            stdout=output,
        )

        self.assertIn("Recovery candidates: 1", output.getvalue())
        self.assertIn("Emails sent: 1", output.getvalue())
        self.assertEqual(len(mail.outbox), 1)

        notice = LearnerAccountClosureNotice.objects.get(user=self.user)

        self.assertEqual(notice.status, LearnerAccountClosureNotice.STATUS_SENT)
        self.assertEqual(
            notice.potential_expiry_at.date(),
            date(2026, 9, 20),
        )
        self.assertIsNotNone(notice.sent_at)

        # Recovery preserves 30 days and schedules closure at 23:59
        # in the configured local time zone.
        local_closure = timezone.localtime(
            notice.effective_closure_at,
            timezone.get_default_timezone(),
        )

        self.assertEqual(local_closure.date(), date(2026, 10, 25))
        self.assertEqual(local_closure.time(), time(23, 59))
        self.assertGreaterEqual(
            notice.effective_closure_at,
            notice.sent_at + timedelta(days=30),
        )

        # The learner receives the extended date, not the old deadline.
        html = mail.outbox[0].alternatives[0][0]
        self.assertIn("25 October 2026", html)
        self.assertIn(
            'href="https://www.englishgrows.com/accounts/login/"',
            html,
        )
        self.assertNotIn("[[CTA]]", html)

        # Running the command again must not resend the notice.
        second_output = StringIO()

        call_command(
            "process_learner_closure_notices",
            "--send",
            stdout=second_output,
        )

        self.assertIn("Previously recorded: 1", second_output.getvalue())
        self.assertIn("Emails sent: 0", second_output.getvalue())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(LearnerAccountClosureNotice.objects.count(), 1)




from datetime import datetime, timedelta
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from django.test import SimpleTestCase

from communications.management.commands.process_learner_closure_notices import Command
from communications.models import LearnerAccountClosureNotice


class DeactivationEligibilityTests(SimpleTestCase):

    def setUp(self):
        self.tz = ZoneInfo("Europe/Madrid")
        self.reference = datetime(2023, 9, 25, 10, 0, tzinfo=self.tz)
        self.expiry = datetime(2026, 9, 25, 10, 0, tzinfo=self.tz)
        self.sent_at = datetime(2026, 8, 26, 9, 0, tzinfo=self.tz)
        self.deadline = datetime(2026, 9, 25, 23, 59, tzinfo=self.tz)

        self.user = SimpleNamespace(
            is_active=True,
            email="learner@example.com",
            last_login=None,
        )
        self.snapshot = {
            "status": "calculable",
            "reference_at": self.reference,
            "potential_expiry_at": self.expiry,
        }
        self.notice = SimpleNamespace(
            status=LearnerAccountClosureNotice.STATUS_SENT,
            sent_at=self.sent_at,
            effective_closure_at=self.deadline,
            reference_at=self.reference,
            potential_expiry_at=self.expiry,
            recipient_email="learner@example.com",
        )

    def ready(self, now=None):
        return Command._ready_for_deactivation(
            self.user, self.snapshot, self.notice,
            now if now is not None else self.deadline, self.tz,
        )

    def test_eligible_at_effective_deadline(self):
        self.assertTrue(self.ready())

    def test_cannot_deactivate_before_2359(self):
        self.assertFalse(self.ready(self.deadline - timedelta(minutes=1)))

    def test_late_notification_preserves_full_30_day_period(self):
        self.notice.sent_at = datetime(2026, 9, 1, 9, 0, tzinfo=self.tz)
        extended_deadline = datetime(2026, 10, 1, 23, 59, tzinfo=self.tz)

        self.assertFalse(self.ready(self.deadline))
        self.assertFalse(self.ready(extended_deadline - timedelta(minutes=1)))
        self.assertTrue(self.ready(extended_deadline))

    def test_old_retention_cycle_cannot_authorise_deactivation(self):
        self.notice.reference_at = self.reference - timedelta(days=1)
        self.assertFalse(self.ready())

        self.notice.reference_at = self.reference
        self.notice.potential_expiry_at = self.expiry - timedelta(days=1)
        self.assertFalse(self.ready())

    def test_notice_must_be_successfully_sent_with_a_deadline(self):
        for field, value in (
            ("status", LearnerAccountClosureNotice.STATUS_FAILED),
            ("sent_at", None),
            ("effective_closure_at", None),
        ):
            with self.subTest(field=field):
                original = getattr(self.notice, field)
                setattr(self.notice, field, value)
                self.assertFalse(self.ready())
                setattr(self.notice, field, original)

    def test_login_after_notice_prevents_deactivation(self):
        self.user.last_login = self.sent_at + timedelta(minutes=1)
        self.assertFalse(self.ready())

    def test_changed_email_prevents_deactivation(self):
        self.user.email = "another@example.com"
        self.assertFalse(self.ready())

    def test_ineligible_or_inactive_account_cannot_be_deactivated(self):
        for status in ("ongoing_enrollment", "needs_review", "company_onboarding_review"):
            with self.subTest(status=status):
                self.snapshot["status"] = status
                self.assertFalse(self.ready())

        self.snapshot["status"] = "calculable"
        self.user.is_active = False
        self.assertFalse(self.ready())

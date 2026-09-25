from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from .models import Attendance, ClassSession, Course, CourseEnrollment, CourseType


class CourseEnrollmentLifecycleTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        identifier = "retention@example.com" if User.USERNAME_FIELD == "email" else "retention_learner"

        cls.user = User.objects.create_user(
            **{User.USERNAME_FIELD: identifier},
            password="test-password",
        )

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

    def change_status(self, status, update_fields=None):
        self.enrollment.status = status
        if update_fields is None:
            self.enrollment.save()
        else:
            self.enrollment.save(update_fields=update_fields)
        self.enrollment.refresh_from_db()

    def test_new_active_enrollment_has_no_end_date(self):
        self.assertIsNone(self.enrollment.ended_at)

    def test_pausing_enrollment_does_not_set_end_date(self):
        self.change_status(CourseEnrollment.STATUS_PAUSED)
        self.assertIsNone(self.enrollment.ended_at)

    def test_completing_enrollment_sets_end_date(self):
        before = timezone.now()
        self.change_status(CourseEnrollment.STATUS_COMPLETED)

        self.assertIsNotNone(self.enrollment.ended_at)
        self.assertGreaterEqual(self.enrollment.ended_at, before)
        self.assertLessEqual(self.enrollment.ended_at, timezone.now())

    def test_cancelling_enrollment_sets_end_date(self):
        self.change_status(CourseEnrollment.STATUS_CANCELLED)
        self.assertIsNotNone(self.enrollment.ended_at)

    def test_paused_enrollment_can_resume_without_end_date(self):
        self.change_status(CourseEnrollment.STATUS_PAUSED)
        self.change_status(CourseEnrollment.STATUS_ACTIVE)

        self.assertIsNone(self.enrollment.ended_at)

    def test_completed_enrollment_reactivation_clears_end_date(self):
        self.change_status(CourseEnrollment.STATUS_COMPLETED)
        self.assertIsNotNone(self.enrollment.ended_at)

        self.change_status(CourseEnrollment.STATUS_ACTIVE)
        self.assertIsNone(self.enrollment.ended_at)

    def test_unchanged_status_preserves_existing_end_date(self):
        self.change_status(CourseEnrollment.STATUS_COMPLETED)
        original_end_date = self.enrollment.ended_at

        self.enrollment.target_level = "B2"
        self.enrollment.save(update_fields=["target_level"])
        self.enrollment.refresh_from_db()

        self.assertEqual(self.enrollment.ended_at, original_end_date)

    def test_update_fields_status_also_saves_end_date(self):
        self.change_status(
            CourseEnrollment.STATUS_COMPLETED,
            update_fields=["status"],
        )

        self.assertEqual(self.enrollment.status, CourseEnrollment.STATUS_COMPLETED)
        self.assertIsNotNone(self.enrollment.ended_at)

    def test_saving_completed_enrollment_again_preserves_end_date(self):
        self.change_status(CourseEnrollment.STATUS_COMPLETED)
        original_end_date = self.enrollment.ended_at

        self.enrollment.save()
        self.enrollment.refresh_from_db()

        self.assertEqual(self.enrollment.ended_at, original_end_date)

    def test_course_completion_records_enrollment_end_date(self):
        now = timezone.now()

        # Create a lesson that has already taken place.
        session = ClassSession.objects.create(
            course=self.course,
            class_number=1,
            start_time=now - timedelta(days=1, hours=1),
            end_time=now - timedelta(days=1),
        )

        # Pending attendance should leave the lesson awaiting submission.
        attendance = Attendance.objects.create(
            class_session=session,
            student=self.user,
        )

        session.refresh_from_db()
        self.assertEqual(
            session.status,
            ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
        )

        # Submitting attendance triggers the normal completion workflow.
        before = timezone.now()
        attendance.status = Attendance.STATUS_ATTENDED
        attendance.save()

        session.refresh_from_db()
        self.course.refresh_from_db()
        self.enrollment.refresh_from_db()

        # The lesson and course should now be completed.
        self.assertEqual(
            session.status,
            ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
        )
        self.assertEqual(self.course.status, "completed")

        # Automatic completion must also record the enrolment end date.
        self.assertEqual(
            self.enrollment.status,
            CourseEnrollment.STATUS_COMPLETED,
        )
        self.assertIsNotNone(self.enrollment.ended_at)
        self.assertGreaterEqual(self.enrollment.ended_at, before)
        self.assertLessEqual(self.enrollment.ended_at, timezone.now())

    def test_course_completion_ends_paused_enrollment_without_completion(self):
        User = get_user_model()
        identifier = "active_learner@example.com" if User.USERNAME_FIELD == "email" else "active_learner"

        active_student = User.objects.create_user(
            **{User.USERNAME_FIELD: identifier},
            password="test-password",
        )

        active_enrollment = CourseEnrollment.objects.create(
            student=active_student,
            course=self.course,
            status=CourseEnrollment.STATUS_ACTIVE,
        )

        # The original learner pauses their enrolment.
        self.change_status(CourseEnrollment.STATUS_PAUSED)

        now = timezone.now()
        session = ClassSession.objects.create(
            course=self.course,
            class_number=1,
            start_time=now - timedelta(days=1, hours=1),
            end_time=now - timedelta(days=1),
        )

        attendance = Attendance.objects.create(
            class_session=session,
            student=active_student,
        )

        before = timezone.now()
        attendance.status = Attendance.STATUS_ATTENDED
        attendance.save()

        self.course.refresh_from_db()
        self.enrollment.refresh_from_db()
        active_enrollment.refresh_from_db()

        # The course and participating learner complete normally.
        self.assertEqual(self.course.status, "completed")
        self.assertEqual(active_enrollment.status, CourseEnrollment.STATUS_COMPLETED)
        self.assertIsNotNone(active_enrollment.ended_at)

        # The paused learner finishes without completing their training.
        self.assertEqual(
            self.enrollment.status,
            CourseEnrollment.STATUS_ENDED_WITHOUT_COMPLETION,
        )
        self.assertIsNotNone(self.enrollment.ended_at)
        self.assertGreaterEqual(self.enrollment.ended_at, before)
        self.assertLessEqual(self.enrollment.ended_at, timezone.now())

        # Running the completion check again must preserve the original date.
        original_end_date = self.enrollment.ended_at
        self.course.update_completion_status()
        self.enrollment.refresh_from_db()

        self.assertEqual(self.enrollment.ended_at, original_end_date)


    def test_course_cancellation_ends_active_and_paused_enrollments(self):
        User = get_user_model()
        identifier = "paused_learner@example.com" if User.USERNAME_FIELD == "email" else "paused_learner"

        paused_student = User.objects.create_user(
            **{User.USERNAME_FIELD: identifier},
            password="test-password",
        )

        paused_enrollment = CourseEnrollment.objects.create(
            student=paused_student,
            course=self.course,
            status=CourseEnrollment.STATUS_PAUSED,
        )

        # Create a future lesson with pending attendance.
        now = timezone.now()
        session = ClassSession.objects.create(
            course=self.course,
            class_number=1,
            start_time=now + timedelta(days=1),
            end_time=now + timedelta(days=1, hours=1),
        )

        Attendance.objects.create(class_session=session, student=self.user)
        Attendance.objects.create(class_session=session, student=paused_student)

        # Cancel the entire course.
        before = timezone.now()
        self.course.status = "cancelled"
        self.course.save(update_fields=["status"])

        self.course.refresh_from_db()
        self.enrollment.refresh_from_db()
        paused_enrollment.refresh_from_db()
        session.refresh_from_db()

        # The course and its future lesson are cancelled.
        self.assertEqual(self.course.status, "cancelled")
        self.assertEqual(session.status, ClassSession.STATUS_CANCELLED)

        # Both ongoing enrolments are closed.
        for enrollment in (self.enrollment, paused_enrollment):
            self.assertEqual(enrollment.status, CourseEnrollment.STATUS_CANCELLED)
            self.assertIsNotNone(enrollment.ended_at)
            self.assertGreaterEqual(enrollment.ended_at, before)
            self.assertLessEqual(enrollment.ended_at, timezone.now())

        # Future operational attendance placeholders are removed.
        self.assertFalse(
            Attendance.objects.filter(class_session=session).exists()
        )

        # An ordinary subsequent save must preserve the original end date.
        original_end_date = self.enrollment.ended_at
        self.course.save()
        self.enrollment.refresh_from_db()

        self.assertEqual(self.enrollment.ended_at, original_end_date)
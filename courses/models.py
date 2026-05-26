from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta
from decimal import Decimal
from math import ceil

class CourseType(models.Model):
    """
    General type/category of course.

    Examples:
    - Individual Classes
    - Company English Training
    - FCE Preparation
    - Conversation Course
    """

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)

    default_hours = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Default number of hours for this course type."
    )

    is_for_companies = models.BooleanField(default=False)
    is_for_individual = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Specific course instance.

    Examples:
    - Individual Classes.01
    - Individual Classes.02
    - Company English - ACME 2026
    - FCE B2 Group.01
    """

    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    course_type = models.ForeignKey(
        CourseType,
        on_delete=models.PROTECT,
        related_name="courses"
    )

    name = models.CharField(max_length=200)

    total_hours = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Actual number of hours for this course."
    )

    class_duration = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Duration of each class in hours, e.g. 1.0, 1.5 or 2.0."
    )

    company = models.ForeignKey(
        "profiles.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        help_text="Only needed for company courses."
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses_taught"
    )

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="confirmed"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at", "name"]

    # If admin creates a Course and leaves total_hours empty,
    # Django automatically copies the hours from the CourseType.
    def save(self, *args, **kwargs):
        if self.total_hours is None and self.course_type.default_hours is not None:
            self.total_hours = self.course_type.default_hours

        super().save(*args, **kwargs)

    @property
    def number_of_classes(self):
        if not self.total_hours or not self.class_duration:
            return None

        if self.class_duration <= 0:
            return None

        # ceil() to make num. of classes a whole number
        # eg: 6.66 classes = 7 classes
        return ceil(self.total_hours / self.class_duration)

    def generate_class_sessions(self):
        """
        Creates the required ClassSession objects for this course based on:
        - start_date
        - number_of_classes
        - timetable slots
        - class_duration

        Also creates scheduled Attendance records for every active enrolled student.

        This method is idempotent:
        - running it twice does not duplicate class sessions
        - adding a new student only creates missing attendance records
        """

        if not self.start_date:
            raise ValidationError(
                "This course needs a start date before sessions can be generated."
            )

        if not self.number_of_classes:
            raise ValidationError(
                "This course needs total hours and class duration before sessions can be generated."
            )

        timetable_slots = self.timetable_slots.all().order_by(
            "day_of_week",
            "start_time"
        )

        if not timetable_slots.exists():
            raise ValidationError(
                "This course needs at least one timetable slot."
            )

        active_enrollments = self.enrollments.filter(
            status="active"
        ).select_related("student")

        enrolled_students = [enrollment.student for enrollment in active_enrollments]

        if not enrolled_students:
            raise ValidationError(
                "This course has no active enrolled students."
            )

        class_duration_minutes = int(self.class_duration * Decimal("60"))

        sessions_created = 0
        attendances_created = 0
        scheduled_class_count = 0

        current_date = self.start_date
        selected_sessions = []

        while scheduled_class_count < self.number_of_classes:
            weekday = current_date.isoweekday()

            slots_for_day = timetable_slots.filter(day_of_week=weekday)

            for slot in slots_for_day:
                if scheduled_class_count >= self.number_of_classes:
                    break

                naive_start = datetime.combine(current_date, slot.start_time)

                aware_start = timezone.make_aware(
                    naive_start,
                    timezone.get_current_timezone()
                )

                aware_end = aware_start + timedelta(
                    minutes=class_duration_minutes
                )

                class_number = scheduled_class_count + 1

                class_session, created = ClassSession.objects.get_or_create(
                    course=self,
                    start_time=aware_start,
                    defaults={
                        "title": f"{self.name} - Lesson {class_number}",
                        "class_number": class_number,
                        "end_time": aware_end,
                        "topic": "",
                        "meeting_link": "",
                        "is_cancelled": False,
                    }
                )

                selected_sessions.append(class_session)

                if created:
                    sessions_created += 1

                scheduled_class_count += 1

            current_date += timedelta(days=1)

        for class_session in selected_sessions:
            for student in enrolled_students:
                _, attendance_created = Attendance.objects.get_or_create(
                    class_session=class_session,
                    student=student,
                    defaults={
                        "status": "scheduled",
                    }
                )

                if attendance_created:
                    attendances_created += 1

        return {
            "sessions_created": sessions_created,
            "attendances_created": attendances_created,
            "students_count": len(enrolled_students),
            "total_scheduled_classes": scheduled_class_count,
        }

    def __str__(self):
        return self.name


class CourseTimetableSlot(models.Model):
    """
    Weekly timetable slot for a course.

    Examples:
    - Monday 10:00 - 11:30
    - Wednesday 18:00 - 19:30
    """

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    DAY_CHOICES = [
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
        (SUNDAY, "Sunday"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="timetable_slots"
    )

    day_of_week = models.PositiveSmallIntegerField(
        choices=DAY_CHOICES
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    class Meta:
        ordering = ["day_of_week", "start_time"]
        unique_together = (
            "course",
            "day_of_week",
            "start_time",
            "end_time",
        )

    def __str__(self):
        return (
            f"{self.course} - "
            f"{self.get_day_of_week_display()} "
            f"{self.start_time:%H:%M} - {self.end_time:%H:%M}"
        )

class CourseEnrollment(models.Model):
    """
    Connects a user/student/employee to a specific course.
    - One course can have many students.
    - One student can be enrolled in many courses.
    - Each enrolment can store its own status/objective.
    """

    ENROLLMENT_STATUS_CHOICES = [
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_enrollments"
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=ENROLLMENT_STATUS_CHOICES,
        default="active"
    )

    target_level = models.CharField(
        max_length=30,
        blank=True,
        help_text="Optional target CEFR level, e.g. B2, C1."
    )

    learning_objective = models.TextField(
        blank=True,
        help_text="Optional individual or company learning objective."
    )

    class Meta:
        unique_together = ("course", "student")
        ordering = ["course", "student"]

    def __str__(self):
        return f"{self.student} - {self.course}"

    @property
    def total_assigned_classes(self):
        return self.course.class_sessions.filter(
            is_cancelled=False
        ).count()

    @property
    def total_completed_classes(self):
        # past classes
        return Attendance.objects.filter(
            student=self.student,
            class_session__course=self.course,
            class_session__is_cancelled=False,
        ).exclude(
            status="scheduled"
        ).values("class_session").distinct().count()

    @property
    def upcoming_classes(self):
        return self.total_assigned_classes - self.total_completed_classes

    @property
    def classes_attended(self):
        return Attendance.objects.filter(
            student=self.student,
            class_session__course=self.course,
            class_session__is_cancelled=False,
            status="attended"
        ).values("class_session").distinct().count()


    @property
    def classes_missed(self):
        return Attendance.objects.filter(
            student=self.student,
            class_session__course=self.course,
            class_session__is_cancelled=False,
            status="missed"
        ).values("class_session").distinct().count()

    @property
    def classes_excused(self):
        return Attendance.objects.filter(
            student=self.student,
            class_session__course=self.course,
            class_session__is_cancelled=False,
            status="excused"
        ).values("class_session").distinct().count()


    @property
    def attendance_percentage(self):
        total = self.total_completed_classes

        if total == 0:
            return 0

        return round((self.classes_attended / total) * 100)

    @property
    def has_low_attendance_warning(self):
        total = self.total_completed_classes

        if total == 0:
            return False

        return self.attendance_percentage < 75

class ClassSession(models.Model):
    """
    One scheduled lesson for a specific course.
    E.g.: Individual Classes.01
    Class 1
    Class 2
    Class 3
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="class_sessions"
    )

    title = models.CharField(
        max_length=200,
        default="English Class"
    )

    class_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Lesson number within the course."
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    meeting_link = models.URLField(blank=True)

    topic = models.CharField(max_length=200, blank=True)

    is_cancelled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "start_time"],
                name="unique_course_session_start_time"
            )
        ]

    def __str__(self):
        return f"{self.course} - {self.start_time:%d/%m/%Y %H:%M}"

    @property
    def is_past(self):
        return self.end_time < timezone.now()



class Attendance(models.Model):
    '''
    In a group/company course, many students attend
    the same class session, but each has 
    their own attendance status.
    Supports:
    - 1-to-1 individual classes
    - group company classes

    '''
    ATTENDANCE_STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("attended", "Attended"),
        ("missed", "Missed"),
        ("excused", "Excused"),
        ("cancelled", "Cancelled"),
    ]

    class_session = models.ForeignKey(
        ClassSession,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    status = models.CharField(
        max_length=20,
        choices=ATTENDANCE_STATUS_CHOICES,
        default="scheduled"
    )

    minutes_late = models.PositiveIntegerField(
        default=0,
        help_text="Number of minutes late. Use 0 if on time."
    )

    notes = models.TextField(blank=True)

    recorded_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["class_session__start_time", "student"]
        constraints = [
            models.UniqueConstraint(
                fields=["class_session", "student"],
                name="unique_attendance_per_student_per_session"
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.class_session} - {self.status}"

    @property
    def was_punctual(self):
        return self.status == "attended" and self.minutes_late == 0

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
        ("paused", "Paused"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    course_type = models.ForeignKey(
        CourseType,
        on_delete=models.PROTECT,
        related_name="courses"
    )

    name = models.CharField(max_length=200)

    course_level = models.CharField(
        max_length=30,
        blank=True,
        help_text="Current CEFR level, e.g. B2, C1."
    )

    total_hours = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="Actual number of hours for this course."
    )

    # Include logic to adapt to whether class_duration
    # or timeslots are introduced first
    CLASS_DURATION_SOURCE_CHOICES = [
        ("manual", "Manually set"),
        ("auto", "Calculated from timetable"),
    ]

    class_duration = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Duration of each class in hours, e.g. 1.25, 1.50, 0.75 or 2.00."
    )

    # Include logic to adapt to whether class_duration
    # or timeslots are introduced first
    class_duration_source = models.CharField(
        max_length=10,
        choices=CLASS_DURATION_SOURCE_CHOICES,
        blank=True,
        help_text="Shows whether class duration was manually set or calculated from timetable slots."
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
        # Include logic to adapt to whether class_duration
        # or timeslots are introduced first
        is_new = self.pk is None
        old_class_duration = None

        if self.pk:
            old_course = Course.objects.get(pk=self.pk)
            old_class_duration = old_course.class_duration

        if self.total_hours is None and self.course_type.default_hours is not None:
            self.total_hours = self.course_type.default_hours

        if self.class_duration and (
            is_new or self.class_duration != old_class_duration
        ):
            self.class_duration_source = "manual"

        super().save(*args, **kwargs)


    def format_duration(self, duration):
        """
        Converts decimal hours into a readable duration.

        Examples:
        0.50 -> 30 min
        0.75 -> 45 min
        1.00 -> 1 h
        1.50 -> 1 h 30 min
        """

        if duration is None:
            return ""

        total_minutes = int(duration * 60)

        hours = total_minutes // 60
        minutes = total_minutes % 60

        if hours == 0:
            return f"{minutes} min"

        if minutes == 0:
            return f"{hours} h"

        return f"{hours} h {minutes} min"
    
    @property
    def class_duration_display(self):
        return self.format_duration(self.class_duration)

    @property
    def number_of_classes(self):
        if not self.total_hours or not self.class_duration:
            return None

        if self.class_duration <= 0:
            return None

        # ceil() to make num. of classes a whole number
        # Pushes upwards; eg: 6.66 classes = 7 classes
        return ceil(self.total_hours / self.class_duration)

    def update_class_duration_from_timetable(self):
        """
        Calculates class_duration from timetable slots.
        Only works when all timetable slots have the same duration.
        """

        slots = self.timetable_slots.all()

        if not slots.exists():
            return

        durations = set()

        for slot in slots:
            duration = slot.duration_in_hours
            durations.add(duration)

        if len(durations) > 1:
            raise ValidationError(
                "All timetable slots must have the same duration if class duration is calculated automatically."
            )

        calculated_duration = durations.pop()

        Course.objects.filter(pk=self.pk).update(
            class_duration=calculated_duration,
            class_duration_source="auto",
        )

        self.class_duration = calculated_duration
        self.class_duration_source = "auto"

    @property
    def final_class_duration(self):
        """
        The duration of the last class of the course,
        if total_hours / class_duration is not a full number,
        then last class' duration varies to adapt to total_hours
        agreed with company/funds
        """
        if not self.total_hours or not self.class_duration:
            return None

        full_classes = self.total_hours // self.class_duration
        remainder = self.total_hours % self.class_duration

        if remainder == 0:
            return self.class_duration

        return remainder

    @property
    def final_class_duration_display(self):
        return self.format_duration(self.final_class_duration)

    @property
    def has_short_final_class(self):
        """
        Boolean, returns True if last class is shorter,
        then final_class_duration is served after
        """
        if not self.total_hours or not self.class_duration:
            return False

        return self.total_hours % self.class_duration != 0

    @property
    def class_duration_display(self):
        return self.format_duration(self.class_duration)

    @property
    def timetable_display(self):
        slots = list(self.timetable_slots.all())

        if not slots:
            return "Not assigned"

        # Do all slots share the same times?
        first_start = slots[0].start_time
        first_end = slots[0].end_time

        same_times = all(
            slot.start_time == first_start and
            slot.end_time == first_end
            for slot in slots
        )

        if same_times:
            days = " & ".join(
                slot.get_day_of_week_display()[:3]
                for slot in slots
            )

            return (
                f"{days} | "
                f"{first_start.strftime('%H:%M')} - "
                f"{first_end.strftime('%H:%M')}"
            )

        # Different times
        return " · ".join(
            f"{slot.get_day_of_week_display()[:3]} "
            f"{slot.start_time.strftime('%H:%M')} - "
            f"{slot.end_time.strftime('%H:%M')}"
            for slot in slots
        )

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

                naive_end = datetime.combine(current_date, slot.end_time)

                aware_end = timezone.make_aware(
                    naive_end,
                    timezone.get_current_timezone()
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

                # Avoid class_number/ session =none is these were previously created
                if created:
                    sessions_created += 1
                else:
                    fields_to_update = []

                    if class_session.class_number != class_number:
                        class_session.class_number = class_number
                        fields_to_update.append("class_number")

                    if class_session.title != f"{self.name} - Lesson {class_number}":
                        class_session.title = f"{self.name} - Lesson {class_number}"
                        fields_to_update.append("title")

                    if class_session.end_time != aware_end:
                        class_session.end_time = aware_end
                        fields_to_update.append("end_time")

                    if fields_to_update:
                        class_session.save(update_fields=fields_to_update)
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

    @property
    def completion_percentage(self):
        now = timezone.now()

        if self.total_sessions == 0:
            return 0

        return round((self.completed_sessions / self.total_sessions) * 100)

    def __str__(self):
        return self.name

    @property
    def total_sessions(self):
        return self.class_sessions.filter(
            is_cancelled=False
        ).count()


    @property
    def completed_sessions(self):
        now = timezone.now()

        return self.class_sessions.filter(
            is_cancelled=False,
            start_time__lt=now,
        ).count()

    @property
    def remaining_sessions(self):
        return max(
            self.total_sessions - self.completed_sessions,
            0
        )



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

    @property
    def duration_in_hours(self):
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)

        duration = end_datetime - start_datetime
        minutes = duration.total_seconds() / 60

        return Decimal(minutes / 60).quantize(Decimal("0.01"))

    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("End time must be after start time.")

        if self.course_id and self.start_time and self.end_time:
            course = self.course

            if (
                course.class_duration
                and course.class_duration_source != "auto"
                and self.duration_in_hours != course.class_duration
            ):
                raise ValidationError(
                    f"This slot duration is {self.duration_in_hours} hours, "
                    f"but the course class duration is {course.class_duration} hours."
                )

    def save(self, *args, **kwargs):
        old_slot = None

        if self.pk:
            old_slot = CourseTimetableSlot.objects.get(pk=self.pk)

        self.full_clean()
        super().save(*args, **kwargs)

        if self.course.class_duration_source != "manual":
            self.course.update_class_duration_from_timetable()

        if old_slot:
            timetable_changed = (
                old_slot.day_of_week != self.day_of_week or
                old_slot.start_time != self.start_time or
                old_slot.end_time != self.end_time
            )

            if timetable_changed:
                self.update_future_class_sessions(old_slot)

    def update_future_class_sessions(self, old_slot):
        now = timezone.now()
        current_timezone = timezone.get_current_timezone()

        future_sessions = self.course.class_sessions.filter(
            start_time__gte=now,
            is_cancelled=False,
        ).order_by("start_time")

        for session in future_sessions:
            old_local_start = timezone.localtime(session.start_time)
            old_local_end = timezone.localtime(session.end_time)

            belongs_to_old_slot = (
                old_local_start.isoweekday() == old_slot.day_of_week and
                old_local_start.time() == old_slot.start_time and
                old_local_end.time() == old_slot.end_time
            )

            if not belongs_to_old_slot:
                continue

            old_session_date = old_local_start.date()

            day_difference = self.day_of_week - old_slot.day_of_week
            new_session_date = old_session_date + timedelta(days=day_difference)

            new_start = timezone.make_aware(
                datetime.combine(new_session_date, self.start_time),
                current_timezone
            )

            new_end = timezone.make_aware(
                datetime.combine(new_session_date, self.end_time),
                current_timezone
            )

            if new_start < now:
                continue

            session.start_time = new_start
            session.end_time = new_end
            session.save(update_fields=["start_time", "end_time"])

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

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and self.status == "active":
            self.create_future_attendance_records()

    def create_future_attendance_records(self):
        future_sessions = self.course.class_sessions.filter(
            start_time__gte=self.enrolled_at,
            is_cancelled=False,
        )

        for session in future_sessions:
            Attendance.objects.get_or_create(
                student=self.student,
                class_session=session,
                defaults={
                    "status": "scheduled",
                }
            )

    def __str__(self):
        return f"{self.student} - {self.course}"

    @property
    def eligible_sessions(self):
        return self.course.class_sessions.filter(
            start_time__gte=self.enrolled_at,
            is_cancelled=False,
        )

    @property
    def total_assigned_classes(self):
        return self.eligible_sessions.count()

    @property
    def total_completed_classes(self):
        return Attendance.objects.filter(
            student=self.student,
            class_session__course=self.course,
            class_session__start_time__gte=self.enrolled_at,
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
            class_session__start_time__gte=self.enrolled_at,
            class_session__is_cancelled=False,
            status="attended"
        ).values("class_session").distinct().count()

    @property
    def classes_missed(self):
        return Attendance.objects.filter(
            student=self.student,
            class_session__course=self.course,
            class_session__start_time__gte=self.enrolled_at,
            class_session__is_cancelled=False,
            status="missed"
        ).values("class_session").distinct().count()

    @property
    def classes_excused(self):
        return Attendance.objects.filter(
            student=self.student,
            class_session__course=self.course,
            class_session__start_time__gte=self.enrolled_at,
            class_session__is_cancelled=False,
            status="excused"
        ).values("class_session").distinct().count()

    @property
    def total_absences(self):
        return self.classes_missed + self.classes_excused

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

    STATUS_SCHEDULED = "scheduled"
    STATUS_PENDING_RESCHEDULE = "pending_reschedule"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_PENDING_RESCHEDULE, "Pending reschedule"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_COMPLETED, "Completed"),
    ]

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

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_SCHEDULED,
    )    

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


    def save(self, *args, **kwargs):
        old_meeting_link = None

        if self.pk:
            old_session = ClassSession.objects.get(pk=self.pk)
            old_meeting_link = old_session.meeting_link

        super().save(*args, **kwargs)

        if self.meeting_link and self.meeting_link != old_meeting_link:
            self.course.class_sessions.exclude(
                pk=self.pk
            ).update(
                meeting_link=self.meeting_link
            )


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
    STATUS_SCHEDULED = "scheduled"
    STATUS_ATTENDED = "attended"
    STATUS_MISSED = "missed"
    STATUS_EXCUSED = "excused"
    STATUS_CANCELLED = "cancelled"
    STATUS_PENDING_RESCHEDULE = "pending_reschedule"

    ATTENDANCE_STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("attended", "Attended"),
        ("missed", "Missed"),
        ("excused", "Excused"),
        ("cancelled", "Cancelled"),
        ("pending_reschedule", "Pending reschedule"),
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
        max_length=30,
        choices=ATTENDANCE_STATUS_CHOICES,
        default=STATUS_SCHEDULED,
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


class BankHoliday(models.Model):
    title = models.CharField(max_length=200)

    start_date = models.DateField(
        null=True,
        blank=True,
        help_text="First day of the bank holiday."
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Optional. Leave empty for a single-day bank holiday."
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Only active holidays are shown in the calendar."
    )

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Bank holiday"
        verbose_name_plural = "Bank holidays"

    def __str__(self):
        return f"{self.title} - {self.start_date}"
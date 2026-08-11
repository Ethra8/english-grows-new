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


# MODEL LOGIC and FUNCTIONALITIES
# 
# class Course 
# → overall course lifecycle/progress

# class ClassSession
# → lesson lifecycle + rescheduling

# class CourseEnrollment
# → learner membership in course
# → automatic assignment to unfinished sessions

# class Attendance
# → individual learner outcome for one lesson

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

        # A newly saved Course may not yet have its related timetable slots
        # and enrollments (e.g. Django Admin saves inline objects afterwards).
        #
        # Therefore this is a SAFE attempt: generation only happens when ALL
        # required data already exists. The related models also call the same
        # helper after they are saved, so generation occurs automatically as
        # soon as the final prerequisite is available.
        if is_new:
            self.try_generate_class_sessions()


    def can_generate_class_sessions(self):
        """
        Return True only when this Course is ready for its ClassSessions
        and initial Attendance records to be generated automatically.

        Generation is allowed only when:
        - the Course has been saved
        - no ClassSessions exist yet
        - start_date exists
        - total_hours/class_duration produce number_of_classes
        - at least one timetable slot exists
        - at least one active enrollment exists

        This guard makes automatic generation safe to call from several
        points in the model lifecycle without ever regenerating a course
        that already has ClassSessions.
        """
        if not self.pk:
            return False

        if self.class_sessions.exists():
            return False

        if not self.start_date:
            return False

        if not self.number_of_classes:
            return False

        if not self.timetable_slots.exists():
            return False

        if not self.enrollments.filter(status="active").exists():
            return False

        return True


    def try_generate_class_sessions(self):
        """
        Automatically generate the Course's complete ClassSession schedule
        and initial Attendance records as soon as all prerequisites exist.

        Returns the generate_class_sessions() result when generation occurs.
        Returns None when the Course is not ready or sessions already exist.

        IMPORTANT:
        This method never regenerates an existing course schedule.
        New learners enrolled later are handled separately by
        CourseEnrollment.create_future_attendance_records().
        """
        if not self.can_generate_class_sessions():
            return None

        return self.generate_class_sessions()


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


    # Returns ONLY DAYS of course timetable
    @property
    def timetable_days_display(self):
        slots = list(self.timetable_slots.all())

        if not slots:
            return "Not assigned"

        return " & ".join(
            slot.get_day_of_week_display()[:3]
            for slot in slots
        )

    # Returns ONLY TIMES of course timetable 
    # (different if days have different times!)
    @property
    def timetable_times_display(self):
        slots = list(self.timetable_slots.all())

        if not slots:
            return ""

        first_start = slots[0].start_time
        first_end = slots[0].end_time

        same_times = all(
            slot.start_time == first_start
            and slot.end_time == first_end
            for slot in slots
        )

        if same_times:
            return (
                f"{first_start.strftime('%H:%M')} - "
                f"{first_end.strftime('%H:%M')}"
            )

        return " · ".join(
            f"{slot.get_day_of_week_display()[:3]} "
            f"{slot.start_time.strftime('%H:%M')} - "
            f"{slot.end_time.strftime('%H:%M')}"
            for slot in slots
        )

    def generate_class_sessions(self):
        """
        Generate the complete set of ClassSession objects for this course
        from its start date and weekly timetable, then create Attendance
        records for every learner who is already actively enrolled.

        This method is invoked automatically once the Course has all required
        setup data. Course.try_generate_class_sessions() guards against running
        it again once ClassSessions already exist.

        It is still defensive/idempotent:
        - a lesson is identified by course + class_number
        - an existing lesson is never duplicated
        - an existing lesson's date/time/status are never overwritten
        - missing Attendance records are created with get_or_create()

        IMPORTANT:
        Rescheduling never creates a replacement ClassSession. The existing
        ClassSession is updated and must eventually reach status="completed".
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

        active_enrollments = (
            self.enrollments
            .filter(status="active")
            .select_related("student")
        )

        enrolled_students = [
            enrollment.student
            for enrollment in active_enrollments
        ]

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
            # CourseTimetableSlot uses ISO weekday numbering:
            # Monday=1 ... Sunday=7.
            weekday = current_date.isoweekday()

            slots_for_day = timetable_slots.filter(
                day_of_week=weekday
            )

            for slot in slots_for_day:
                if scheduled_class_count >= self.number_of_classes:
                    break

                class_number = scheduled_class_count + 1

                naive_start = datetime.combine(
                    current_date,
                    slot.start_time
                )

                aware_start = timezone.make_aware(
                    naive_start,
                    timezone.get_current_timezone()
                )

                # The final lesson may be shorter when total_hours is not
                # perfectly divisible by the standard class duration.
                is_final_class = (
                    class_number == self.number_of_classes
                )

                if is_final_class and self.has_short_final_class:
                    aware_end = aware_start + timedelta(
                        seconds=float(
                            self.final_class_duration * Decimal("3600")
                        )
                    )
                else:
                    naive_end = datetime.combine(
                        current_date,
                        slot.end_time
                    )

                    aware_end = timezone.make_aware(
                        naive_end,
                        timezone.get_current_timezone()
                    )

                expected_title = (
                    f"{self.name} - Lesson {class_number}"
                )

                # class_number is the stable identity of a lesson within
                # the course. start_time is deliberately NOT used here
                # because a lesson can later be rescheduled.
                class_session, created = ClassSession.objects.get_or_create(
                    course=self,
                    class_number=class_number,
                    defaults={
                        "title": expected_title,
                        "start_time": aware_start,
                        "end_time": aware_end,
                        "topic": "",
                        "meeting_link": "",
                        "status": ClassSession.STATUS_SCHEDULED,
                    }
                )

                if created:
                    sessions_created += 1
                else:
                    # Do not overwrite start_time, end_time or status on an
                    # existing ClassSession. It may have been rescheduled.
                    if class_session.title != expected_title:
                        class_session.title = expected_title
                        class_session.save(
                            update_fields=["title"]
                        )

                selected_sessions.append(class_session)
                scheduled_class_count += 1

            current_date += timedelta(days=1)

        # Create missing Attendance records for learners who were already
        # actively enrolled when the course sessions were generated.
        for class_session in selected_sessions:
            for student in enrolled_students:
                _, attendance_created = Attendance.objects.get_or_create(
                    class_session=class_session,
                    student=student,
                    defaults={
                        "status": Attendance.STATUS_SCHEDULED,
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
    def total_sessions(self):
        """
        Total number of ClassSession records belonging to this course.

        No sessions are excluded based on cancellation/rescheduling.
        Every generated session must eventually be completed.
        """
        return self.class_sessions.count()


    @property
    def completed_sessions(self):
        """
        A ClassSession counts as completed ONLY when its own
        status has explicitly been set to "completed".

        Being in the past does not automatically mean completed.
        """
        return self.class_sessions.filter(
            status="completed"
        ).count()


    @property
    def remaining_sessions(self):
        """
        Any session that has not yet reached status="completed"
        is still outstanding.

        This includes scheduled/rescheduled/pending-reschedule
        sessions.
        """
        return max(
            self.total_sessions - self.completed_sessions,
            0
        )


    @property
    def completion_percentage(self):
        """
        Percentage of this course's ClassSession records
        that have reached status="completed".
        """
        if self.total_sessions == 0:
            return 0

        return round(
            (
                self.completed_sessions
                / self.total_sessions
            ) * 100
        )


    def update_completion_status(self):
        """
        Mark the Course as completed when EVERY ClassSession
        belonging to it has status="completed".

        Active enrollments are also marked completed at the same time.

        Returns:
            True  -> all sessions are completed
            False -> at least one session is still outstanding
        """

        # A course with no sessions should never auto-complete.
        if not self.class_sessions.exists():
            return False

        # If even ONE session is not completed,
        # the course must remain unfinished.
        has_unfinished_sessions = (
            self.class_sessions
            .exclude(status="completed")
            .exists()
        )

        if has_unfinished_sessions:
            return False

        # All ClassSessions are completed.
        if self.status != "completed":
            self.status = "completed"
            self.save(
                update_fields=["status"]
            )

        # Keep enrollment lifecycle consistent with course lifecycle.
        self.enrollments.filter(
            status="active"
        ).update(
            status="completed"
        )

        return True



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

        # Automatic initial generation:
        # Course.save() happens before related Admin inline objects are saved.
        # Once a timetable slot exists (and all other prerequisites are ready),
        # this safely creates the complete ClassSession schedule exactly once.
        self.course.try_generate_class_sessions()

    def update_future_class_sessions(self, old_slot):
        now = timezone.now()
        current_timezone = timezone.get_current_timezone()

        future_sessions = self.course.class_sessions.filter(
            start_time__gte=now,
            status=ClassSession.STATUS_SCHEDULED,
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
    - Each enrollment can store its own status/objective.

    IMPORTANT:

    ClassSessions are generated at course setup.

    If a learner joins later:
    - no new ClassSessions are created
    - Attendance records are created automatically
      for that learner
    - completed ClassSessions are NOT assigned retroactively
    - scheduled / pending_reschedule / rescheduled sessions
      are assigned

    A ClassSession is considered completed ONLY when:

        ClassSession.status == "completed"
    """

    # ---------------------------------------------------------
    # ENROLLMENT STATUS
    # ---------------------------------------------------------

    ENROLLMENT_STATUS_CHOICES = [
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]


    # ---------------------------------------------------------
    # COURSE / STUDENT
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # ENROLLMENT INFORMATION
    # ---------------------------------------------------------

    enrolled_at = models.DateTimeField(
        auto_now_add=True
    )

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


    # ---------------------------------------------------------
    # META
    # ---------------------------------------------------------

    class Meta:
        unique_together = (
            "course",
            "student"
        )

        ordering = [
            "course",
            "student"
        ]


    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    def save(self, *args, **kwargs):
        """
        Save the enrollment.

        Whenever an enrollment becomes active:
        - create missing Attendance records
        - only for unfinished ClassSessions

        This happens when:
        - a new enrollment is created as active
        - an existing enrollment becomes active again
    """

        is_new = self.pk is None
        old_status = None

        if self.pk:
            old_enrollment = CourseEnrollment.objects.get(
                pk=self.pk
            )

            old_status = old_enrollment.status

        super().save(*args, **kwargs)

        became_active = (
            self.status == "active"
            and (
                is_new
                or old_status != "active"
            )
        )

        if became_active:
            # If the Course already has ClassSessions, assign this learner
            # automatically to every unfinished lesson.
            self.create_future_attendance_records()

            # If this enrollment is the final prerequisite during initial
            # Course setup, generate the Course's full ClassSession schedule
            # and Attendance records automatically.
            #
            # The Course helper includes a "no existing ClassSessions" guard,
            # so enrolling learners later will NEVER regenerate the schedule.
            self.course.try_generate_class_sessions()


    # ---------------------------------------------------------
    # CREATE MISSING ATTENDANCE
    # ---------------------------------------------------------

    def create_future_attendance_records(self):
        """
        Create missing Attendance records for this learner
        for every unfinished ClassSession in the course.

        Completed sessions are NOT assigned retroactively.

        Included:
        - scheduled
        - pending_reschedule
        - rescheduled

        Excluded:
        - completed

        This supports learners who join after the course
        has already started.
        """

        eligible_sessions = (
            self.course.class_sessions
            .exclude(
                status=ClassSession.STATUS_COMPLETED
            )
            .order_by("start_time")
        )

        for session in eligible_sessions:
            Attendance.objects.get_or_create(
                student=self.student,
                class_session=session,
                defaults={
                    "status": Attendance.STATUS_SCHEDULED,
                }
            )


    # ---------------------------------------------------------
    # STRING REPRESENTATION
    # ---------------------------------------------------------

    def __str__(self):
        return f"{self.student} - {self.course}"


    # ---------------------------------------------------------
    # ASSIGNED SESSIONS
    # ---------------------------------------------------------

    @property
    def eligible_sessions(self):
        """
        Return the ClassSessions actually assigned to this learner.

        Attendance records are used as the source of truth.

        This is safer than filtering by start_time because
        ClassSession.start_time can change when a lesson is
        rescheduled.

        Once an Attendance record exists for a learner/session,
        that session remains part of that learner's enrollment.
        """

        assigned_session_ids = (
            Attendance.objects
            .filter(
                student=self.student,
                class_session__course=self.course,
            )
            .values_list(
                "class_session_id",
                flat=True
            )
        )

        return (
            self.course.class_sessions
            .filter(
                id__in=assigned_session_ids
            )
            .order_by("start_time")
        )


    # ---------------------------------------------------------
    # TOTAL ASSIGNED CLASSES
    # ---------------------------------------------------------

    @property
    def total_assigned_classes(self):
        """
        Total number of ClassSessions assigned to this learner.
        """

        return self.eligible_sessions.count()


    # ---------------------------------------------------------
    # TOTAL COMPLETED CLASSES
    # ---------------------------------------------------------

    @property
    def total_completed_classes(self):
        """
        Number of assigned ClassSessions explicitly marked
        as completed.

        A session being in the past does NOT automatically
        count as completed.
        """

        return (
            self.eligible_sessions
            .filter(
                status=ClassSession.STATUS_COMPLETED
            )
            .count()
        )


    # ---------------------------------------------------------
    # REMAINING CLASSES
    # ---------------------------------------------------------

    @property
    def upcoming_classes(self):
        """
        Number of assigned sessions still unfinished.

        Despite the property name "upcoming_classes",
        this includes:

        - scheduled
        - pending_reschedule
        - rescheduled

        because all three still need to reach "completed".
        """

        return max(
            self.total_assigned_classes
            - self.total_completed_classes,
            0
        )


    # ---------------------------------------------------------
    # ATTENDED CLASSES
    # ---------------------------------------------------------

    @property
    def classes_attended(self):
        """
        Completed ClassSessions where this learner
        was marked as attended.
        """

        return (
            Attendance.objects
            .filter(
                student=self.student,
                class_session__course=self.course,
                class_session__status=ClassSession.STATUS_COMPLETED,
                status=Attendance.STATUS_ATTENDED,
            )
            .values(
                "class_session_id"
            )
            .distinct()
            .count()
        )


    # ---------------------------------------------------------
    # MISSED CLASSES
    # ---------------------------------------------------------

    @property
    def classes_missed(self):
        """
        Completed ClassSessions where this learner
        was marked as missed.
        """

        return (
            Attendance.objects
            .filter(
                student=self.student,
                class_session__course=self.course,
                class_session__status=ClassSession.STATUS_COMPLETED,
                status=Attendance.STATUS_MISSED,
            )
            .values(
                "class_session_id"
            )
            .distinct()
            .count()
        )


    # ---------------------------------------------------------
    # EXCUSED CLASSES
    # ---------------------------------------------------------

    @property
    def classes_excused(self):
        """
        Completed ClassSessions where this learner
        was marked as excused.
        """

        return (
            Attendance.objects
            .filter(
                student=self.student,
                class_session__course=self.course,
                class_session__status=ClassSession.STATUS_COMPLETED,
                status=Attendance.STATUS_EXCUSED,
            )
            .values(
                "class_session_id"
            )
            .distinct()
            .count()
        )


    # ---------------------------------------------------------
    # TOTAL ABSENCES
    # ---------------------------------------------------------

    @property
    def total_absences(self):
        """
        Total missed + excused completed sessions.
        """

        return (
            self.classes_missed
            + self.classes_excused
        )


    # ---------------------------------------------------------
    # ATTENDANCE PERCENTAGE
    # ---------------------------------------------------------

    @property
    def attendance_percentage(self):
        """
        Attendance percentage calculated only from completed
        ClassSessions.

        Example:

        10 completed classes
        8 attended

        attendance_percentage = 80
        """

        total = self.total_completed_classes

        if total == 0:
            return 0

        return round(
            (
                self.classes_attended
                / total
            ) * 100
        )


    # ---------------------------------------------------------
    # LOW ATTENDANCE WARNING
    # ---------------------------------------------------------

    @property
    def has_low_attendance_warning(self):
        """
        Returns True when attendance is below 75%.

        No warning is shown until at least one ClassSession
        has been completed.
        """

        if self.total_completed_classes == 0:
            return False

        return self.attendance_percentage < 75



class ClassSession(models.Model):
    """
    One scheduled lesson for a specific course.

    Examples:
    - Individual Classes.01 - Lesson 1
    - Individual Classes.01 - Lesson 2
    - Individual Classes.01 - Lesson 3

    A ClassSession is created once when the course sessions
    are initially generated.

    NORMAL FLOW:

        scheduled
            ↓
        completed

    RESCHEDULING FLOW:

        scheduled
            ↓
        pending_reschedule
            ↓
        rescheduled
            ↓
        completed

    IMPORTANT:
    A rescheduled lesson remains the SAME ClassSession object.

    Rescheduling does NOT create a new ClassSession.
    Instead, the existing session's:
    - status
    - start_time
    - end_time

    are updated.

    Every ClassSession belonging to a course must eventually
    reach status="completed" before the Course itself can be
    automatically marked as completed.
    """

    # ---------------------------------------------------------
    # STATUS CHOICES
    # ---------------------------------------------------------

    STATUS_SCHEDULED = "scheduled"
    STATUS_PENDING_RESCHEDULE = "pending_reschedule"
    STATUS_RESCHEDULED = "rescheduled"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_PENDING_RESCHEDULE, "Pending reschedule"),
        (STATUS_RESCHEDULED, "Rescheduled"),
        (STATUS_COMPLETED, "Completed"),
    ]


    # ---------------------------------------------------------
    # COURSE
    # ---------------------------------------------------------

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="class_sessions"
    )


    # ---------------------------------------------------------
    # CLASS INFORMATION
    # ---------------------------------------------------------

    title = models.CharField(
        max_length=200,
        default="English Class"
    )

    # class_number is now mandatory.
    #
    # Already checked that:
    # - no existing sessions have class_number=None
    # - no course has duplicate class_numbers
    #
    # It is the stable identity of a lesson within a course,
    # even when the lesson is rescheduled.
    class_number = models.PositiveIntegerField(
        help_text="Lesson number within the course."
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    meeting_link = models.URLField(
        blank=True
    )

    topic = models.CharField(
        max_length=200,
        blank=True
    )


    # ---------------------------------------------------------
    # SESSION STATUS
    # ---------------------------------------------------------

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_SCHEDULED,
    )


    # ---------------------------------------------------------
    # METADATA
    # ---------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    # ---------------------------------------------------------
    # META
    # ---------------------------------------------------------

    class Meta:
        ordering = ["start_time"]

        constraints = [
            # A course can have only ONE Lesson 1,
            # ONE Lesson 2, ONE Lesson 3, etc.
            #
            # start_time is deliberately NOT used here because
            # start_time can change when a lesson is rescheduled.
            models.UniqueConstraint(
                fields=["course", "class_number"],
                name="unique_course_class_number"
            )
        ]


    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def clean(self):
        """
        Validate the ClassSession before it is saved through
        forms/Admin.

        A session must always finish after it starts.
        """

        super().clean()

        if (
            self.start_time
            and self.end_time
            and self.end_time <= self.start_time
        ):
            raise ValidationError({
                "end_time": (
                    "End time must be after start time."
                )
            })


    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    def save(self, *args, **kwargs):
        """
        Save the ClassSession and perform related updates.

        1. If the meeting link changes, propagate it to the
           other ClassSessions belonging to the same course.

        2. If this ClassSession changes TO status="completed",
           check whether every ClassSession belonging to the
           Course is now completed.

           If every ClassSession is completed:

               Course.status -> completed
               active CourseEnrollments -> completed
        """

        old_meeting_link = None
        old_status = None


        # -----------------------------------------------------
        # GET PREVIOUS VALUES BEFORE SAVING
        # -----------------------------------------------------

        if self.pk:
            old_session = ClassSession.objects.get(
                pk=self.pk
            )

            old_meeting_link = old_session.meeting_link
            old_status = old_session.status


        # -----------------------------------------------------
        # SAVE SESSION
        # -----------------------------------------------------
        #
        # Save first so that the database already contains
        # the latest:
        #
        # - status
        # - start_time
        # - end_time
        # - meeting_link
        #
        # before any related logic is executed.
        # -----------------------------------------------------

        super().save(*args, **kwargs)


        # -----------------------------------------------------
        # PROPAGATE MEETING LINK
        # -----------------------------------------------------
        #
        # The meeting link belongs conceptually to the course.
        #
        # Therefore, changing it on one ClassSession propagates
        # the same link to all the other sessions belonging to
        # the same course.
        #
        # QuerySet.update() is deliberate:
        # it avoids calling ClassSession.save() separately
        # for every other session.
        # -----------------------------------------------------

        if (
            self.meeting_link
            and self.meeting_link != old_meeting_link
        ):
            self.course.class_sessions.exclude(
                pk=self.pk
            ).update(
                meeting_link=self.meeting_link
            )


        # -----------------------------------------------------
        # CHECK COURSE COMPLETION
        # -----------------------------------------------------
        #
        # Only check the Course when THIS session has just
        # changed TO "completed".
        #
        # This avoids unnecessary Course queries when:
        #
        # - topic changes
        # - meeting link changes
        # - start_time changes
        # - end_time changes
        # - scheduled -> pending_reschedule
        # - pending_reschedule -> rescheduled
        #
        # Course.update_completion_status() then checks ALL
        # ClassSessions belonging to the Course.
        #
        # scheduled             -> unfinished
        # pending_reschedule    -> unfinished
        # rescheduled           -> unfinished
        # completed             -> finished
        #
        # The Course completes only when EVERY session is
        # completed.
        # -----------------------------------------------------

        became_completed = (
            self.status == self.STATUS_COMPLETED
            and old_status != self.STATUS_COMPLETED
        )

        if became_completed:
            self.course.update_completion_status()


    # ---------------------------------------------------------
    # STRING REPRESENTATION
    # ---------------------------------------------------------

    def __str__(self):
        return (
            f"{self.course} - "
            f"Lesson {self.class_number} - "
            f"{self.start_time:%d/%m/%Y %H:%M}"
        )


    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------

    @property
    def is_past(self):
        """
        Return True when the session's current end time
        has passed.

        IMPORTANT:

        is_past is only a date/time helper.

        A past ClassSession is NOT necessarily completed.

        For example:

            end_time in the past
            status = pending_reschedule

        means the lesson is still outstanding.

        Completion depends exclusively on:

            status == STATUS_COMPLETED
        """

        return self.end_time < timezone.now()



class Attendance(models.Model):
    """
    Stores the individual attendance record for one learner
    in one ClassSession.

    In a group/company course, many learners attend the same
    ClassSession, but each learner has their own Attendance record.

    Supports:
    - individual / 1-to-1 courses
    - group courses
    - company courses

    IMPORTANT:

    ClassSession controls the lifecycle of the LESSON:

        NORMAL FLOW:

            scheduled
                ↓
            completed

        RESCHEDULING FLOW:

            scheduled
                ↓
            pending_reschedule
                ↓
            rescheduled
                ↓
            completed

    Attendance controls only the individual LEARNER'S outcome
    for that lesson:

        scheduled
        attended
        missed
        excused

    Rescheduling does NOT create a new Attendance record.

    The existing Attendance record remains attached to the same
    ClassSession and normally remains status="scheduled" until
    the lesson actually takes place.
    """

    # ---------------------------------------------------------
    # ATTENDANCE STATUS
    # ---------------------------------------------------------

    STATUS_SCHEDULED = "scheduled"
    STATUS_ATTENDED = "attended"
    STATUS_MISSED = "missed"
    STATUS_EXCUSED = "excused"

    ATTENDANCE_STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_ATTENDED, "Attended"),
        (STATUS_MISSED, "Missed"),
        (STATUS_EXCUSED, "Excused"),
    ]


    # ---------------------------------------------------------
    # CLASS SESSION / STUDENT
    # ---------------------------------------------------------

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


    # ---------------------------------------------------------
    # ATTENDANCE INFORMATION
    # ---------------------------------------------------------

    status = models.CharField(
        max_length=30,
        choices=ATTENDANCE_STATUS_CHOICES,
        default=STATUS_SCHEDULED,
    )

    minutes_late = models.PositiveIntegerField(
        default=0,
        help_text="Number of minutes late. Use 0 if on time."
    )

    notes = models.TextField(
        blank=True
    )


    # ---------------------------------------------------------
    # METADATA
    # ---------------------------------------------------------

    recorded_at = models.DateTimeField(
        auto_now=True
    )


    # ---------------------------------------------------------
    # META
    # ---------------------------------------------------------

    class Meta:
        ordering = [
            "class_session__start_time",
            "student",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "class_session",
                    "student",
                ],
                name="unique_attendance_per_student_per_session"
            )
        ]


    # ---------------------------------------------------------
    # STRING REPRESENTATION
    # ---------------------------------------------------------

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.class_session} - "
            f"{self.get_status_display()}"
        )


    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------

    @property
    def was_punctual(self):
        """
        Returns True only when the learner attended
        and arrived on time.
        """

        return (
            self.status == self.STATUS_ATTENDED
            and self.minutes_late == 0
        )



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
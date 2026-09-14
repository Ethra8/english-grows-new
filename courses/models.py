from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from datetime import datetime, timedelta
from decimal import Decimal
from math import ceil

from courses.utils.course_dates import calculate_course_schedule


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
        ("confirmed", _("Confirmed")),
        ("active", _("Active")),
        ("paused", _("Paused")),
        ("completed", _("Completed")),
        ("cancelled", _("Cancelled")),
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

        else:
            # Existing courses may need their future scheduled lessons
            # synchronized when:
            # - a BankHoliday has been added/changed since course creation
            # - start_date / total_hours / class_duration has changed
            # - the Course is simply opened and saved again in Django Admin
            #
            # Avoid doing this for narrow internal saves such as:
            #     self.save(update_fields=["status"])
            # when the course is being marked completed.
            update_fields = kwargs.get("update_fields")

            should_sync_schedule = (
                update_fields is None
                or bool(
                    {
                        "start_date",
                        "total_hours",
                        "class_duration",
                    }
                    & set(update_fields)
                )
            )

            if should_sync_schedule:
                self.synchronize_future_scheduled_sessions()


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

        Bank-holiday handling does NOT happen here.
        It is applied later by calculate_course_schedule()
        inside generate_class_sessions().

        This guard makes automatic generation safe to call from several
        points in the model lifecycle without ever regenerating a course
        that already has ClassSessions.
        """

        if not self.pk:
            return False
        
        if self.status not in ["confirmed", "active"]:
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

        The actual teaching dates are calculated by
        calculate_course_schedule(), which takes into account:

        - course start_date
        - weekly timetable slots
        - number_of_classes
        - active BankHoliday records

        Therefore, ClassSessions are not generated on active bank holidays.

        Returns:
            generate_class_sessions() result when generation occurs.

            None when:
            - the Course is not ready
            - ClassSessions already exist

        IMPORTANT:
        This method never regenerates an existing course schedule.

        New learners enrolled later are handled separately by
        CourseEnrollment.create_future_attendance_records().
        """

        if not self.can_generate_class_sessions():
            return None

        return self.generate_class_sessions()


    def sync_end_date_from_sessions(self):
        """
        Synchronize Course.end_date with the actual final ClassSession.

        Once ClassSessions exist, they are the source of truth for the
        operational end date because individual lessons may later be
        rescheduled.

        QuerySet.update() is used deliberately to avoid re-entering
        Course.save() and triggering schedule synchronization recursively.
        """

        if not self.pk:
            return None

        final_session = (
            self.class_sessions
            .order_by("-start_time")
            .first()
        )

        if not final_session:
            return None

        calculated_end_date = timezone.localtime(
            final_session.start_time
        ).date()

        if self.end_date != calculated_end_date:
            Course.objects.filter(
                pk=self.pk
            ).update(
                end_date=calculated_end_date
            )

            self.end_date = calculated_end_date

        return calculated_end_date


    def synchronize_future_scheduled_sessions(self):
        """
        Recalculate future ClassSessions that are still status="scheduled"
        from the Course's canonical timetable.

        This is used to keep existing courses consistent when:
        - BankHoliday records are added or changed later
        - the course start date / duration data changes
        - a timetable slot changes

        Safety rules:
        - Held/complete sessions are NEVER moved.
        - pending_reschedule sessions are NEVER moved.
        - rescheduled sessions are NEVER moved.
        - Past sessions are NEVER moved.
        - Existing ClassSession IDs and class_numbers are preserved.
        - Attendance rows remain attached to the same ClassSession.
        - The final short lesson keeps its correct shortened duration.
        - end_date is synchronized from the actual final ClassSession.

        Returns the number of ClassSessions whose date/time changed.
        """

        if not self.pk:
            return 0

        if not self.start_date:
            return 0

        if not self.number_of_classes:
            return 0

        if not self.timetable_slots.exists():
            return 0

        if not self.class_sessions.exists():
            return 0

        schedule = calculate_course_schedule(self)

        if not schedule:
            return 0

        schedule_by_class_number = {
            item["class_number"]: item
            for item in schedule
        }

        now = timezone.now()
        current_timezone = timezone.get_current_timezone()

        future_scheduled_sessions = (
            self.class_sessions
            .filter(
                start_time__gte=now,
                status=ClassSession.STATUS_SCHEDULED,
            )
            .order_by("class_number")
        )

        sessions_updated = 0

        for session in future_scheduled_sessions:
            schedule_item = schedule_by_class_number.get(
                session.class_number
            )

            if not schedule_item:
                continue

            target_date = schedule_item["date"]
            slot = schedule_item["slot"]

            naive_start = datetime.combine(
                target_date,
                slot.start_time
            )

            target_start = timezone.make_aware(
                naive_start,
                current_timezone
            )

            # Never move a currently-future session backwards into the past.
            # This mainly protects established courses if their structural
            # settings are edited after teaching has already begun.
            if target_start < now:
                continue

            is_final_class = (
                session.class_number
                == self.number_of_classes
            )

            if (
                is_final_class
                and self.has_short_final_class
            ):
                target_end = target_start + timedelta(
                    seconds=float(
                        self.final_class_duration
                        * Decimal("3600")
                    )
                )

            else:
                naive_end = datetime.combine(
                    target_date,
                    slot.end_time
                )

                target_end = timezone.make_aware(
                    naive_end,
                    current_timezone
                )

            if (
                session.start_time == target_start
                and session.end_time == target_end
            ):
                continue

            session.start_time = target_start
            session.end_time = target_end

            session.save(
                update_fields=[
                    "start_time",
                    "end_time",
                ]
            )

            sessions_updated += 1

        self.sync_end_date_from_sessions()

        return sessions_updated


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

        return "/ ".join(
            slot.day_abbreviation
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
            f"{slot.day_abbreviation} "
            f"{slot.start_time.strftime('%H:%M')} - "
            f"{slot.end_time.strftime('%H:%M')}"
            for slot in slots
        )


    def generate_class_sessions(self):
        """
        Generate the complete set of ClassSession objects for this course
        using the centralized course schedule calculator.

        The schedule takes into account:
        - course start date
        - weekly timetable
        - number of classes
        - active bank holidays

        Bank holidays are skipped automatically.

        After the ClassSessions are generated, Attendance records are
        created for every learner who is already actively enrolled.

        This method remains defensive/idempotent:
        - a lesson is identified by course + class_number
        - an existing lesson is never duplicated
        - an existing lesson's date/time/status are never overwritten
        - missing Attendance records are created with get_or_create()

        IMPORTANT:
        Rescheduling never creates a replacement ClassSession.
        The existing ClassSession is updated and must eventually
        reach status="complete_attendance_submitted".
        """

        if not self.start_date:
            raise ValidationError(
                "This course needs a start date before sessions can be generated."
            )

        if not self.number_of_classes:
            raise ValidationError(
                "This course needs total hours and class duration before sessions can be generated."
            )

        if not self.timetable_slots.exists():
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

        # ---------------------------------------------------------
        # BUILD THE COURSE SCHEDULE
        # ---------------------------------------------------------
        #
        # This is now the single source of truth for lesson dates.
        #
        # It takes into account:
        # - start_date
        # - timetable slots
        # - number_of_classes
        # - active BankHoliday records
        #
        # Therefore, lessons are NOT generated on bank holidays.
        # ---------------------------------------------------------

        schedule = calculate_course_schedule(self)

        if not schedule:
            raise ValidationError(
                "A class schedule could not be generated for this course."
            )


        # ---------------------------------------------------------
        # SYNCHRONIZE COURSE END DATE
        # ---------------------------------------------------------
        #
        # The final scheduled lesson is the authoritative end date.
        # Because this uses the SAME schedule as ClassSession
        # generation, the two can never disagree.
        # ---------------------------------------------------------

        calculated_end_date = schedule[-1]["date"]

        if self.end_date != calculated_end_date:
            Course.objects.filter(
                pk=self.pk
            ).update(
                end_date=calculated_end_date
            )

            self.end_date = calculated_end_date

        sessions_created = 0
        attendances_created = 0
        selected_sessions = []


        # ---------------------------------------------------------
        # CREATE CLASS SESSIONS
        # ---------------------------------------------------------

        for schedule_item in schedule:

            current_date = schedule_item["date"]
            slot = schedule_item["slot"]
            class_number = schedule_item["class_number"]

            naive_start = datetime.combine(
                current_date,
                slot.start_time
            )

            aware_start = timezone.make_aware(
                naive_start,
                timezone.get_current_timezone()
            )

            # -----------------------------------------------------
            # CALCULATE CLASS END TIME
            # -----------------------------------------------------
            #
            # The final lesson may be shorter when total_hours
            # is not perfectly divisible by standard class duration.
            # -----------------------------------------------------

            is_final_class = (
                class_number == self.number_of_classes
            )

            if (
                is_final_class
                and self.has_short_final_class
            ):
                aware_end = aware_start + timedelta(
                    seconds=float(
                        self.final_class_duration
                        * Decimal("3600")
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

            # -----------------------------------------------------
            # CREATE OR RETRIEVE CLASS SESSION
            # -----------------------------------------------------
            #
            # class_number is the stable identity of the lesson.
            #
            # start_time is deliberately NOT used because lessons
            # may later be rescheduled.
            # -----------------------------------------------------

            class_session, created = (
                ClassSession.objects.get_or_create(
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
            )

            if created:
                sessions_created += 1

            else:
                # Do not overwrite start_time, end_time or status.
                #
                # An existing ClassSession may have been rescheduled.
                if class_session.title != expected_title:
                    class_session.title = expected_title

                    class_session.save(
                        update_fields=[
                            "title",
                        ]
                    )

            selected_sessions.append(
                class_session
            )

        # ---------------------------------------------------------
        # CREATE ATTENDANCE RECORDS
        # ---------------------------------------------------------
        #
        # Create missing Attendance rows for learners who are
        # actively enrolled when the initial schedule is generated.
        # ---------------------------------------------------------

        for class_session in selected_sessions:

            for student in enrolled_students:

                _, attendance_created = (
                    Attendance.objects.get_or_create(
                        class_session=class_session,
                        student=student,
                        defaults={
                            "status": Attendance.STATUS_PENDING,
                        }
                    )
                )

                if attendance_created:
                    attendances_created += 1

        # ClassSessions now exist, so use the actual final session as the
        # authoritative operational end date.
        self.sync_end_date_from_sessions()

        return {
            "sessions_created": sessions_created,
            "attendances_created": attendances_created,
            "students_count": len(enrolled_students),
            "total_scheduled_classes": len(schedule),
        }

    @property
    def total_sessions(self):
        """
        Total number of ClassSession records belonging to this course.

        No sessions are excluded based on lifecycle status.
        """
        return self.class_sessions.count()


    @property
    def held_attendance_pending_sessions(self):
        """
        Number of lessons that have been held but whose attendance
        has not yet been fully submitted.
        """
        return self.class_sessions.filter(
            status=ClassSession.STATUS_HELD_ATTENDANCE_PENDING
        ).count()


    @property
    def complete_attendance_submitted_sessions(self):
        """
        Number of lessons that have been held and whose attendance
        has been fully submitted.
        """
        return self.class_sessions.filter(
            status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
        ).count()


    @property
    def total_held_sessions(self):
        """
        Total number of lessons that have been held, regardless of
        whether attendance is pending or already submitted.
        """
        return self.class_sessions.filter(
            status__in=[
                ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            ]
        ).count()


    @property
    def completed_sessions(self):
        """
        Backwards-compatible alias for lessons whose attendance has
        been fully submitted.

        Prefer complete_attendance_submitted_sessions in new code.
        """
        return self.complete_attendance_submitted_sessions


    @property
    def remaining_sessions(self):
        """
        ClassSessions that still require teaching.

        Held, complete and cancelled sessions are not outstanding
        teaching sessions.
        """
        return self.class_sessions.filter(
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_PENDING_RESCHEDULE,
                ClassSession.STATUS_RESCHEDULED,
            ]
        ).count()


    @property
    def teaching_progress_percentage(self):
        """
        Percentage of this course's ClassSessions that have been held,
        regardless of whether attendance has already been submitted.
        """
        if self.total_sessions == 0:
            return 0

        return round(
            (
                self.total_held_sessions
                / self.total_sessions
            ) * 100
        )


    @property
    def completion_percentage(self):
        """
        Backwards-compatible course teaching progress percentage.

        Prefer teaching_progress_percentage in new code.
        """
        return self.teaching_progress_percentage


    def update_completion_status(self):
        """
        Mark the Course as completed only when EVERY ClassSession
        has reached the terminal status:

            complete_attendance_submitted

        Active enrollments are also marked completed at the same time.

        Returns:
            True  -> all sessions are complete and attendance submitted
            False -> at least one session is still outstanding
        """

        # A course with no sessions should never auto-complete.
        if not self.class_sessions.exists():
            return False

        has_unfinished_sessions = (
            self.class_sessions
            .exclude(
                status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            )
            .exists()
        )

        if has_unfinished_sessions:
            return False

        if self.status != "completed":
            self.status = "completed"
            self.save(
                update_fields=["status"]
            )

        self.enrollments.filter(
            status="active"
        ).update(
            status="completed"
        )

        return True

    def cancel_future_sessions(self):
        """
        Cancel future ClassSessions that have not yet been held.

        Attendance does not have a cancelled learner outcome. Instead,
        untouched Attendance(status="scheduled") placeholders are deleted
        because a cancelled lesson will never produce an attendance outcome.

        Genuine attendance history (attended/missed/excused) is never deleted.

        Returns the number of ClassSessions cancelled.
        """

        future_sessions = self.class_sessions.filter(
            start_time__gte=timezone.now(),
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_PENDING_RESCHEDULE,
                ClassSession.STATUS_RESCHEDULED,
            ],
        )

        session_ids = list(
            future_sessions.values_list("id", flat=True)
        )

        if not session_ids:
            return 0

        with transaction.atomic():
            Attendance.objects.filter(
                class_session_id__in=session_ids,
                status=Attendance.STATUS_PENDING,
            ).delete()

            cancelled_count = future_sessions.update(
                status=ClassSession.STATUS_CANCELLED
            )

        return cancelled_count



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
        (MONDAY, _("Monday")),
        (TUESDAY, _("Tuesday")),
        (WEDNESDAY, _("Wednesday")),
        (THURSDAY, _("Thursday")),
        (FRIDAY, _("Friday")),
        (SATURDAY, _("Saturday")),
        (SUNDAY, _("Sunday")),
    ]

    DAY_ABBREVIATIONS = {
        MONDAY: _("Mon."),
        TUESDAY: _("Tue."),
        WEDNESDAY: _("Wed."),
        THURSDAY: _("Thu."),
        FRIDAY: _("Fri."),
        SATURDAY: _("Sat."),
        SUNDAY: _("Sun."),
    }

    @property
    def day_abbreviation(self):
        return str (
            self.DAY_ABBREVIATIONS[self.day_of_week]   
        )


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

    def update_future_class_sessions(self, old_slot=None):
        """
        Synchronize the Course's complete future scheduled timetable.

        This delegates to Course.synchronize_future_scheduled_sessions()
        so timetable edits and BankHoliday changes use the SAME canonical
        scheduling logic as initial ClassSession generation.

        old_slot is retained as an optional argument for backwards
        compatibility with existing callers, but is no longer needed.
        """

        return self.course.synchronize_future_scheduled_sessions()


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
    - already-held / complete / cancelled ClassSessions are NOT
      assigned retroactively
    - scheduled / pending_reschedule / rescheduled sessions
      are assigned

    A ClassSession has completed its lesson + attendance workflow
    ONLY when:

        ClassSession.status == "complete_attendance_submitted"
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
        Create missing Attendance records for this learner only for
        ClassSessions that have not yet been held.

        Included:
        - scheduled
        - pending_reschedule
        - rescheduled

        Excluded:
        - held_attendance_pending
        - complete_attendance_submitted
        - cancelled

        This prevents a learner who joins later from being assigned
        retroactively to a lesson that has already been held.
        """

        eligible_sessions = (
            self.course.class_sessions
            .filter(
                status__in=[
                    ClassSession.STATUS_SCHEDULED,
                    ClassSession.STATUS_PENDING_RESCHEDULE,
                    ClassSession.STATUS_RESCHEDULED,
                ]
            )
            .order_by("start_time")
        )

        for session in eligible_sessions:
            Attendance.objects.get_or_create(
                student=self.student,
                class_session=session,
                defaults={
                    "status": Attendance.STATUS_PENDING,
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
    # HELD / COMPLETE CLASSES
    # ---------------------------------------------------------

    @property
    def held_attendance_pending_classes(self):
        """
        Assigned lessons that have been held but whose attendance
        has not yet been fully submitted.
        """

        return (
            self.eligible_sessions
            .filter(
                status=ClassSession.STATUS_HELD_ATTENDANCE_PENDING
            )
            .count()
        )


    @property
    def complete_attendance_submitted_classes(self):
        """
        Assigned lessons that have been held and whose attendance
        has been fully submitted.
        """

        return (
            self.eligible_sessions
            .filter(
                status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            )
            .count()
        )


    @property
    def total_held_classes(self):
        """
        Total assigned lessons that have been held, regardless of
        whether attendance is pending or already submitted.
        """

        return (
            self.eligible_sessions
            .filter(
                status__in=[
                    ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                    ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
                ]
            )
            .count()
        )


    @property
    def total_completed_classes(self):
        """
        Backwards-compatible alias for assigned lessons whose attendance
        has been fully submitted.

        Prefer complete_attendance_submitted_classes in new code.
        """

        return self.complete_attendance_submitted_classes


    # ---------------------------------------------------------
    # REMAINING / UPCOMING CLASSES
    # ---------------------------------------------------------

    @property
    def remaining_classes(self):
        """
        Number of assigned sessions that still require teaching.

        Included:
        - scheduled
        - pending_reschedule
        - rescheduled

        Held and cancelled lessons are excluded.
        """

        return (
            self.eligible_sessions
            .filter(
                status__in=[
                    ClassSession.STATUS_SCHEDULED,
                    ClassSession.STATUS_PENDING_RESCHEDULE,
                    ClassSession.STATUS_RESCHEDULED,
                ]
            )
            .count()
        )


    @property
    def upcoming_classes(self):
        """
        Backwards-compatible alias for remaining_classes.
        """

        return self.remaining_classes


    # ---------------------------------------------------------
    # ATTENDED CLASSES
    # ---------------------------------------------------------

    @property
    def classes_attended(self):
        """
        ClassSessions with submitted attendance where this learner
        was marked as attended.
        """

        return (
            Attendance.objects
            .filter(
                student=self.student,
                class_session__course=self.course,
                class_session__status=(
                    ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
                ),
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
        ClassSessions with submitted attendance where this learner
        was marked as missed.
        """

        return (
            Attendance.objects
            .filter(
                student=self.student,
                class_session__course=self.course,
                class_session__status=(
                    ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
                ),
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
        ClassSessions with submitted attendance where this learner
        was marked as excused.
        """

        return (
            Attendance.objects
            .filter(
                student=self.student,
                class_session__course=self.course,
                class_session__status=(
                    ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
                ),
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
        Total missed + excused lessons with submitted attendance.
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
        Attendance percentage calculated only from lessons whose
        attendance has been fully submitted.

        Example:

        10 complete_attendance_submitted classes
        8 attended

        attendance_percentage = 80
        """

        total = self.complete_attendance_submitted_classes

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

        No warning is shown until at least one ClassSession has
        submitted attendance.
        """

        if self.complete_attendance_submitted_classes == 0:
            return False

        return self.attendance_percentage < 75


    # ---------------------------------------------------------
    # SAFE ENROLLMENT DELETION
    # ---------------------------------------------------------

    @property
    def can_be_deleted(self):
        """
        Return whether this enrollment can safely be permanently deleted.

        Permanent deletion is intended only for enrollments created
        by mistake.

        Genuine attendance history consists of Attendance records
        explicitly recorded as:

        - attended
        - missed
        - excused

        Other operational statuses do not, by themselves, prevent
        deletion.
        """

        if not self.pk:
            return True

        return not Attendance.objects.filter(
            student=self.student,
            class_session__course=self.course,
            status__in=[
                Attendance.STATUS_ATTENDED,
                Attendance.STATUS_MISSED,
                Attendance.STATUS_EXCUSED,
            ],
        ).exists()


    def delete(self, *args, **kwargs):
        """
        Permanently delete an erroneous enrollment.

        Deletion is blocked when genuine attendance history exists.

        When deletion is permitted:
        - all Attendance records for this learner/course are removed
        - the CourseEnrollment itself is removed
        - both operations happen inside one database transaction

        A legitimate enrollment that should remain part of the
        historical record must be marked cancelled instead.
        """

        if not self.can_be_deleted:
            raise ValidationError(
                "This enrollment cannot be deleted because attendance "
                "has already been recorded for this learner."
            )

        with transaction.atomic():

            Attendance.objects.filter(
                student=self.student,
                class_session__course=self.course,
            ).delete()

            return super().delete(*args, **kwargs)



class ClassSession(models.Model):
    """
    One scheduled lesson for a specific course.

    A ClassSession is created once when the course sessions
    are initially generated.

    NORMAL FLOW:

        scheduled
            ↓
        lesson ends
            ↓
        ┌─────────────────────────────────────┐
        │ attendance already submitted       │
        │ → complete_attendance_submitted    │
        │                                     │
        │ attendance not yet submitted       │
        │ → held_attendance_pending          │
        └─────────────────────────────────────┘

        held_attendance_pending
            ↓
        attendance submitted
            ↓
        complete_attendance_submitted

    RESCHEDULING FLOW:

        scheduled
            ↓
        pending_reschedule
            ↓
        rescheduled
            ↓
        lesson ends
            ↓
        held_attendance_pending
            OR
        complete_attendance_submitted

    CANCELLATION FLOW:

        scheduled / pending_reschedule / rescheduled
            ↓
        cancelled

    IMPORTANT:

    Attendance records MAY be submitted after start_time but
    before end_time.

    In that case the Attendance records are stored immediately,
    but the ClassSession remains scheduled/rescheduled until the
    lesson has actually ended.

    After end_time:
    - submitted attendance -> complete_attendance_submitted
    - attendance pending   -> held_attendance_pending

    A rescheduled lesson remains the SAME ClassSession object.
    Rescheduling does NOT create a new ClassSession.

    Every ClassSession belonging to a course must eventually
    reach complete_attendance_submitted before the Course itself
    can be automatically marked as completed.
    """

    # ---------------------------------------------------------
    # STATUS CHOICES
    # ---------------------------------------------------------
    STATUS_SCHEDULED = "scheduled"
    STATUS_PENDING_RESCHEDULE = "pending_reschedule"
    STATUS_RESCHEDULED = "rescheduled"
    STATUS_HELD_ATTENDANCE_PENDING = "held_attendance_pending"
    STATUS_COMPLETE_ATTENDANCE_SUBMITTED = "complete_attendance_submitted"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_PENDING_RESCHEDULE, "Pending reschedule"),
        (STATUS_RESCHEDULED, "Rescheduled"),
        (STATUS_HELD_ATTENDANCE_PENDING, "Held — attendance pending"),
        (STATUS_COMPLETE_ATTENDANCE_SUBMITTED, "Complete — attendance submitted"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    # ---------------------------------------------------------
    # COURSE
    # ---------------------------------------------------------
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="class_sessions",
    )

    # ---------------------------------------------------------
    # CLASS INFORMATION
    # ---------------------------------------------------------
    title = models.CharField(
        max_length=200,
        default="English Class",
    )

    # Stable lesson identity within the Course.
    # It does not change when a lesson is rescheduled.
    class_number = models.PositiveIntegerField(
        help_text="Lesson number within the course."
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    meeting_link = models.URLField(blank=True)
    topic = models.CharField(max_length=200, blank=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

    # ---------------------------------------------------------
    # META
    # ---------------------------------------------------------
    class Meta:
        ordering = ["start_time"]

        constraints = [
            # A course can have only ONE Lesson 1,
            # ONE Lesson 2, ONE Lesson 3, etc.
            #
            # start_time is deliberately NOT used because it
            # can change when a lesson is rescheduled.
            models.UniqueConstraint(
                fields=["course", "class_number"],
                name="unique_course_class_number",
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
                "end_time": "End time must be after start time."
            })

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------
    def save(self, *args, **kwargs):
        """
        Save the ClassSession and perform related updates.

        1. If the meeting link changes, propagate it to the
           other ClassSessions belonging to the same course.

        2. If this ClassSession changes TO
           complete_attendance_submitted, check whether every
           ClassSession belonging to the Course has reached
           that same terminal status.

        If every ClassSession is complete:
            Course.status -> completed
            active CourseEnrollments -> completed
        """
        old_meeting_link = None
        old_status = None

        if self.pk:
            old_session = ClassSession.objects.get(pk=self.pk)
            old_meeting_link = old_session.meeting_link
            old_status = old_session.status

        super().save(*args, **kwargs)

        if (
            self.meeting_link
            and self.meeting_link != old_meeting_link
        ):
            self.course.class_sessions.exclude(pk=self.pk).update(
                meeting_link=self.meeting_link
            )

        became_complete = (
            self.status == self.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            and old_status != self.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
        )

        if became_complete:
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
    # TIME / LIFECYCLE HELPERS
    # ---------------------------------------------------------
    @property
    def is_past(self):
        """
        Return True when the session's current end_time has passed.

        This is only a temporal helper.

        A past pending_reschedule or cancelled session was not
        necessarily held.
        """
        return self.end_time <= timezone.now()

    @property
    def is_held(self):
        """
        Return True only when the lifecycle explicitly records
        that the lesson has been held.
        """
        return self.status in {
            self.STATUS_HELD_ATTENDANCE_PENDING,
            self.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
        }

    @property
    def attendance_is_pending(self):
        """
        Return True when the lesson has ended but attendance
        has not yet been fully submitted.
        """
        return self.status == self.STATUS_HELD_ATTENDANCE_PENDING

    @property
    def attendance_is_submitted(self):
        """
        Return True when the lesson has ended AND attendance
        has been fully submitted.

        This describes the ClassSession lifecycle state.

        It is deliberately different from
        attendance_records_submitted, because Attendance records
        may be submitted before the lesson ends.
        """
        return self.status == self.STATUS_COMPLETE_ATTENDANCE_SUBMITTED

    # ---------------------------------------------------------
    # ATTENDANCE RECORD STATE
    # ---------------------------------------------------------
    @property
    def attendance_records_submitted(self):
        """
        Return True when this ClassSession has Attendance records
        and every record contains a final submitted outcome.

        Final Attendance outcomes:
        - attended
        - missed
        - excused

        This may legitimately be True BEFORE end_time while the
        ClassSession itself is still scheduled/rescheduled.
        """
        attendance_records = self.attendance_records.all()

        if not attendance_records.exists():
            return False

        final_statuses = {
            Attendance.STATUS_ATTENDED,
            Attendance.STATUS_MISSED,
            Attendance.STATUS_EXCUSED,
        }

        return not attendance_records.exclude(
            status__in=final_statuses
        ).exists()

    # ---------------------------------------------------------
    # SYNCHRONIZE ONE FINISHED SESSION
    # ---------------------------------------------------------
    def synchronize_status_after_end(self):
        """
        Synchronize this ClassSession after its end_time passes.

        scheduled/rescheduled + attendance already submitted
            -> complete_attendance_submitted

        scheduled/rescheduled + attendance not submitted
            -> held_attendance_pending

        pending_reschedule and cancelled are deliberately untouched.

        Returns:
            True  -> status changed
            False -> no transition was required
        """
        if not self.pk:
            return False

        with transaction.atomic():
            session = (
                ClassSession.objects
                .select_for_update()
                .select_related("course")
                .get(pk=self.pk)
            )

            if session.status not in {
                self.STATUS_SCHEDULED,
                self.STATUS_RESCHEDULED,
            }:
                self.status = session.status
                return False

            if not session.is_past:
                self.status = session.status
                return False

            if session.attendance_records_submitted:
                session.status = self.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            else:
                session.status = self.STATUS_HELD_ATTENDANCE_PENDING

            # Deliberately use save(), rather than QuerySet.update(),
            # because transitioning directly to COMPLETE must trigger
            # Course.update_completion_status().
            session.save(update_fields=["status"])

            self.status = session.status

        return True

    # ---------------------------------------------------------
    # SYNCHRONIZE ALL FINISHED SESSIONS
    # ---------------------------------------------------------
    @classmethod
    def transition_past_sessions(cls, course=None):
        """
        Synchronize finished scheduled/rescheduled ClassSessions.

        For every eligible lesson:

        attendance already submitted
            -> complete_attendance_submitted

        attendance not submitted
            -> held_attendance_pending

        If course is provided, only sessions belonging to that
        Course are synchronized.

        Without course, all eligible ClassSessions are synchronized.

        Returns the number of ClassSessions whose status changed.
        """
        sessions = cls.objects.filter(
            end_time__lte=timezone.now(),
            status__in=[
                cls.STATUS_SCHEDULED,
                cls.STATUS_RESCHEDULED,
            ],
        )

        if course is not None:
            sessions = sessions.filter(course=course)

        session_ids = list(
            sessions.values_list("pk", flat=True)
        )

        updated_count = 0

        for session_id in session_ids:
            session = cls.objects.get(pk=session_id)

            if session.synchronize_status_after_end():
                updated_count += 1

        return updated_count

    # ---------------------------------------------------------
    # TEMPORARY BACKWARDS-COMPATIBILITY WRAPPERS
    #
    # Keep these while existing views / the deployed Render
    # management command still call the old method names.
    #
    # They now execute the NEW business logic.
    # ---------------------------------------------------------
    # def transition_to_held_if_past(self):
    #     return self.synchronize_status_after_end()

    # @classmethod
    # def transition_past_sessions_to_held(cls, course=None):
    #     return cls.transition_past_sessions(course=course)

    def update_status_from_attendance(self):
        """
        Mark this ClassSession as complete_attendance_submitted when:

        - the lesson has ended;
        - its lifecycle is eligible to become complete; and
        - every Attendance record has a submitted outcome.

        Attendance may be submitted before end_time, but the
        ClassSession must not become complete until the lesson ends.

        Returns:
            True  -> status changed
            False -> no transition was required
        """
        if self.status not in {
            self.STATUS_SCHEDULED,
            self.STATUS_RESCHEDULED,
            self.STATUS_HELD_ATTENDANCE_PENDING,
        }:
            return False

        if not self.is_past:
            return False

        if not self.attendance_records_submitted:
            return False

        self.status = self.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
        self.save(update_fields=["status"])

        return True


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

            pending
                ↓
            held_attendance_pending
                ↓
            complete_attendance_submitted

        RESCHEDULING FLOW:

            pending
                ↓
            pending_reschedule
                ↓
            rescheduled
                ↓
            held_attendance_pending
                ↓
            complete_attendance_submitted

    Attendance controls only the individual LEARNER'S outcome
    for that lesson:

        pending
        attended
        missed
        excused

    Rescheduling does NOT create a new Attendance record.

    The existing Attendance record remains attached to the same
    ClassSession and normally remains status="scheduled" until
    the lesson actually takes place.

    If a future ClassSession is cancelled, untouched scheduled
    Attendance placeholders are deleted because no learner attendance
    outcome can exist for a lesson that never takes place.
    """

    # ---------------------------------------------------------
    # ATTENDANCE STATUS
    # ---------------------------------------------------------

    STATUS_PENDING = "pending"
    STATUS_ATTENDED = "attended"
    STATUS_MISSED = "missed"
    STATUS_EXCUSED = "excused"

    ATTENDANCE_STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
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
        default=STATUS_PENDING,
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
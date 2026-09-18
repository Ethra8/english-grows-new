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



class Programme(models.Model):
    """
    Reusable training programme category that defines the broad
    learning focus of a course.

    Initial programme examples:
    - Meetings & Negotiations
    - Presentations & Speeches
    - Business English Communication
    - Email & Written Communication
    - Everyday General English
    - Cambridge Exams Preparation

    A course can be linked to multiple programmes so that training
    can be combined and adapted to the organisation's objectives.
    """
    name = models.CharField(
        max_length=120,
        unique=True
    )

    slug = models.SlugField(
        max_length=140,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    icon = models.ImageField(
        upload_to="programme_icons/",
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(
        default=True
    )

    order = models.PositiveSmallIntegerField(
        default=0
    )

    class Meta:
        ordering = ["order", "name"]

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

    programmes = models.ManyToManyField(
        Programme,
        blank=True,
        related_name="courses"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        """
        Save the Course and enforce Course-level lifecycle transitions.

        Status transitions:

        -> paused:
           future scheduled/rescheduled ClassSessions become
           pending_reschedule because their current teaching slot
           is no longer valid.

        -> cancelled:
           unresolved ClassSessions that will no longer take place
           are cancelled through cancel_future_sessions().

        Schedule synchronization:

        Existing future scheduled ClassSessions are synchronized only
        when a schedule-defining Course field actually changes:
        - start_date
        - total_hours
        - class_duration

        Simply opening and saving an unchanged Course must NEVER
        reschedule its ClassSessions.

        Timetable changes are handled separately by CourseTimetableSlot.

        Course status does not alter individual CourseEnrollment
        statuses or learner-specific Attendance outcomes.
        """
        is_new = self.pk is None

        with transaction.atomic():
            old_class_duration = None
            old_total_hours = None
            old_start_date = None
            old_status = None

            if self.pk:
                old_course = (
                    Course.objects
                    .select_for_update()
                    .get(pk=self.pk)
                )
                old_class_duration = old_course.class_duration
                old_total_hours = old_course.total_hours
                old_start_date = old_course.start_date
                old_status = old_course.status

            if self.total_hours is None and self.course_type.default_hours is not None:
                self.total_hours = self.course_type.default_hours

            if self.class_duration and (
                is_new
                or self.class_duration != old_class_duration
            ):
                self.class_duration_source = "manual"

            became_paused = (
                self.status == "paused"
                and old_status != "paused"
            )

            became_cancelled = (
                self.status == "cancelled"
                and old_status != "cancelled"
            )

            update_fields = kwargs.get("update_fields")

            changed_schedule_fields = set()

            if not is_new:
                if self.start_date != old_start_date:
                    changed_schedule_fields.add("start_date")

                if self.total_hours != old_total_hours:
                    changed_schedule_fields.add("total_hours")

                if self.class_duration != old_class_duration:
                    changed_schedule_fields.add("class_duration")

                if update_fields is not None:
                    changed_schedule_fields &= set(update_fields)

            super().save(*args, **kwargs)

            # ---------------------------------------------------------
            # COURSE STATUS TRANSITIONS
            # ---------------------------------------------------------
            if became_paused:
                self.pause_future_sessions()

            if became_cancelled:
                self.cancel_future_sessions()

            # ---------------------------------------------------------
            # INITIAL CLASS SESSION GENERATION
            # ---------------------------------------------------------
            if is_new:
                self.try_generate_class_sessions()

            # ---------------------------------------------------------
            # EXISTING COURSE SCHEDULE SYNCHRONIZATION
            # ---------------------------------------------------------
            #
            # Only genuine schedule-defining field changes trigger
            # synchronization. An unchanged Admin save must do nothing.
            # ---------------------------------------------------------
            elif (
                self.status in {
                    "confirmed",
                    "active",
                }
                and changed_schedule_fields
            ):
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
        Rebuild ONLY the remaining future scheduled teaching sequence
        from the Course's CURRENT timetable.

        This method is deliberately different from initial generation.

        Initial generation:
        - starts from Course.start_date
        - creates the complete lesson sequence

        Existing-course synchronization:
        - preserves every ClassSession object and class_number
        - preserves all held / complete history
        - preserves pending_reschedule and rescheduled lessons
        - preserves lessons that have already started
        - moves only future ClassSessions still status="scheduled"
        - starts the replacement teaching sequence from now / start_date
        - skips active BankHoliday dates
        - skips times already occupied by protected future lessons

        IMPORTANT:

        We must NOT recalculate the whole course from Lesson 1 and then
        selectively apply those dates by class_number. Doing so can mix
        an old historical timetable with a new future timetable and create
        duplicate or chronologically corrupted lesson sequences.

        Returns the number of ClassSessions whose date/time changed.
        """
        if not self.pk:
            return 0

        if self.status not in {
            "confirmed",
            "active",
        }:
            return 0

        if not self.start_date:
            return 0

        timetable_slots = list(
            self.timetable_slots
            .all()
            .order_by(
                "day_of_week",
                "start_time",
            )
        )

        if not timetable_slots:
            return 0

        now = timezone.now()
        current_timezone = timezone.get_current_timezone()

        with transaction.atomic():
            all_sessions = list(
                self.class_sessions
                .select_for_update()
                .all()
            )

            if not all_sessions:
                return 0

            # -----------------------------------------------------
            # FUTURE SCHEDULED SESSIONS THAT MAY BE MOVED
            # -----------------------------------------------------
            mutable_sessions = sorted(
                [
                    session
                    for session in all_sessions
                    if (
                        session.status == ClassSession.STATUS_SCHEDULED
                        and session.start_time > now
                    )
                ],
                key=lambda session: (
                    session.class_number,
                    session.start_time,
                ),
            )

            if not mutable_sessions:
                self.sync_end_date_from_sessions()
                return 0

            # -----------------------------------------------------
            # PROTECT AGAINST EXISTING SEQUENCE CORRUPTION
            # -----------------------------------------------------
            #
            # Once Lesson N has genuinely been held, an earlier numbered
            # lesson must not still exist as an ordinary future scheduled
            # lesson. That indicates pre-existing inconsistent data and
            # must be repaired deliberately rather than "fixed" by another
            # automatic schedule synchronization.
            # -----------------------------------------------------
            held_class_numbers = [
                session.class_number
                for session in all_sessions
                if session.status in {
                    ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                    ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
                }
            ]

            if held_class_numbers:
                highest_held_class_number = max(held_class_numbers)

                invalid_future_numbers = [
                    session.class_number
                    for session in mutable_sessions
                    if session.class_number <= highest_held_class_number
                ]

                if invalid_future_numbers:
                    raise ValidationError(
                        "This Course has future scheduled lessons whose "
                        "class numbers precede an already-held lesson. "
                        "Automatic schedule synchronization has been blocked "
                        "to protect historical ClassSession data. "
                        "Repair the inconsistent Course schedule first."
                    )

            mutable_session_ids = {
                session.pk
                for session in mutable_sessions
            }

            # -----------------------------------------------------
            # PROTECTED FUTURE TEACHING WINDOWS
            # -----------------------------------------------------
            #
            # pending_reschedule:
            # - its stored slot is no longer a valid teaching appointment
            #
            # cancelled:
            # - it will not take place
            #
            # Every other non-mutable future session is treated as fixed
            # and blocks overlapping automatically scheduled slots.
            # -----------------------------------------------------
            blocked_intervals = [
                (
                    session.start_time,
                    session.end_time,
                )
                for session in all_sessions
                if (
                    session.pk not in mutable_session_ids
                    and session.end_time > now
                    and session.status not in {
                        ClassSession.STATUS_PENDING_RESCHEDULE,
                        ClassSession.STATUS_CANCELLED,
                    }
                )
            ]

            # -----------------------------------------------------
            # ACTIVE BANK HOLIDAYS
            # -----------------------------------------------------
            holiday_ranges = list(
                BankHoliday.objects
                .filter(
                    is_active=True,
                    start_date__isnull=False,
                )
                .values_list(
                    "start_date",
                    "end_date",
                )
            )

            def is_bank_holiday(candidate_date):
                return any(
                    start_date
                    <= candidate_date
                    <= (end_date or start_date)
                    for start_date, end_date in holiday_ranges
                )

            def overlaps_blocked_interval(candidate_start, candidate_end):
                return any(
                    candidate_start < blocked_end
                    and candidate_end > blocked_start
                    for blocked_start, blocked_end in blocked_intervals
                )

            # -----------------------------------------------------
            # FUTURE TIMETABLE SLOT GENERATOR
            # -----------------------------------------------------
            #
            # Continue from today for an in-progress Course, or from the
            # Course start_date when the Course has not started yet.
            # -----------------------------------------------------
            local_today = timezone.localtime(
                now,
                current_timezone,
            ).date()

            candidate_date = max(
                self.start_date,
                local_today,
            )

            max_days_to_scan = max(
                3660,
                len(mutable_sessions) * 14,
            )

            def future_timetable_slots():
                current_date = candidate_date

                for _ in range(max_days_to_scan):
                    if not is_bank_holiday(current_date):
                        current_day = current_date.isoweekday()

                        for slot in timetable_slots:
                            if slot.day_of_week != current_day:
                                continue

                            naive_start = datetime.combine(
                                current_date,
                                slot.start_time,
                            )

                            naive_end = datetime.combine(
                                current_date,
                                slot.end_time,
                            )

                            target_start = timezone.make_aware(
                                naive_start,
                                current_timezone,
                            )

                            target_end = timezone.make_aware(
                                naive_end,
                                current_timezone,
                            )

                            if target_start <= now:
                                continue

                            yield (
                                target_start,
                                target_end,
                            )

                    current_date += timedelta(days=1)

            slot_iterator = future_timetable_slots()
            sessions_to_update = []

            # -----------------------------------------------------
            # ASSIGN THE NEW FUTURE SEQUENCE
            # -----------------------------------------------------
            for session in mutable_sessions:
                slot_found = False

                for target_start, standard_target_end in slot_iterator:
                    target_end = standard_target_end

                    if (
                        session.class_number == self.number_of_classes
                        and self.has_short_final_class
                    ):
                        target_end = target_start + timedelta(
                            seconds=float(
                                self.final_class_duration
                                * Decimal("3600")
                            )
                        )

                    if overlaps_blocked_interval(
                        target_start,
                        target_end,
                    ):
                        continue

                    blocked_intervals.append(
                        (
                            target_start,
                            target_end,
                        )
                    )

                    slot_found = True
                    break

                if not slot_found:
                    raise ValidationError(
                        "A safe future timetable could not be generated "
                        "for all remaining scheduled ClassSessions."
                    )

                if (
                    session.start_time == target_start
                    and session.end_time == target_end
                ):
                    continue

                session.start_time = target_start
                session.end_time = target_end
                sessions_to_update.append(session)

            if sessions_to_update:
                ClassSession.objects.bulk_update(
                    sessions_to_update,
                    [
                        "start_time",
                        "end_time",
                    ],
                )

            self.sync_end_date_from_sessions()

        return len(sessions_to_update)


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

    # ---------------------------------------------------------
    # COURSE-WIDE DELIVERY
    #
    # Course is the source of truth for whole-course delivery:
    #
    # - total lessons
    # - held lessons
    # - attendance-pending held lessons
    # - attendance-submitted held lessons
    # - remaining lessons
    # - total course minutes
    # - held minutes / hours
    # - delivery percentage
    #
    # Display formatting remains outside the model.
    # ---------------------------------------------------------

    def _held_sessions_queryset(self):
        """
        Whole-course ClassSessions that have actually been taught.

        Attendance may still be pending or already submitted.
        """
        return self.class_sessions.filter(
            status__in=[
                ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            ]
        )


    def _remaining_sessions_queryset(self):
        """
        Whole-course ClassSessions that still require teaching.
        """
        return self.class_sessions.filter(
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_PENDING_RESCHEDULE,
                ClassSession.STATUS_RESCHEDULED,
            ]
        )


    @staticmethod
    def _calculate_session_minutes(sessions):
        """
        Return the combined actual duration of a ClassSession queryset
        in whole minutes.

        Uses each session's actual start/end times so shorter final
        classes and rescheduled lessons are handled correctly.
        """
        total_seconds = sum(
            (end_time - start_time).total_seconds()
            for start_time, end_time
            in sessions.values_list("start_time", "end_time")
            if start_time and end_time
        )

        return round(total_seconds / 60)


    # ---------------------------------------------------------
    # SESSION COUNTS
    # ---------------------------------------------------------

    @property
    def total_sessions(self):
        """
        Total number of ClassSession records belonging to this course.

        No lifecycle status is excluded, including cancelled sessions.
        """
        return self.class_sessions.count()


    @property
    def held_attendance_pending_sessions(self):
        """
        Lessons that have been held but whose attendance has not yet
        been fully submitted.
        """
        return self.class_sessions.filter(
            status=ClassSession.STATUS_HELD_ATTENDANCE_PENDING
        ).count()


    @property
    def complete_attendance_submitted_sessions(self):
        """
        Lessons that have been held and whose attendance workflow has
        been fully submitted.
        """
        return self.class_sessions.filter(
            status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
        ).count()


    @property
    def total_held_sessions(self):
        """
        Total lessons actually delivered, regardless of whether
        attendance is pending or already submitted.
        """
        return self._held_sessions_queryset().count()


    @property
    def remaining_sessions(self):
        """
        Lessons that still require teaching.

        Included:
        - scheduled
        - pending_reschedule
        - rescheduled

        Held and cancelled lessons are excluded.
        """
        return self._remaining_sessions_queryset().count()


    # ---------------------------------------------------------
    # COURSE HOURS
    # ---------------------------------------------------------

    @property
    def total_minutes(self):
        """
        Original total course duration expressed in minutes.

        Based on Course.total_hours, which represents the agreed
        total duration of the course.
        """
        if not self.total_hours:
            return 0

        return round(
            self.total_hours
            * Decimal("60")
        )


    @property
    def held_minutes(self):
        """
        Actual duration in minutes of all lessons already delivered.

        Includes BOTH held lifecycle states:
        - held_attendance_pending
        - complete_attendance_submitted
        """
        return self._calculate_session_minutes(
            self._held_sessions_queryset()
        )


    @property
    def held_hours(self):
        """
        Actual delivered course hours as a Decimal.
        """
        return (
            Decimal(self.held_minutes)
            / Decimal("60")
        )


    # ---------------------------------------------------------
    # COURSE DELIVERY %
    # ---------------------------------------------------------

    @property
    def delivery_percentage(self):
        """
        Percentage of the whole course's ClassSessions that have
        actually been delivered.

        Cancelled sessions remain part of total_sessions because they
        belonged to the originally generated course schedule, but they
        are not counted as delivered.
        """
        total_sessions = self.total_sessions

        if not total_sessions:
            return 0

        return round(
            self.total_held_sessions
            / total_sessions
            * 100
        )


    # ---------------------------------------------------------
    # BACKWARDS-COMPATIBILITY ALIASES
    #
    # Keep temporarily while older views/templates are migrated.
    # New code should use the explicit properties above.
    # ---------------------------------------------------------


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

    def pause_future_sessions(self):
        """
        Move future scheduled/rescheduled lessons to pending_reschedule.

        Lessons that have already started, held lessons, completed lessons
        and cancelled lessons remain untouched.
        """
        now = timezone.now()

        return self.class_sessions.filter(
            start_time__gt=now,
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
            ],
        ).update(
            status=ClassSession.STATUS_PENDING_RESCHEDULE
        )
    
    def cancel_future_sessions(self):
        """
        Cancel ClassSessions that will no longer take place.

        scheduled / rescheduled:
        - cancelled only when the lesson has not yet started

        pending_reschedule:
        - always cancelled because the lesson has not taken place,
        even when its original scheduled time is already past

        Attendance does not have a cancelled learner outcome.

        Operational Attendance placeholders are deleted:
        - pending
        - enrollment_paused

        Genuine Attendance outcomes are preserved:
        - attended
        - missed
        - excused

        Returns the number of ClassSessions cancelled.
        """
        now = timezone.now()

        sessions_to_cancel = self.class_sessions.filter(
            models.Q(
                start_time__gte=now,
                status__in=[
                    ClassSession.STATUS_SCHEDULED,
                    ClassSession.STATUS_RESCHEDULED,
                ],
            )
            | models.Q(
                status=ClassSession.STATUS_PENDING_RESCHEDULE
            )
        )

        session_ids = list(
            sessions_to_cancel.values_list("id", flat=True)
        )

        if not session_ids:
            return 0

        with transaction.atomic():
            Attendance.objects.filter(
                class_session_id__in=session_ids,
                status__in=[
                    Attendance.STATUS_PENDING,
                    Attendance.STATUS_ENROLLMENT_PAUSED,
                ],
            ).delete()

            cancelled_count = sessions_to_cancel.update(
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

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "course",
                    "day_of_week",
                    "start_time",
                ],
                name="unique_course_timetable_start",
            )
        ]


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
        """
        Save the timetable slot and synchronize the Course only when
        this timetable definition genuinely changes.

        Existing held / complete lesson history is never rewritten.

        For an established confirmed/active Course, adding or editing a
        timetable slot delegates future schedule rebuilding to
        Course.synchronize_future_scheduled_sessions().

        Initial Course setup remains safe because synchronization is a
        no-op when no ClassSessions exist; try_generate_class_sessions()
        then performs the one-time initial generation when ready.
        """
        is_new = self.pk is None
        old_slot = None

        with transaction.atomic():
            if self.pk:
                old_slot = (
                    CourseTimetableSlot.objects
                    .select_for_update()
                    .get(pk=self.pk)
                )

            self.full_clean()
            super().save(*args, **kwargs)

            if self.course.class_duration_source != "manual":
                self.course.update_class_duration_from_timetable()

            timetable_changed = (
                is_new
                or old_slot.day_of_week != self.day_of_week
                or old_slot.start_time != self.start_time
                or old_slot.end_time != self.end_time
            )

            if (
                timetable_changed
                and self.course.status in {
                    "confirmed",
                    "active",
                }
                and self.course.class_sessions.exists()
            ):
                self.course.synchronize_future_scheduled_sessions()

            # Automatic initial generation:
            # Course.save() happens before related Admin inline objects are saved.
            # Once the final prerequisite exists, generation occurs exactly once.
            self.course.try_generate_class_sessions()

    def delete(self, *args, **kwargs):
        """
        Delete this timetable slot and safely synchronize the remaining
        future scheduled ClassSessions when the Course is operational.

        Historical / held / rescheduled lesson records are preserved.
        """
        course = self.course

        with transaction.atomic():
            result = super().delete(*args, **kwargs)

            if course.class_duration_source != "manual":
                course.update_class_duration_from_timetable()

            if (
                course.status in {
                    "confirmed",
                    "active",
                }
                and course.class_sessions.exists()
                and course.timetable_slots.exists()
            ):
                course.synchronize_future_scheduled_sessions()

        return result

    def update_future_class_sessions(self, old_slot=None):
        """
        Synchronize only the Course's remaining future scheduled lessons.

        The Course model owns the scheduling rules. old_slot is retained
        for backwards compatibility with existing callers.
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

    If an active enrollment becomes paused:
    - remaining pending Attendance records become enrollment_paused
    - genuine historical Attendance outcomes are preserved
    - lessons that have already started are not changed

    If a paused enrollment becomes active again:
    - remaining enrollment_paused Attendance records return to pending
    - missing Attendance records are created for eligible lessons
    - historical enrollment_paused Attendance records are preserved

    A ClassSession has completed its lesson + attendance workflow
    ONLY when:

        ClassSession.status == "complete_attendance_submitted"
    """

    # ---------------------------------------------------------
    # ENROLLMENT STATUS
    # ---------------------------------------------------------

    STATUS_ACTIVE = "active"
    STATUS_PAUSED = "paused"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    ENROLLMENT_STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_PAUSED, "Paused"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
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
        default=STATUS_ACTIVE
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
        Save the enrollment and synchronize its Attendance records.

        When an enrollment becomes paused:
        - remaining pending Attendance records become enrollment_paused

        When an enrollment becomes active:
        - remaining enrollment_paused Attendance records return to pending
        - missing Attendance records are created for unfinished lessons

        When an enrollment becomes cancelled:
        - remaining pending Attendance records are deleted
        - remaining enrollment_paused Attendance records are deleted
        - genuine attendance outcomes are preserved

        Historical Attendance outcomes are never overwritten or deleted.
        """
        is_new = self.pk is None
        old_status = None

        if self.pk:
            old_enrollment = CourseEnrollment.objects.get(
                pk=self.pk
            )
            old_status = old_enrollment.status

        super().save(*args, **kwargs)

        became_paused = (
            self.status == self.STATUS_PAUSED
            and old_status != self.STATUS_PAUSED
        )

        became_active = (
            self.status == self.STATUS_ACTIVE
            and (
                is_new
                or old_status != self.STATUS_ACTIVE
            )
        )

        became_cancelled = (
            self.status == self.STATUS_CANCELLED
            and old_status != self.STATUS_CANCELLED
        )

        if became_paused:
            self.pause_remaining_attendance_records()

        if became_active:
            # Restore Attendance rows that were paused because the
            # enrollment itself was paused.
            self.restore_remaining_attendance_records()

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

        if became_cancelled:
            self.cancel_remaining_attendance_records()


    # ---------------------------------------------------------
    # PAUSE REMAINING ATTENDANCE
    # ---------------------------------------------------------

    def pause_remaining_attendance_records(self):
        """
        Change this learner's remaining pending Attendance records
        to enrollment_paused.

        scheduled/rescheduled:
        - only lessons that have not yet started are changed

        pending_reschedule:
        - always changed because the lesson has not taken place,
          even when its original scheduled time is already past

        Never changed:
        - lessons that have already started
        - held lessons
        - complete lessons
        - cancelled lessons
        - attended
        - missed
        - excused

        Returns the number of Attendance records updated.
        """
        now = timezone.now()

        pending_attendance = Attendance.objects.filter(
            student=self.student,
            class_session__course=self.course,
            status=Attendance.STATUS_PENDING,
        )

        future_count = pending_attendance.filter(
            class_session__status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
            ],
            class_session__start_time__gt=now,
        ).update(
            status=Attendance.STATUS_ENROLLMENT_PAUSED
        )

        pending_reschedule_count = pending_attendance.filter(
            class_session__status=ClassSession.STATUS_PENDING_RESCHEDULE,
        ).update(
            status=Attendance.STATUS_ENROLLMENT_PAUSED
        )

        return future_count + pending_reschedule_count


    # ---------------------------------------------------------
    # RESTORE REMAINING ATTENDANCE
    # ---------------------------------------------------------

    def restore_remaining_attendance_records(self):
        """
        Restore this learner's remaining enrollment_paused Attendance
        records to pending when the enrollment becomes active again.

        scheduled/rescheduled:
        - only lessons that have not yet started are restored

        pending_reschedule:
        - always restored because the lesson still has to take place

        Historical enrollment_paused records remain unchanged.

        Returns the number of Attendance records updated.
        """
        now = timezone.now()

        paused_attendance = Attendance.objects.filter(
            student=self.student,
            class_session__course=self.course,
            status=Attendance.STATUS_ENROLLMENT_PAUSED,
        )

        future_count = paused_attendance.filter(
            class_session__status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
            ],
            class_session__start_time__gt=now,
        ).update(
            status=Attendance.STATUS_PENDING
        )

        pending_reschedule_count = paused_attendance.filter(
            class_session__status=ClassSession.STATUS_PENDING_RESCHEDULE,
        ).update(
            status=Attendance.STATUS_PENDING
        )

        return future_count + pending_reschedule_count


    # ---------------------------------------------------------
    # CANCEL REMAINING ATTENDANCE
    # ---------------------------------------------------------

    def cancel_remaining_attendance_records(self):
        """
        Delete this learner's remaining operational Attendance records
        when the enrollment becomes cancelled.

        scheduled/rescheduled:
        - only lessons that have not yet started are affected

        pending_reschedule:
        - always affected because the lesson has not taken place,
          even when its original scheduled time is already past

        Deleted:
        - pending
        - enrollment_paused

        Preserved:
        - attended
        - missed
        - excused

        Returns the number of Attendance records deleted.
        """
        now = timezone.now()

        attendance_records = Attendance.objects.filter(
            student=self.student,
            class_session__course=self.course,
            status__in=[
                Attendance.STATUS_PENDING,
                Attendance.STATUS_ENROLLMENT_PAUSED,
            ],
        )

        future_deleted, _ = attendance_records.filter(
            class_session__status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_RESCHEDULED,
            ],
            class_session__start_time__gt=now,
        ).delete()

        pending_reschedule_deleted, _ = attendance_records.filter(
            class_session__status=ClassSession.STATUS_PENDING_RESCHEDULE,
        ).delete()

        return future_deleted + pending_reschedule_deleted


    # ---------------------------------------------------------
    # CREATE MISSING ATTENDANCE
    # ---------------------------------------------------------

    def create_future_attendance_records(self):
        """
        Create missing Attendance records for this learner only for
        ClassSessions that still represent future teaching.

        Included:

        scheduled / rescheduled:
        - only when start_time is still in the future

        pending_reschedule:
        - always included because the lesson has not taken place,
          even when its original scheduled time is already past

        Excluded:
        - scheduled/rescheduled lessons that have already started
        - held_attendance_pending
        - complete_attendance_submitted
        - cancelled

        This prevents a learner who joins or becomes active later
        from being assigned retroactively to a lesson that has
        already started or finished.
        """
        now = timezone.now()

        eligible_sessions = (
            self.course.class_sessions
            .filter(
                models.Q(
                    status__in=[
                        ClassSession.STATUS_SCHEDULED,
                        ClassSession.STATUS_RESCHEDULED,
                    ],
                    start_time__gt=now,
                )
                | models.Q(
                    status=ClassSession.STATUS_PENDING_RESCHEDULE
                )
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
    # LEARNER-SPECIFIC DELIVERY / ATTENDANCE
    #
    # CourseEnrollment is the source of truth for:
    #
    # - sessions assigned to this learner
    # - held / remaining assigned lessons
    # - submitted attendance outcomes
    # - learner delivery percentage
    # - assigned / held / remaining minutes and hours
    # - submitted / attended minutes and hours
    #
    # Attendance records remain the source of truth for which
    # ClassSessions belong to this learner's enrollment.
    #
    # Formatting remains outside the model.
    # ---------------------------------------------------------

    @staticmethod
    def _calculate_session_minutes(sessions):
        """
        Return the combined actual duration of a ClassSession queryset
        in whole minutes.

        Actual start/end times are used so shorter final lessons and
        rescheduled lessons are handled correctly.
        """
        total_seconds = sum(
            (end_time - start_time).total_seconds()
            for start_time, end_time
            in sessions.values_list("start_time", "end_time")
            if start_time and end_time
        )

        return round(total_seconds / 60)


    # ---------------------------------------------------------
    # ASSIGNED SESSIONS
    # ---------------------------------------------------------

    @property
    def assigned_sessions(self):
        """
        Return the ClassSessions actually assigned to this learner.

        Attendance records are the source of truth.

        This is safer than filtering by start_time because a session
        can be rescheduled without becoming a new ClassSession.

        Once an Attendance record exists for a learner/session, that
        session belongs to this enrollment for as long as the Attendance
        record is preserved.
        """
        assigned_session_ids = (
            Attendance.objects
            .filter(
                student=self.student,
                class_session__course=self.course,
            )
            .values_list(
                "class_session_id",
                flat=True,
            )
        )

        return (
            self.course.class_sessions
            .filter(id__in=assigned_session_ids)
            .order_by("start_time")
        )


    # ---------------------------------------------------------
    # ASSIGNED CLASS COUNTS
    # ---------------------------------------------------------

    @property
    def total_assigned_classes(self):
        """
        Total number of ClassSessions currently assigned to this learner.
        """
        return self.assigned_sessions.count()


    @property
    def held_attendance_pending_classes(self):
        """
        Assigned lessons that have been held but whose attendance has
        not yet been fully submitted.
        """
        return self.assigned_sessions.filter(
            status=ClassSession.STATUS_HELD_ATTENDANCE_PENDING
        ).count()


    @property
    def complete_attendance_submitted_classes(self):
        """
        Assigned lessons that have been held and whose attendance
        workflow has been fully submitted.
        """
        return self.assigned_sessions.filter(
            status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
        ).count()


    @property
    def total_held_classes(self):
        """
        Total assigned lessons actually delivered, regardless of
        whether attendance is pending or already submitted.
        """
        return self.assigned_sessions.filter(
            status__in=[
                ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            ]
        ).count()


    @property
    def remaining_classes(self):
        """
        Number of assigned lessons that still require teaching.

        Included:
        - scheduled
        - pending_reschedule
        - rescheduled

        Held and cancelled lessons are excluded.
        """
        return self.assigned_sessions.filter(
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_PENDING_RESCHEDULE,
                ClassSession.STATUS_RESCHEDULED,
            ]
        ).count()


    # ---------------------------------------------------------
    # LEARNER DELIVERY %
    # ---------------------------------------------------------

    @property
    def delivery_percentage(self):
        """
        Percentage of this learner's assigned ClassSessions that have
        actually been delivered.

        Held includes both:
        - held_attendance_pending
        - complete_attendance_submitted
        """
        total_classes = self.total_assigned_classes

        if not total_classes:
            return 0

        return round(
            self.total_held_classes
            / total_classes
            * 100
        )


    # ---------------------------------------------------------
    # ASSIGNED / HELD / REMAINING HOURS
    # ---------------------------------------------------------

    @property
    def total_assigned_minutes(self):
        """
        Actual combined duration of every ClassSession currently
        assigned to this learner.
        """
        return self._calculate_session_minutes(
            self.assigned_sessions
        )


    @property
    def total_assigned_hours(self):
        """
        Total assigned learner hours as a Decimal.
        """
        return (
            Decimal(self.total_assigned_minutes)
            / Decimal("60")
        )


    @property
    def held_minutes(self):
        """
        Actual duration of this learner's assigned lessons that have
        already been delivered.

        Includes both held lifecycle states.
        """
        held_sessions = self.assigned_sessions.filter(
            status__in=[
                ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            ]
        )

        return self._calculate_session_minutes(
            held_sessions
        )


    @property
    def held_hours(self):
        """
        Delivered learner hours as a Decimal.
        """
        return (
            Decimal(self.held_minutes)
            / Decimal("60")
        )


    @property
    def remaining_minutes(self):
        """
        Actual duration of this learner's assigned lessons that still
        require teaching.

        Cancelled lessons are not considered remaining.
        """
        remaining_sessions = self.assigned_sessions.filter(
            status__in=[
                ClassSession.STATUS_SCHEDULED,
                ClassSession.STATUS_PENDING_RESCHEDULE,
                ClassSession.STATUS_RESCHEDULED,
            ]
        )

        return self._calculate_session_minutes(
            remaining_sessions
        )


    @property
    def remaining_hours(self):
        """
        Remaining learner teaching hours as a Decimal.
        """
        return (
            Decimal(self.remaining_minutes)
            / Decimal("60")
        )


    # ---------------------------------------------------------
    # SUBMITTED ATTENDANCE
    # ---------------------------------------------------------

    @property
    def submitted_attendances(self):
        """
        Finalized Attendance records for this learner/course.

        A record belongs to the submitted-attendance population only
        when:
        - its ClassSession has completed the attendance workflow
        - the learner has a genuine final attendance outcome

        Operational pending / enrollment_paused records are excluded.
        """
        return (
            Attendance.objects
            .filter(
                student=self.student,
                class_session__course=self.course,
                class_session__status=(
                    ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
                ),
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


    @property
    def attendance_metrics(self):
        """
        Return all submitted-attendance metrics using explicit names.

        Included attendance outcomes:
        - attended
        - missed
        - excused

        Pending and enrollment_paused records are excluded.

        New helpers/views should retrieve this dictionary once rather
        than independently querying the same attendance population.
        """
        submitted_attendance_counts = self.submitted_attendances.aggregate(
            total_submitted_attendance_records=models.Count("id"),
            attended_classes=models.Count(
                "id",
                filter=models.Q(status=Attendance.STATUS_ATTENDED),
            ),
            missed_classes=models.Count(
                "id",
                filter=models.Q(status=Attendance.STATUS_MISSED),
            ),
            excused_classes=models.Count(
                "id",
                filter=models.Q(status=Attendance.STATUS_EXCUSED),
            ),
        )

        total_submitted_attendance_records = (
            submitted_attendance_counts["total_submitted_attendance_records"] or 0
        )
        attended_classes = submitted_attendance_counts["attended_classes"] or 0
        missed_classes = submitted_attendance_counts["missed_classes"] or 0
        excused_classes = submitted_attendance_counts["excused_classes"] or 0
        total_absences = missed_classes + excused_classes

        attendance_percentage = (
            round(
                attended_classes
                / total_submitted_attendance_records
                * 100
            )
            if total_submitted_attendance_records else 0
        )

        return {
            "total_submitted_attendance_records": total_submitted_attendance_records,
            "attended_classes": attended_classes,
            "missed_classes": missed_classes,
            "excused_classes": excused_classes,
            "total_absences": total_absences,
            "attendance_percentage": attendance_percentage,
            "has_low_attendance_warning": (
                total_submitted_attendance_records > 0
                and attendance_percentage < 75
            ),
        }


    # ---------------------------------------------------------
    # SUBMITTED / ATTENDED HOURS
    # ---------------------------------------------------------

    def _submitted_sessions_queryset(self):
        """
        Return this learner's assigned ClassSessions whose attendance
        has been finalized.
        """
        submitted_session_ids = (
            self.submitted_attendances
            .values_list(
                "class_session_id",
                flat=True,
            )
        )

        return (
            self.course.class_sessions
            .filter(id__in=submitted_session_ids)
            .order_by("start_time")
        )


    def _attended_sessions_queryset(self):
        """
        Return submitted ClassSessions this learner actually attended.
        """
        attended_session_ids = (
            self.submitted_attendances
            .filter(
                status=Attendance.STATUS_ATTENDED
            )
            .values_list(
                "class_session_id",
                flat=True,
            )
        )

        return (
            self.course.class_sessions
            .filter(id__in=attended_session_ids)
            .order_by("start_time")
        )


    @property
    def submitted_minutes(self):
        """
        Duration of all assigned sessions whose attendance has been
        fully submitted for this learner.
        """
        return self._calculate_session_minutes(
            self._submitted_sessions_queryset()
        )


    @property
    def submitted_hours(self):
        """
        Submitted-attendance learner hours as a Decimal.
        """
        return (
            Decimal(self.submitted_minutes)
            / Decimal("60")
        )


    @property
    def attended_minutes(self):
        """
        Duration of submitted sessions this learner actually attended.
        """
        return self._calculate_session_minutes(
            self._attended_sessions_queryset()
        )


    @property
    def attended_hours(self):
        """
        Actually attended learner hours as a Decimal.
        """
        return (
            Decimal(self.attended_minutes)
            / Decimal("60")
        )


    # ---------------------------------------------------------
    # EXPLICIT ATTENDANCE COUNT PROPERTIES
    #
    # These remain convenient for templates/admin code.
    # New packaging helpers should prefer attendance_metrics so all
    # attendance counts come from one aggregate query.
    # ---------------------------------------------------------

    @property
    def total_submitted_attendance_records(self):
        return self.attendance_metrics["total_submitted_attendance_records"]


    @property
    def attended_classes(self):
        return self.attendance_metrics["attended_classes"]


    @property
    def missed_classes(self):
        return self.attendance_metrics["missed_classes"]


    @property
    def excused_classes(self):
        return self.attendance_metrics["excused_classes"]


    @property
    def total_absences(self):
        return self.attendance_metrics["total_absences"]


    @property
    def attendance_percentage(self):
        return self.attendance_metrics["attendance_percentage"]


    @property
    def has_low_attendance_warning(self):
        return self.attendance_metrics["has_low_attendance_warning"]


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

        pending and enrollment_paused are operational states and do
        not, by themselves, prevent deletion.
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


    def delete(self, *args, force=False, **kwargs):
        """
        Permanently delete an erroneous enrollment.

        Normal deletion is blocked when genuine Attendance history exists.

        A deliberate administrative correction may use force=True to remove:
        - the CourseEnrollment
        - every Attendance record belonging to this learner/course

        The underlying ClassSessions remain because they belong to the Course,
        not to this individual enrollment.

        Legitimate enrollment lifecycle changes should use:
        active / paused / completed / cancelled
        rather than permanent deletion.
        """
        if not force and not self.can_be_deleted:
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
    def validate_timing(self):
        """
        Enforce ClassSession timing invariants.

        A lesson must always finish after it starts.
        """
        if (
            self.start_time
            and self.end_time
            and self.end_time <= self.start_time
        ):
            raise ValidationError({
                "end_time": "End time must be after start time."
            })

    def validate_lifecycle(self):
        """
        Enforce ClassSession lifecycle invariants.

        Rules:
        - held / complete states cannot exist before the lesson ends
        - complete_attendance_submitted requires all attendance
          requirements to be resolved and at least one genuine
          attendance outcome

        These rules are deliberately separate from Django's clean()
        lifecycle so they can also be enforced by programmatic save().
        """
        if (
            self.end_time
            and self.end_time > timezone.now()
            and self.status in {
                self.STATUS_HELD_ATTENDANCE_PENDING,
                self.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            }
        ):
            raise ValidationError({
                "status": (
                    "A lesson cannot be held or complete before its end time."
                )
            })

        if (
            self.status == self.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            and not self.pk
        ):
            raise ValidationError({
                "status": (
                    "A new ClassSession cannot be created directly as complete. "
                    "Attendance records must exist and be resolved first."
                )
            })

        if (
            self.pk
            and self.status == self.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            and (
                not self.attendance_requirements_resolved
                or not self.has_genuine_attendance_outcomes
            )
        ):
            raise ValidationError({
                "status": (
                    "A lesson can be complete only when all required attendance "
                    "has been resolved and at least one genuine attendance "
                    "outcome exists."
                )
            })

    def clean(self):
        """
        Validate ClassSession timing and lifecycle consistency.

        Django forms/Admin call model validation through clean().
        Programmatic saves are protected separately in save() by calling
        the same explicit business-rule validators.
        """
        super().clean()
        self.validate_timing()
        self.validate_lifecycle()

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------
    def save(self, *args, **kwargs):
        """
        Save the ClassSession and perform related updates.

        Before persistence:
        - enforce timing invariants
        - enforce lifecycle invariants

        After persistence:
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

        self.validate_timing()
        self.validate_lifecycle()

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

        Attendance records
        may be submitted before the lesson ends.
        """
        return self.status == self.STATUS_COMPLETE_ATTENDANCE_SUBMITTED

    # ---------------------------------------------------------
    # ATTENDANCE RECORD STATE
    # ---------------------------------------------------------
    @property
    def has_attendance_records(self):
        """
        Return True when at least one learner is assigned to this
        ClassSession through an Attendance record.
        """
        return self.attendance_records.exists()

    @property
    def has_genuine_attendance_outcomes(self):
        """
        Return True when at least one learner has a genuine finalized
        attendance outcome for this lesson.

        Genuine outcomes:
        - attended
        - missed
        - excused

        enrollment_paused is deliberately excluded because it means
        no attendance outcome was required for that learner.
        """
        return self.attendance_records.filter(
            status__in=Attendance.FINAL_OUTCOME_STATUSES
        ).exists()

    @property
    def attendance_requirements_resolved(self):
        """
        Return True when this ClassSession has Attendance records and
        none still requires teacher attendance action.

        Resolved states:
        - attended
        - missed
        - excused
        - enrollment_paused

        enrollment_paused is resolved operationally, but it is NOT a
        submitted attendance outcome.

        This may legitimately be True before end_time. The ClassSession
        itself must still remain scheduled/rescheduled until the lesson
        has actually ended.
        """
        if not self.has_attendance_records:
            return False

        return not self.attendance_records.exclude(
            status__in=Attendance.RESOLVED_STATUSES
        ).exists()


    @property
    def all_attendance_enrollment_paused(self):
        """
        Return True when this ClassSession has Attendance records and
        every assigned learner is enrollment_paused.

        No learner is currently expected to attend this lesson, so time
        passing alone must not cause the lesson to be classified as held.
        """
        if not self.has_attendance_records:
            return False

        return not self.attendance_records.exclude(
            status=Attendance.STATUS_ENROLLMENT_PAUSED
        ).exists()

    # ---------------------------------------------------------
    # SYNCHRONIZE ONE FINISHED SESSION
    # ---------------------------------------------------------
    def synchronize_status_after_end(self):
        """
        Synchronize this ClassSession after its end_time passes.

        scheduled/rescheduled + no Attendance records
            -> no automatic transition

        scheduled/rescheduled + all learners enrollment_paused
            -> pending_reschedule

        scheduled/rescheduled + unresolved attendance
            -> held_attendance_pending

        scheduled/rescheduled + all requirements resolved + at least
        one genuine attendance outcome
            -> complete_attendance_submitted

        held_attendance_pending + all requirements resolved + at least
        one genuine attendance outcome
            -> complete_attendance_submitted

        pending_reschedule, cancelled and already-complete sessions
        are deliberately untouched.

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

            if not session.is_past:
                self.status = session.status
                return False

            if session.status not in {
                self.STATUS_SCHEDULED,
                self.STATUS_RESCHEDULED,
                self.STATUS_HELD_ATTENDANCE_PENDING,
            }:
                self.status = session.status
                return False

            attendance_statuses = list(
                session.attendance_records.values_list(
                    "status",
                    flat=True,
                )
            )

            has_attendance_records = bool(attendance_statuses)

            all_attendance_enrollment_paused = (
                has_attendance_records
                and all(
                    status == Attendance.STATUS_ENROLLMENT_PAUSED
                    for status in attendance_statuses
                )
            )

            attendance_requirements_resolved = (
                has_attendance_records
                and all(
                    status in Attendance.RESOLVED_STATUSES
                    for status in attendance_statuses
                )
            )

            has_genuine_attendance_outcomes = any(
                status in Attendance.FINAL_OUTCOME_STATUSES
                for status in attendance_statuses
            )

            if not has_attendance_records:
                self.status = session.status
                return False

            if (
                session.status in {
                    self.STATUS_SCHEDULED,
                    self.STATUS_RESCHEDULED,
                }
                and all_attendance_enrollment_paused
            ):
                new_status = self.STATUS_PENDING_RESCHEDULE

            elif (
                attendance_requirements_resolved
                and has_genuine_attendance_outcomes
            ):
                new_status = self.STATUS_COMPLETE_ATTENDANCE_SUBMITTED

            elif session.status in {
                self.STATUS_SCHEDULED,
                self.STATUS_RESCHEDULED,
            }:
                new_status = self.STATUS_HELD_ATTENDANCE_PENDING

            else:
                self.status = session.status
                return False

            if new_status == session.status:
                self.status = session.status
                return False

            session.status = new_status
            session.save(update_fields=["status"])

            self.status = session.status

        return True

    # ---------------------------------------------------------
    # SYNCHRONIZE ALL FINISHED SESSIONS
    # ---------------------------------------------------------
    @classmethod
    def transition_past_sessions(cls, course=None):
        """
        Synchronize all finished ClassSessions whose lifecycle may
        still require an automatic transition.

        Included:
        - scheduled
        - rescheduled
        - held_attendance_pending

        held_attendance_pending is included so a session can still move
        to complete_attendance_submitted if attendance was finalized by
        a bulk/database operation that did not call Attendance.save().

        If course is provided, only sessions belonging to that Course
        are synchronized.

        Returns the number of ClassSessions whose status changed.
        """
        sessions = cls.objects.filter(
            end_time__lte=timezone.now(),
            status__in=[
                cls.STATUS_SCHEDULED,
                cls.STATUS_RESCHEDULED,
                cls.STATUS_HELD_ATTENDANCE_PENDING,
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
            held_attendance_pending
                ↓
            complete_attendance_submitted

        RESCHEDULING FLOW:

            scheduled
                ↓
            pending_reschedule
                ↓
            rescheduled
                ↓
            held_attendance_pending
                ↓
            complete_attendance_submitted

    Attendance controls only the individual LEARNER'S state
    for that lesson:

        pending
        attended
        missed
        excused
        enrollment_paused

    "pending" means the learner's attendance outcome has not yet
    been submitted.

    "enrollment_paused" means no attendance outcome is required
    because the learner's CourseEnrollment is paused for that
    ClassSession.

    Rescheduling does NOT create a new Attendance record.

    The existing Attendance record remains attached to the same
    ClassSession and normally remains status="pending" until
    the lesson actually takes place.

    If a future ClassSession is cancelled, untouched pending
    Attendance placeholders are deleted because no learner attendance
    outcome can exist for a lesson that never takes place.

    If a learner's CourseEnrollment is paused, applicable future
    pending Attendance records become status="enrollment_paused".

    If the CourseEnrollment later becomes active again, applicable
    future enrollment_paused Attendance records return to "pending".

    Historical Attendance outcomes are never overwritten by an
    enrollment status change.
    """

    # ---------------------------------------------------------
    # ATTENDANCE STATUS
    # ---------------------------------------------------------

    STATUS_PENDING = "pending"
    STATUS_ATTENDED = "attended"
    STATUS_MISSED = "missed"
    STATUS_EXCUSED = "excused"
    STATUS_ENROLLMENT_PAUSED = "enrollment_paused"

    FINAL_OUTCOME_STATUSES = (
        STATUS_ATTENDED,
        STATUS_MISSED,
        STATUS_EXCUSED,
    )

    RESOLVED_STATUSES = (
        *FINAL_OUTCOME_STATUSES,
        STATUS_ENROLLMENT_PAUSED,
    )

    ATTENDANCE_STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ATTENDED, "Attended"),
        (STATUS_MISSED, "Missed"),
        (STATUS_EXCUSED, "Excused"),
        (STATUS_ENROLLMENT_PAUSED, "Enrollment paused"),
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
    # VALIDATION
    # ---------------------------------------------------------

    def clean(self):
        """
        Validate learner attendance against the lesson/enrollment state.

        Rules:
        - a learner must have a CourseEnrollment for this Course
        - attended / missed / excused cannot be submitted for a
        pending_reschedule or cancelled lesson
        - attended / missed / excused cannot be submitted before
        ClassSession.start_time
        - a completed ClassSession cannot be made unresolved
        """
        super().clean()

        # ---------------------------------------------------------
        # LEARNER MUST BELONG TO THE COURSE
        # ---------------------------------------------------------
        if self.class_session_id and self.student_id:
            if not CourseEnrollment.objects.filter(
                course=self.class_session.course,
                student=self.student,
            ).exists():
                raise ValidationError({
                    "student": (
                        "This learner is not enrolled in the selected course."
                    )
                })


        # ---------------------------------------------------------
        # NO ATTENDANCE OUTCOME FOR LESSONS NOT DELIVERED
        # ---------------------------------------------------------
        if (
            self.class_session_id
            and self.status in self.FINAL_OUTCOME_STATUSES
            and self.class_session.status in {
                ClassSession.STATUS_PENDING_RESCHEDULE,
                ClassSession.STATUS_CANCELLED,
            }
        ):
            raise ValidationError({
                "status": (
                    "Attendance outcomes cannot be submitted for a lesson "
                    "that is pending reschedule or cancelled."
                )
            })


        # ---------------------------------------------------------
        # NO ATTENDANCE SUBMISSION BEFORE LESSON START
        # ---------------------------------------------------------
        if (
            self.class_session_id
            and self.status in self.FINAL_OUTCOME_STATUSES
            and timezone.now() < self.class_session.start_time
        ):
            raise ValidationError({
                "status": (
                    "Attendance cannot be submitted before the lesson starts."
                )
            })


        # ---------------------------------------------------------
        # COMPLETED SESSION MUST KEEP FINAL OUTCOMES
        # ---------------------------------------------------------
        if (
            self.class_session_id
            and self.class_session.status
            == ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
            and self.status not in self.FINAL_OUTCOME_STATUSES
        ):
            raise ValidationError({
                "status": (
                    "Attendance for a completed lesson must remain a "
                    "final attendance outcome."
                )
            })

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    def save(self, *args, **kwargs):
        """
        Save the learner's Attendance state and then allow the
        parent ClassSession to synchronize its lifecycle status.

        If the lesson has already ended and all attendance requirements
        are resolved, with at least one genuine attendance outcome, the
        ClassSession can become complete_attendance_submitted automatically.
        """
        if self.status != self.STATUS_ATTENDED and self.minutes_late != 0:
            self.minutes_late = 0

            update_fields = kwargs.get("update_fields")
            if update_fields is not None:
                kwargs["update_fields"] = set(update_fields) | {"minutes_late"}

        self.clean()
        super().save(*args, **kwargs)

        self.class_session.synchronize_status_after_end()


    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------

    @property
    def was_punctual(self):
        """
        Return True only when the learner attended
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
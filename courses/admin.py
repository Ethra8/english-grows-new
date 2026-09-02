from django.contrib import admin
from django.utils import timezone

from .models import (
    CourseType,
    Course,
    CourseTimetableSlot,
    CourseEnrollment,
    ClassSession,
    Attendance,
    BankHoliday,
)

from courses.utils.course_dates import calculate_course_end_date


@admin.register(CourseType)
class CourseTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "default_hours",
        "is_for_individual",
        "is_for_companies",
    )

    list_filter = (
        "is_for_individual",
        "is_for_companies",
    )

    search_fields = (
        "name",
        "description",
    )


# -------------------------------------------------------------------------
# COURSE ENROLLMENT INLINE
# -------------------------------------------------------------------------
#
# Enrollments can be added from the Course admin.
#
# When a new enrollment becomes active:
# - NO new ClassSessions are generated if the course already has sessions.
# - CourseEnrollment.save() automatically creates Attendance records for
#   this learner for every unfinished ClassSession.
#
# We avoid deleting enrollments from the Course page because the enrollment
# lifecycle already provides paused/completed/cancelled statuses.
# -------------------------------------------------------------------------
class CourseEnrollmentInline(admin.TabularInline):
    model = CourseEnrollment
    extra = 0
    can_delete = True

    autocomplete_fields = (
        "student",
    )

    fields = (
        "student",
        "status",
        "target_level",
        "learning_objective",
        "enrolled_at",
    )

    readonly_fields = (
        "enrolled_at",
    )


# -------------------------------------------------------------------------
# COURSE TIMETABLE INLINE
# -------------------------------------------------------------------------
class CourseTimetableSlotInline(admin.TabularInline):
    model = CourseTimetableSlot
    extra = 1

    fields = (
        "day_of_week",
        "start_time",
        "end_time",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    @admin.display(description="Class Duration")
    def class_duration_display(self, obj):
        return obj.class_duration_display

    @admin.display(description="Final Class Duration")
    def final_class_duration_display(self, obj):
        return obj.final_class_duration_display

    list_display = (
        "name",
        "course_type",
        "course_level",
        "status",
        "total_hours",
        "class_duration_display",
        "number_of_classes",
        "company",
        "teacher",
        "start_date",
        "end_date",
    )

    fields = (
        "name",
        "course_type",
        "course_level",
        "status",
        "total_hours",
        "class_duration",
        "class_duration_display",
        "class_duration_source",
        "number_of_classes",
        "final_class_duration_display",
        "company",
        "teacher",
        "start_date",
        "end_date",
    )

    readonly_fields = (
        "class_duration_display",
        "final_class_duration_display",
        "number_of_classes",
        "end_date",
    )

    list_filter = (
        "status",
        "course_type",
        "company",
        "start_date",
        "course_level",
        "teacher",
    )

    search_fields = (
        "name",
        "course_type__name",
        "company__name",
        "teacher__username",
        "teacher__first_name",
        "teacher__last_name",
        "teacher__email",
    )

    autocomplete_fields = (
        "course_type",
        "company",
        "teacher",
    )

    # Manual "Generate class sessions" action removed.
    #
    # ClassSessions + initial Attendance records are now generated
    # automatically by the model lifecycle once all prerequisites exist.

    def save_related(self, request, form, formsets, change):
        """
        Run after Django Admin has saved all Course-related inline objects.

        Processing order:

        1. Save Course-related inline objects.
        2. Synchronize automatically calculated class duration.
        3. If ClassSessions already exist:
           - recalculate only future scheduled sessions
           - skip active bank holidays
           - preserve completed / pending-reschedule / rescheduled sessions
           - preserve ClassSession IDs and Attendance records
           - synchronize end_date from the actual final ClassSession
        4. If no ClassSessions exist yet:
           - calculate the expected end_date from the timetable
           - skip active bank holidays
        5. Perform the final safe initial ClassSession generation attempt.
        6. If generation occurred, synchronize end_date from the actual
           final ClassSession.

        Existing ClassSessions are never deleted or regenerated here.
        """

        super().save_related(
            request,
            form,
            formsets,
            change,
        )

        course = form.instance

        # -------------------------------------------------------------
        # 1. SYNCHRONIZE AUTOMATIC CLASS DURATION
        # -------------------------------------------------------------
        #
        # Django Admin saves timetable inline rows before save_related()
        # finishes, so the timetable is now available for calculating
        # automatic class duration.
        # -------------------------------------------------------------
        if (
            course.timetable_slots.exists()
            and course.class_duration_source == "auto"
        ):
            course.update_class_duration_from_timetable()

            # Refresh values written by
            # update_class_duration_from_timetable().
            course.refresh_from_db()

        # -------------------------------------------------------------
        # 2. SYNCHRONIZE EXISTING COURSE SCHEDULE
        # -------------------------------------------------------------
        #
        # If ClassSessions already exist, they must NOT be regenerated.
        #
        # Instead, synchronize_future_scheduled_sessions() updates only:
        #
        #     future + status="scheduled"
        #
        # It deliberately leaves untouched:
        #
        #     completed
        #     pending_reschedule
        #     rescheduled
        #     past sessions
        #
        # This allows newly added/changed BankHoliday records and timetable
        # changes to be reflected safely without breaking:
        #
        # - ClassSession IDs
        # - class_number
        # - Attendance records
        # - completed history
        # - manual rescheduling
        # -------------------------------------------------------------
        if course.class_sessions.exists():

            course.synchronize_future_scheduled_sessions()

            # Existing ClassSessions are the operational source of truth
            # for the Course end date.
            course.sync_end_date_from_sessions()

        else:

            # ---------------------------------------------------------
            # 3. CALCULATE EXPECTED END DATE BEFORE INITIAL GENERATION
            # ---------------------------------------------------------
            #
            # No ClassSessions exist yet, so calculate the expected
            # end_date directly from:
            #
            # - start_date
            # - timetable slots
            # - number_of_classes
            # - active BankHoliday records
            #
            # calculate_course_end_date() uses the same centralized
            # scheduling rules as ClassSession generation.
            # ---------------------------------------------------------
            if (
                course.start_date
                and course.number_of_classes
                and course.timetable_slots.exists()
            ):
                calculated_end_date = calculate_course_end_date(
                    course
                )

                if calculated_end_date != course.end_date:
                    Course.objects.filter(
                        pk=course.pk
                    ).update(
                        end_date=calculated_end_date
                    )

                    course.end_date = calculated_end_date

        # -------------------------------------------------------------
        # 4. FINAL SAFE INITIAL CLASS SESSION GENERATION ATTEMPT
        # -------------------------------------------------------------
        #
        # try_generate_class_sessions() generates only when:
        #
        # - no ClassSessions exist yet
        # - start_date exists
        # - number_of_classes is available
        # - timetable slots exist
        # - at least one active enrollment exists
        #
        # The model guard prevents regeneration of an existing schedule.
        # -------------------------------------------------------------
        course.try_generate_class_sessions()

        # -------------------------------------------------------------
        # 5. FINAL END-DATE SYNCHRONIZATION
        # -------------------------------------------------------------
        #
        # If ClassSessions were generated above, their real final date
        # becomes authoritative immediately.
        #
        # This also keeps end_date correct if the final lesson has been
        # shortened or if active BankHoliday records extended the course.
        # -------------------------------------------------------------
        if course.class_sessions.exists():
            course.sync_end_date_from_sessions()

    inlines = (
        CourseTimetableSlotInline,
        CourseEnrollmentInline,
    )


class CourseEnrollmentCourseFilter(admin.SimpleListFilter):
    """
    Filter CourseEnrollments by course name.

    Displays Course.name instead of:
        Course object (4)
    """

    title = "course"
    parameter_name = "course"

    def lookups(self, request, model_admin):
        courses = (
            Course.objects
            .filter(enrollments__isnull=False)
            .distinct()
            .order_by("name")
        )

        return [
            (course.pk, course.name)
            for course in courses
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                course_id=self.value()
            )

        return queryset


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course_name",
        "status",
        "target_level",
        "enrolled_at",
        "total_assigned_classes",
        "classes_attended",
        "classes_missed",
        "attendance_percentage",
    )

    list_filter = (
        "status",
        CourseEnrollmentCourseFilter,
        "course__course_type",
        "enrolled_at",
    )

    search_fields = (
        "student__username",
        "student__first_name",
        "student__last_name",
        "student__email",
        "course__name",
    )

    autocomplete_fields = (
        "course",
        "student",
    )

    readonly_fields = (
        "enrolled_at",
        "total_assigned_classes",
        "classes_attended",
        "classes_missed",
        "classes_excused",
        "total_absences",
        "attendance_percentage",
        "has_low_attendance_warning",
    )

    @admin.display(
        description="Course",
        ordering="course__name",
    )
    def course_name(self, obj):
        return obj.course.name

    def has_delete_permission(self, request, obj=None):
        """
        Preserve enrollment history.

        Use the enrollment status
        (paused/completed/cancelled)
        instead of deleting the enrollment record.

        Only superuser can alter.
        """
        if request.user.is_superuser:
            return True

        return False


# -------------------------------------------------------------------------
# ATTENDANCE INLINE
# -------------------------------------------------------------------------
#
# Attendance rows are generated automatically:
# - initially when the Course schedule is generated
# - later when a new learner becomes actively enrolled
#
# Admin users edit the learner outcome, but do not manually add/delete rows.
# -------------------------------------------------------------------------
class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    can_delete = False

    autocomplete_fields = (
        "student",
    )

    fields = (
        "student",
        "status",
        "minutes_late",
        "notes",
        "recorded_at",
    )

    readonly_fields = (
        "student",
        "recorded_at",
    )

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        return False


class ClassSessionCourseFilter(admin.SimpleListFilter):
    """
    Filter ClassSessions by course name.

    Displays Course.name in the sidebar instead of:
        Course object (1)
    """

    title = "course"
    parameter_name = "course"

    def lookups(self, request, model_admin):
        courses = (
            Course.objects
            .filter(class_sessions__isnull=False)
            .distinct()
            .order_by("name")
        )

        return [
            (course.pk, course.name)
            for course in courses
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                course_id=self.value()
            )

        return queryset


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = (
        "course_name",
        "class_number",
        "session_datetime",
        "status",
        "topic",
    )

    list_filter = (
        "status",
        ClassSessionCourseFilter,
        "course__course_type",
        "start_time",
    )

    search_fields = (
        "title",
        "topic",
        "course__name",
    )

    autocomplete_fields = (
        "course",
    )

    fields = (
        "course",
        "class_number",
        "title",
        "status",
        "start_time",
        "end_time",
        "topic",
        "meeting_link",
        "created_at",
    )

    readonly_fields = (
        "course",
        "class_number",
        "created_at",
    )

    inlines = (
        AttendanceInline,
    )

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        return False

    # ----------------------------------------
    # COURSE NAME
    # ----------------------------------------
    @admin.display(
        description="Course",
        ordering="course__name",
    )
    def course_name(self, obj):
        return obj.course.name

    # ----------------------------------------
    # SESSION DATE + TIME
    # ----------------------------------------
    @admin.display(
        description="Date & time",
        ordering="start_time",
    )
    def session_datetime(self, obj):
        if not obj.start_time:
            return "—"

        start_time = timezone.localtime(obj.start_time)

        if obj.end_time:
            end_time = timezone.localtime(obj.end_time)

            return (
                f"{start_time.strftime('%d/%m/%Y %H:%M')}"
                f"–{end_time.strftime('%H:%M')}"
            )

        return start_time.strftime("%d/%m/%Y %H:%M")


class AttendanceCourseFilter(admin.SimpleListFilter):
    """
    Filter Attendance records by course.

    Displays the actual Course.name in the admin sidebar
    instead of Django's default representation:
        Course object (3)
    """

    title = "course"
    parameter_name = "course"

    def lookups(self, request, model_admin):
        """
        Build the list of courses that actually have
        Attendance records.
        """
        courses = (
            Course.objects
            .filter(
                class_sessions__attendance_records__isnull=False
            )
            .distinct()
            .order_by("name")
        )

        return [
            (course.pk, course.name)
            for course in courses
        ]

    def queryset(self, request, queryset):
        """
        Apply the selected course filter.
        """
        if self.value():
            return queryset.filter(
                class_session__course_id=self.value()
            )

        return queryset


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "student_display",
        "course_name",
        "class_session_display",
        "session_datetime",
        "status",
        "was_punctual",
    )

    list_filter = (
        "status",
        AttendanceCourseFilter,
        "recorded_at",
    )

    search_fields = (
        "student__username",
        "student__first_name",
        "student__last_name",
        "student__email",
        "class_session__course__name",
    )

    autocomplete_fields = (
        "student",
        "class_session",
    )

    fields = (
        "student",
        "class_session",
        "status",
        "minutes_late",
        "notes",
        "recorded_at",
        "was_punctual",
    )

    readonly_fields = (
        "student",
        "class_session",
        "recorded_at",
        "was_punctual",
    )

    list_select_related = (
        "student",
        "class_session",
        "class_session__course",
    )

    def has_add_permission(self, request):
        """
        Attendance rows are created automatically from CourseEnrollment /
        Course generation logic.

        Only superuser can alter.
        """
        if request.user.is_superuser:
            return True

        return False

    def has_delete_permission(self, request, obj=None):
        """
        Preserve attendance history and the one-record-per-student/session
        invariant.

        Only superuser can alter.
        """
        if request.user.is_superuser:
            return True

        return False

    # ----------------------------------------
    # STUDENT NAME
    # First + Last name if available.
    # Otherwise username.
    # ----------------------------------------
    @admin.display(
        description="Student",
        ordering="student__last_name",
    )
    def student_display(self, obj):
        full_name = obj.student.get_full_name().strip()

        if full_name:
            return full_name

        return obj.student.username

    # ----------------------------------------
    # COURSE NAME
    # ----------------------------------------
    @admin.display(
        description="Course",
        ordering="class_session__course__name",
    )
    def course_name(self, obj):
        return obj.class_session.course.name

    # ----------------------------------------
    # CLASS SESSION
    # e.g. Lesson 1
    # ----------------------------------------
    @admin.display(
        description="Class session",
        ordering="class_session__class_number",
    )
    def class_session_display(self, obj):
        return f"Lesson {obj.class_session.class_number}"

    # ----------------------------------------
    # SESSION DATE + TIME
    # e.g. 22/06/2026 12:00
    # ----------------------------------------
    @admin.display(
        description="Date & time",
        ordering="class_session__start_time",
    )
    def session_datetime(self, obj):
        if not obj.class_session.start_time:
            return "—"

        start_time = timezone.localtime(
            obj.class_session.start_time
        )

        return start_time.strftime("%d/%m/%Y %H:%M")


@admin.register(BankHoliday)
class BankHolidayAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "start_date",
        "end_date",
        "is_active",
    )

    list_filter = (
        "is_active",
        "start_date",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "start_date",
    )
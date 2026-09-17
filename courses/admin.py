from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from django.forms.models import BaseInlineFormSet

from .models import (
    CourseType,
    Course,
    CourseTimetableSlot,
    CourseEnrollment,
    StudentNeedsAnalysis,
    ClassSession,
    Attendance,
    BankHoliday,
    Programme,
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


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):

    @admin.display(description="Icon")
    def icon_preview(self, obj):
        if not obj.icon:
            return "—"

        return format_html(
            '''
            <span style="
                width: 46px;
                height: 46px;
                padding: 3px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                background: #006B7D;
                vertical-align: middle;
            ">
                <img
                    src="{}"
                    alt=""
                    style="
                        width: 40px;
                        height: 40px;
                        object-fit: contain;
                    "
                >
            </span>
            ''',
            obj.icon.url,
        )
    
    list_display = (
        "icon_preview",
        "name",
        "slug",
        "is_active",
        "order",
    )

    list_editable = (
        "is_active",
        "order",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    search_fields = (
        "name",
        "description",
    )

# -------------------------------------------------------------------------
# COURSE ENROLLMENT INLINE FORMSET
# -------------------------------------------------------------------------
#
# Django Admin inline deletion normally calls CourseEnrollment.delete()
# without any custom arguments.
#
# CourseEnrollment.delete() deliberately protects genuine historical
# enrollments from accidental permanent deletion unless force=True is used.
#
# This custom inline formset provides the explicit superuser correction path:
#
# - the CourseEnrollmentInline itself restricts deletion to superusers
# - when a superuser confirms deletion from the Course admin
# - delete_existing() calls obj.delete(force=True)
# - the erroneous CourseEnrollment is permanently removed
# - all learner-specific Attendance records for that learner/course are removed
# - the Course's ClassSessions remain unchanged
#
# This is intended only for correcting genuinely erroneous enrollments,
# such as assigning a learner to the wrong Course.
#
# Legitimate enrollment lifecycle changes should use:
# active / paused / completed / cancelled
# rather than permanent deletion.
# -------------------------------------------------------------------------
class CourseEnrollmentInlineFormSet(BaseInlineFormSet):
    def delete_existing(self, obj, commit=True):
        if commit:
            obj.delete(force=True)


# -------------------------------------------------------------------------
# COURSE ENROLLMENT INLINE
# -------------------------------------------------------------------------
#
# Enrollments can be added and managed from the Course admin.
#
# When a new enrollment becomes active:
# - NO new ClassSessions are generated if the course already has sessions.
# - CourseEnrollment.save() automatically creates Attendance records for
#   this learner for the relevant unfinished ClassSessions.
#
# Normal enrollment lifecycle changes should use:
# - active
# - paused
# - completed
# - cancelled
#
# Permanent deletion is reserved for superusers and should be used only
# to correct genuinely erroneous enrollments, such as assigning a learner
# to the wrong Course.
#
# Deleting an erroneous enrollment removes the learner-specific Attendance
# records belonging to that enrollment, while the Course's ClassSessions
# remain unchanged because lesson identity belongs to the Course itself.
# -------------------------------------------------------------------------
class CourseEnrollmentInline(admin.TabularInline):
    model = CourseEnrollment
    formset = CourseEnrollmentInlineFormSet
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

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


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
        "programmes",
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
        "programmes",
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

    filter_horizontal = (
        "programmes",
    )
    # Manual "Generate class sessions" action removed.
    #
    # ClassSessions + initial Attendance records are generated
    # automatically by the model lifecycle once all prerequisites exist.

    def save_related(self, request, form, formsets, change):
        """
        Run after Django Admin has saved all Course-related inline objects.

        Processing order:

        1. Save Course-related inline objects.
        2. Synchronize automatically calculated class duration.
        3. Do NOT resynchronize an existing Course merely because the
           Admin form was saved.
        4. If no ClassSessions exist yet and the Course is confirmed/active:
           - calculate the expected end_date from the timetable
           - perform the final safe initial generation attempt
        5. If ClassSessions exist after processing:
           - synchronize end_date from the actual final ClassSession

        Existing-course schedule synchronization is owned by the model:

        - Course.save() triggers it only when a schedule-defining Course
          field genuinely changes:
          start_date / total_hours / class_duration

        - CourseTimetableSlot.save()/delete() trigger it only when the
          timetable genuinely changes.

        Django Admin must therefore NOT call
        synchronize_future_scheduled_sessions() unconditionally.

        Paused, cancelled and completed Courses do not generate teaching
        sessions here.

        Course-level pause/cancellation lifecycle rules are owned by
        Course.save(), not Django Admin.

        Existing ClassSessions are never deleted or regenerated here.
        """
        super().save_related(
            request,
            form,
            formsets,
            change,
        )

        course = form.instance

        operational_course = course.status in {
            "confirmed",
            "active",
        }

        # -------------------------------------------------------------
        # 1. SYNCHRONIZE AUTOMATIC CLASS DURATION
        # -------------------------------------------------------------
        #
        # Timetable inline objects have now been saved.
        #
        # CourseTimetableSlot already owns schedule synchronization when
        # a timetable change genuinely occurs. This final calculation
        # simply guarantees that the stored automatic class duration
        # reflects the complete final inline state.
        # -------------------------------------------------------------
        if (
            course.timetable_slots.exists()
            and course.class_duration_source == "auto"
        ):
            course.update_class_duration_from_timetable()
            course.refresh_from_db()

        # -------------------------------------------------------------
        # 2. EXISTING CLASS SESSIONS
        # -------------------------------------------------------------
        #
        # IMPORTANT:
        #
        # Do NOT call course.synchronize_future_scheduled_sessions() here.
        #
        # An ordinary Admin save must never rebuild the teaching schedule.
        # Genuine Course/timetable changes are detected and handled by the
        # corresponding model methods.
        # -------------------------------------------------------------
        if not course.class_sessions.exists() and operational_course:

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
            # Only confirmed/active Courses should establish an
            # operational teaching schedule.
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

            # ---------------------------------------------------------
            # 4. FINAL SAFE INITIAL CLASS SESSION GENERATION ATTEMPT
            # ---------------------------------------------------------
            #
            # try_generate_class_sessions() contains its own prerequisite
            # guards, including the no-existing-ClassSessions guard.
            # ---------------------------------------------------------
            course.try_generate_class_sessions()

        # -------------------------------------------------------------
        # 5. FINAL END-DATE SYNCHRONIZATION
        # -------------------------------------------------------------
        #
        # Once ClassSessions exist, their actual final session remains
        # the operational source of truth for Course.end_date.
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
        "attended_classes",
        "missed_classes",
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
        "attended_classes",
        "missed_classes",
        "excused_classes",
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
        Permanent deletion is restricted to superusers.

        Legitimate enrollment lifecycle changes should use status values.
        Permanent deletion is reserved for correcting genuinely erroneous
        enrollments.
        """
        return request.user.is_superuser

    def delete_model(self, request, obj):
        """
        Superuser-only correction path.

        Force-delete the erroneous CourseEnrollment together with that
        learner's Attendance records for the Course. ClassSessions remain
        unchanged because they belong to the Course itself.
        """
        obj.delete(force=True)

    def get_actions(self, request):
        """
        Disable bulk deletion.

        Enrollment deletion is exceptional and should be evaluated
        individually by CourseEnrollment.delete().
        """
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions


@admin.register(StudentNeedsAnalysis)
class StudentNeedsAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "status",
        "submitted_at",
        "reviewed_at",
    )

    list_filter = (
        "status",
        "enrollment__course",
    )

    search_fields = (
        "enrollment__student__username",
        "enrollment__student__first_name",
        "enrollment__student__last_name",
        "enrollment__student__email",
        "enrollment__course__name",
    )

    readonly_fields = (
        "submitted_at",
        "reviewed_at",
    )

    @admin.display(description="Student")
    def student(self, obj):
        return obj.enrollment.student

    @admin.display(description="Course")
    def course(self, obj):
        return obj.enrollment.course

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
        return False

    def has_delete_permission(self, request, obj=None):
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

        Superuser cannot alter.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Preserve attendance history and the one-record-per-student/session
        invariant.

        Superuser cannot alter.
        """
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
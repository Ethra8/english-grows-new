from django.contrib import admin

from django.contrib.admin.views.main import ChangeList

from django import forms
from django.forms.models import BaseInlineFormSet

from django.utils import timezone
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import AdminDateWidget

from django.db.models import (
    BooleanField, 
    Case, 
    Count, 
    F,
    IntegerField, 
    Q, 
    Value, 
    When
)

from profiles.models import UserProfile

from .models import (
    CourseType,
    Programme,
    BankHoliday,
    Course,
    CourseTimetableSlot,
    CourseEnrollment,
    ClassSession,
    Attendance,
)

from courses.utils.course_dates import calculate_course_end_date

from math import ceil


User = get_user_model()


# -------------------------------------------------------------------------
# REFERENCE / CONFIGURATION ADMINS
# -------------------------------------------------------------------------
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


# -------------------------------------------------------------------------
# COURSE ADMIN
# -------------------------------------------------------------------------

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



class TeacherListFilter(admin.SimpleListFilter):
    '''
    Teacher first_name displays on the list
    Teacher username only as fallback
    '''
    title = "teacher"
    parameter_name = "teacher"

    def lookups(self, request, model_admin):
        teachers = (
            User.objects
            .filter(
                profile__role=UserProfile.ROLE_TEACHER,
                courses_taught__isnull=False,
            )
            .distinct()
            .order_by(
                "first_name",
                "last_name",
                "username",
            )
        )

        return [
            (
                teacher.pk,
                teacher.get_full_name() or teacher.username,
            )
            for teacher in teachers
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                teacher_id=self.value(),
            )

        return queryset


class TeacherChoiceField(forms.ModelChoiceField):
    '''
    Inside Course object, teacher first_name displays instead of
    teacher username 
    '''
    def label_from_instance(self, obj):
        return obj.first_name or obj.username



class CourseAdminForm(forms.ModelForm):
    '''
    For Course object, teacher first_name displays instead of
    teacher username 
    '''
    teacher = TeacherChoiceField(
        queryset=User.objects.filter(
            profile__role=UserProfile.ROLE_TEACHER,
        ).order_by(
            "first_name",
            "username",
        ),
        required=False,
    )

    '''
    For Course object, format start date selected to
    d/m/yy ; e.g.: 21/12/27 
    '''
    start_date = forms.DateField(
        required=False,
        input_formats=[
            "%d/%m/%y",
            "%d/%m/%Y",
            "%Y-%m-%d",
        ],
        widget=AdminDateWidget(
            format="%d/%m/%y",
        ),
    )

    class Meta:
        model = Course
        fields = "__all__"




class LowAttendanceFilter(admin.SimpleListFilter):
    '''
    Filter Courses list by low_attendance
    '''
    title = "low attendance"
    parameter_name = "has_low_attendance"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() not in {"yes", "no"}:
            return queryset

        # Equivalent to:
        #
        # submitted_classes >= ceil(total_sessions * 0.25)
        #
        # Because submitted_classes is an integer:
        # submitted_classes * 4 >= total_sessions
        queryset = queryset.annotate(
            _resolved_attendance=(
                F("_attended_count")
                + F("_missed_count")
                + F("_excused_count")
            ),
            _submitted_threshold_check=F("_submitted_classes") * 4,
            _attendance_numerator_check=F("_attended_count") * 4,
            _attendance_denominator_check=(
                F("_attended_count")
                + F("_missed_count")
                + F("_excused_count")
            ) * 3,
        )

        low_attendance = Q(
            _total_sessions__gt=0,
            _resolved_attendance__gt=0,
            _submitted_threshold_check__gte=F("_total_sessions"),
            _attendance_numerator_check__lt=F(
                "_attendance_denominator_check"
            ),
        )

        if self.value() == "yes":
            queryset = queryset.filter(low_attendance)

            return queryset.annotate(
                _low_attendance_status_order=Case(
                    When(status="active", then=Value(1)),
                    When(status="paused", then=Value(2)),
                    When(status="completed", then=Value(3)),
                    When(status="cancelled", then=Value(4)),
                    default=Value(5),
                    output_field=IntegerField(),
                )
            ).order_by(
                "_low_attendance_status_order",
                "name",
            )

        return queryset.exclude(low_attendance)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    form = CourseAdminForm

    list_display = (
        "name",
        "company",
        "course_type_admin",
        "course_level_admin",
        "status",
        "completion_admin",
        "total_hours_admin",
        "active_enrollments",
        "attendance_rate_admin",
        "teacher_admin",
        "start_date_admin",
        "end_date_admin",
    )

    fields = (
        "name",
        "company",
        "course_type",
        "status",
        "course_level",
        "programmes",
        "active_enrollments",
        "completion_admin",
        "attendance_rate_admin",
        "class_duration",
        "class_duration_display",
        "class_duration_source",
        "number_of_classes",
        "final_class_duration_display",
        "teacher",
        "start_date",
        "end_date",
    )

    readonly_fields = (
        "active_enrollments",
        "completion_admin",
        "attendance_rate_admin",
        "class_duration_display",
        "final_class_duration_display",
        "number_of_classes",
        "end_date",
    )

    list_filter = (
        "status",
        LowAttendanceFilter,
        "course_type",
        "programmes",
        "company",
        "start_date",
        "course_level",
        TeacherListFilter,
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
    )

    filter_horizontal = (
        "programmes",
    )

    inlines = (
        CourseTimetableSlotInline,
        CourseEnrollmentInline,
    )


    # ---------------------------------------------------------
    # COURSE LIST DISPLAY
    # ---------------------------------------------------------
    @admin.display(description="Type", ordering="course_type__name")
    def course_type_admin(self, obj):
        return obj.course_type

    @admin.display(description="Level", ordering="course_level")
    def course_level_admin(self, obj):
        return obj.course_level

    @admin.display(description="Total Hours", ordering="total_hours")
    def total_hours_admin(self, obj):
        return obj.total_hours

    @admin.display(description="Teacher", ordering="teacher__first_name")
    def teacher_admin(self, obj):
        if not obj.teacher:
            return "—"

        return obj.teacher.first_name or obj.teacher.username


    @admin.display(description="Start date", ordering="start_date")
    def start_date_admin(self, obj):
        return obj.start_date.strftime("%d/%m/%y") if obj.start_date else "—"

    @admin.display(description="End date", ordering="end_date")
    def end_date_admin(self, obj):
        return obj.end_date.strftime("%d/%m/%y") if obj.end_date else "—"


    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                _active_enrollments=Count(
                    "enrollments",
                    filter=Q(
                        enrollments__status=CourseEnrollment.STATUS_ACTIVE,
                    ),
                    distinct=True,
                ),
                _total_sessions=Count(
                    "class_sessions",
                    distinct=True,
                ),
                _submitted_classes=Count(
                    "class_sessions",
                    filter=Q(
                        class_sessions__status=(
                            ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
                        ),
                    ),
                    distinct=True,
                ),
                _attended_count=Count(
                    "class_sessions__attendance_records",
                    filter=Q(
                        class_sessions__status=(
                            ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
                        ),
                        class_sessions__attendance_records__status=(
                            Attendance.STATUS_ATTENDED
                        ),
                    ),
                    distinct=True,
                ),
                _missed_count=Count(
                    "class_sessions__attendance_records",
                    filter=Q(
                        class_sessions__status=(
                            ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
                        ),
                        class_sessions__attendance_records__status=(
                            Attendance.STATUS_MISSED
                        ),
                    ),
                    distinct=True,
                ),
                _excused_count=Count(
                    "class_sessions__attendance_records",
                    filter=Q(
                        class_sessions__status=(
                            ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED
                        ),
                        class_sessions__attendance_records__status=(
                            Attendance.STATUS_EXCUSED
                        ),
                    ),
                    distinct=True,
                ),
                _held_sessions=Count(
                    "class_sessions",
                    filter=Q(
                        class_sessions__status__in=[
                            ClassSession.STATUS_HELD_ATTENDANCE_PENDING,
                            ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
                        ],
                    ),
                    distinct=True,
                ),
            )
        )


    # ---------------------------------------------------------
    # ACTIVE ENROLLMENTS DISPLAY
    # ---------------------------------------------------------
    @admin.display(description="Active Enrollments", ordering="_active_enrollments")
    def active_enrollments(self, obj):
        return obj._active_enrollments

    # ---------------------------------------------------------
    # COURSE ATTENDANCE DISPLAY
    # ---------------------------------------------------------
    @admin.display(description="Attendance")
    def attendance_rate_admin(self, obj):
        attended_count = obj._attended_count
        missed_count = obj._missed_count
        excused_count = obj._excused_count

        total_final_attendance_records = (
            attended_count
            + missed_count
            + excused_count
        )

        if not total_final_attendance_records:
            return "—"

        attendance_rate = round(
            attended_count
            / total_final_attendance_records
            * 100
        )

        minimum_submitted_classes = ceil(
            obj._total_sessions * 0.25
        )

        course_low_attendance = (
            obj._total_sessions > 0
            and obj._submitted_classes >= minimum_submitted_classes
            and attendance_rate < 75
        )

        if course_low_attendance:
            return format_html(
                '<strong title="Course attendance is below the recommended 75%">'
                '⚠ {}%</strong>',
                attendance_rate,
            )

        return f"{attendance_rate}%"


    @admin.display(description="Completion")
    def completion_admin(self, obj):
        if not obj._total_sessions:
            return "—"

        return f"{round(obj._held_sessions / obj._total_sessions * 100)}%"
    
    @admin.display(description="Class Duration")
    def class_duration_display(self, obj):
        return obj.class_duration_display

    @admin.display(description="Final Class Duration")
    def final_class_duration_display(self, obj):
        return obj.final_class_duration_display


    class Media:
        css = {
            "all": (
                "courses/css/admin/course_admin.css",
            )
        }

    # ClassSessions + initial Attendance records are generated
    # automatically by the model lifecycle once all prerequisites exist.
    # ----------------------------------------

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
        if (
            course.timetable_slots.exists()
            and course.class_duration_source == "auto"
        ):
            course.update_class_duration_from_timetable()
            course.refresh_from_db()

        # -------------------------------------------------------------
        # 2. EXISTING CLASS SESSIONS
        # -------------------------------------------------------------
        if not course.class_sessions.exists() and operational_course:

            # ---------------------------------------------------------
            # 3. CALCULATE EXPECTED END DATE BEFORE INITIAL GENERATION
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
            course.try_generate_class_sessions()

        # -------------------------------------------------------------
        # 5. FINAL END-DATE SYNCHRONIZATION
        # -------------------------------------------------------------
        if course.class_sessions.exists():
            course.sync_end_date_from_sessions()



class LowAttendanceWarningFilter(admin.SimpleListFilter):
    title = "low attendance warning"
    parameter_name = "low_attendance_warning"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(admin_low_attendance_warning=True)

        if self.value() == "no":
            return queryset.filter(admin_low_attendance_warning=False)

        return queryset



# -------------------------------------------------------------------------
# COURSE ENROLLMENT ADMIN
# -------------------------------------------------------------------------
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



class CourseEnrollmentChangeList(ChangeList):
    def _get_default_ordering(self):
        return (
            "-admin_low_attendance_warning",
            "-enrolled_at",
        )


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course_name",
        "status",
        "low_attendance_warning",
        "attendance_percentage",
        "enrolled_at",
    )

    list_filter = (
        "status",
        LowAttendanceWarningFilter,
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

    class Media:
        css = {
            "all": ("courses/css/admin/admin_course_enrollment.css",)
        }

    def get_changelist(self, request, **kwargs):
        return CourseEnrollmentChangeList


    @admin.display(
        description="Low attendance warning",
        ordering="admin_low_attendance_warning",
    )
    def low_attendance_warning(self, obj):
        if obj.admin_low_attendance_warning:
            return format_html(
                '<strong class="low-attendance-warning">{}</strong>',
                "Yes",
            )

        return "No"


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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        submitted_filter = Q(
            student__attendance_records__class_session__course_id=F("course_id"),
            student__attendance_records__class_session__status=ClassSession.STATUS_COMPLETE_ATTENDANCE_SUBMITTED,
            student__attendance_records__status__in=Attendance.FINAL_OUTCOME_STATUSES,
        )

        return (
            queryset
            .annotate(
                admin_submitted_count=Count(
                    "student__attendance_records",
                    filter=submitted_filter,
                    distinct=True,
                ),
                admin_attended_count=Count(
                    "student__attendance_records",
                    filter=submitted_filter & Q(
                        student__attendance_records__status=Attendance.STATUS_ATTENDED,
                    ),
                    distinct=True,
                ),
            )
            .annotate(
                admin_low_attendance_score=(
                    200 * F("admin_attended_count")
                    - 149 * F("admin_submitted_count")
                )
            )
            .annotate(
                admin_low_attendance_warning=Case(
                    When(
                        admin_submitted_count__gt=0,
                        admin_low_attendance_score__lte=0,
                        then=Value(True),
                    ),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
            .order_by(
                "-admin_low_attendance_warning",
                "-enrolled_at",
            )
        )

    @admin.display(
        description="Course",
        ordering="course__name",
    )
    def course_name(self, obj):
        return obj.course.name


# -------------------------------------------------------------------------
# CLASS SESSION ADMIN
# -------------------------------------------------------------------------
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

# -------------------------------------------------------------------------
# ATTENDANCE ADMIN
# -------------------------------------------------------------------------
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


class AttendanceClassStatusFilter(admin.SimpleListFilter):
    """
    Filter Attendance records by the lifecycle status of their ClassSession.

    Attendance.status and ClassSession.status describe different things:
    - Attendance status = learner outcome for that lesson
    - Class status = lifecycle state of the lesson itself
    """

    title = "class status"
    parameter_name = "class_status"

    def lookups(self, request, model_admin):
        return ClassSession._meta.get_field("status").choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                class_session__status=self.value()
            )

        return queryset


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "student_display",
        "course_name",
        "class_session_display",
        "session_datetime",
        "class_session_status",
        "attendance_status",
        "was_punctual",
    )

    list_filter = (
        "status",
        AttendanceClassStatusFilter,
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
        "class_session_status",
        "status",
        "minutes_late",
        "notes",
        "recorded_at",
        "was_punctual",
    )

    readonly_fields = (
        "student",
        "class_session",
        "class_session_status",
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

    # ----------------------------------------
    # CLASS SESSION STATUS
    # e.g. Scheduled / Pending reschedule /
    # Rescheduled / Completed
    # ----------------------------------------
    @admin.display(
        description="Class status",
        ordering="class_session__status",
    )
    def class_session_status(self, obj):
        return obj.class_session.get_status_display()

    # ----------------------------------------
    # ATTENDANCE STATUS
    # e.g. Pending / Attended / Missed / Excused
    # ----------------------------------------
    @admin.display(
        description="Attendance status",
        ordering="status",
    )
    def attendance_status(self, obj):
        return obj.get_status_display()

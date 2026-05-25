from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import CourseType, Course, CourseTimetableSlot, CourseEnrollment, ClassSession, Attendance


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


class CourseEnrollmentInline(admin.TabularInline):
    model = CourseEnrollment
    extra = 1
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


class ClassSessionInline(admin.TabularInline):
    model = ClassSession
    extra = 1

    fields = (
        "title",
        "start_time",
        "end_time",
        "topic",
        "meeting_link",
        "is_cancelled",
    )


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
    list_display = (
        "name",
        "course_type",
        "status",
        "total_hours",
        "class_duration",
        "number_of_classes",
        "company",
        "teacher",
        "start_date",
        "end_date",
    )

    readonly_fields = (
        "number_of_classes",
    )

    list_filter = (
        "status",
        "course_type",
        "company",
        "start_date",
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

    actions = (
        "generate_class_sessions",
    )

    def generate_class_sessions(self, request, queryset):
        for course in queryset:
            try:
                result = course.generate_class_sessions()

                self.message_user(
                    request,
                    (
                        f"{course.name}: "
                        f"{result['sessions_created']} class sessions created, "
                        f"{result['attendances_created']} attendance records created "
                        f"for {result['students_count']} enrolled student(s)."
                    )
                )

            except ValidationError as error:
                self.message_user(
                    request,
                    f"{course.name}: {error.message}",
                    level="ERROR"
                )

    generate_class_sessions.short_description = "Generate class sessions and attendance records"  

    inlines = (
        CourseTimetableSlotInline,
        CourseEnrollmentInline,
        ClassSessionInline,
    )


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
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
        "course",
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
        "attendance_percentage",
        "has_low_attendance_warning",
    )


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 1

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
        "recorded_at",
    )


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "start_time",
        "end_time",
        "topic",
        "is_cancelled",
    )

    list_filter = (
        "is_cancelled",
        "course",
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

    inlines = (
        AttendanceInline,
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "class_session",
        "status",
        "minutes_late",
        "was_punctual",
        "recorded_at",
    )

    list_filter = (
        "status",
        "class_session__course",
        "recorded_at",
    )

    search_fields = (
        "student__username",
        "student__first_name",
        "student__last_name",
        "student__email",
        "class_session__title",
        "class_session__course__name",
    )

    autocomplete_fields = (
        "student",
        "class_session",
    )

    readonly_fields = (
        "recorded_at",
        "was_punctual",
    )
# Register your models here.

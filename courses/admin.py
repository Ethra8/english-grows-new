from django.contrib import admin

from .models import CourseType, Course, CourseEnrollment, ClassSession, Attendance


@admin.register(CourseType)
class CourseTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
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


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "course_type",
        "company",
        "teacher",
        "start_date",
        "end_date",
        "status",
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

    inlines = (
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

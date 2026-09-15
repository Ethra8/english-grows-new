from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.html import format_html, format_html_join

from .models import (
    Company,
    UserProfile,
    StudentAcademicProfile,
    LearningGoal,
    StudentSkillAssessment,
    StudentSubSkillAssessment,
    SUBSKILLS,
)

from courses.models import Course, CourseEnrollment

User = get_user_model()


# USER PROFILE INLINE ==========================================================

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0

    fields = (
        "company",
        "role",
        "country",
        "current_level",
        "profile_photo",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


# USER ADMIN ==================================================================

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    readonly_fields = (
        *UserAdmin.readonly_fields,
        "skills_assessments_editor",
    )

    list_display = (
        "username",
        "email",
        "current_level",
        "is_active",
        "first_name",
        "last_name",
        "get_role",
        "get_company",
        "is_staff",
    )

    list_select_related = (
        "profile",
        "profile__company",
    )

    list_filter = (
        "profile__role",
        "profile__company",
        "is_staff",
        "is_active",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "profile__role",
        "profile__company__name",
    )

    ordering = (
        "profile__role",
        "last_name",
        "first_name",
        "username",
    )


    # -------------------------------------------------------------------------
    # USER CHANGE PAGE FIELDSETS
    # -------------------------------------------------------------------------

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if obj is None:
            return fieldsets

        return (
            *fieldsets,
            (
                "Skills assessments",
                {
                    "fields": ("skills_assessments_editor",),
                    "description": (
                        "Update the student's subskill ratings directly here. "
                        "Assessments are grouped by course and skill."
                    ),
                },
            ),
        )


    # -------------------------------------------------------------------------
    # SKILLS ASSESSMENT EDITOR
    # -------------------------------------------------------------------------

    def skills_assessments_editor(self, obj):
        # ---------------------------------------------------------------------
        # COURSES
        #
        # Build from enrollments, NOT from existing skill assessments.
        # This ensures a student can be assessed for the first time from Admin.
        # ---------------------------------------------------------------------
        enrollments = (
            CourseEnrollment.objects
            .filter(student=obj)
            .select_related("course")
            .order_by("course__name", "course_id")
        )

        courses = []
        seen_course_ids = set()

        for enrollment in enrollments:
            if enrollment.course_id not in seen_course_ids:
                courses.append(enrollment.course)
                seen_course_ids.add(enrollment.course_id)

        # ---------------------------------------------------------------------
        # EXISTING ASSESSMENTS
        #
        # These are optional. Missing assessments/subskills will still be
        # displayed from the canonical SUBSKILLS definition.
        # ---------------------------------------------------------------------
        assessments = (
            StudentSkillAssessment.objects
            .filter(student=obj)
            .select_related("course")
            .prefetch_related("subskill_assessments")
        )

        # Keep historical assessment courses visible even if an enrollment
        # record is unexpectedly unavailable.
        for assessment in assessments:
            if assessment.course_id not in seen_course_ids:
                courses.append(assessment.course)
                seen_course_ids.add(assessment.course_id)

        if not courses:
            return "No courses are associated with this user."

        existing = {}

        for assessment in assessments:
            existing[(assessment.course_id, assessment.skill)] = {
                subskill.subskill: subskill
                for subskill in assessment.subskill_assessments.all()
            }

        course_blocks = []

        # ---------------------------------------------------------------------
        # ALWAYS DISPLAY THE COMPLETE CANONICAL ASSESSMENT FRAMEWORK
        # ---------------------------------------------------------------------
        for course in courses:
            skill_blocks = []

            for skill_value, skill_label in StudentSkillAssessment.SKILL_AREA_CHOICES:
                rows = []
                existing_subskills = existing.get(
                    (course.id, skill_value),
                    {},
                )

                for subskill_value, subskill_label in SUBSKILLS.get(
                    skill_value,
                    [],
                ):
                    subskill = existing_subskills.get(subskill_value)

                    current_rating = (
                        subskill.rating
                        if subskill
                        else ""
                    )

                    field_name = (
                        f"subskill_rating__"
                        f"{course.id}__"
                        f"{skill_value}__"
                        f"{subskill_value}"
                    )

                    choices = [
                        ("", "— Not assessed —"),
                        *StudentSubSkillAssessment.Rating.choices,
                    ]

                    select = forms.Select(
                        choices=choices
                    ).render(
                        name=field_name,
                        value=current_rating,
                        attrs={
                            "style": "min-width:260px;",
                        },
                    )

                    rows.append(
                        format_html(
                            "<tr>"
                            '<td style="padding:8px 16px 8px 0;width:45%;">{}</td>'
                            '<td style="padding:8px 0;">{}</td>'
                            "</tr>",
                            subskill_label,
                            select,
                        )
                    )

                rows_html = format_html_join(
                    "",
                    "{}",
                    ((row,) for row in rows),
                )

                skill_blocks.append(
                    format_html(
                        '<div style="margin:0 0 24px;">'
                        '<h3 style="margin:0 0 8px;">{}</h3>'
                        '<table style="width:100%;max-width:760px;">{}</table>'
                        "</div>",
                        skill_label,
                        rows_html,
                    )
                )

            skills_html = format_html_join(
                "",
                "{}",
                ((block,) for block in skill_blocks),
            )

            course_blocks.append(
                format_html(
                    '<div style="margin:0 0 32px;">'
                    '<h2 style="margin:0 0 18px;padding-bottom:8px;'
                    'border-bottom:1px solid var(--hairline-color);">{}</h2>'
                    "{}"
                    "</div>",
                    course.name,
                    skills_html,
                )
            )

        return format_html_join(
            "",
            "{}",
            ((block,) for block in course_blocks),
        )
    skills_assessments_editor.short_description = "Subskill ratings"


    # -------------------------------------------------------------------------
    # SAVE SUBSKILL RATINGS
    # -------------------------------------------------------------------------

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if not form.instance.pk:
            return

        user = form.instance

        allowed_course_ids = set(
            CourseEnrollment.objects
            .filter(student=user)
            .values_list("course_id", flat=True)
        )

        valid_skills = {
            value
            for value, label
            in StudentSkillAssessment.SKILL_AREA_CHOICES
        }

        valid_subskills = {
            skill: {
                value
                for value, label
                in subskills
            }
            for skill, subskills in SUBSKILLS.items()
        }

        allowed_ratings = {
            value
            for value, label
            in StudentSubSkillAssessment.Rating.choices
        }

        for field_name, submitted_rating in request.POST.items():
            if not field_name.startswith("subskill_rating__"):
                continue

            try:
                prefix, course_id, skill, subskill = field_name.split("__", 3)
                course_id = int(course_id)
            except (ValueError, TypeError):
                continue

            # -----------------------------------------------------------------
            # VALIDATE THE POSTED STRUCTURE
            # -----------------------------------------------------------------
            if course_id not in allowed_course_ids:
                continue

            if skill not in valid_skills:
                continue

            if subskill not in valid_subskills.get(skill, set()):
                continue

            rating = submitted_rating or None

            if rating is not None and rating not in allowed_ratings:
                continue

            # -----------------------------------------------------------------
            # BLANK RATING
            #
            # Do not create assessment records merely because Admin displayed
            # them. Only clear an existing rating when necessary.
            # -----------------------------------------------------------------
            if rating is None:
                assessment = (
                    StudentSkillAssessment.objects
                    .filter(
                        student=user,
                        course_id=course_id,
                        skill=skill,
                    )
                    .first()
                )

                if not assessment:
                    continue

                subskill_assessment = (
                    StudentSubSkillAssessment.objects
                    .filter(
                        skill_assessment=assessment,
                        subskill=subskill,
                    )
                    .first()
                )

                if (
                    subskill_assessment
                    and subskill_assessment.rating
                ):
                    subskill_assessment.rating = None
                    subskill_assessment.save(
                        update_fields=(
                            "rating",
                            "updated_at",
                        )
                    )

                continue

            # -----------------------------------------------------------------
            # FIRST OR EXISTING ASSESSMENT
            #
            # Create the parent skill assessment and subskill only if necessary.
            # -----------------------------------------------------------------
            assessment, created = (
                StudentSkillAssessment.objects.get_or_create(
                    student=user,
                    course_id=course_id,
                    skill=skill,
                )
            )

            subskill_assessment, created = (
                StudentSubSkillAssessment.objects.get_or_create(
                    skill_assessment=assessment,
                    subskill=subskill,
                )
            )

            if subskill_assessment.rating == rating:
                continue

            subskill_assessment.rating = rating
            subskill_assessment.save(
                update_fields=(
                    "rating",
                    "updated_at",
                )
            )

    # -------------------------------------------------------------------------
    # DISPLAY HELPERS
    # -------------------------------------------------------------------------

    def current_level(self, obj):
        if hasattr(obj, "profile") and obj.profile.current_level:
            return obj.profile.current_level
        return "-"

    current_level.short_description = "Current Level"


    def get_role(self, obj):
        if hasattr(obj, "profile") and obj.profile.role:
            return obj.profile.get_role_display()
        return "-"

    get_role.short_description = "Role"
    get_role.admin_order_field = "profile__role"


    def get_company(self, obj):
        if hasattr(obj, "profile") and obj.profile.company:
            return obj.profile.company.name
        return "-"

    get_company.short_description = "Company"
    get_company.admin_order_field = "profile__company__name"


# COMPANY =====================================================================

class CompanyUserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 0
    can_delete = False

    fields = (
        "user",
        "get_first_name",
        "get_last_name",
        "get_email",
        "role",
        "current_level",
        "country",
    )

    readonly_fields = (
        "user",
        "get_first_name",
        "get_last_name",
        "get_email",
    )

    def get_first_name(self, obj):
        return obj.user.first_name or "-"

    get_first_name.short_description = "First name"

    def get_last_name(self, obj):
        return obj.user.last_name or "-"

    get_last_name.short_description = "Last name"

    def get_email(self, obj):
        return obj.user.email or "-"

    get_email.short_description = "Email"


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tax_id",
        "billing_email",
        "phone_number",
        "country",
        "get_number_of_users",
        "created_at",
    )

    search_fields = (
        "name",
        "tax_id",
        "billing_email",
        "phone_number",
        "user_profiles__user__username",
        "user_profiles__user__first_name",
        "user_profiles__user__last_name",
        "user_profiles__user__email",
    )

    list_filter = (
        "country",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    inlines = (
        CompanyUserProfileInline,
    )

    def get_number_of_users(self, obj):
        return obj.user_profiles.count()

    get_number_of_users.short_description = "Users"


# USER PROFILE ================================================================

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "current_level",
        "get_first_name",
        "get_last_name",
        "get_email",
        "role",
        "company",
        "country",
        "native_language",
        "created_at",
    )

    list_filter = (
        "role",
        "level",
        "company",
        "country",
        "native_language",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "company__name",
    )

    list_select_related = (
        "user",
        "company",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def get_first_name(self, obj):
        return obj.user.first_name or "-"

    get_first_name.short_description = "First name"

    def get_last_name(self, obj):
        return obj.user.last_name or "-"

    get_last_name.short_description = "Last name"

    def get_email(self, obj):
        return obj.user.email or "-"

    get_email.short_description = "Email"


# STUDENT ACADEMIC PROFILE ====================================================

@admin.register(StudentAcademicProfile)
class StudentAcademicProfileAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "next_review_date",
        "updated_at",
    )

    filter_horizontal = ("learning_goals",)


# LEARNING GOALS ==============================================================

@admin.register(LearningGoal)
class LearningGoalAdmin(admin.ModelAdmin):
    list_display = (
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


# REGISTRATION ================================================================

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Company, CompanyAdmin)
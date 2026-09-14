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
        assessments = list(
            StudentSkillAssessment.objects
            .filter(student=obj)
            .select_related("course")
            .prefetch_related("subskill_assessments")
        )

        if not assessments:
            return "No skill assessments are available for this user."

        skill_order = {
            value: index
            for index, (value, label)
            in enumerate(StudentSkillAssessment.SKILL_AREA_CHOICES)
        }

        assessments.sort(
            key=lambda assessment: (
                (assessment.course.name or "").lower(),
                assessment.course_id,
                skill_order.get(assessment.skill, 999),
            )
        )

        course_blocks = []
        course_ids = []

        for assessment in assessments:
            if assessment.course_id not in course_ids:
                course_ids.append(assessment.course_id)

        for course_id in course_ids:
            course_assessments = [
                assessment
                for assessment in assessments
                if assessment.course_id == course_id
            ]

            course = course_assessments[0].course
            skill_blocks = []

            for assessment in course_assessments:
                canonical_order = {
                    value: index
                    for index, (value, label)
                    in enumerate(SUBSKILLS.get(assessment.skill, []))
                }

                subskills = sorted(
                    assessment.subskill_assessments.all(),
                    key=lambda subskill: canonical_order.get(
                        subskill.subskill,
                        999,
                    ),
                )

                rows = []

                for subskill in subskills:
                    choices = [
                        ("", "— Not assessed —"),
                        *StudentSubSkillAssessment.Rating.choices,
                    ]

                    options = []

                    for value, label in choices:
                        if (subskill.rating or "") == value:
                            options.append(
                                format_html(
                                    '<option value="{}" selected>{}</option>',
                                    value,
                                    label,
                                )
                            )
                        else:
                            options.append(
                                format_html(
                                    '<option value="{}">{}</option>',
                                    value,
                                    label,
                                )
                            )

                    options_html = format_html_join(
                        "",
                        "{}",
                        ((option,) for option in options),
                    )

                    select = format_html(
                        '<select name="subskill_rating_{}" '
                        'style="min-width:260px;">{}</select>',
                        subskill.pk,
                        options_html,
                    )

                    rows.append(
                        format_html(
                            '<tr>'
                            '<td style="padding:8px 16px 8px 0; width:45%;">{}</td>'
                            '<td style="padding:8px 0;">{}</td>'
                            '</tr>',
                            subskill.get_subskill_display(),
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
                        '<table style="width:100%; max-width:760px;">{}</table>'
                        '</div>',
                        assessment.get_skill_display(),
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
                    '<h2 style="margin:0 0 18px; padding-bottom:8px; '
                    'border-bottom:1px solid var(--hairline-color);">'
                    '{}'
                    '</h2>'
                    '{}'
                    '</div>',
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

        allowed_ratings = {
            value
            for value, label
            in StudentSubSkillAssessment.Rating.choices
        }

        subskills = (
            StudentSubSkillAssessment.objects
            .filter(skill_assessment__student=form.instance)
        )

        for subskill in subskills:
            field_name = f"subskill_rating_{subskill.pk}"

            if field_name not in request.POST:
                continue

            rating = request.POST.get(field_name) or None

            if rating is not None and rating not in allowed_ratings:
                continue

            if subskill.rating == rating:
                continue

            subskill.rating = rating
            subskill.save(
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

class StudentAcademicProfileAdminForm(forms.ModelForm):
    strengths = forms.MultipleChoiceField(
        choices=StudentAcademicProfile.SKILL_AREA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    weaknesses = forms.MultipleChoiceField(
        choices=StudentAcademicProfile.SKILL_AREA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = StudentAcademicProfile
        fields = "__all__"


@admin.register(StudentAcademicProfile)
class StudentAcademicProfileAdmin(admin.ModelAdmin):
    form = StudentAcademicProfileAdminForm

    list_display = (
        "student",
        "current_level",
        "target_level",
        "participation",
        "risk_status",
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
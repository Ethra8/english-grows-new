from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.html import format_html, format_html_join

from .models import (
    Company,
    UserProfile,
    StudentNeedsAnalysis,
    StudentAcademicProfile,
    LearningGoal,
    StudentSkillAssessment,
    StudentSubSkillAssessment,
    SUBSKILLS,
)

from courses.models import CourseEnrollment

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

    list_select_related = (
        "enrollment__student",
        "enrollment__course",
    )

    readonly_fields = (
        "submitted_at",
        "reviewed_at",
    )

    fieldsets = (
        (
            "Enrollment / Workflow",
            {
                "fields": (
                    "enrollment",
                    "status",
                    "submitted_at",
                    "reviewed_at",
                ),
            },
        ),
        (
            "1. Your English",
            {
                "fields": (
                    "english_use_frequency",
                    "communication_situations",
                ),
            },
        ),
        (
            "2. Your Communication",
            {
                "fields": (
                    "communication_partners",
                    "accent_exposure",
                    "accent_exposure_other",
                ),
            },
        ),
        (
            "3. Your Confidence",
            {
                "fields": (
                    "speaking_confidence",
                    "listening_confidence",
                    "reading_confidence",
                    "writing_confidence",
                ),
            },
        ),
        (
            "4. Challenges & Priorities",
            {
                "fields": (
                    "priority_areas",
                    "course_goal",
                ),
            },
        ),
        (
            "5. How You Learn",
            {
                "fields": (
                    "learning_preferences",
                ),
            },
        ),
        (
            "6. Anything Else",
            {
                "fields": (
                    "preferred_topics",
                    "additional_information",
                ),
            },
        ),
    )

    @admin.display(description="Student")
    def student(self, obj):
        return obj.enrollment.student

    @admin.display(description="Course")
    def course(self, obj):
        return obj.enrollment.course



# STUDENT ACADEMIC PROFILE ====================================================
@admin.register(StudentAcademicProfile)
class StudentAcademicProfileAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "next_review_date",
        "updated_at",
    )

    list_select_related = ("student",)

    search_fields = (
        "student__username",
        "student__first_name",
        "student__last_name",
        "student__email",
    )

    autocomplete_fields = ("student",)
    filter_horizontal = ("learning_goals",)

    readonly_fields = (
        "updated_at",
        "skills_assessments_editor",
    )

    fieldsets = (
        (
            "Academic profile",
            {
                "fields": (
                    "student",
                    "learning_goals",
                    "next_review_date",
                    "updated_at",
                ),
            },
        ),
        (
            "Skills assessments",
            {
                "fields": ("skills_assessments_editor",),
                "description": (
                    "Update the student's subskill ratings here. "
                    "Assessments are grouped by course and skill."
                ),
            },
        ),
    )

    # -------------------------------------------------------------------------
    # SKILLS ASSESSMENT EDITOR
    # -------------------------------------------------------------------------

    @admin.display(description="Subskill ratings")
    def skills_assessments_editor(self, obj):
        if not obj or not obj.pk or not obj.student_id:
            return "Save the academic profile first to manage skills assessments."

        user = obj.student

        # ---------------------------------------------------------------------
        # COURSES
        #
        # Build primarily from enrollments so first-time assessments are shown.
        # Also retain historical courses that already contain assessment data.
        # ---------------------------------------------------------------------
        enrollments = (
            CourseEnrollment.objects
            .filter(student=user)
            .select_related("course")
            .order_by("course__name", "course_id")
        )

        courses = []
        seen_course_ids = set()

        for enrollment in enrollments:
            if enrollment.course_id not in seen_course_ids:
                courses.append(enrollment.course)
                seen_course_ids.add(enrollment.course_id)

        assessments = (
            StudentSkillAssessment.objects
            .filter(student=user)
            .select_related("course")
            .prefetch_related("subskill_assessments")
        )

        for assessment in assessments:
            if assessment.course_id not in seen_course_ids:
                courses.append(assessment.course)
                seen_course_ids.add(assessment.course_id)

        if not courses:
            return "No courses are associated with this student."

        courses.sort(key=lambda course: (course.name.lower(), course.pk))

        existing = {
            (assessment.course_id, assessment.skill): {
                subskill.subskill: subskill
                for subskill in assessment.subskill_assessments.all()
            }
            for assessment in assessments
        }

        course_blocks = []

        # ---------------------------------------------------------------------
        # COURSE ACCORDION -> SKILL ACCORDION -> SUBSKILL RATINGS
        # ---------------------------------------------------------------------
        for course in courses:
            skill_blocks = []
            complete_skills = 0
            total_skills = 0
            assessed_subskills = 0
            total_subskills = 0

            for skill_value, skill_label in StudentSkillAssessment.SKILL_AREA_CHOICES:
                expected_subskills = SUBSKILLS.get(skill_value, [])

                if not expected_subskills:
                    continue

                total_skills += 1
                existing_subskills = existing.get((course.id, skill_value), {})
                rows = []
                skill_assessed_count = 0
                skill_total_count = len(expected_subskills)

                for subskill_value, subskill_label in expected_subskills:
                    subskill = existing_subskills.get(subskill_value)
                    current_rating = subskill.rating if subskill else ""

                    if current_rating:
                        skill_assessed_count += 1

                    field_name = (
                        f"subskill_rating__{course.id}__"
                        f"{skill_value}__{subskill_value}"
                    )

                    select = forms.Select(
                        choices=[
                            ("", "— Not assessed —"),
                            *StudentSubSkillAssessment.Rating.choices,
                        ]
                    ).render(
                        name=field_name,
                        value=current_rating,
                        attrs={"style": "width:100%;max-width:320px;"},
                    )

                    rows.append(
                        format_html(
                            '<div style="display:grid;grid-template-columns:minmax(220px,1fr) minmax(260px,320px);'
                            'gap:16px;align-items:center;padding:8px 0;border-top:1px solid var(--hairline-color);">'
                            '<span>{}</span><span>{}</span></div>',
                            subskill_label,
                            select,
                        )
                    )

                assessed_subskills += skill_assessed_count
                total_subskills += skill_total_count

                if skill_total_count and skill_assessed_count == skill_total_count:
                    complete_skills += 1

                rows_html = format_html_join(
                    "",
                    "{}",
                    ((row,) for row in rows),
                )

                skill_blocks.append(
                    format_html(
                        '<details style="margin:8px 0 0;border:1px solid var(--hairline-color);'
                        'border-radius:6px;background:var(--body-bg);">'
                        '<summary style="cursor:pointer;padding:10px 12px;font-weight:600;">'
                        '{} <span style="float:right;font-weight:400;opacity:.7;">{}/{}</span>'
                        '</summary><div style="padding:0 12px 10px;">{}</div></details>',
                        skill_label,
                        skill_assessed_count,
                        skill_total_count,
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
                    '<details style="margin:0 0 12px;border:1px solid var(--hairline-color);'
                    'border-radius:8px;overflow:hidden;">'
                    '<summary style="cursor:pointer;padding:12px 14px;background:var(--darkened-bg);font-weight:600;">'
                    '{} <span style="float:right;font-weight:400;opacity:.75;">'
                    '{}/{} skills complete · {}/{} subskills assessed</span></summary>'
                    '<div style="padding:8px 14px 14px;">{}</div></details>',
                    course.name,
                    complete_skills,
                    total_skills,
                    assessed_subskills,
                    total_subskills,
                    skills_html,
                )
            )

        return format_html_join(
            "",
            "{}",
            ((block,) for block in course_blocks),
        )

    # -------------------------------------------------------------------------
    # SAVE SUBSKILL RATINGS
    # -------------------------------------------------------------------------

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        academic_profile = form.instance

        if not academic_profile.pk or not academic_profile.student_id:
            return

        user = academic_profile.student

        allowed_course_ids = set(
            CourseEnrollment.objects
            .filter(student=user)
            .values_list("course_id", flat=True)
        )

        # Historical assessment courses remain editable even if their
        # enrollment record is no longer available.
        allowed_course_ids.update(
            StudentSkillAssessment.objects
            .filter(student=user)
            .values_list("course_id", flat=True)
        )

        valid_skills = {
            value
            for value, label
            in StudentSkillAssessment.SKILL_AREA_CHOICES
        }

        valid_subskills = {
            skill: {value for value, label in subskills}
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

            if course_id not in allowed_course_ids:
                continue

            if skill not in valid_skills:
                continue

            if subskill not in valid_subskills.get(skill, set()):
                continue

            rating = submitted_rating or None

            if rating is not None and rating not in allowed_ratings:
                continue

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

                if subskill_assessment and subskill_assessment.rating:
                    subskill_assessment.rating = None
                    subskill_assessment.save(
                        update_fields=("rating", "updated_at")
                    )

                continue

            assessment, created = StudentSkillAssessment.objects.get_or_create(
                student=user,
                course_id=course_id,
                skill=skill,
            )

            subskill_assessment, created = StudentSubSkillAssessment.objects.get_or_create(
                skill_assessment=assessment,
                subskill=subskill,
            )

            if subskill_assessment.rating == rating:
                continue

            subskill_assessment.rating = rating
            subskill_assessment.save(
                update_fields=("rating", "updated_at")
            )


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
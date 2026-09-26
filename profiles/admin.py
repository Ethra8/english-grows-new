from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.urls import path, reverse
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.html import format_html, format_html_join

from allauth.account.models import EmailAddress
from allauth.account.internal.flows.email_verification import (
    send_verification_email_to_address,
)

from .models import (
    Company,
    UserProfile,
    StudentNeedsAnalysis,
    StudentAcademicProfile,
    StudentSkillAssessment,
    StudentSubSkillAssessment,
    StudentSkillAssessmentSnapshot,
    StudentSkillTermSnapshot,
    SUBSKILLS,
)

from .forms.student_needs_analysis import (
    StudentNeedsAnalysisForm,
    SITUATION_CHOICES,
)

from courses.models import CourseEnrollment



User = get_user_model()


def get_pending_email_address(user):
    """
    Return a genuine pending replacement email.

    An account's original unverified primary email is excluded,
    because that is not an email-change request.
    """
    if not user or not user.pk:
        return None

    return (
        EmailAddress.objects
        .filter(user=user, verified=False)
        .exclude(email__iexact=user.email)
        .order_by("pk")
        .last()
    )


# Custom admin creation form that requires a unique email address
# and assigns role/company before email verification is sent.
class CustomAdminUserCreationForm(AdminUserCreationForm):
    email = forms.EmailField(required=True)

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        initial=UserProfile.ROLE_INDIVIDUAL_LEARNER,
        required=True,
    )

    company = forms.ModelChoiceField(
        queryset=Company.objects.order_by("name"),
        required=False,
        empty_label="— No company —",
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if (
            User.objects.filter(email__iexact=email).exists()
            or EmailAddress.objects.filter(email__iexact=email).exists()
        ):
            raise forms.ValidationError(
                "A user with this email address already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        if (
            cleaned_data.get("role") in [
                UserProfile.ROLE_EMPLOYEE,
                UserProfile.ROLE_COMPANY_ADMIN,
            ]
            and not cleaned_data.get("company")
        ):
            self.add_error(
                "company",
                "Company is required for employees and company administrators.",
            )

        return cleaned_data


class PendingEmailWidget(forms.EmailInput):
    """
    Display the pending email field together with a resend button
    when an email change is already awaiting verification.
    """

    resend_url = None

    def render(self, name, value, attrs=None, renderer=None):
        email_input = super().render(name, value, attrs, renderer)

        if not self.resend_url:
            return email_input

        return format_html(
            '<div style="display:flex;align-items:center;gap:10px;">'
            '{}'
            '<button type="submit" class="button" formaction="{}" '
            'formmethod="post" formnovalidate>'
            'Resend verification email'
            '</button>'
            '</div>',
            email_input,
            self.resend_url,
        )


class CustomAdminUserChangeForm(UserChangeForm):
    pending_email = forms.EmailField(
        required=False,
        label="New email pending verification",
        help_text=(
            "Enter a replacement email and save. "
            "The current email remains active until the new address is verified."
        ),
        widget=PendingEmailWidget,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pending = get_pending_email_address(self.instance)

        if pending:
            self.fields["pending_email"].initial = pending.email

            opts = self.instance._meta
            self.fields["pending_email"].widget.resend_url = reverse(
                f"admin:{opts.app_label}_{opts.model_name}"
                "_resend_email_verification",
                args=[self.instance.pk],
            )

    def clean_pending_email(self):
        email = (
            self.cleaned_data.get("pending_email") or ""
        ).strip().lower()

        if not email:
            return ""

        if email == (self.instance.email or "").strip().lower():
            raise forms.ValidationError(
                "The new email must be different from the current email."
            )

        if (
            User.objects
            .filter(email__iexact=email)
            .exclude(pk=self.instance.pk)
            .exists()
            or EmailAddress.objects
            .filter(email__iexact=email)
            .exclude(user=self.instance)
            .exists()
        ):
            raise forms.ValidationError(
                "A user with this email address already exists."
            )

        return email


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
    add_form = CustomAdminUserCreationForm
    form = CustomAdminUserChangeForm
    inlines = (UserProfileInline,)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "role",
                    "company",
                    "usable_password",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Email change",
            {
                "fields": ("pending_email",),
                "description": (
                    "The current email remains active until the replacement "
                    "email has been verified."
                ),
            },
        ),
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

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)

        if obj:
            return (*readonly_fields, "email")

        return readonly_fields

    def get_urls(self):
        urls = super().get_urls()
        opts = self.model._meta

        custom_urls = [
            path(
                "<path:object_id>/resend-email-verification/",
                self.admin_site.admin_view(
                    self.resend_email_verification
                ),
                name=(
                    f"{opts.app_label}_{opts.model_name}"
                    "_resend_email_verification"
                ),
            ),
        ]

        return custom_urls + urls

    def resend_email_verification(self, request, object_id):
        user = self.get_object(request, object_id)

        if user is None:
            raise Http404("User does not exist.")

        if not self.has_change_permission(request, user):
            raise PermissionDenied

        opts = self.model._meta
        change_url = reverse(
            f"admin:{opts.app_label}_{opts.model_name}_change",
            args=[user.pk],
        )

        if request.method != "POST":
            return HttpResponseRedirect(change_url)

        pending = get_pending_email_address(user)

        if not pending:
            self.message_user(
                request,
                "There is no pending email address to verify.",
                level=messages.WARNING,
            )
            return HttpResponseRedirect(change_url)

        posted_email = (
            request.POST.get("pending_email") or ""
        ).strip().lower()

        if posted_email and posted_email != pending.email.lower():
            self.message_user(
                request,
                "The pending email field contains unsaved changes. "
                "Save the new email before resending verification.",
                level=messages.WARNING,
            )
            return HttpResponseRedirect(change_url)

        sent = send_verification_email_to_address(
            request,
            pending,
        )

        if not sent:
            self.message_user(
                request,
                "The verification email was not resent because the "
                "resend cooldown is still active. Please try again later.",
                level=messages.WARNING,
            )

        return HttpResponseRedirect(change_url)


    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            # The User post_save signal has already created UserProfile.
            # Assign role/company before sending email verification.
            profile, _ = UserProfile.objects.get_or_create(user=obj)
            profile.role = form.cleaned_data["role"]
            profile.company = form.cleaned_data.get("company")
            profile.save()

            email_address = EmailAddress.objects.add_email(
                request=request,
                user=obj,
                email=obj.email,
                confirm=False,
            )

            email_address.set_as_primary()

            send_verification_email_to_address(
                request,
                email_address,
                signup=True,
            )

            return

        pending_email = form.cleaned_data.get("pending_email")
        current_pending = get_pending_email_address(obj)

        if (
            pending_email
            and (
                not current_pending
                or current_pending.email.lower()
                != pending_email.lower()
            )
        ):
            EmailAddress.objects.add_new_email(
                request=request,
                user=obj,
                email=pending_email,
                send_verification=True,
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

    actions = ["reset_selected_to_pending"]

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
            "4. Your Priorities",
            {
                "fields": (
                    "priority_areas",
                ),
            },
        ),
        (
            "5. Anything Else?",
            {
                "fields": (
                    "additional_information",
                ),
            },
        ),
    )

    # ---------------------------------------------------------
    # READ-ONLY DISPLAY FIELD MAPPING
    #
    # Replace stored values with human-readable answers
    # once the questionnaire has been submitted.
    # ---------------------------------------------------------
    DISPLAY_FIELDS = {
        "english_use_frequency": "english_use_frequency_display",
        "communication_situations": "communication_situations_display",
        "communication_partners": "communication_partners_display",
        "accent_exposure": "accent_exposure_display",
        "speaking_confidence": "speaking_confidence_display",
        "listening_confidence": "listening_confidence_display",
        "reading_confidence": "reading_confidence_display",
        "writing_confidence": "writing_confidence_display",
        "priority_areas": "priority_areas_display",
    }

    # ---------------------------------------------------------
    # DYNAMIC FIELDSETS
    #
    # Pending: original editable fields.
    # Submitted/Reviewed: human-readable display methods.
    # ---------------------------------------------------------
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if obj is None or obj.status == "pending":
            return fieldsets

        return tuple(
            (
                title,
                {
                    **options,
                    "fields": tuple(
                        self.DISPLAY_FIELDS.get(field, field)
                        for field in options["fields"]
                    ),
                },
            )
            for title, options in fieldsets
        )

    def get_readonly_fields(self, request, obj=None):
        return (
            *super().get_readonly_fields(request, obj),
            *self.DISPLAY_FIELDS.values(),
        )

    # ---------------------------------------------------------
    # DISPLAY HELPERS
    #
    # Reuse the canonical choices from StudentNeedsAnalysisForm.
    # No duplicated choice mappings in Admin.
    # ---------------------------------------------------------
    def _choice_list(self, obj, field_name):
        form = StudentNeedsAnalysisForm()

        labels = form.choice_labels(
            field_name,
            getattr(obj, field_name),
        )

        if not labels:
            return "—"

        items = format_html_join(
            "",
            '<li style="display:list-item; list-style-type:disc;">{}</li>',
            ((label,) for label in labels),
        )

        return format_html(
            '<ul style="list-style-type:disc; margin:0; padding-left:1.5rem;">{}</ul>',
            items,
        )

    def _choice_value(self, obj, field_name):
        form = StudentNeedsAnalysisForm()

        labels = form.choice_labels(
            field_name,
            getattr(obj, field_name),
        )

        return ", ".join(labels) if labels else "—"

    def _confidence_value(self, obj, field_name):
        form = StudentNeedsAnalysisForm()

        return form.confidence_display(
            getattr(obj, field_name),
        ) or "—"

    # ---------------------------------------------------------
    # 1. YOUR ENGLISH
    # ---------------------------------------------------------
    @admin.display(description="English use frequency")
    def english_use_frequency_display(self, obj):
        return self._choice_value(obj, "english_use_frequency")

    @admin.display(description="Communication situations")
    def communication_situations_display(self, obj):
        return self._choice_list(obj, "communication_situations")

    # ---------------------------------------------------------
    # 2. YOUR COMMUNICATION
    # ---------------------------------------------------------
    @admin.display(description="Communication partners")
    def communication_partners_display(self, obj):
        return self._choice_list(obj, "communication_partners")

    @admin.display(description="Accent exposure")
    def accent_exposure_display(self, obj):
        return self._choice_list(obj, "accent_exposure")

    # ---------------------------------------------------------
    # 3. YOUR CONFIDENCE
    # ---------------------------------------------------------
    @admin.display(description="Speaking confidence")
    def speaking_confidence_display(self, obj):
        return self._confidence_value(obj, "speaking_confidence")

    @admin.display(description="Listening confidence")
    def listening_confidence_display(self, obj):
        return self._confidence_value(obj, "listening_confidence")

    @admin.display(description="Reading confidence")
    def reading_confidence_display(self, obj):
        return self._confidence_value(obj, "reading_confidence")

    @admin.display(description="Writing confidence")
    def writing_confidence_display(self, obj):
        return self._confidence_value(obj, "writing_confidence")

    # ---------------------------------------------------------
    # 4. CHALLENGES & PRIORITIES
    # ---------------------------------------------------------
    @admin.display(description="Priority areas")
    def priority_areas_display(self, obj):
        return self._choice_list(obj, "priority_areas")

    # ---------------------------------------------------------
    # LIST DISPLAY
    # ---------------------------------------------------------
    @admin.display(description="Student")
    def student(self, obj):
        return obj.enrollment.student

    @admin.display(description="Course", ordering="enrollment__course__name")
    def course(self, obj):
        return obj.enrollment.course.name

    # ---------------------------------------------------------
    # RESET NEEDS ANALYSIS
    # ---------------------------------------------------------
    @admin.action(description="Reset selected Needs Analyses to Pending")
    def reset_selected_to_pending(self, request, queryset):
        count = 0

        for needs_analysis in queryset:
            needs_analysis.reset_to_pending()
            count += 1

        self.message_user(
            request,
            f"{count} Needs Analysis record(s) reset to Pending.",
            messages.SUCCESS,
        )

    # ---------------------------------------------------------
    # PREVENT PERMANENT DELETION
    # ---------------------------------------------------------
    def has_delete_permission(self, request, obj=None):
        return False




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

    readonly_fields = (
        "updated_at",
        "academic_records_editor",
    )

    fieldsets = (
        (
            "Academic profile",
            {
                "fields": (
                    "student",
                    "next_review_date",
                    "updated_at",
                ),
            },
        ),
        (
            "Academic records",
            {
                "classes": ("wide",),
                "fields": ("academic_records_editor",),
                "description": (
                    "Course-specific learning needs and skills assessments. "
                    "Learning Needs are read-only; subskill ratings can be updated here."
                ),
            },
        ),
    )

    class Media:
        css = {
            "all": (
                "css/base/variables.css",
                "profiles/css/admin/student_academic_profile.css",
            )
        }

    # -------------------------------------------------------------------------
    # LEARNING NEEDS SUMMARY
    # -------------------------------------------------------------------------

    def learning_needs_summary(self, enrollment):
        """
        Display the learner's submitted Needs Analysis.

        Questionnaire answers remain read-only and are stored in
        StudentNeedsAnalysis.
        """

        # HISTORICAL ASSESSMENT WITHOUT ENROLLMENT
        if enrollment is None:
            return format_html(
                '<p class="academic-needs__empty">{}</p>',
                "No enrollment record is available for this historical assessment.",
            )

        needs_analysis = getattr(enrollment, "needs_analysis", None)

        # NO NEEDS ANALYSIS RECORD
        if needs_analysis is None:
            return format_html(
                '<p class="academic-needs__empty">{}</p>',
                "The learner has not completed their Learning Needs questionnaire.",
            )

        # PENDING — DO NOT DISPLAY UNFINISHED RESPONSES
        if needs_analysis.status == needs_analysis.Status.PENDING:
            return format_html(
                '<p class="academic-needs__empty">{}</p>',
                "Awaiting learner submission.",
            )

        # ---------------------------------------------------------------------
        # PRIORITY AREAS
        #
        # Reuse the original choices from StudentNeedsAnalysisForm.
        # ---------------------------------------------------------------------

        priorities = needs_analysis.priority_areas or []
        situation_labels = dict(SITUATION_CHOICES)

        if priorities:
            priority_badges = format_html_join(
                "",
                '<span class="academic-needs__priority">{}</span>',
                (
                    (situation_labels.get(value, value),)
                    for value in priorities
                    if value
                ),
            )
        else:
            priority_badges = format_html(
                '<span class="academic-needs__empty">{}</span>',
                "No priority areas selected.",
            )

        # ---------------------------------------------------------------------
        # ADDITIONAL INFORMATION
        # ---------------------------------------------------------------------

        additional_information = (
            needs_analysis.additional_information.strip()
            if needs_analysis.additional_information
            else "Not provided."
        )

        # ---------------------------------------------------------------------
        # SUBMISSION / REVIEW DATES
        # ---------------------------------------------------------------------

        dates = []

        if needs_analysis.submitted_at:
            dates.append(
                format_html(
                    '<span><strong>Submitted:</strong> {}</span>',
                    date_format(
                        timezone.localtime(needs_analysis.submitted_at),
                        "j M Y",
                    ),
                )
            )

        if needs_analysis.reviewed_at:
            dates.append(
                format_html(
                    '<span><strong>Reviewed:</strong> {}</span>',
                    date_format(
                        timezone.localtime(needs_analysis.reviewed_at),
                        "j M Y",
                    ),
                )
            )

        dates_html = format_html_join(
            " · ",
            "{}",
            ((item,) for item in dates),
        )

        # ---------------------------------------------------------------------
        # FULL QUESTIONNAIRE LINK
        # ---------------------------------------------------------------------

        questionnaire_url = reverse(
            f"admin:{needs_analysis._meta.app_label}_{needs_analysis._meta.model_name}_change",
            args=[needs_analysis.pk],
        )

        # ---------------------------------------------------------------------
        # RENDER SUMMARY
        # ---------------------------------------------------------------------

        return format_html(
            '<div class="academic-needs__group">'
                '<span class="academic-needs__label">Priority Areas</span>'
                '<div class="academic-needs__priorities">{}</div>'
            '</div>'

            '<div class="academic-needs__group">'
                '<span class="academic-needs__label">Additional Information</span>'
                '<p class="academic-needs__information">{}</p>'
            '</div>'

            '<div class="academic-needs__footer">'
                '<span class="academic-needs__dates">{}</span>'
                '<a class="academic-needs__link" href="{}">'
                    'View full questionnaire ↗'
                '</a>'
            '</div>',
            priority_badges,
            additional_information,
            dates_html,
            questionnaire_url,
        )

    # -------------------------------------------------------------------------
    # ACADEMIC RECORDS EDITOR
    #
    # ONE COURSE ACCORDION:
    # - Learning Needs (read-only)
    # - Skills Assessment (editable)
    # -------------------------------------------------------------------------

    @admin.display(description="Course academic records")
    def academic_records_editor(self, obj):
        if not obj or not obj.pk or not obj.student_id:
            return "Save the academic profile first to manage academic records."

        user = obj.student

        # ---------------------------------------------------------------------
        # ENROLLMENTS
        #
        # Include all statuses to preserve historical courses.
        # ---------------------------------------------------------------------

        enrollments = list(
            CourseEnrollment.objects
            .filter(student=user)
            .select_related("course", "needs_analysis")
            .order_by("course__name", "course_id")
        )

        enrollment_by_course = {
            enrollment.course_id: enrollment
            for enrollment in enrollments
        }

        courses = [
            enrollment.course
            for enrollment in enrollments
        ]

        seen_course_ids = set(enrollment_by_course)

        # ---------------------------------------------------------------------
        # EXISTING ASSESSMENTS
        #
        # Retain historical courses with assessment data even if their
        # enrollment record no longer exists.
        # ---------------------------------------------------------------------

        assessments = list(
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
        # COURSE ACCORDIONS
        # ---------------------------------------------------------------------

        for course in courses:
            enrollment = enrollment_by_course.get(course.id)

            # -----------------------------------------------------------------
            # LEARNING NEEDS
            # -----------------------------------------------------------------

            needs_html = self.learning_needs_summary(enrollment)

            needs_analysis = (
                getattr(enrollment, "needs_analysis", None)
                if enrollment else None
            )

            if needs_analysis:
                needs_status = needs_analysis.status
                needs_status_label = needs_analysis.get_status_display()
            elif enrollment:
                needs_status = "pending"
                needs_status_label = "Awaiting submission"
            else:
                needs_status = "unavailable"
                needs_status_label = "Unavailable"

            needs_section = format_html(
                '<section class="academic-panel academic-panel--needs">'
                    '<header class="academic-panel__header">'
                        '<h3 class="academic-panel__title">Learning Needs</h3>'
                        '<span class="academic-needs-status academic-needs-status--{}">{}</span>'
                    '</header>'
                    '<div class="academic-panel__body">{}</div>'
                '</section>',
                needs_status,
                needs_status_label,
                needs_html,
            )

            # -----------------------------------------------------------------
            # SKILLS ASSESSMENT
            # -----------------------------------------------------------------

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
                        attrs={"class": "academic-subskill__select"},
                    )

                    rows.append(
                        format_html(
                            '<div class="academic-subskill">'
                                '<span class="academic-subskill__label">{}</span>'
                                '<span class="academic-subskill__control">{}</span>'
                            '</div>',
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

                # -------------------------------------------------------------
                # INDIVIDUAL SKILL ACCORDION
                # -------------------------------------------------------------

                skill_blocks.append(
                    format_html(
                        '<details class="academic-skill">'
                            '<summary class="academic-skill__summary">'
                                '<span class="academic-skill__name">{}</span>'
                                '<span class="academic-skill__count">{}/{} assessed</span>'
                            '</summary>'
                            '<div class="academic-skill__content">{}</div>'
                        '</details>',
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

            # -----------------------------------------------------------------
            # SKILLS ASSESSMENT PANEL
            # -----------------------------------------------------------------

            skills_section = format_html(
                '<section class="academic-panel academic-panel--skills">'
                    '<header class="academic-panel__header">'
                        '<h3 class="academic-panel__title">Skills Assessment</h3>'
                        '<span class="academic-panel__count">'
                            '{}/{} skills complete · {}/{} subskills assessed'
                        '</span>'
                    '</header>'
                    '<div class="academic-panel__body">{}</div>'
                '</section>',
                complete_skills,
                total_skills,
                assessed_subskills,
                total_subskills,
                skills_html,
            )

            # -----------------------------------------------------------------
            # ASSESSMENT HISTORY
            # -----------------------------------------------------------------

            history_section = format_html(
                '<section class="academic-panel academic-panel--history">'
                    '<header class="academic-panel__header">'
                        '<h3 class="academic-panel__title">Assessment History</h3>'
                    '</header>'
                    '<div class="academic-panel__body">{}</div>'
                '</section>',
                self.assessment_history(user, course),
            )

            # -----------------------------------------------------------------
            # COURSE STATUS BADGE
            # -----------------------------------------------------------------

            course_status = course.get_status_display()

            status_class = (
                course.status
                if course.status in {
                    "active",
                    "confirmed",
                    "paused",
                    "completed",
                    "cancelled",
                }
                else "default"
            )


            # -----------------------------------------------------------------
            # COURSE CEFR LEVEL BADGE
            # -----------------------------------------------------------------

            level_code = str(course.course_level or "").strip().upper()
            level_family = level_code[:2].lower()

            level_badge = (
                format_html(
                    '<span class="academic-course__level academic-course__level--{}">{}</span>',
                    level_family,
                    level_code,
                )
                if level_family in {"a1", "a2", "b1", "b2", "c1", "c2"}
                else ""
            )

            # -----------------------------------------------------------------
            # ONE COURSE ACCORDION CONTAINING BOTH SECTIONS
            # -----------------------------------------------------------------

            course_blocks.append(
                format_html(
                    '<details class="academic-course">'
                        '<summary class="academic-course__summary">'

                            '<span class="academic-course__summary-main">'
                                '<span class="academic-course__chevron" aria-hidden="true"></span>'

                                '<span class="academic-course__identity">'
                                    '<span class="academic-course__title">'
                                        '<span class="academic-course__name">{}</span>'
                                        '{}'
                                    '</span>'
                                    '<span class="academic-course__metrics">'
                                        '{}/{} skills complete · {}/{} subskills assessed'
                                    '</span>'
                                '</span>'
                            '</span>'

                            '<span class="academic-course__status academic-course__status--{}">{}</span>'

                        '</summary>'

                        '<div class="academic-course__content">'
                            '{}'
                            '{}'
                            '{}'
                        '</div>'
                    '</details>',
                    course.name,
                    level_badge,
                    complete_skills,
                    total_skills,
                    assessed_subskills,
                    total_subskills,
                    status_class,
                    course_status,
                    needs_section,
                    skills_section,
                    history_section,
                )
            )

        return format_html(
            '<div class="academic-records">{}</div>',
            format_html_join(
                "",
                "{}",
                ((block,) for block in course_blocks),
            ),
        )

    # -------------------------------------------------------------------------
    # SAVE SUBSKILL RATINGS
    #
    # Existing saving behaviour is preserved.
    # Learning Needs remain read-only and are never modified here.
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

            # -----------------------------------------------------------------
            # BLANK RATING
            #
            # Do not create assessment records merely because they were
            # displayed in Admin.
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

                if subskill_assessment and subskill_assessment.rating:
                    subskill_assessment.rating = None
                    subskill_assessment.save(
                        update_fields=("rating", "updated_at")
                    )

                continue

            # -----------------------------------------------------------------
            # FIRST OR EXISTING ASSESSMENT
            # -----------------------------------------------------------------

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

    # -------------------------------------------------------------------------
    # ASSESSMENT HISTORY
    # Read-only historical records for one learner and course.
    # -------------------------------------------------------------------------

    def assessment_history(self, student, course):
        assessments = (
            StudentSkillAssessment.objects
            .filter(student=student, course=course)
            .prefetch_related("assessment_snapshots", "term_snapshots")
        )

        history = []

        for assessment in assessments:
            for snapshot in assessment.assessment_snapshots.all():
                history.append({
                    "date": snapshot.recorded_at,
                    "skill": assessment.get_skill_display(),
                    "type": "Skills assessment",
                    "score": snapshot.score,
                    "term": "",
                    "pk": snapshot.pk,
                })

            for snapshot in assessment.term_snapshots.all():
                history.append({
                    "date": snapshot.recorded_at,
                    "skill": assessment.get_skill_display(),
                    "type": "Term assessment",
                    "score": snapshot.score,
                    "term": snapshot.term_label,
                    "pk": snapshot.pk,
                })

        if not history:
            return format_html(
                '<p class="academic-needs__empty">{}</p>',
                "No historical assessments have been recorded for this course.",
            )

        history.sort(
            key=lambda item: (
                item["date"].date()
                if hasattr(item["date"], "date")
                else item["date"],
                item["pk"],
            ),
            reverse=True,
        )

        rows = format_html_join(
            "",
            '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>',
            (
                (
                    date_format(item["date"], "j M Y, H:i")
                    if hasattr(item["date"], "hour")
                    else date_format(item["date"], "j M Y"),
                    item["skill"],
                    item["type"],
                    item["term"] or "—",
                    f'{item["score"]}/10',
                )
                for item in history
            ),
        )

        return format_html(
            '<div style="overflow-x:auto;">'
                '<table style="width:100%;border-collapse:collapse;">'
                    '<thead><tr>'
                        '<th>Date</th>'
                        '<th>Skill</th>'
                        '<th>Assessment</th>'
                        '<th>Term</th>'
                        '<th>Score</th>'
                    '</tr></thead>'
                    '<tbody>{}</tbody>'
                '</table>'
            '</div>',
            rows,
        )


# REGISTRATION ================================================================

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Company, CompanyAdmin)
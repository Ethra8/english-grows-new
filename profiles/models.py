from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.translation import gettext_lazy as _

from decimal import Decimal, ROUND_HALF_UP

from courses.models import Course, CourseEnrollment


class Company(models.Model):
    """
    A company or organisation that can pay for courses
    for multiple employees/users.
    """

    name = models.CharField(max_length=255)

    tax_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Company tax/VAT ID, e.g. CIF/NIF/VAT number."
    )

    billing_email = models.EmailField(
        max_length=254,
        null=True,
        blank=True,
        help_text="Email used for invoices and billing communication."
    )

    billing_address = models.TextField(
        null=True,
        blank=True
    )

    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Company contact phone number."
    )

    country = CountryField(
        blank_label="Country",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    Extra profile information for each user.

    User model stores:
    - username
    - first_name
    - last_name
    - email
    - password

    UserProfile stores:
    - company relationship
    - role
    - country
    - English level
    """

    ROLE_TEACHER = "teacher"
    ROLE_INDIVIDUAL_LEARNER = "learner"
    ROLE_COMPANY_ADMIN = "company_admin"
    ROLE_EMPLOYEE = "employee"

    # from django.utils.translation,
    # _ allows translation
    ROLE_CHOICES = [
        (ROLE_TEACHER, _("Teacher")),
        (ROLE_INDIVIDUAL_LEARNER, _("Learner")),
        (ROLE_COMPANY_ADMIN, _("Company Admin")),
        (ROLE_EMPLOYEE, _("Employee")),
    ]

    LEVEL_UNKNOWN = "Pending"
    LEVEL_A1 = "A1"
    LEVEL_A2 = "A2"
    LEVEL_B1_1 = "B1.1"
    LEVEL_B1_2 = "B1.2"
    LEVEL_B2_1 = "B2.1"
    LEVEL_B2_2 = "B2.2"
    LEVEL_C1_1 = "C1.1"
    LEVEL_C1_2 = "C1.2"
    LEVEL_C2 = "C2"

    LEVEL_CHOICES = [
        (LEVEL_UNKNOWN, _("Pending")),
        (LEVEL_A1, _("A1 - Beginner")),
        (LEVEL_A2, _("A2 - Elementary")),
        (LEVEL_B1_1, _("B1.1 - Pre-Intermediate")),
        (LEVEL_B1_2, _("B1.2 - Lower Intermediate")),
        (LEVEL_B2_1, _("B2.1 - Intermediate")),
        (LEVEL_B2_2, _("B2.2 - Higher Intermediate")),
        (LEVEL_C1_1, _("C1.1 - Lower Advanced")),
        (LEVEL_C1_2, _("C1.2 - Higher Advanced")),
        (LEVEL_C2, _("C2 Proficiency")),
    ]

    NATIVE_LANGUAGE_CHOICES = [
        ("", "Native language"),
        ("es", "Spanish"),
        ("fr", "French"),
        ("it", "Italian"),
        ("de", "German"),
        ("pt", "Portuguese"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_profiles",
        help_text="Leave empty for individual students."
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default=ROLE_INDIVIDUAL_LEARNER
    )

    native_language = models.CharField(
        max_length=20,
        choices=NATIVE_LANGUAGE_CHOICES,
        blank=True,
    )

    country = CountryField(
        blank_label="Country of origin",
        null=True,
        blank=True
    )

    current_level = models.CharField(
        max_length=200,
        choices=LEVEL_CHOICES,
        blank=True,
        default="",
        help_text="Current English level. Only admin should update this."
    )

    profile_photo = models.ImageField(
        upload_to="profile_photos/",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_teacher(self):
        return self.role == self.ROLE_TEACHER

    @property
    def is_company_admin(self):
        return self.role == self.ROLE_COMPANY_ADMIN

    @property
    def is_employee(self):
        return self.role == self.ROLE_EMPLOYEE

    @property
    def is_individual(self):
        return self.role == self.ROLE_INDIVIDUAL_LEARNER

    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile whenever a new User is created.
    """

    if created:
        UserProfile.objects.get_or_create(user=instance)



class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )

    bio = models.TextField(blank=True)

    specialties = models.CharField(
        max_length=255,
        blank=True,
        help_text="Example: Business English, FCE, CAE, Kids, Conversation"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class StudentNeedsAnalysis(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUBMITTED = "submitted", "Submitted"
        REVIEWED = "reviewed", "Reviewed"

    # ---------------------------------------------------------
    # ENROLLMENT / WORKFLOW
    # ---------------------------------------------------------
    enrollment = models.OneToOneField(
        CourseEnrollment,
        on_delete=models.CASCADE,
        related_name="needs_analysis",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # ---------------------------------------------------------
    # 1. ENGLISH USE
    # ---------------------------------------------------------
    english_use_frequency = models.CharField(
        max_length=30,
        blank=True,
    )

    communication_situations = models.JSONField(
        default=list,
        blank=True,
    )


    # ---------------------------------------------------------
    # 2. COMMUNICATION
    # ---------------------------------------------------------
    communication_partners = models.JSONField(
        default=list,
        blank=True,
    )

    accent_exposure = models.JSONField(
        default=list,
        blank=True,
    )

    accent_exposure_other = models.CharField(
        max_length=150,
        blank=True,
    )   
    # ---------------------------------------------------------
    # 3. CONFIDENCE
    #
    # Values:
    # 1 = Not confident yet
    # 2 = Slightly confident
    # 3 = Fairly confident
    # 4 = Confident
    # 5 = Very confident
    # ---------------------------------------------------------
    speaking_confidence = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    listening_confidence = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    reading_confidence = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    writing_confidence = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    # ---------------------------------------------------------
    # 4. PRIORITIES
    # ---------------------------------------------------------
    priority_areas = models.JSONField(
        default=list,
        blank=True,
    )

    # ---------------------------------------------------------
    # 5. ADDITIONAL INFORMATION
    # ---------------------------------------------------------
    additional_information = models.TextField(
        blank=True,
    )

    # ---------------------------------------------------------
    # SUBMISSION / REVIEW
    # ---------------------------------------------------------
    submitted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Student needs analysis"
        verbose_name_plural = "Student needs analysis"


    def __str__(self):
        return (
            f"Needs Analysis - "
            f"{self.enrollment.student} - "
            f"{self.enrollment.course}"
        )

    # ---------------------------------------------------------
    # RESET NEEDS ANALYSIS
    # ---------------------------------------------------------
    def reset_to_pending(self):
        self.status = "pending"
        self.submitted_at = None
        self.reviewed_at = None

        self.english_use_frequency = ""
        self.communication_situations = []

        self.communication_partners = []
        self.accent_exposure = []
        self.accent_exposure_other = ""

        self.speaking_confidence = None
        self.listening_confidence = None
        self.reading_confidence = None
        self.writing_confidence = None

        self.priority_areas = []

        self.additional_information = ""

        fields = [
            "status", "submitted_at", "reviewed_at",
            "english_use_frequency", "communication_situations",
            "communication_partners", "accent_exposure", "accent_exposure_other",
            "speaking_confidence", "listening_confidence",
            "reading_confidence", "writing_confidence",
            "priority_areas", "additional_information",
        ]

        self.save(update_fields=fields)


class StudentAcademicProfile(models.Model):
    """
    Persistent learner-wide academic information.

    Course-specific data such as target level, learning objective,
    participation, attendance and teacher observations belong to
    their respective course/enrollment/review models.

    Current level is read from UserProfile.

    Strengths and development areas are derived from the student's
    skills and subskills assessment data rather than stored here.
    """

    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="academic_profile"
    )

    next_review_date = models.DateField(
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Academic Profile - {self.student}"


SUBSKILLS = {
    "speaking": [
        ("fluency", "Fluency"),
        ("accuracy_and_range", "Grammar & vocabulary (Accuracy & range)"),
        ("pronunciation", "Pronunciation"),
        ("interaction", "Interaction"),
    ],

    "reading": [
        ("scanning", "Scanning (Specific information)"),
        ("skimming", "Skimming (General Idea)"),
        ("detailed", "In detail (Deep Understanding)"),
    ],

    "listening": [
        ("gist", "For Gist (General Idea)"),
        ("specific_information", "For Specific Information"),
        ("detailed", "In detail (Deep Understanding)"),
    ],

    "writing": [
        ("organization", "Structure & Organization"),
        ("cohesion", "Cohesion & Coherence"),
        ("vocabulary_grammar", "Grammar & vocabulary (Accuracy & range)"),
        ("register", "Register (Style accuracy)"),
    ],
}

SUBSKILL_CHOICES = [
    choice
    for subskills in SUBSKILLS.values()
    for choice in subskills
]

class StudentSkillAssessment(models.Model):
    SKILL_AREA_CHOICES = [
        ("speaking", "Speaking"),
        ("reading", "Reading"),
        ("writing", "Writing"),
        ("listening", "Listening"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="skill_assessments",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="student_skill_assessments",
    )

    skill = models.CharField(
        max_length=20,
        choices=SKILL_AREA_CHOICES,
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "course", "skill")
    
    def __str__(self):
        return (
            f"{self.student.get_full_name()} · "
            f"{self.course.name} · "
            f"{self.get_skill_display()}"
        )

    @property
    def average_score(self):
        assessed_subskills = (
            self.subskill_assessments
            .exclude(rating__isnull=True)
            .exclude(rating="")
        )

        if not assessed_subskills.exists():
            return None

        scores = [
            subskill.score
            for subskill in assessed_subskills
            if subskill.score is not None
        ]

        if not scores:
            return None

        total = sum(
            scores,
            Decimal("0"),
        )

        average = total / Decimal(len(scores))

        return average.quantize(
            Decimal("0.1"),
            rounding=ROUND_HALF_UP,
        )



# =========================================================
# STUDENT SUBSKILL ASSESSMENT
# =========================================================
class StudentSubSkillAssessment(models.Model):

    class Rating(models.TextChoices):
        NEEDS_WORK = (
            "needs_work",
            "Focus areas",
        )
        DEVELOPING = (
            "developing",
            "Developing",
        )
        REQUIRED_STANDARD = (
            "required_standard",
            "Required standard achieved",
        )
        CONFIDENT = (
            "confident",
            "Confident in",
        )
        STRONG = (
            "strong",
            "Key strengths",
        )

    # Numeric representation of each assessment rating.
    # Used for:
    # - overall skill averages
    # - progress graphs
    # - historical snapshots
    SCORE_BY_RATING = {
        Rating.NEEDS_WORK: Decimal("4.0"),
        Rating.DEVELOPING: Decimal("5.0"),
        Rating.REQUIRED_STANDARD: Decimal("6.0"),
        Rating.CONFIDENT: Decimal("7.5"),
        Rating.STRONG: Decimal("10.0"),
    }

    skill_assessment = models.ForeignKey(
        StudentSkillAssessment,
        on_delete=models.CASCADE,
        related_name="subskill_assessments",
    )

    subskill = models.CharField(
        max_length=50,
        choices=SUBSKILL_CHOICES,
    )

    # An unrated subskill is represented by a blank/NULL rating.
    rating = models.CharField(
        max_length=30,
        choices=Rating.choices,
        blank=True,
        null=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        unique_together = (
            "skill_assessment",
            "subskill",
        )
        ordering = ["subskill"]

    @property
    def score(self):
        """
        Return the numeric representation of this
        subskill assessment on a 0-10 scale.

        Unrated subskills return None.
        """
        if not self.rating:
            return None

        return self.SCORE_BY_RATING.get(self.rating)

    # ---------------------------------------------------------
    # ASSESSMENT HISTORY
    #
    # No custom save() method is required.
    #
    # This model stores the CURRENT rating of one subskill.
    # Saving an individual rating must NOT create a historical
    # assessment snapshot.
    #
    # The teacher_edit_student_skill() view is responsible for:
    # 1. Validating the complete subskill formset.
    # 2. Saving all submitted ratings.
    # 3. Calculating the final overall skill average.
    # 4. Creating ONE ongoing assessment snapshot.
    #
    # A new snapshot is created for every valid explicit
    # assessment submission, even when ratings are unchanged.
    #
    # An entirely unrated skill produces no snapshot.
    # ---------------------------------------------------------

    def __str__(self):
        return (
            f"{self.skill_assessment.get_skill_display()} → "
            f"{self.get_subskill_display()}"
        )


# =========================================================
# STUDENT SKILL ASSESSMENT SNAPSHOT
# =========================================================
class StudentSkillAssessmentSnapshot(models.Model):
    """
    Historical record of ONE completed ongoing skill assessment.

    Created explicitly by teacher_edit_student_skill() after
    all submitted subskill ratings have been saved.

    Each valid assessment submission creates one snapshot
    containing the final overall skill average.

    IMPORTANT:
    - Unchanged ratings still constitute a new assessment.
    - An entirely unrated skill produces no snapshot.
    - Individual subskill saves do not create snapshots.
    - Written feedback is generated separately on request.
    - Formal term assessments use StudentSkillTermSnapshot.

    Used to build the detailed ongoing skill progress history.
    """

    skill_assessment = models.ForeignKey(
        StudentSkillAssessment,
        on_delete=models.CASCADE,
        related_name="assessment_snapshots",
    )

    # Final overall skill average at the time of submission.
    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
    )

    # Timestamp of the completed assessment submission.
    recorded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["recorded_at"]

    def __str__(self):
        score_display = (
            int(self.score)
            if self.score == self.score.to_integral()
            else self.score
        )

        return (
            f"{self.skill_assessment.student.get_full_name()} · "
            f"{self.skill_assessment.get_skill_display()} · "
            f"{score_display}/10 · "
            f"{self.recorded_at:%d %b %Y %H:%M}"
        )


# =========================================================
# STUDENT TERM ASSESSMENT
# =========================================================
class StudentTermAssessment(models.Model):
    """
    Formal assessment of one learner within one course.

    Draft assessments contain independent copies of the learner's
    subskill ratings, which the teacher may review and adjust.

    Submitted assessments preserve their final academic results
    independently of subsequent ongoing Skills Assessment changes.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        SUBMITTED = "submitted", _("Submitted")

    enrollment = models.ForeignKey(
        CourseEnrollment,
        on_delete=models.CASCADE,
        related_name="term_assessments",
    )

    term_label = models.CharField(
        max_length=50,
        help_text=_("For example: Assessment 1, Mid-course review or Final review."),
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    assessment_date = models.DateField(
        null=True,
        blank=True,
        help_text=_("Academic date of the formal assessment."),
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submitted_term_assessments",
    )

    overall_score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    overall_feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["enrollment", "term_label"],
                name="unique_term_assessment_per_enrollment",
            ),
        ]

    @property
    def calculated_overall_score(self):
        """Calculate the equally weighted average of all four skills."""
        snapshots = list(self.skill_snapshots.all())

        if len(snapshots) != len(SUBSKILLS):
            return None

        scores = [snapshot.calculated_score for snapshot in snapshots]

        if any(score is None for score in scores):
            return None

        average = sum(scores, Decimal("0")) / Decimal(len(scores))
        return average.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

    def save(self, *args, **kwargs):
        if self.pk:
            previous = type(self).objects.filter(pk=self.pk).values("status").first()

            if previous and previous["status"] == self.Status.SUBMITTED:
                raise ValidationError("Submitted assessments cannot be modified.")

        super().save(*args, **kwargs)    

    def __str__(self):
        return (
            f"{self.enrollment.student.get_full_name() or self.enrollment.student.username} · "
            f"{self.enrollment.course} · {self.term_label}"
        )


# =========================================================
# STUDENT SKILL TERM SNAPSHOT
# =========================================================
class StudentSkillTermSnapshot(models.Model):
    """
    Formal assessment result for one skill within a term assessment.

    Stores the calculated skill score independently of ongoing
    Skills Assessment records.
    """
    term_assessment = models.ForeignKey(
        StudentTermAssessment,
        on_delete=models.CASCADE,
        related_name="skill_snapshots",
    )

    skill = models.CharField(
        max_length=20,
        choices=StudentSkillAssessment.SKILL_AREA_CHOICES,
    )

    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    class Meta:
        ordering = ["skill"]
        constraints = [
            models.UniqueConstraint(
                fields=["term_assessment", "skill"],
                name="unique_skill_per_term_assessment",
            ),
        ]

    @property
    def calculated_score(self):
        """Calculate the formal skill average from its rated subskills."""
        scores = [
            subskill.score
            for subskill in self.subskill_assessments.all()
            if subskill.score is not None
        ]

        if not scores:
            return None

        average = sum(scores, Decimal("0")) / Decimal(len(scores))
        return average.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

    def _ensure_editable(self):
        status = StudentTermAssessment.objects.filter(
            pk=self.term_assessment_id,
        ).values_list("status", flat=True).first()

        if status == StudentTermAssessment.Status.SUBMITTED:
            raise ValidationError("Submitted skill results cannot be modified.")

    def save(self, *args, **kwargs):
        self._ensure_editable()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self._ensure_editable()
        return super().delete(*args, **kwargs)


    def __str__(self):
        return (
            f"{self.term_assessment} · "
            f"{self.get_skill_display()}"
        )


# =========================================================
# STUDENT TERM SUBSKILL ASSESSMENT
# =========================================================
class StudentTermSubSkillAssessment(models.Model):
    """
    Independent formal subskill rating within a term assessment.

    Initially copied from the learner's ongoing assessment.
    Subsequent changes do not modify ongoing subskill ratings.
    """

    skill_snapshot = models.ForeignKey(
        StudentSkillTermSnapshot,
        on_delete=models.CASCADE,
        related_name="subskill_assessments",
    )

    subskill = models.CharField(
        max_length=50,
        choices=SUBSKILL_CHOICES,
    )

    rating = models.CharField(
        max_length=30,
        choices=StudentSubSkillAssessment.Rating.choices,
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["subskill"]
        constraints = [
            models.UniqueConstraint(
                fields=["skill_snapshot", "subskill"],
                name="unique_subskill_per_term_skill",
            ),
        ]

    @property
    def score(self):
        if not self.rating:
            return None

        return StudentSubSkillAssessment.SCORE_BY_RATING.get(self.rating)

    def _ensure_editable(self):
        status = StudentTermAssessment.objects.filter(
            pk=self.skill_snapshot.term_assessment_id,
        ).values_list("status", flat=True).first()

        if status == StudentTermAssessment.Status.SUBMITTED:
            raise ValidationError("Submitted assessment ratings cannot be modified.")

    def save(self, *args, **kwargs):
        self._ensure_editable()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self._ensure_editable()
        return super().delete(*args, **kwargs)

    
    def __str__(self):
        return (
            f"{self.skill_snapshot} · "
            f"{self.get_subskill_display()}"
        )




# =========================================================
# STUDENT TERM ASSESSMENT REPORT
# =========================================================

class StudentTermAssessmentReport(models.Model):
    """
    Persisted report generated from a submitted Formal Term Assessment.

    One report per assessment. Its content is stored independently
    and is not automatically regenerated or overwritten.

    Generation does not imply publication to the learner.
    """

    assessment = models.OneToOneField(
        StudentTermAssessment,
        on_delete=models.CASCADE,
        related_name="report",
    )

    content = models.JSONField(
        help_text=_("Snapshot of the generated assessment report."),
    )

    generated_at = models.DateTimeField(auto_now_add=True)

    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_term_assessment_reports",
    )

    class Meta:
        ordering = ["-generated_at"]
        verbose_name = _("Student Term Assessment Report")
        verbose_name_plural = _("Student Term Assessment Reports")

    def __str__(self):
        return f"{self.assessment} · Report"

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError(
                _("Generated assessment reports cannot be modified.")
            )

        if self.assessment.status != StudentTermAssessment.Status.SUBMITTED:
            raise ValidationError(
                _("Reports can only be created for submitted assessments.")
            )

        if not self.content:
            raise ValidationError(_("Report content cannot be empty."))

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError(
            _("Generated assessment reports cannot be deleted directly.")
        )

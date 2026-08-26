from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from django_countries.fields import CountryField

from django.utils.translation import gettext_lazy as _

from decimal import Decimal, ROUND_HALF_UP

from courses.models import Course


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
    ROLE_INDIVIDUAL = "learner"
    ROLE_COMPANY_ADMIN = "company_admin"
    ROLE_EMPLOYEE = "employee"

    # from django.utils.translation,
    # _ allows translation
    ROLE_CHOICES = [
        (ROLE_TEACHER, _("Teacher")),
        (ROLE_INDIVIDUAL, _("Learner")),
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
        default=ROLE_INDIVIDUAL
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
        return self.role == self.ROLE_INDIVIDUAL

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


# TO be able to update learning_goals in student profile
# ALSO from the Admin Panel
class LearningGoal(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class StudentAcademicProfile(models.Model):

    LEARNING_GOAL_CHOICES = [
        ("conversation", "Conversation Fluency"),
        ("grammar_accuracy", "Grammar Accuracy"),
        ("vocabulary", "Vocabulary Building"),
        ("pronunciation", "Pronunciation"),
        ("listening", "Listening Confidence"),
        ("business_english", "Business English"),
        ("emails", "Professional Emails"),
        ("meetings", "Meetings"),
        ("presentations", "Presentations"),
        ("exam_prep", "Exam Preparation"),
    ]

    SKILL_AREA_CHOICES = [
        ("speaking", "Speaking"),
        ("listening", "Listening"),
        ("reading", "Reading"),
        ("writing", "Writing"),
        ("grammar", "Grammar"),
        ("vocabulary", "Vocabulary"),
        ("pronunciation", "Pronunciation"),
        ("fluency", "Fluency"),
        ("accuracy", "Accuracy"),
        ("confidence", "Confidence"),
    ]

    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="academic_profile"
    )

    current_level = models.CharField(
        max_length=10,
        choices=UserProfile.LEVEL_CHOICES,
        blank=True,
        null=True
    )

    target_level = models.CharField(
        max_length=10,
        choices=UserProfile.LEVEL_CHOICES,
        blank=True,
        null=True
    )

    learning_goals = models.ManyToManyField(
        LearningGoal,
        blank=True,
        related_name="student_academic_profiles"
    )

    strengths = models.JSONField(
        default=list,
        blank=True
    )

    weaknesses = models.JSONField(
        default=list,
        blank=True
    )   
    
    teacher_notes = models.TextField(blank=True)

    participation = models.CharField(
        max_length=20,
        choices=[
            ("excellent", "Excellent"),
            ("good", "Good"),
            ("average", "Average"),
            ("needs_support", "Needs Support"),
        ],
        blank=True,
        null=True
    )

    risk_status = models.CharField(
        max_length=20,
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        default="low"
    )

    next_review_date = models.DateField(blank=True, null=True)

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

    teacher_notes = models.TextField(blank=True)

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


    def generate_teacher_notes(self):
        subskills = self.subskill_assessments.all()

        if not subskills.exists():
            return ""

        strengths = []
        confident = []
        required_standard = []
        developing = []
        needs_work = []

        for subskill in subskills:
            label = subskill.get_subskill_display()

            if subskill.rating == "strong":
                strengths.append(label)

            elif subskill.rating == "confident":
                confident.append(label)

            elif subskill.rating == "required_standard":
                required_standard.append(label)

            elif subskill.rating == "developing":
                developing.append(label)

            elif subskill.rating == "needs_work":
                needs_work.append(label)


        notes = []

        if strengths:
            notes.append(
                f"Key strengths: {', '.join(strengths)}."
            )

        if confident:
            notes.append(
                f"Confident in: {', '.join(confident)}."
            )

        if required_standard:
            notes.append(
                f"Required standard achieved: {', '.join(required_standard)}."
            )

        if developing:
            notes.append(
                f"Developing: {', '.join(developing)}."
            )

        if needs_work:
            notes.append(
                f"Focus areas: {', '.join(needs_work)}."
            )

        return "\n".join(notes)


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
        """
        if not self.rating:
            return None

        return self.SCORE_BY_RATING.get(self.rating)

    def save(self, *args, **kwargs):
        """
        Save the subskill assessment.

        Create a historical snapshot ONLY when:
        - a real teacher rating is assigned for the first time, or
        - an existing teacher rating is changed.

        Saving an unrated subskill does NOT create a snapshot.
        """

        previous_rating = None

        # -----------------------------------------------------
        # GET PREVIOUS RATING
        # -----------------------------------------------------
        if self.pk:
            previous_rating = (
                StudentSubSkillAssessment.objects
                .filter(pk=self.pk)
                .values_list("rating", flat=True)
                .first()
            )

        # A real assessment exists only when rating is not blank/null.
        has_real_rating = bool(self.rating)

        rating_changed = (
            has_real_rating
            and previous_rating != self.rating
        )

        # -----------------------------------------------------
        # SAVE FIRST
        #
        # The new rating must exist in the DB before calculating
        # the new overall skill average.
        # -----------------------------------------------------
        super().save(*args, **kwargs)

        # -----------------------------------------------------
        # CREATE HISTORICAL SNAPSHOT
        # -----------------------------------------------------
        if rating_changed:
            current_score = self.skill_assessment.average_score

            if current_score is not None:
                StudentSkillAssessmentSnapshot.objects.create(
                    skill_assessment=self.skill_assessment,
                    score=current_score,
                )

    def __str__(self):
        return (
            f"{self.skill_assessment.get_skill_display()} → "
            f"{self.get_subskill_display()}"
        )


class StudentSkillAssessmentSnapshot(models.Model):
    """
    Stores the overall skill score whenever any subskill
    rating changes.

    Used to build the detailed skill progress history.
    """
    skill_assessment = models.ForeignKey(
        StudentSkillAssessment,
        on_delete=models.CASCADE,
        related_name="assessment_snapshots",
    )

    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
    )

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



class StudentSkillTermSnapshot(models.Model):
    '''
    For TERM ASSESSMENTS snapshots
    (ALL SKILLS Assessed)
    To display progress over time
    '''

    skill_assessment = models.ForeignKey(
        StudentSkillAssessment,
        on_delete=models.CASCADE,
        related_name="term_snapshots",
    )

    term_label = models.CharField(
        max_length=50,
    )

    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
    )

    recorded_at = models.DateField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            "skill_assessment",
            "term_label",
        )
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
            f"{self.term_label}: {score_display}/10"
        )
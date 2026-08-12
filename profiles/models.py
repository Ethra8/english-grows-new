from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from django_countries.fields import CountryField

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

    ROLE_CHOICES = [
        (ROLE_TEACHER, "Teacher"),
        (ROLE_INDIVIDUAL, "Student Profile"),
        (ROLE_COMPANY_ADMIN, "Company Admin"),
        (ROLE_EMPLOYEE, "Employee"),
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
        (LEVEL_UNKNOWN, "Pending"),
        (LEVEL_A1, "A1 Beginner"),
        (LEVEL_A2, "A2 Elementary"),
        (LEVEL_B1_1, "B1.1 - Pre-Intermediate"),
        (LEVEL_B1_2, "B1.2 - Lower Intermediate"),
        (LEVEL_B2_1, "B2.1 - Intermediate"),
        (LEVEL_B2_2, "B2.2 - Higher Intermediate"),
        (LEVEL_C1_1, "C1.1 - Lower Advanced"),
        (LEVEL_C1_2, "C1.2 - Higher Advanced"),
        (LEVEL_C2, "C2 Proficiency"),
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
        ("gist", "Gist (General Idea)"),
        ("specific_information", "Specific Information"),
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
    def average_percentage(self):
        subskills = self.subskill_assessments.all()

        if not subskills.exists():
            return 0

        total = sum(
            subskill.percentage
            for subskill in subskills
        )

        return round(total / subskills.count())

    @property
    def average_score(self):
        return round(self.average_percentage / 10, 1)

    def generate_teacher_notes(self):
        subskills = self.subskill_assessments.all()

        if not subskills.exists():
            return ""

        strengths = []
        meets_expectations = []
        developing = []
        needs_work = []

        for subskill in subskills:
            label = subskill.get_subskill_display()

            if subskill.rating in ["strong", "confident"]:
                strengths.append(label)

            elif subskill.rating == "pass":
                meets_expectations.append(label)

            elif subskill.rating == "developing":
                developing.append(label)

            elif subskill.rating == "needs_work":
                needs_work.append(label)

        notes = []

        if strengths:
            notes.append(
                f"Strengths: {', '.join(strengths)}."
            )

        if meets_expectations:
            notes.append(
                f"Meets expectations: {', '.join(meets_expectations)}."
            )

        if developing:
            notes.append(
                f"Developing areas: {', '.join(developing)}."
            )

        if needs_work:
            notes.append(
                f"Needs work: {', '.join(needs_work)}."
            )

        return "\n".join(notes)


class StudentSubSkillAssessment(models.Model):
    RATING_CHOICES = [
        ("needs_work", "Needs Work"),
        ("developing", "Developing"),
        ("pass", "Pass"),
        ("confident", "Confident"),
        ("strong", "Strong"),
    ]

    RATING_PERCENTAGES = {
        "needs_work": 40,
        "developing": 50,
        "pass": 60,
        "confident": 75,
        "strong": 100,
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

    percentage = models.PositiveSmallIntegerField(
        default=50,
        editable=False,
    )

    rating = models.CharField(
        max_length=20,
        choices=RATING_CHOICES,
        default="developing",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("skill_assessment", "subskill")
        ordering = ["subskill"]

    def save(self, *args, **kwargs):
        self.percentage = self.RATING_PERCENTAGES.get(
            self.rating,
            45,
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.skill_assessment.get_skill_display()} → "
            f"{self.get_subskill_display()}"
        )



# Creates a Snapshot every time teacher assesses SKILLS
# To then read snapshots in time to create 
# visual STUDENT PROGRESS GRAPH
class StudentSkillTermSnapshot(models.Model):
    skill_assessment = models.ForeignKey(
        StudentSkillAssessment,
        on_delete=models.CASCADE,
        related_name="term_snapshots",
    )

    term_label = models.CharField(max_length=50)  # e.g. "Term 1", "Jun 2026"
    percentage = models.PositiveSmallIntegerField()
    recorded_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("skill_assessment", "term_label")
        ordering = ["recorded_at"]

    def __str__(self):
        return (
            f"{self.skill_assessment.student.get_full_name()} · "
            f"{self.skill_assessment.get_skill_display()} · "
            f"{self.term_label}: {self.percentage}%"
        )
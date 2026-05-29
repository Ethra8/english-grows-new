from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


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
    ROLE_INDIVIDUAL = "individual"
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
        (LEVEL_B1_1, "B1.1 Pre-Intermediate"),
        (LEVEL_B1_2, "B1.2 Low Intermediate"),
        (LEVEL_B2_1, "B2.1 Intermediate"),
        (LEVEL_B2_2, "B2.2 High Intermediate"),
        (LEVEL_C1_1, "C1.1 Low Advance"),
        (LEVEL_C1_2, "C1.2 High Advance"),
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
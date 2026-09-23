import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class EmailTemplate(models.Model):
    """
    Stores reusable email types and their editable content.

    Each record represents one type of application email. Its unique `key`
    is automatically generated from the name when the template is first
    created and then remains stable because application logic may refer
    to it directly.

    Business logic decides WHEN an email must be sent and requests the
    appropriate template by its key.

    The name, subject and body remain database-driven so they can be edited
    through Django Admin without changing application code.
    """

    # Stable application identifier. It is generated automatically from
    # `name` when the template is first created and should not change later,
    # even if the human-readable name is edited.
    key = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        help_text="Generated automatically from the template name.",
    )

    name = models.CharField(max_length=150)
    subject = models.CharField(max_length=255)

    body_html = CKEditor5Field(
        "Email content",
        config_name="email",
    )

    heading = models.CharField(
        max_length=255,
        blank=True,
        help_text="Heading displayed inside the email.",
    )

    body_text = models.TextField(
        blank=True,
        help_text="Optional plain-text version of the email.",
    )

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        # Generate the key only once. Existing keys remain unchanged because
        # application code may already use them to identify this email type.
        if not self.key:
            base_key = slugify(self.name).replace("-", "_")
            key = base_key
            counter = 2

            while EmailTemplate.objects.filter(key=key).exclude(pk=self.pk).exists():
                key = f"{base_key}_{counter}"
                counter += 1

            self.key = key

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MarketingSubscriber(models.Model):
    """
    Manages optional marketing subscriptions independently of learner
    accounts and placement attempts.

    Explicit marketing consent activates the subscription immediately.
    Only active subscribers with recorded consent may receive marketing emails.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending confirmation"
        ACTIVE = "active", "Active"
        UNSUBSCRIBED = "unsubscribed", "Unsubscribed"

    class Source(models.TextChoices):
        PLACEMENT_TEST = "placement_test", "Placement test"
        WEBSITE = "website", "Website subscription"
        ACCOUNT = "account", "Account preferences"

    email = models.EmailField(unique=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="marketing_subscriptions",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    source = models.CharField(
        max_length=30,
        choices=Source.choices,
        default=Source.PLACEMENT_TEST,
    )

    consent_text = models.TextField(
        blank=True,
        help_text="Exact marketing consent wording presented to the subscriber.",
    )

    requested_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    last_unsubscribed_at = models.DateTimeField(null=True, blank=True)

    confirmation_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["email"]
        verbose_name = "Marketing subscriber"
        verbose_name_plural = "Marketing subscribers"

    def save(self, *args, **kwargs):
        self.email = self.email.strip().casefold()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} · {self.get_status_display()}"

    @property
    def can_receive_marketing(self):
        return self.status == self.Status.ACTIVE and self.confirmed_at is not None

    @classmethod
    def subscribe(cls, *, email, source, consent_text, user=None):
        """Activate a marketing subscription after explicit opt-in."""
        email = (email or "").strip().casefold()
        consent_text = (consent_text or "").strip()

        if not email or not consent_text:
            raise ValueError("An email address and consent wording are required.")

        now = timezone.now()

        with transaction.atomic():
            subscriber, _ = cls.objects.select_for_update().get_or_create(email=email)

            # An existing active subscription needs no further action.
            if subscriber.can_receive_marketing:
                return subscriber

            # Invalidate the previous unsubscribe link when subscribing again.
            if subscriber.status == cls.Status.UNSUBSCRIBED:
                subscriber.unsubscribe_token = uuid.uuid4()

            subscriber.status = cls.Status.ACTIVE
            subscriber.source = source
            subscriber.consent_text = consent_text
            subscriber.requested_at = now
            subscriber.confirmed_at = now

            if user is not None and user.is_authenticated and (user.email or "").strip().casefold() == email:
                subscriber.user = user

            subscriber.save()

        return subscriber

    def unsubscribe(self):
        """Withdraws the subscription without deleting its consent evidence."""
        if self.status == self.Status.UNSUBSCRIBED:
            return False

        self.status = self.Status.UNSUBSCRIBED
        self.last_unsubscribed_at = timezone.now()
        self.confirmation_token = uuid.uuid4()
        self.save(update_fields=["status", "last_unsubscribed_at", "confirmation_token", "updated_at"])
        return True
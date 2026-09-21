from django.db import models

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
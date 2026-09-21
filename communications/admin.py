from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import EmailTemplate


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "key", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "key", "subject")
    readonly_fields = ("key", "updated_at")

    fieldsets = (
        (
            "Email template",
            {
                "fields": (
                    "name",
                    "key",
                    "is_active",
                    "subject",
                    "heading",
                    "body_html",
                    "body_text",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("updated_at",),
                "classes": ("collapse",),
            },
        ),
    )
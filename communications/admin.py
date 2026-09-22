from django.contrib import admin

from .models import EmailTemplate, MarketingSubscriber


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


@admin.register(MarketingSubscriber)
class MarketingSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "status", "source", "requested_at", "confirmed_at", "last_unsubscribed_at")
    list_filter = ("status", "source")
    search_fields = ("email", "user__email", "user__first_name", "user__last_name")
    ordering = ("-created_at",)
    list_per_page = 50

    readonly_fields = (
        "email",
        "user",
        "status",
        "source",
        "consent_text",
        "requested_at",
        "confirmed_at",
        "last_unsubscribed_at",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Subscriber",
            {
                "fields": ("email", "user", "status", "source"),
            },
        ),
        (
            "Consent and subscription history",
            {
                "fields": (
                    "consent_text",
                    "requested_at",
                    "confirmed_at",
                    "last_unsubscribed_at",
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def has_add_permission(self, request):
        return False
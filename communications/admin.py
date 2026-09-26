
from django.contrib import admin

from .models import EmailTemplate, MarketingSubscriber, LearnerAccountClosureNotice


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



@admin.register(LearnerAccountClosureNotice)
class LearnerAccountClosureNoticeAdmin(admin.ModelAdmin):
    list_display = (
        "recipient_email",
        "user",
        "status",
        "potential_expiry_at",
        "effective_closure_at",
        "sent_at",
        "created_at",
    )
    list_display_links = ("recipient_email",)
    list_filter = ("status", "created_at", "potential_expiry_at")
    search_fields = (
        "recipient_email",
        "user__email",
        "user__username",
        "user__first_name",
        "user__last_name",
    )
    ordering = ("-created_at",)
    list_select_related = ("user",)
    list_per_page = 50

    readonly_fields = (
        "user",
        "recipient_email",
        "status",
        "reference_at",
        "potential_expiry_at",
        "effective_closure_at",
        "created_at",
        "sent_at",
    )

    fieldsets = (
        (
            "Learner and notification status",
            {
                "fields": (
                    "user",
                    "recipient_email",
                    "status",
                ),
            },
        ),
        (
            "Retention and closure dates",
            {
                "fields": (
                    "reference_at",
                    "potential_expiry_at",
                    "effective_closure_at",
                ),
            },
        ),
        (
            "Notification history",
            {
                "fields": (
                    "created_at",
                    "sent_at",
                ),
            },
        ),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

from django.contrib import admin
from .models import PlacementAttempt, PlacementQuestion


@admin.register(PlacementQuestion)
class PlacementQuestionAdmin(admin.ModelAdmin):
    list_display = ("number", "language_point", "area", "target_level", "version", "is_active")
    list_filter = ("version", "area", "target_level", "is_active")
    search_fields = ("text", "language_point")
    ordering = ("version", "number")


@admin.register(PlacementAttempt)
class PlacementAttemptAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "score", "recommended_level", "cefr_reference", "completed_at")
    list_filter = ("recommended_level", "cefr_reference", "test_version", "completed_at")
    search_fields = ("name", "email")
    readonly_fields = ("user", "name", "email", "test_version", "answers", "answer_snapshot", "score",
                       "recommended_level", "cefr_reference", "created_at", "completed_at")

    def has_add_permission(self, request):
        return False

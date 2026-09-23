from urllib.parse import urlencode

from django import forms
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseNotAllowed
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html, format_html_join

from .models import PlacementAttempt, PlacementQuestion, TOTAL_QUESTIONS


def version_is_locked(version):
    return PlacementAttempt.objects.filter(
        test_version=version,
        completed_at__isnull=False,
    ).exists()


class PlacementQuestionAdminForm(forms.ModelForm):
    class Meta:
        model = PlacementQuestion
        fields = "__all__"

    def clean_version(self):
        version = self.cleaned_data["version"]
        original_version = None

        if self.instance.pk:
            original_version = PlacementQuestion.objects.filter(
                pk=self.instance.pk
            ).values_list("version", flat=True).first()

        if version != original_version and version_is_locked(version):
            raise forms.ValidationError(
                f"Version V{version} already has completed assessments. "
                "Create a new test version instead."
            )

        return version


@admin.register(PlacementQuestion)
class PlacementQuestionAdmin(admin.ModelAdmin):
    form = PlacementQuestionAdminForm
    list_display = ("number", "language_point", "area", "target_level", "version", "is_active")
    list_filter = ("version", "area", "target_level", "is_active")
    search_fields = ("text", "language_point")
    ordering = ("version", "number")
    readonly_fields = ("version_protection",)
    change_list_template = "admin/placement/placementquestion/change_list.html"

    @admin.display(description="Version protection")
    def version_protection(self, obj):
        if not obj or not obj.pk:
            return "New questions cannot be added to a version with completed assessments."

        if version_is_locked(obj.version):
            return "Locked — this version has completed assessments. Create a new version for revisions."

        return "Editable — no completed assessments exist for this version."

    def has_change_permission(self, request, obj=None):
        if not super().has_change_permission(request, obj):
            return False
        return not (obj and version_is_locked(obj.version))

    def has_delete_permission(self, request, obj=None):
        if not super().has_delete_permission(request, obj):
            return False
        return not (obj and version_is_locked(obj.version))

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def get_urls(self):
        custom_urls = [
            path(
                "preview/<str:version>/",
                self.admin_site.admin_view(self.preview_view),
                name="placement_placementquestion_preview",
            ),
        ]
        return custom_urls + super().get_urls()

    def changelist_view(self, request, extra_context=None):
        versions = self.get_queryset(request).order_by("version").values_list("version", flat=True).distinct()
        preview_versions = [
            {
                "version": version,
                "url": reverse("admin:placement_placementquestion_preview", args=[version]),
            }
            for version in versions
        ]

        extra_context = {**(extra_context or {}), "preview_versions": preview_versions}
        return super().changelist_view(request, extra_context=extra_context)

    def preview_view(self, request, version):
        if request.method != "GET":
            return HttpResponseNotAllowed(["GET"])

        if not self.has_view_permission(request):
            raise PermissionDenied

        queryset = self.get_queryset(request).filter(version=version)

        if not queryset.exists():
            raise Http404("Placement test version not found.")

        questions = list(queryset.filter(is_active=True).order_by("number"))

        bank_complete = (
            [question.number for question in questions] == list(range(1, TOTAL_QUESTIONS + 1))
            and all(
                all((question.option_a, question.option_b, question.option_c, question.option_d))
                for question in questions
            )
        )

        rows = [
            {
                "number": question.number,
                "text": question.text,
                "options": (
                    ("A", question.option_a),
                    ("B", question.option_b),
                    ("C", question.option_c),
                    ("D", question.option_d),
                ),
            }
            for question in questions
        ]

        context = {
            **self.admin_site.each_context(request),
            "title": f"Placement Test V{version} — Preview",
            "opts": self.model._meta,
            "version": version,
            "pages": [rows[i:i + 10] for i in range(0, len(rows), 10)],
            "question_count": len(rows),
            "expected_count": TOTAL_QUESTIONS,
            "bank_complete": bank_complete,
            "question_bank_url": (
                f"{reverse('admin:placement_placementquestion_changelist')}?"
                f"{urlencode({'version__exact': version})}"
            ),
        }

        return TemplateResponse(request, "admin/placement/placementquestion/preview.html", context)


@admin.register(PlacementAttempt)
class PlacementAttemptAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "score", "recommended_level", "cefr_reference", "completed_at")
    list_filter = ("recommended_level", "cefr_reference", "test_version", "completed_at")
    search_fields = ("name", "email")

    readonly_fields = (
        "user", "name", "email", "test_version", "test_version_link", "preview_test_link",
        "score", "recommended_level", "cefr_reference",
        "created_at", "completed_at", "answer_review",
    )

    fieldsets = (
        ("Learner", {
            "fields": ("user", "name", "email"),
        }),
        ("Assessment", {
            "fields": ("test_version_link", "preview_test_link", "created_at", "completed_at"),
        }),
        ("Placement result", {
            "fields": ("score", "recommended_level", "cefr_reference"),
        }),
        ("Answer review", {
            "fields": ("answer_review",),
        }),
    )

    class Media:
        css = {"all": ("placement/css/placement_admin.css",)}

    def has_add_permission(self, request):
        return False

    @admin.display(description="Test version")
    def test_version_link(self, obj):
        if not obj.pk:
            return "—"

        url = reverse("admin:placement_placementquestion_changelist")
        query = urlencode({"version__exact": obj.test_version})

        return format_html(
            '<a href="{}?{}">V{} — View question bank →</a>',
            url, query, obj.test_version
        )

    @admin.display(description="Test preview")
    def preview_test_link(self, obj):
        if not obj.pk:
            return "—"

        url = reverse("admin:placement_placementquestion_preview", args=[obj.test_version])
        return format_html('<a href="{}">Preview complete V{} assessment →</a>', url, obj.test_version)

    @staticmethod
    def _render_answer(number, data):
        options = data.get("options") or {}
        selected = data.get("selected")
        correct = data.get("correct_answer")
        is_correct = data.get("is_correct", False)

        if not selected:
            status, status_label = "unanswered", "Unanswered"
            selected_label = "Not answered"
        elif is_correct:
            status, status_label = "correct", "Correct"
            selected_label = f"{selected} — {options.get(selected, 'Option unavailable')}"
        else:
            status, status_label = "incorrect", "Incorrect"
            selected_label = f"{selected} — {options.get(selected, 'Option unavailable')}"

        correct_label = f"{correct} — {options.get(correct, 'Option unavailable')}"

        return format_html(
            '<details id="placement-answer-{}" class="placement-review__item placement-review__item--{}"{}>'
                '<summary>'
                    '<span class="placement-review__number">Q{}</span>'
                    '<span class="placement-review__level">{}</span>'
                    '<span class="placement-review__status">{}</span>'
                '</summary>'
                '<div class="placement-review__body">'
                    '<p class="placement-review__text">{}</p>'
                    '<p><strong>Learner’s answer:</strong> {}</p>'
                    '<p><strong>Correct answer:</strong> {}</p>'
                    '<p><strong>Language point:</strong> {}</p>'
                '</div>'
            '</details>',
            number, status, " open" if status != "correct" else "",
            number, data.get("target_level") or "—", status_label,
            data.get("text") or "Question unavailable",
            selected_label, correct_label, data.get("language_point") or "—",
        )

    @admin.display(description="Question-by-question review")
    def answer_review(self, obj):
        snapshot = obj.answer_snapshot

        if not isinstance(snapshot, dict) or not snapshot:
            return "No graded answers available."

        questions = sorted(
            (
                (int(number), data)
                for number, data in snapshot.items()
                if str(number).isdigit() and isinstance(data, dict)
            ),
            key=lambda item: item[0],
        )

        correct = sum(bool(data.get("is_correct")) for _, data in questions)
        unanswered = sum(not data.get("selected") for _, data in questions)
        incorrect = len(questions) - correct - unanswered
        mistakes = [number for number, data in questions if not data.get("is_correct")]

        mistake_links = (
            format_html_join(
                " · ",
                '<a href="#placement-answer-{}">Q{}</a>',
                ((number, number) for number in mistakes),
            )
            if mistakes else "No incorrect or unanswered responses."
        )

        answers = format_html_join(
            "",
            "{}",
            ((self._render_answer(number, data),) for number, data in questions),
        )

        return format_html(
            '<div class="placement-review">'
                '<div class="placement-review__summary">'
                    '<strong>{} correct</strong>'
                    '<span>{} incorrect</span>'
                    '<span>{} unanswered</span>'
                '</div>'
                '<p class="placement-review__mistakes"><strong>Review mistakes:</strong> {}</p>'
                '<div class="placement-review__questions">{}</div>'
            '</div>',
            correct, incorrect, unanswered, mistake_links, answers,
        )
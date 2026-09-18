from django import forms
from django.db.models import Q

from ..models import (
    StudentAcademicProfile,
    LearningGoal,
)


class StudentAcademicProfileForm(forms.ModelForm):
    class Meta:
        model = StudentAcademicProfile
        fields = [
            "learning_goals",
            "next_review_date",
        ]

        widgets = {
            "learning_goals": forms.CheckboxSelectMultiple,
            "next_review_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        selected_goals = self.instance.learning_goals.values_list(
            "pk",
            flat=True,
        ) if self.instance.pk else []

        self.fields["learning_goals"].queryset = (
            LearningGoal.objects
            .filter(
                Q(is_active=True) |
                Q(pk__in=selected_goals)
            )
            .distinct()
        )

from django import forms
from django.db.models import Q

from ..models import (
    StudentAcademicProfile,
)


class StudentAcademicProfileForm(forms.ModelForm):
    class Meta:
        model = StudentAcademicProfile
        fields = [
            "next_review_date",
        ]

        widgets = {
            "next_review_date": forms.DateInput(attrs={"type": "date"}),
        }

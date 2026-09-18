from django import forms
from django.forms import inlineformset_factory

from ..models import (
    StudentSkillAssessment,
    StudentSubSkillAssessment,
)

# ---------------------------------------------------------
# SKILL ASSESSMENT
# ---------------------------------------------------------
class StudentSkillAssessmentForm(forms.ModelForm):
    class Meta:
        model = StudentSkillAssessment
        fields = [
            "teacher_notes",
        ]

        widgets = {
            "teacher_notes": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
        }


# ---------------------------------------------------------
# SUBSKILL ASSESSMENT
#
# A blank rating means:
# "Not assessed yet"
#
# This is important because unrated subskills must:
# - have no score
# - be excluded from average_score
# - create no historical snapshot
# ---------------------------------------------------------
class StudentSubSkillAssessmentInlineForm(forms.ModelForm):

    class Meta:
        model = StudentSubSkillAssessment
        fields = [
            "rating",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The model already allows blank / NULL ratings.
        # Explicitly keep the form field optional as well.
        self.fields["rating"].required = False

        # Give the empty option a meaningful label instead
        # of Django's default "---------".
        self.fields["rating"].empty_label = "Not assessed yet"


# ---------------------------------------------------------
# INLINE FORMSET
#
# Only existing predefined subskills are displayed.
#
# extra=0:
#     Do not create blank/new subskill forms.
#
# can_delete=False:
#     Teachers cannot remove predefined subskills.
# ---------------------------------------------------------
StudentSubSkillAssessmentFormSet = inlineformset_factory(
    StudentSkillAssessment,
    StudentSubSkillAssessment,
    form=StudentSubSkillAssessmentInlineForm,
    extra=0,
    can_delete=False,
)
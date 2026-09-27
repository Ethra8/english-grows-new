from django import forms
from django.forms import inlineformset_factory

from ..models import StudentSkillAssessment, StudentSubSkillAssessment


# ---------------------------------------------------------
# INDIVIDUAL SUBSKILL RATING FORM
#
# StudentSubSkillAssessmentInlineForm represents ONE
# subskill rating within a larger skill assessment.
#
# Example:
# Speaking (parent skill assessment)
#     - Fluency       -> one form
#     - Pronunciation -> one form
#     - Interaction   -> one form
#
# Each form:
# - Displays the rating field for one existing subskill.
# - Allows the teacher to select a rating.
# - Allows the rating to remain blank ("Not assessed yet").
#
# It does NOT:
# - Represent the complete Speaking/Reading/etc. assessment.
# - Generate written feedback.
# - Create assessment history directly.
#
# The formset defined below groups these individual forms.
# ---------------------------------------------------------
class StudentSubSkillAssessmentInlineForm(forms.ModelForm):

    class Meta:
        model = StudentSubSkillAssessment
        fields = ["rating"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # A subskill does not need to be assessed immediately.
        # Blank ratings are permitted and excluded from the
        # parent skill's calculated average.
        self.fields["rating"].required = False

        # Replace Django's default empty dropdown label
        # ("---------") with a meaningful description.
        self.fields["rating"].empty_label = "Not assessed yet"


# ---------------------------------------------------------
# COMPLETE SKILL ASSESSMENT FORMSET
#
# StudentSubSkillAssessmentFormSet groups the individual
# subskill forms belonging to ONE StudentSkillAssessment.
#
# Example:
# Parent: Speaking assessment for a particular learner/course
#
# Formset:
#     Fluency       -> rating dropdown
#     Pronunciation -> rating dropdown
#     Interaction   -> rating dropdown
#     ...           -> rating dropdown
#
# Django uses the relationship between:
#
#     StudentSkillAssessment (parent)
#     StudentSubSkillAssessment (children)
#
# to retrieve and save the corresponding subskill records.
#
# Configuration:
#
# form:
#     Use the individual subskill rating form defined above.
#
# extra=0:
#     Do not display additional empty forms for creating
#     new subskill records.
#
# can_delete=False:
#     Teachers cannot delete predefined subskill records
#     through this formset.
#
# IMPORTANT:
# The formset saves the individual subskill ratings.
# The teacher assessment view is responsible for generating
# the written feedback after the ratings have been saved.
#
# Historical snapshot creation will be moved into the
# explicit assessment submission workflow separately.
# ---------------------------------------------------------
StudentSubSkillAssessmentFormSet = inlineformset_factory(
    StudentSkillAssessment,
    StudentSubSkillAssessment,
    form=StudentSubSkillAssessmentInlineForm,
    extra=0,
    can_delete=False,
)
from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper

from .models import UserProfile, TeacherProfile, StudentAcademicProfile, LearningGoal, StudentSkillAssessment, StudentSubSkillAssessment

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=False,
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
    )

    email = forms.EmailField(
        required=True,
    )

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'native_language',
            'country',
            'profile_photo',
        ]


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)
        self.fields['profile_photo'].label = "Update your profile picture"

        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

        self.helper = FormHelper()
        self.helper.form_method = 'POST'

        placeholders = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email address',
            'native_language': 'Native Language',
            'country': 'Country',
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            if field_name == 'country':
                field.widget.attrs.update({
                    'aria-label': 'Country selection',
                    'class': 'border-black rounded-0 profile-form-input',
                })
            
            elif field_name == 'profile_photo':
                field.widget.attrs.update({
                    'class': 'border-black rounded-0 profile-form-input',
                })

    
            else:
                field.widget.attrs.update({
                    'placeholder': placeholders[field_name],
                    'class': 'border-black rounded-0 profile-form-input',
                })

            if field_name != 'profile_photo':
                field.label = False

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.user:
            self.user.first_name = self.cleaned_data.get('first_name')
            self.user.last_name = self.cleaned_data.get('last_name')
            self.user.email = self.cleaned_data.get('email')

            if commit:
                self.user.save()
                profile.save()

        elif commit:
            profile.save()

        return profile


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = [
            "bio",
            "specialties",
        ]


class StudentAcademicProfileForm(forms.ModelForm):
    strengths = forms.MultipleChoiceField(
        choices=StudentAcademicProfile.SKILL_AREA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    weaknesses = forms.MultipleChoiceField(
        choices=StudentAcademicProfile.SKILL_AREA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = StudentAcademicProfile
        fields = [
            "current_level",
            "target_level",
            "learning_goals",
            "strengths",
            "weaknesses",
            "teacher_notes",
            "participation",
            "risk_status",
            "next_review_date",
        ]

        widgets = {
            "learning_goals": forms.CheckboxSelectMultiple,
            "next_review_date": forms.DateInput(attrs={"type": "date"}),
            "teacher_notes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["learning_goals"].queryset = LearningGoal.objects.filter(
            is_active=True
        )



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


class StudentSubSkillAssessmentInlineForm(forms.ModelForm):
    class Meta:
        model = StudentSubSkillAssessment
        fields = [
            "rating",
        ]


StudentSubSkillAssessmentFormSet = inlineformset_factory(
    StudentSkillAssessment,
    StudentSubSkillAssessment,
    form=StudentSubSkillAssessmentInlineForm,
    extra=0,
    can_delete=False,
)
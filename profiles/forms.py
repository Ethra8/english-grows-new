from django import forms
from crispy_forms.helper import FormHelper

from .models import UserProfile


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
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

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
            else:
                field.widget.attrs.update({
                    'placeholder': placeholders[field_name],
                    'class': 'border-black rounded-0 profile-form-input',
                })

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
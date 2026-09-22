from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML

from ..models import (
    UserProfile,
    TeacherProfile,
)


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
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "native_language",
            "country",
            "profile_photo",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        self.fields["profile_photo"].label = False

        if self.user:
            self.fields["first_name"].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
            self.fields["email"].initial = self.user.email

        placeholders = {
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email address",
            "native_language": "Native Language",
            "country": "Country",
        }

        self.fields["first_name"].widget.attrs["autofocus"] = True

        for field_name, field in self.fields.items():
            if field_name == "country":
                field.widget.attrs.update({
                    "aria-label": "Country selection",
                    "class": "border-black rounded-0 profile-form-input",
                })

            elif field_name == "profile_photo":
                field.widget.attrs.update({
                    "class": "border-black rounded-0 profile-form-input",
                })
            elif field_name == "profile_photo":
                field.widget.attrs.update({
                    "class": "border-black rounded-0 profile-form-input",
                    "aria-label": "Profile picture",
                })
            else:
                field.widget.attrs.update({
                    "placeholder": placeholders[field_name],
                    "class": "border-black rounded-0 profile-form-input",
                })

        self.fields["email"].widget.attrs.update({
            "readonly": True,
            "aria-readonly": "true",
        })

        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                HTML('<h2 class="account-settings-section-title">Account email</h2>'),
                HTML(
                    """
                    <p class="profile-email-info">
                        Your email address is used to sign in. For your security, any change requires verification of your new email address before it can be used.
                    </p>
                    """
                ),
                Field("email"),
                HTML(
                    """
                    <div class="profile-email-actions">
                        <a href="{% url 'account_email' %}"
                        class="btn btn-update text-uppercase">
                            Change email
                            <span aria-hidden="true" class="ml-2">&rarr;</span>
                        </a>
                    </div>
                    """
                ),
                css_class="profile-email-field",
            ),

            Div(
                HTML('<h2 class="account-settings-section-title">Personal information</h2>'),
                Field("first_name"),
                Field("last_name"),
                Field("native_language"),
                Field("country"),
                css_class="profile-personal-section",
            ),

            HTML('<h2 class="account-settings-section-title">Profile picture</h2>'),
            Field("profile_photo"),
        )

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.user:
            self.user.first_name = self.cleaned_data.get("first_name")
            self.user.last_name = self.cleaned_data.get("last_name")

            if commit:
                self.user.save(update_fields=["first_name", "last_name"])
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
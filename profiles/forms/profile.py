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

        self.fields["profile_photo"].label = "Profile picture"

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

            else:
                field.widget.attrs.update({
                    "placeholder": placeholders[field_name],
                    "class": "border-black rounded-0 profile-form-input",
                })

            if field_name != "profile_photo":
                field.label = False

        self.fields["email"].widget.attrs.update({
            "readonly": True,
            "aria-readonly": "true",
        })

        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                HTML(
                    """
                    <p class="profile-email-info">
                        <strong>Your account is linked to the email address below</strong>, which is used
                        for authentication and login. To change it, you will need to verify
                        your new email address using the verification email we send you.
                    </p>
                    """
                ),
                Field("email"),
                HTML(
                    """
                    <div class="profile-email-actions">
                        <a href="{% url 'account_email' %}"
                           class="btn btn-update text-uppercase">
                            Edit email
                            <span aria-hidden="true" class="ml-2">&rarr;</span>
                        </a>
                    </div>
                    """
                ),
                css_class="profile-email-field",
            ),

            Field("first_name"),
            Field("last_name"),
            Field("native_language"),
            Field("country"),
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
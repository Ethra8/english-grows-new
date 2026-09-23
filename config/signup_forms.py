from urllib.parse import urlsplit

from allauth.account.forms import SignupForm
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .turnstile import verify_turnstile


class TurnstileSignupForm(SignupForm):
    """Preserve allauth signup while requiring Turnstile verification."""

    @property
    def turnstile_sitekey(self):
        return settings.TURNSTILE_SITEKEY

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        token = self.data.get("cf-turnstile-response", "")

        # Cloudflare's dummy tokens return action="test", not "signup".
        is_test_key = settings.TURNSTILE_SITEKEY == "1x00000000000000000000AA"

        if not verify_turnstile(
            token,
            expected_hostname=None if is_test_key else urlsplit(settings.SITE_URL).hostname,
            expected_action=None if is_test_key else "signup",
        ):
            raise forms.ValidationError(
                _("Security verification failed. Please try again.")
            )

        return cleaned_data
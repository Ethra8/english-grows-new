from django import forms
from django.utils.translation import gettext_lazy as _


class PlacementTestForm(forms.Form):
    name = forms.CharField(
        label=_("Full name"),
        max_length=150,
        required=False,
        strip=True,
    )

    email = forms.EmailField(
        label=_("Email address"),
        max_length=254,
    )

    acknowledge = forms.BooleanField(
        label=_("I have read the Privacy Policy and understand how my placement information will be processed."),
    )

    marketing_opt_in = forms.BooleanField(
        label=_("I would also like to receive news, course information and special offers from English Grows by email. I can unsubscribe at any time."),
        required=False,
        initial=False,
    )

    token = forms.CharField(widget=forms.HiddenInput)
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, questions, **kwargs):
        super().__init__(*args, **kwargs)

        for q in questions:
            self.fields[f"q_{q.number}"] = forms.ChoiceField(
                required=False,
                label=q.text,
                choices=(
                    ("A", q.option_a),
                    ("B", q.option_b),
                    ("C", q.option_c),
                    ("D", q.option_d),
                ),
                widget=forms.RadioSelect,
            )

    def clean(self):
        data = super().clean()

        if data.get("website"):
            raise forms.ValidationError(
                _("Unable to process this submission. Please try again.")
            )

        return data
from django import forms
from django.utils.translation import gettext_lazy as _


# ---------------------------------------------------------
# ENGLISH USE FREQUENCY
# ---------------------------------------------------------
FREQUENCY_CHOICES = [
    ("daily", _("Every day")),
    ("several_week", _("Several times a week")),
    ("occasionally", _("Occasionally")),
    ("rarely", _("Rarely or never")),
]

# ---------------------------------------------------------
# COMMUNICATION SITUATIONS
# ---------------------------------------------------------
SITUATION_CHOICES = [
    ("meetings_calls", _("Meetings and video calls")),
    ("phone_calls", _("Phone calls")),
    ("presentations", _("Presentations")),
    ("written_communication", _("Emails, reports and documents")),
    ("customer_communication", _("Customer communication")),
    ("networking", _("Networking")),
    ("other", _("Other")),
]

# ---------------------------------------------------------
# COMMUNICATION PARTNERS
# ---------------------------------------------------------
COMMUNICATION_PARTNER_CHOICES = [
    ("internal", _("Colleagues and internal teams")),
    ("managers", _("Managers")),
    ("customers", _("Customers")),
    ("external", _("External partners")),
    ("other", _("Other")),
]

# ---------------------------------------------------------
# ACCENT / ENGLISH VARIETY EXPOSURE
# ---------------------------------------------------------
ACCENT_EXPOSURE_CHOICES = [
    ("england", _("English accents from England")),
    ("scottish", _("Scottish English")),
    ("irish", _("Irish English")),
    ("american", _("American English")),
    ("indian", _("Indian English")),
    ("international", _("International / non-native English accents")),
    ("other", _("Other")),
]
# ---------------------------------------------------------
# CONFIDENCE
#
# Confidence itself is stored as an integer from 1–5.
# These labels are used for display/read-only purposes.
# ---------------------------------------------------------
CONFIDENCE_LABELS = {
    1: _("Not confident yet"),
    2: _("Slightly confident"),
    3: _("Fairly confident"),
    4: _("Confident"),
    5: _("Very confident"),
}

# ---------------------------------------------------------
# LEARNING PREFERENCES
# ---------------------------------------------------------
LEARNING_PREFERENCE_CHOICES = [
    ("conversation", _("Conversation and discussion")),
    ("role_plays", _("Role plays and real-life situations")),
    ("structured_exercises", _("Structured exercises")),
    ("grammar", _("Grammar practice")),
    ("vocabulary", _("Vocabulary practice")),
    ("listening", _("Listening activities")),
    ("reading", _("Reading activities")),
    ("writing", _("Writing activities")),
    ("real_materials", _("Real-world materials")),
    ("projects", _("Projects and practical tasks")),
]


# ---------------------------------------------------------
# STUDENT NEEDS ANALYSIS FORM
# ---------------------------------------------------------
class StudentNeedsAnalysisForm(forms.Form):

    # -----------------------------------------------------
    # 1. YOUR ENGLISH
    # -----------------------------------------------------
    english_use_frequency = forms.ChoiceField(
        label=_("How often do you currently use English outside your lessons?"),
        choices=FREQUENCY_CHOICES,
        widget=forms.RadioSelect,
    )

    communication_situations = forms.MultipleChoiceField(
        label=_("In which situations do you use, or expect to use, English?"),
        choices=SITUATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )


    # -----------------------------------------------------
    # 2. YOUR COMMUNICATION
    # -----------------------------------------------------
    communication_partners = forms.MultipleChoiceField(
        label=_("Who do you mainly communicate with in English?"),
        help_text=_("Select all that apply."),
        choices=COMMUNICATION_PARTNER_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    accent_exposure = forms.MultipleChoiceField(
        label=_("Which English accents or varieties do you regularly hear?"),
        help_text=_("Select all that apply."),
        choices=ACCENT_EXPOSURE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    accent_exposure_other = forms.CharField(
        label=_("Please specify"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("For example: Australian, South African, Welsh, Texan ..."),
            }
        ),
        required=False,
    )

    # -----------------------------------------------------
    # 3. CONFIDENCE
    #
    # Discrete 1–5 range sliders.
    # -----------------------------------------------------
    speaking_confidence = forms.IntegerField(
        label=_("How confident do you currently feel speaking English?"),
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "min": 1,
                "max": 5,
                "step": 1,
                "class": "confidence-range",
            }
        ),
    )

    listening_confidence = forms.IntegerField(
        label=_("How confident do you currently feel understanding spoken English?"),
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "min": 1,
                "max": 5,
                "step": 1,
                "class": "confidence-range",
            }
        ),
    )

    reading_confidence = forms.IntegerField(
        label=_("How confident do you currently feel reading English?"),
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "min": 1,
                "max": 5,
                "step": 1,
                "class": "confidence-range",
            }
        ),
    )

    writing_confidence = forms.IntegerField(
        label=_("How confident do you currently feel writing English?"),
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "min": 1,
                "max": 5,
                "step": 1,
                "class": "confidence-range",
            }
        ),
    )


    # -----------------------------------------------------
    # 4. YOUR PRIORITIES
    # -----------------------------------------------------
    priority_areas = forms.MultipleChoiceField(
        label=_("Which communication situations would you most like to focus on during this course?"),
        help_text=_("Choose up to three."),
        choices=SITUATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    # -----------------------------------------------------
    # 5. ADDITIONAL INFORMATION
    # -----------------------------------------------------
    additional_information = forms.CharField(
        label=_("Is there anything else you would like your teacher to know?"),
        widget=forms.Textarea(attrs={"rows": 2}),
        required=False,
    )

    # -----------------------------------------------------
    # DISPLAY HELPERS
    # -----------------------------------------------------
    def choice_labels(self, field_name, values, exclude_values=None):
        if not values:
            return []

        if not isinstance(values, (list, tuple, set)):
            values = [values]

        choices = dict(self.fields[field_name].choices)
        exclude_values = set(exclude_values or [])

        return [
            str(choices.get(value, value))
            for value in values
            if value not in exclude_values
        ]


    def confidence_display(self, value):
        if value is None:
            return ""

        return f"{value} / 5 — {CONFIDENCE_LABELS.get(value, value)}"


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------
    def clean_priority_areas(self):
        priorities = self.cleaned_data["priority_areas"]

        if len(priorities) > 3:
            raise forms.ValidationError(
                _("Please choose no more than three priorities.")
            )

        return priorities


    def clean(self):
        cleaned_data = super().clean()

        accent_exposure = cleaned_data.get("accent_exposure", [])
        accent_exposure_other = cleaned_data.get(
            "accent_exposure_other",
            "",
        ).strip()

        if "other" in accent_exposure:
            if not accent_exposure_other:
                self.add_error(
                    "accent_exposure_other",
                    _("Please specify the other accent or variety of English."),
                )
        else:
            cleaned_data["accent_exposure_other"] = ""

        return cleaned_data
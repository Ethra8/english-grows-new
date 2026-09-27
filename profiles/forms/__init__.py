# Expose forms and formsets from their individual modules.
# Other modules can import them directly from profiles.forms
# without needing to know their individual file locations.

from .profile import UserProfileForm, TeacherProfileForm
from .academic_profile import StudentAcademicProfileForm
from .skill_assessment import (
    StudentSubSkillAssessmentInlineForm,
    StudentSubSkillAssessmentFormSet,
)
from .student_needs_analysis import StudentNeedsAnalysisForm
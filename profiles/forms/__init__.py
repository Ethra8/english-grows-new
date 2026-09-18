# Adding all forms here allows models/admin to access them
# although they have been moved to forms/ folder
# So no further update is needed

from .profile import UserProfileForm, TeacherProfileForm
from .academic_profile import StudentAcademicProfileForm
from .skill_assessment import (
    StudentSkillAssessmentForm,
    StudentSubSkillAssessmentInlineForm,
    StudentSubSkillAssessmentFormSet,
)
from .student_needs_analysis import StudentNeedsAnalysisForm
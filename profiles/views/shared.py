from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.shortcuts import redirect
from django.utils import timezone
from django.utils.formats import date_format


from decimal import Decimal, ROUND_HALF_UP


from profiles.models import (
    UserProfile, 
    StudentSkillAssessmentSnapshot, 
)

from profiles.forms import (
    UserProfileForm,
)


User = get_user_model()


# =========================================================
# SHARED SKILLS CHART CONFIGURATION
# =========================================================
# Keep the same skill colors everywhere the progress chart is used.
# Dictionary order also controls the dataset / legend order.
SKILL_CHART_COLORS = {
    "Listening": "#4E2496",
    "Reading": "#E1752D",
    "Speaking": "#f5be58",
    "Writing": "#0ea5b7",
}

# =========================================================
# CALENDAR EVENT HELPERS
# =========================================================

def get_calendar_meeting_link(session):
    """
    Return the meeting link available for a ClassSession.

    Prefer the session-specific link.

    Fall back to the Course meeting link when the Course model
    provides one.
    """

    if session.meeting_link:
        return session.meeting_link

    return getattr(
        session.course,
        "meeting_link",
        "",
    ) or ""



@login_required
def login_redirect(request):
    profile = request.user.profile

    if profile.role == "teacher":
        return redirect("profiles:teacher_dashboard")

    return redirect("profiles:profile")



# Common login to profile... THEN custom role profile
@login_required
def profile(request):
    user_profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if user_profile.role == UserProfile.ROLE_COMPANY_ADMIN:
        return redirect("profiles:company_admin_dashboard")

    if user_profile.role == UserProfile.ROLE_TEACHER:
        return redirect("profiles:teacher_dashboard")

    if user_profile.role in [
        UserProfile.ROLE_EMPLOYEE,
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
    ]:
        return redirect("profiles:student_dashboard")

    return redirect("home")


@login_required
def profile_settings(request):
    profile_user = request.user
    profile = get_object_or_404(UserProfile, user=profile_user)

    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=profile_user,
        )

        if form.is_valid():
            form.save()
            return redirect("profiles:profile_settings")

    else:
        form = UserProfileForm(
            instance=profile,
            user=profile_user,
        )

    context = {
        "form": form,
        "profile": profile,
        "profile_user": profile_user,
    }

    return render(
        request,
        "profiles/profile_settings.html",
        context,
    )




# BUILD STD SKILLS GRAPH
def build_skill_progress_chart_data(student, course):
    """
    Build skill progress chart data from detailed assessment snapshots.

    Multiple subskill changes can create multiple snapshots for the
    same skill on the same day.

    For the chart's daily point, use the LAST snapshot recorded for
    that skill on that date. This ensures the latest graph point
    matches the current skill-card score.
    """

    snapshots = (
        StudentSkillAssessmentSnapshot.objects
        .filter(
            skill_assessment__student=student,
            skill_assessment__course=course,
        )
        .select_related(
            "skill_assessment",
        )
        .order_by(
            "recorded_at",
        )
    )

    # ---------------------------------------------------------
    # GROUP SNAPSHOTS BY DATE + SKILL
    #
    # Because snapshots are ordered chronologically, assigning
    # repeatedly to the same date/skill automatically leaves us
    # with the LAST snapshot for that day.
    # ---------------------------------------------------------
    daily_scores = {}

    for snapshot in snapshots:
        date = timezone.localtime(
            snapshot.recorded_at
        ).date()

        skill = snapshot.skill_assessment.skill

        daily_scores.setdefault(date, {})

        daily_scores[date][skill] = snapshot.score


    # ---------------------------------------------------------
    # CHART DATES
    # ---------------------------------------------------------
    chart_dates = sorted(daily_scores.keys())

    chart_labels = [
        date_format(date, "j M")
        for date in chart_dates
    ]


    # ---------------------------------------------------------
    # DATASETS
    # ---------------------------------------------------------
    datasets = []

    for skill_name, color in SKILL_CHART_COLORS.items():

        skill_value = skill_name.lower()

        values = []

        for date in chart_dates:
            score = daily_scores.get(
                date,
                {},
            ).get(
                skill_value,
            )

            values.append(
                float(score)
                if score is not None
                else None
            )

        datasets.append({
            "label": skill_name,
            "data": values,
            "borderColor": color,
            "backgroundColor": color,
            "tension": 0.2,
        })


    return {
        "labels": chart_labels,
        "datasets": datasets,
    }



def build_overall_skill_progress_chart_data(student, course):
    """
    Build one overall skill-development score per assessment date.

    Each point represents the average of the latest known scores
    for all four skills on that date.

    Rules:
    - Uses existing term snapshots as historical baseline.
    - Uses detailed assessment snapshots for newer changes.
    - If a skill is assessed several times on the same day,
      only its LAST score that day is used.
    - A chart point is created only once all four skills have
      an available assessment score.
    """

    skill_names = {
        "listening",
        "reading",
        "speaking",
        "writing",
    }

    # ---------------------------------------------------------
    # DETAILED ASSESSMENT SNAPSHOTS
    # ---------------------------------------------------------
    assessment_snapshots = (
        StudentSkillAssessmentSnapshot.objects
        .filter(
            skill_assessment__student=student,
            skill_assessment__course=course,
        )
        .select_related("skill_assessment")
        .order_by("recorded_at")
    )


    # ---------------------------------------------------------
    # COLLECT ALL CHANGES BY DATE
    #
    # {
    #     date: {
    #         "listening": Decimal(...),
    #         "reading": Decimal(...),
    #         ...
    #     }
    # }
    # ---------------------------------------------------------
    daily_changes = {}

    # New detailed assessment history
    #
    # These are processed second, so they take precedence
    # over a term snapshot on the same date.
    for snapshot in assessment_snapshots:
        date = timezone.localtime(
            snapshot.recorded_at
        ).date()

        skill = snapshot.skill_assessment.skill

        daily_changes.setdefault(date, {})

        # Because queryset is chronological, the last
        # snapshot for this skill/date wins.
        daily_changes[date][skill] = snapshot.score


    if not daily_changes:
        return {
            "labels": [],
            "datasets": [],
        }


    # ---------------------------------------------------------
    # WALK THROUGH HISTORY
    #
    # Carry forward the latest known value for every skill.
    # ---------------------------------------------------------
    latest_scores = {}

    chart_labels = []
    overall_scores = []


    for date in sorted(daily_changes.keys()):

        # Apply all assessment changes made on this date.
        for skill, score in daily_changes[date].items():
            latest_scores[skill] = score


        # -----------------------------------------------------
        # ONLY CREATE A POINT WHEN ALL 4 SKILLS HAVE
        # ACTUALLY BEEN ASSESSED.
        # -----------------------------------------------------
        if not skill_names.issubset(latest_scores.keys()):
            continue


        total = sum(
            (
                latest_scores[skill]
                for skill in skill_names
            ),
            Decimal("0"),
        )

        average = (
            total / Decimal("4")
        ).quantize(
            Decimal("0.1"),
            rounding=ROUND_HALF_UP,
        )


        chart_labels.append(
            date_format(date, "j M")
        )

        overall_scores.append(
            float(average)
        )


    return {
        "labels": chart_labels,

        "datasets": [
            {
                "label": "Overall Skills",
                "data": overall_scores,

                # I'd use ONE brand colour here,
                # not one of the individual skill colours.
                "borderColor": "#007A7D",
                "backgroundColor": "#007A7D",

                "tension": 0.2,
            }
        ],
    }



# Helper to display Teacher notes (+ future automated reports ???)
def build_skill_note_display(skill_assessment):
    subskills = skill_assessment.subskill_assessments.all()

    return {
        "skill": skill_assessment.get_skill_display(),
        "score": skill_assessment.average_score,

        "strengths": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating == "strong"
        ],

        "confident": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating == "confident"
        ],

        "satisfactory": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating == "satisfactory"
        ],

        "developing": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating == "developing"
        ],

        "needs_work": [
            subskill.get_subskill_display()
            for subskill in subskills
            if subskill.rating == "needs_work"
        ],

    }


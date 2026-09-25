import logging
import re

from datetime import datetime, time, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape, strip_tags

from .models import EmailTemplate, LearnerAccountClosureNotice
from courses.models import CourseEnrollment
from placement.models import TOTAL_QUESTIONS
from profiles.models import UserProfile
from profiles.utils.learner_account_retention import get_learner_retention_snapshot



def _render_template_string(value, context):
    """Render {{ variables }} stored inside an EmailTemplate database field."""
    return Template(value or "").render(Context(context))


def _build_cta(label, url):
    """Return email-safe HTML for a branded call-to-action button."""
    return f"""
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin:28px auto;">
            <tr>
                <td align="center" bgcolor="#006B7D" style="border-radius:6px;">
                    <a href="{escape(url)}" style="display:inline-block;padding:12px 24px;color:#ffffff;text-decoration:none;font-weight:600;">
                        {escape(label)}
                    </a>
                </td>
            </tr>
        </table>
    """


def _replace_cta(body_html, body_text, marker, label=None, url=None):
    """Replace a CTA marker with the shared email button and plain-text link."""
    cta_html = _build_cta(label, url) if label and url else ""
    cta_text = f"{label}: {url}" if label and url else ""

    # CKEditor normally wraps standalone markers in <p> tags.
    body_html = re.sub(
        rf"<p(?:\s[^>]*)?>\s*{re.escape(marker)}\s*</p>",
        cta_html,
        body_html,
        flags=re.IGNORECASE,
    )

    body_html = body_html.replace(marker, cta_html)
    body_text = body_text.replace(marker, cta_text)

    return body_html, body_text


def send_template_email(
    template_key,
    recipient,
    context=None,
    cta_label=None,
    cta_url=None,
    cta_2_label=None,
    cta_2_url=None,
):
    """
    Send one database-managed EmailTemplate.

    [[CTA]]   = primary button.
    [[CTA_2]] = optional second button.

    Both use the same shared email styling.
    """

    email_template = EmailTemplate.objects.get(
        key=template_key,
        is_active=True,
    )

    context = context or {}

    subject = _render_template_string(email_template.subject, context)
    heading = _render_template_string(email_template.heading, context)
    body_html = _render_template_string(email_template.body_html, context)
    body_text = _render_template_string(email_template.body_text, context)

    # Build the fallback before replacing markers, so their URLs remain
    # available in the plain-text version of the email.
    if not body_text.strip():
        body_text = strip_tags(body_html)

    body_html, body_text = _replace_cta(
        body_html, body_text, "[[CTA]]", cta_label, cta_url,
    )

    body_html, body_text = _replace_cta(
        body_html, body_text, "[[CTA_2]]", cta_2_label, cta_2_url,
    )

    logo_path = static("images/logo_noBg_512x512.png")
    logo_url = (
        logo_path
        if logo_path.startswith(("http://", "https://"))
        else f"{settings.SITE_URL.rstrip('/')}/{logo_path.lstrip('/')}"
    )

    html_message = render_to_string(
        "communications/emails/base_email.html",
        {
            "subject": subject,
            "heading": heading,
            "body_html": body_html,
            "logo_url": logo_url,
        },
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=body_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )

    email.attach_alternative(html_message, "text/html")
    return email.send(fail_silently=False)


def send_course_enrollment_learning_needs_email(enrollment_id):
    """
    Send the appropriate welcome email for a newly created enrollment.

    Individual learners receive the existing Learning Needs invitation.
    Corporate learners receive the onboarding email with both activities.

    The enrollment provides the learner and Course context.
    """

    enrollment = (
        CourseEnrollment.objects
        .select_related(
            "student",
            "student__profile",
            "course",
        )
        .get(pk=enrollment_id)
    )

    student = enrollment.student
    role = student.profile.role

    if not student.email:
        return 0

    if role in {
        UserProfile.ROLE_INDIVIDUAL_LEARNER,
        UserProfile.ROLE_EMPLOYEE,
    }:
        path = reverse("profiles:my_needs_analysis")

    elif role == UserProfile.ROLE_COMPANY_ADMIN:
        path = reverse(
            "profiles:company_admin_student_needs_analysis",
            args=[student.id],
        )

    else:
        return 0

    learning_goals_url = (
        f"{settings.SITE_URL.rstrip('/')}"
        f"{path}"
        f"?course={enrollment.course_id}"
    )

    is_corporate = role in {
        UserProfile.ROLE_EMPLOYEE,
        UserProfile.ROLE_COMPANY_ADMIN,
    }

    return send_template_email(
        template_key=(
            "corporate_learner_onboarding"
            if is_corporate
            else "welcome_learning_needs_questionnaire"
        ),
        recipient=student.email,
        context={
            "first_name": student.first_name or student.username,
            "course_name": enrollment.course.name,
        },
        cta_label="Complete my Learning Needs",
        cta_url=learning_goals_url,
        cta_2_label="Take my Placement Test" if is_corporate else None,
        cta_2_url=(
            f"{settings.SITE_URL.rstrip('/')}/placement-test/"
            if is_corporate else None
        ),
    )


def send_placement_result_emails(attempt):
    """Email a saved placement result to the learner and relevant staff."""
    logger = logging.getLogger(__name__)

    name = attempt.name or (
        attempt.user.get_full_name() or attempt.user.get_username()
        if attempt.user_id else ""
    ) or "Learner"

    context = {
        "first_name": attempt.user.first_name or name.split()[0] if attempt.user_id else name.split()[0],
        "learner_name": name,
        "learner_email": attempt.email,
        "score": attempt.score,
        "total": TOTAL_QUESTIONS,
        "recommended_level": attempt.get_recommended_level_display(),
        "cefr_reference": attempt.cefr_reference,
        "test_version": attempt.test_version,
        "completed_at": attempt.completed_at,
    }

    # One staff message per distinct address. The general inbox is mandatory.
    staff_recipients = {"info@englishgrows.com": "info@englishgrows.com"}

    if attempt.user_id:
        teacher_emails = CourseEnrollment.objects.filter(
            student_id=attempt.user_id,
            status="active",
            course__status__in=("active", "confirmed"),
            course__teacher__isnull=False,
        ).values_list("course__teacher__email", flat=True)

        for teacher_email in teacher_emails:
            teacher_email = (teacher_email or "").strip()
            if teacher_email:
                staff_recipients.setdefault(
                    teacher_email.casefold(),
                    teacher_email,
                )

    messages = []

    if attempt.email.strip():
        messages.append(("placement_result_learner", attempt.email.strip()))

    messages.extend(
        ("placement_test_result_staff", recipient)
        for recipient in staff_recipients.values()
    )

    sent = 0

    for template_key, recipient in messages:
        try:
            sent += send_template_email(
                template_key=template_key,
                recipient=recipient,
                context=context,
            )
        except Exception:
            logger.exception(
                "Placement result email failed: attempt=%s, template=%s, recipient=%s",
                attempt.pk, template_key, recipient,
            )

    return sent





def send_learner_account_closure_notice(user_id):
    """
    Send an advance learner account-closure notice.

    Normal execution: 30 calendar days before the retention deadline.
    Missed execution: send when processing resumes and postpone closure
    to preserve at least 30 days after successful email submission.

    Existing notification records prevent automatic duplicate attempts.
    Failed or interrupted attempts remain blocked pending review.

    Returns the number of emails sent (0 or 1).
    Never closes, deactivates or deletes an account.
    """
    logger = logging.getLogger(__name__)

    # ---------------------------------------------------------
    # 1. RETRIEVE THE CURRENT USER
    # ---------------------------------------------------------

    user = get_user_model().objects.filter(
        pk=user_id,
        is_active=True,
    ).first()

    if not user or not (user.email or "").strip():
        return 0

    # ---------------------------------------------------------
    # 2. RECALCULATE ACCOUNT RETENTION
    # ---------------------------------------------------------

    snapshot = get_learner_retention_snapshot(user)

    if snapshot["status"] not in {"never_enrolled", "calculable"}:
        return 0

    reference_at = snapshot["reference_at"]
    expiry_at = snapshot["potential_expiry_at"]

    if reference_at is None or expiry_at is None:
        return 0

    # ---------------------------------------------------------
    # 3. CALCULATE THE EFFECTIVE CLOSURE DATE
    # ---------------------------------------------------------

    local_tz = timezone.get_default_timezone()
    today = timezone.localdate(timezone=local_tz)
    original_closure_date = timezone.localtime(expiry_at, local_tz).date()
    days_remaining = (original_closure_date - today).days

    # Do not send before the scheduled 30-day notification date.
    # Missed notifications are recovered automatically.
    if days_remaining > 30:
        return 0

    # Preserve the original date unless a missed notification
    # requires postponement to provide 30 calendar days of notice.
    effective_closure_date = max(
        original_closure_date,
        today + timedelta(days=30),
    )

    # Account closure is scheduled for 23:59 local time.
    effective_closure_at = timezone.make_aware(
        datetime.combine(effective_closure_date, time(23, 59)),
        local_tz,
    )


    # ---------------------------------------------------------
    # 4. REGISTER THE NOTIFICATION ATTEMPT
    # ---------------------------------------------------------

    recipient = user.email.strip()

    notice, created = LearnerAccountClosureNotice.objects.get_or_create(
        user=user,
        reference_at=reference_at,
        defaults={
            "potential_expiry_at": expiry_at,
            "recipient_email": recipient,
        },
    )

    # A previous attempt already exists for this retention period.
    # Never automatically resend an uncertain or failed delivery.
    if not created:
        return 0

    # ---------------------------------------------------------
    # 5. PREPARE EMAIL CONTENT AND BRANDED CTA
    # ---------------------------------------------------------

    login_url = (
        f"{settings.SITE_URL.rstrip('/')}"
        f"{reverse('account_login')}"
    )

    context = {
        "first_name": user.first_name or user.get_username(),
        "closure_date": effective_closure_date.strftime("%d %B %Y"),
    }

    # ---------------------------------------------------------
    # 6. SEND USING THE EXISTING EMAIL SERVICE
    # ---------------------------------------------------------

    try:
        sent = send_template_email(
            template_key="learner_account_closure_notice",
            recipient=recipient,
            context=context,
            cta_label="Sign in to my account",
            cta_url=login_url,
        )

    except Exception:
        notice.status = LearnerAccountClosureNotice.STATUS_FAILED
        notice.save(update_fields=["status"])

        logger.exception(
            "Account-closure notice failed: user_id=%s, notice_id=%s",
            user.pk,
            notice.pk,
        )
        return 0

    # ---------------------------------------------------------
    # 7. RECORD SUCCESSFUL SUBMISSION
    # ---------------------------------------------------------

    if sent:
        notice.status = LearnerAccountClosureNotice.STATUS_SENT
        notice.sent_at = timezone.now()
        notice.effective_closure_at = effective_closure_at
        notice.save(update_fields=[
            "status",
            "sent_at",
            "effective_closure_at",
        ])
        return sent

    # ---------------------------------------------------------
    # 8. RECORD UNSUCCESSFUL SUBMISSION
    # ---------------------------------------------------------

    notice.status = LearnerAccountClosureNotice.STATUS_FAILED
    notice.save(update_fields=["status"])

    logger.warning(
        "Account-closure notice was not sent: user_id=%s, notice_id=%s",
        user.pk,
        notice.pk,
    )

    return 0

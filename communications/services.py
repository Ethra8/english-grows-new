from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.html import strip_tags

from .models import EmailTemplate

from django.urls import reverse
from courses.models import CourseEnrollment
from profiles.models import UserProfile


def _render_template_string(value, context):
    """Render {{ variables }} stored inside an EmailTemplate database field."""
    return Template(value or "").render(Context(context))


def _build_cta(label, url):
    """Return email-safe HTML for an optional call-to-action button."""
    return f"""
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin:28px auto;">
            <tr>
                <td align="center" bgcolor="#006B7D" style="border-radius:6px;">
                    <a href="{url}" style="display:inline-block;padding:12px 24px;color:#ffffff;text-decoration:none;font-weight:600;">
                        {label}
                    </a>
                </td>
            </tr>
        </table>
    """


def send_template_email(template_key, recipient, context=None, cta_label=None, cta_url=None):
    """
    Send one database-managed EmailTemplate.

    `template_key` identifies the email type.
    `context` supplies the approved {{ variables }} used by that email.
    `cta_label` and `cta_url` are optional. If supplied, [[CTA]] inside the
    editable email body is replaced by the shared styled button.
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

    # CKEditor normally places a standalone [[CTA]] inside its own paragraph.
    # Replace that whole paragraph first so the button is not nested inside <p>.
    if cta_label and cta_url:
        cta_html = _build_cta(cta_label, cta_url)
        body_html = body_html.replace("<p>[[CTA]]</p>", cta_html)
        body_html = body_html.replace("[[CTA]]", cta_html)
        body_text = body_text.replace("[[CTA]]", f"{cta_label}: {cta_url}")
    else:
        body_html = body_html.replace("<p>[[CTA]]</p>", "")
        body_html = body_html.replace("[[CTA]]", "")
        body_text = body_text.replace("[[CTA]]", "")

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

    # If no dedicated plain-text version has been written, derive one from
    # the rendered HTML so every email still has a text alternative.
    if not body_text.strip():
        body_text = strip_tags(body_html)

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
    Send the Learning Needs welcome email for a newly created enrollment.

    The CourseEnrollment provides the learner and Course context.
    The email template itself remains editable in Django Admin.

    Email delivery must never affect whether the enrollment itself succeeds.
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

    return send_template_email(
        template_key="welcome_learning_needs_questionnaire",
        recipient=student.email,
        context={
            "first_name": student.first_name or student.username,
            "course_name": enrollment.course.name,
        },
        cta_label="Complete my Learning Needs",
        cta_url=learning_goals_url,
    )
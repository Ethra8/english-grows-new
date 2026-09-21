from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from courses.models import CourseEnrollment

from .services import send_course_enrollment_learning_needs_email


@receiver(
    post_save,
    sender=CourseEnrollment,
    dispatch_uid="send_learning_needs_email_on_enrollment",
)
def send_learning_needs_email_on_enrollment(
    sender,
    instance,
    created,
    **kwargs,
):
    """
    Send the Learning Needs welcome email once a new active
    CourseEnrollment has been successfully created.

    Existing enrollments are deliberately ignored, so editing, pausing,
    completing or cancelling an enrollment never resends the welcome email.
    """
    if not created or instance.status != "active":
        return

    enrollment_id = instance.pk

    transaction.on_commit(
        lambda: send_course_enrollment_learning_needs_email(
            enrollment_id
        ),
        robust=True,
    )
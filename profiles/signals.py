from django.db.models.signals import post_save
from django.dispatch import receiver

from courses.models import CourseEnrollment
from .models import StudentAcademicProfile, StudentNeedsAnalysis


@receiver(post_save, sender=CourseEnrollment)
def ensure_student_academic_records(sender, instance, **kwargs):
    StudentAcademicProfile.objects.get_or_create(
        student=instance.student,
    )

    if instance.status == CourseEnrollment.STATUS_ACTIVE:
        StudentNeedsAnalysis.objects.get_or_create(
            enrollment=instance,
        )
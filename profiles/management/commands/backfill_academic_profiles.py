from django.core.management.base import BaseCommand
from courses.models import CourseEnrollment
from profiles.models import StudentAcademicProfile


class Command(BaseCommand):
    help = "Create missing academic profiles for existing enrolled students."

    def handle(self, *args, **options):
        student_ids = (
            CourseEnrollment.objects
            .values_list("student_id", flat=True)
            .distinct()
        )

        created_count = 0
        existing_count = 0

        for student_id in student_ids:
            _, created = StudentAcademicProfile.objects.get_or_create(
                student_id=student_id,
            )

            if created:
                created_count += 1
            else:
                existing_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Academic profiles created: {created_count}. "
                f"Already existing: {existing_count}."
            )
        )
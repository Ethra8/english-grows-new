from django.core.management.base import BaseCommand

from courses.models import ClassSession


class Command(BaseCommand):
    help = "Transition finished scheduled/rescheduled ClassSessions to held attendance pending."

    def handle(self, *args, **options):
        updated = ClassSession.transition_past_sessions_to_held()

        self.stdout.write(
            self.style.SUCCESS(
                f"{updated} ClassSession(s) transitioned to held attendance pending."
            )
        )
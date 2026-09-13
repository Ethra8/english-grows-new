from django.core.management.base import BaseCommand

from courses.models import ClassSession

# On Render, a Cron Job triggers this command every 5 minutes.
# ONLY ClassSessions that have finished (end_time < now) are synchronized.
# Finished scheduled/rescheduled ClassSessions are synchronized
# according to their attendance state:
#
# - attendance already submitted before end_time (session)
#   -> STATUS_COMPLETE_ATTENDANCE_SUBMITTED
#
# - attendance not yet submitted after end_time (session)
#   -> STATUS_HELD_ATTENDANCE_PENDING

class Command(BaseCommand):
    help = "Synchronize finished ClassSession lifecycle statuses."

    def handle(self, *args, **options):
        updated = ClassSession.transition_past_sessions()

        self.stdout.write(
            self.style.SUCCESS(
                f"{updated} ClassSession(s) synchronized after end time."
            )
        )
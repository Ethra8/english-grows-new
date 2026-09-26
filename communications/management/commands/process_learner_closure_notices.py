
from datetime import datetime, time, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from communications.models import LearnerAccountClosureNotice
from communications.services import send_learner_account_closure_notice
from profiles.utils.learner_account_retention import get_learner_retention_snapshot


class Command(BaseCommand):
    help = "Preview learner closure notices and deactivation eligibility, or send notices with --send."

    def add_arguments(self, parser):
        parser.add_argument(
            "--send",
            action="store_true",
            help="Send eligible closure notices instead of running a read-only preview.",
        )

    @staticmethod
    def _ready_for_deactivation(user, snapshot, notice, now, local_tz):
        """Read-only check. Never deactivates an account."""
        if not user.is_active or snapshot["status"] not in {"never_enrolled", "calculable"}:
            return False

        if (
            notice.status != LearnerAccountClosureNotice.STATUS_SENT
            or notice.sent_at is None
            or notice.effective_closure_at is None
            or notice.reference_at != snapshot["reference_at"]
            or notice.potential_expiry_at != snapshot["potential_expiry_at"]
            or (notice.recipient_email or "").strip().casefold() != (user.email or "").strip().casefold()
        ):
            return False

        # A login after notification invalidates the previous closure notice.
        if user.last_login and user.last_login > notice.sent_at:
            return False

        # Independently enforce 30 calendar days from the ACTUAL sending date.
        sent_date = timezone.localtime(notice.sent_at, local_tz).date()
        earliest_closure = timezone.make_aware(
            datetime.combine(sent_date + timedelta(days=30), time(23, 59)),
            local_tz,
        )

        return now >= max(
            snapshot["potential_expiry_at"],
            notice.effective_closure_at,
            earliest_closure,
        )

    def handle(self, *args, **options):
        now = timezone.now()
        local_tz = timezone.get_default_timezone()
        today = timezone.localtime(now, local_tz).date()
        send_mode = options["send"]

        eligible_count = 0
        already_recorded_count = 0
        ready_count = 0
        recovery_count = 0
        deactivation_ready_count = 0
        sent_count = 0
        not_sent_count = 0

        users = (
            get_user_model().objects
            .filter(is_active=True)
            .select_related("profile")
            .iterator(chunk_size=200)
        )

        mode = "SEND" if send_mode else "PREVIEW"
        self.stdout.write(f"Account-closure notifications — {mode} — {today}")
        self.stdout.write("-" * 55)

        for user in users:
            if not (user.email or "").strip():
                continue

            snapshot = get_learner_retention_snapshot(user)

            if snapshot["status"] not in {"never_enrolled", "calculable"}:
                continue

            reference_at = snapshot["reference_at"]
            expiry_at = snapshot["potential_expiry_at"]

            if reference_at is None or expiry_at is None:
                continue

            original_closure_date = timezone.localtime(expiry_at, local_tz).date()
            days_remaining = (original_closure_date - today).days

            # Never send a notification more than 30 days before its deadline.
            if days_remaining > 30:
                continue

            eligible_count += 1

            existing_notice = LearnerAccountClosureNotice.objects.filter(
                user=user,
                reference_at=reference_at,
            ).first()

            if existing_notice:
                already_recorded_count += 1
                self.stdout.write(
                    f"User #{user.pk}: already recorded ({existing_notice.status})"
                )

                # Deactivation is deliberately PREVIEW ONLY.
                if not send_mode and self._ready_for_deactivation(
                    user, snapshot, existing_notice, now, local_tz
                ):
                    deactivation_ready_count += 1
                    self.stdout.write(
                        f"User #{user.pk}: DEACTIVATION READY (preview only)"
                    )

                continue

            ready_count += 1
            is_recovery = days_remaining < 30

            if is_recovery:
                recovery_count += 1

            timing = "RECOVERY" if is_recovery else "ON SCHEDULE"

            if not send_mode:
                self.stdout.write(
                    f"User #{user.pk}: READY | "
                    f"Timing: {timing} | "
                    f"Original deadline: {original_closure_date} | "
                    f"Days remaining: {days_remaining}"
                )
                continue

            # The service independently recalculates eligibility,
            # registers the attempt and calculates the effective deadline.
            sent = send_learner_account_closure_notice(user.pk)

            if sent:
                sent_count += sent
                self.stdout.write(
                    self.style.SUCCESS(
                        f"User #{user.pk}: SENT | "
                        f"Timing: {timing} | "
                        f"Original deadline: {original_closure_date}"
                    )
                )
            else:
                not_sent_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"User #{user.pk}: NOT SENT | "
                        "Check notification status and application logs."
                    )
                )

        self.stdout.write("-" * 55)
        self.stdout.write(f"Eligible accounts: {eligible_count}")
        self.stdout.write(f"Previously recorded: {already_recorded_count}")
        self.stdout.write(f"Ready for notification: {ready_count}")
        self.stdout.write(f"Recovery candidates: {recovery_count}")

        if send_mode:
            self.stdout.write(f"Emails sent: {sent_count}")
            self.stdout.write(f"Not sent: {not_sent_count}")
            self.stdout.write(self.style.SUCCESS("Sending process complete."))
        else:
            self.stdout.write(f"Deactivation-ready accounts: {deactivation_ready_count}")
            self.stdout.write(
                self.style.SUCCESS(
                    "Preview complete. No emails sent, accounts deactivated or database records modified."
                )
            )

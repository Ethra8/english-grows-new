from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from placement.models import PlacementQuestion, TOTAL_QUESTIONS


class Command(BaseCommand):
    help = "Copy a complete placement question bank into a new test version."

    def add_arguments(self, parser):
        parser.add_argument("source", help="Existing version, e.g. 1.1")
        parser.add_argument("target", help="New version, e.g. 1.2")

    @transaction.atomic
    def handle(self, *args, **options):
        source, target = options["source"], options["target"]

        if source == target:
            raise CommandError("Source and target versions must be different.")

        if len(target) > PlacementQuestion._meta.get_field("version").max_length:
            raise CommandError("The target version identifier is too long.")

        if PlacementQuestion.objects.filter(version=target).exists():
            raise CommandError(f"Version {target} already contains questions. Nothing was copied.")

        questions = list(PlacementQuestion.objects.filter(version=source).order_by("number"))

        if (
            len(questions) != TOTAL_QUESTIONS
            or [q.number for q in questions] != list(range(1, TOTAL_QUESTIONS + 1))
            or any(not q.is_active for q in questions)
        ):
            raise CommandError(
                f"Version {source} must contain exactly {TOTAL_QUESTIONS} active, "
                "consecutively numbered questions before it can be cloned."
            )

        PlacementQuestion.objects.bulk_create([
            PlacementQuestion(
                version=target,
                number=q.number,
                text=q.text,
                option_a=q.option_a,
                option_b=q.option_b,
                option_c=q.option_c,
                option_d=q.option_d,
                correct_answer=q.correct_answer,
                area=q.area,
                language_point=q.language_point,
                target_level=q.target_level,
                is_active=q.is_active,
            )
            for q in questions
        ])

        self.stdout.write(self.style.SUCCESS(
            f"Copied {TOTAL_QUESTIONS} questions from V{source} to V{target}."
        ))
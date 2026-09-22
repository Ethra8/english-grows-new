from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


TEST_VERSION = "1.1"
TOTAL_QUESTIONS = 50


class PlacementQuestion(models.Model):
    class Answer(models.TextChoices):
        A = "A", "A"
        B = "B", "B"
        C = "C", "C"
        D = "D", "D"

    class Area(models.TextChoices):
        GRAMMAR = "grammar", "Grammar"
        VOCABULARY = "vocabulary", "Vocabulary"
        LANGUAGE_USE = "language_use", "Language use"

    class Level(models.TextChoices):
        A1 = "A1", "A1"
        A2 = "A2", "A2"
        B1 = "B1", "B1"
        B2 = "B2", "B2"
        C1 = "C1", "C1"
        C2 = "C2", "C2"

    version = models.CharField(max_length=10, default=TEST_VERSION)
    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(TOTAL_QUESTIONS)])
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255, default="")
    correct_answer = models.CharField(max_length=1, choices=Answer.choices)
    area = models.CharField(max_length=20, choices=Area.choices)
    language_point = models.CharField(max_length=200)
    target_level = models.CharField(max_length=2, choices=Level.choices)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["version", "number"]
        constraints = [models.UniqueConstraint(fields=["version", "number"], name="unique_placement_question_per_version")]

    def __str__(self):
        return f"V{self.version} · Question {self.number} · {self.target_level}"


class PlacementAttempt(models.Model):
    class CourseLevel(models.TextChoices):
        FOUNDATION = "foundation", "Foundation / Teacher review"
        ELEMENTARY = "elementary", "Elementary"
        PRE_INTERMEDIATE = "pre_intermediate", "Pre-Intermediate"
        INTERMEDIATE = "intermediate", "Intermediate"
        UPPER_INTERMEDIATE = "upper_intermediate", "Upper-Intermediate"
        ADVANCED = "advanced", "Advanced"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="placement_attempts")
    name = models.CharField(max_length=150, blank=True, default="")
    email = models.EmailField()
    test_version = models.CharField(max_length=10, default=TEST_VERSION)
    answers = models.JSONField(default=dict, blank=True)
    answer_snapshot = models.JSONField(default=dict, blank=True)
    score = models.PositiveSmallIntegerField(null=True, blank=True, editable=False, validators=[MaxValueValidator(TOTAL_QUESTIONS)])
    recommended_level = models.CharField(max_length=20, choices=CourseLevel.choices, blank=True, editable=False)
    cefr_reference = models.CharField(max_length=2, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name or self.email} · {self.score if self.score is not None else '—'}/50"

    @classmethod
    def placement_for_score(cls, score):
        if type(score) is not int or not 0 <= score <= TOTAL_QUESTIONS:
            raise ValueError("Placement score must be an integer between 0 and 50.")
        bands = (
            (7, cls.CourseLevel.FOUNDATION, ""),
            (14, cls.CourseLevel.ELEMENTARY, "A1"),
            (24, cls.CourseLevel.PRE_INTERMEDIATE, "A2"),
            (33, cls.CourseLevel.INTERMEDIATE, "B1"),
            (44, cls.CourseLevel.UPPER_INTERMEDIATE, "B2"),
            (50, cls.CourseLevel.ADVANCED, "C1"),
        )
        for maximum, level, cefr in bands:
            if score <= maximum:
                return level, cefr

    def grade(self):
        if self.score is not None:
            raise ValidationError("This placement attempt has already been graded.")
        questions = list(PlacementQuestion.objects.filter(version=self.test_version, is_active=True).order_by("number"))
        if [q.number for q in questions] != list(range(1, TOTAL_QUESTIONS + 1)) or any(
            not all((q.option_a, q.option_b, q.option_c, q.option_d)) for q in questions
        ):
            raise ValidationError("The placement question bank is incomplete.")
        if not isinstance(self.answers, dict):
            raise ValidationError("Answers must be provided as a dictionary.")
        if set(self.answers) - {str(q.number) for q in questions}:
            raise ValidationError("The submission contains unknown questions.")

        snapshot, correct = {}, 0
        for question in questions:
            selected = self.answers.get(str(question.number))
            if selected not in (None, "", *PlacementQuestion.Answer.values):
                raise ValidationError(f"Invalid answer for question {question.number}.")
            is_correct = selected == question.correct_answer
            correct += int(is_correct)
            snapshot[str(question.number)] = {
                "text": question.text,
                "options": {"A": question.option_a, "B": question.option_b, "C": question.option_c, "D": question.option_d},
                "selected": selected or None,
                "correct_answer": question.correct_answer,
                "is_correct": is_correct,
                "target_level": question.target_level,
                "language_point": question.language_point,
            }

        self.score = correct
        self.recommended_level, self.cefr_reference = self.placement_for_score(correct)
        self.answer_snapshot = snapshot
        self.completed_at = timezone.now()
        self.save()
        return self

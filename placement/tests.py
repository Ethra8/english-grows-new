from collections import Counter
from io import StringIO

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, TestCase

from .models import PlacementAttempt, PlacementQuestion, TEST_VERSION


class PlacementScoringTests(SimpleTestCase):
    def test_placement_boundaries(self):
        cases = (
            (0, "foundation", ""), (7, "foundation", ""),
            (8, "elementary", "A1"), (14, "elementary", "A1"),
            (15, "pre_intermediate", "A2"), (24, "pre_intermediate", "A2"),
            (25, "intermediate", "B1"), (33, "intermediate", "B1"),
            (34, "upper_intermediate", "B2"), (44, "upper_intermediate", "B2"),
            (45, "advanced", "C1"), (50, "advanced", "C1"),
        )
        for score, level, cefr in cases:
            with self.subTest(score=score):
                self.assertEqual(PlacementAttempt.placement_for_score(score), (level, cefr))

    def test_every_possible_score(self):
        for score in range(51):
            self.assertIsNotNone(PlacementAttempt.placement_for_score(score)[0])

    def test_invalid_scores(self):
        for score in (-1, 51, 2.5, None, True):
            with self.subTest(score=score), self.assertRaises(ValueError):
                PlacementAttempt.placement_for_score(score)


class PlacementQuestionBankTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_placement_questions", stdout=StringIO())

    def test_question_count_order_levels_and_four_options(self):
        questions = list(PlacementQuestion.objects.filter(version=TEST_VERSION).order_by("number"))
        self.assertEqual([q.number for q in questions], list(range(1, 51)))
        self.assertEqual(Counter(q.target_level for q in questions),
                         {"A1": 8, "A2": 7, "B1": 10, "B2": 13, "C1": 11, "C2": 1})
        self.assertTrue(all(q.option_a and q.option_b and q.option_c and q.option_d for q in questions))
        self.assertTrue(all(q.is_active for q in questions))
        self.assertEqual(Counter(q.correct_answer for q in questions), {"A": 13, "B": 13, "C": 12, "D": 12})

    def test_import_is_idempotent(self):
        call_command("seed_placement_questions", stdout=StringIO())
        self.assertEqual(PlacementQuestion.objects.filter(version=TEST_VERSION).count(), 50)

    def test_existing_question_is_not_silently_overwritten(self):
        question = PlacementQuestion.objects.get(version=TEST_VERSION, number=1)
        question.text = "Altered question"
        question.save(update_fields=["text"])
        with self.assertRaises(CommandError):
            call_command("seed_placement_questions", stdout=StringIO())
        question.refresh_from_db()
        self.assertEqual(question.text, "Altered question")

    def test_grade_all_correct_including_d(self):
        answers = {str(q.number): q.correct_answer for q in PlacementQuestion.objects.filter(version=TEST_VERSION)}
        self.assertIn("D", answers.values())
        attempt = PlacementAttempt(name="Test Learner", email="learner@example.com", answers=answers).grade()
        self.assertEqual((attempt.score, attempt.recommended_level, attempt.cefr_reference), (50, "advanced", "C1"))
        self.assertEqual(len(attempt.answer_snapshot), 50)
        self.assertTrue(all(row["is_correct"] for row in attempt.answer_snapshot.values()))
        self.assertEqual(len(attempt.answer_snapshot["1"]["options"]), 4)

    def test_unanswered_questions_score_zero(self):
        attempt = PlacementAttempt(name="Test Learner", email="learner@example.com", answers={}).grade()
        self.assertEqual((attempt.score, attempt.recommended_level), (0, "foundation"))
        self.assertIsNone(attempt.answer_snapshot["1"]["selected"])

    def test_invalid_answer_is_rejected(self):
        attempt = PlacementAttempt(name="Test Learner", email="learner@example.com", answers={"1": "E"})
        with self.assertRaises(ValidationError):
            attempt.grade()
        self.assertIsNone(attempt.score)

    def test_attempt_cannot_be_graded_twice(self):
        attempt = PlacementAttempt(name="Test Learner", email="learner@example.com", answers={}).grade()
        with self.assertRaises(ValidationError):
            attempt.grade()

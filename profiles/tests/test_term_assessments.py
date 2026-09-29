from unittest.mock import patch
from itertools import product
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from courses.models import Course, CourseEnrollment, CourseType
from profiles.models import (
    UserProfile,
    SUBSKILLS,
    StudentSkillAssessment,
    StudentSubSkillAssessment,
    StudentTermAssessment,
    StudentSkillTermSnapshot,
    StudentTermSubSkillAssessment,
    StudentTermAssessmentReport,
)
from profiles.utils.term_assessments import (
    get_or_create_term_assessment_draft,
    submit_term_assessment,
    update_term_subskill_rating,
)
from profiles.utils.term_assessment_reports import (
    analyse_speaking_profile,
    build_speaking_performance_summary,
    create_term_assessment_report,
    generate_term_assessment_report,
)


class SpeakingPerformanceSummaryTests(TestCase):
    """Exhaustive tests for the Speaking performance-summary engine."""
    subskills = (
        "fluency",
        "accuracy_and_range",
        "pronunciation",
        "interaction",
    )
    @staticmethod
    def build_items(combination):
        return [
            {
                "subskill": subskill,
                "rating": subskill_rating,
            }
            for subskill, subskill_rating in zip(
                SpeakingPerformanceSummaryTests.subskills,
                combination,
            )
        ]
    def test_every_speaking_rating_combination_generates_valid_summary(self):
        rating = StudentSubSkillAssessment.Rating
        ratings = (
            rating.NEEDS_WORK,
            rating.DEVELOPING,
            rating.SATISFACTORY,
            rating.CONFIDENT,
            rating.STRONG,
        )
        expected_profiles = {
            "consistently_strong",
            "generally_secure",
            "developing_evenly",
            "broad_support_needed",
            "mixed",
            "pronounced_strength",
            "pronounced_weakness",
        }
        profiles_found = set()
        summaries = {}
        for combination in product(ratings, repeat=4):
            items = self.build_items(combination)
            profile = analyse_speaking_profile(items)
            summary = build_speaking_performance_summary(profile, "Maria")
            profiles_found.add(profile["profile"])
            summaries[combination] = summary
            self.assertIn(profile["profile"], expected_profiles)
            self.assertTrue(summary.strip())
            self.assertNotIn("None", summary)
            self.assertNotIn("{learner_name}", summary)
        self.assertEqual(len(summaries), 625)
        self.assertEqual(profiles_found, expected_profiles)
    def test_speaking_performance_summary_is_deterministic(self):
        rating = StudentSubSkillAssessment.Rating
        items = self.build_items(
            (
                rating.SATISFACTORY,
                rating.DEVELOPING,
                rating.CONFIDENT,
                rating.CONFIDENT,
            )
        )
        first_profile = analyse_speaking_profile(items)
        second_profile = analyse_speaking_profile(items)
        first_summary = build_speaking_performance_summary(
            first_profile,
            "Maria",
        )
        second_summary = build_speaking_performance_summary(
            second_profile,
            "Maria",
        )
        self.assertEqual(first_profile, second_profile)
        self.assertEqual(first_summary, second_summary)
    def test_representative_speaking_profiles_are_classified_correctly(self):
        rating = StudentSubSkillAssessment.Rating
        cases = (
            (
                (
                    rating.STRONG,
                    rating.STRONG,
                    rating.STRONG,
                    rating.STRONG,
                ),
                "consistently_strong",
            ),
            (
                (
                    rating.SATISFACTORY,
                    rating.CONFIDENT,
                    rating.SATISFACTORY,
                    rating.CONFIDENT,
                ),
                "generally_secure",
            ),
            (
                (
                    rating.DEVELOPING,
                    rating.DEVELOPING,
                    rating.SATISFACTORY,
                    rating.DEVELOPING,
                ),
                "developing_evenly",
            ),
            (
                (
                    rating.NEEDS_WORK,
                    rating.DEVELOPING,
                    rating.NEEDS_WORK,
                    rating.DEVELOPING,
                ),
                "broad_support_needed",
            ),
            (
                (
                    rating.SATISFACTORY,
                    rating.SATISFACTORY,
                    rating.SATISFACTORY,
                    rating.STRONG,
                ),
                "pronounced_strength",
            ),
            (
                (
                    rating.SATISFACTORY,
                    rating.NEEDS_WORK,
                    rating.SATISFACTORY,
                    rating.SATISFACTORY,
                ),
                "pronounced_weakness",
            ),
            (
                (
                    rating.NEEDS_WORK,
                    rating.DEVELOPING,
                    rating.CONFIDENT,
                    rating.STRONG,
                ),
                "mixed",
            ),
        )
        for combination, expected_profile in cases:
            with self.subTest(
                combination=combination,
                expected_profile=expected_profile,
            ):
                profile = analyse_speaking_profile(
                    self.build_items(combination)
                )
                self.assertEqual(
                    profile["profile"],
                    expected_profile,
                )
    def test_speaking_profile_rejects_incomplete_assessment(self):
        rating = StudentSubSkillAssessment.Rating
        items = [
            {"subskill": "fluency", "rating": rating.SATISFACTORY},
            {
                "subskill": "accuracy_and_range",
                "rating": rating.SATISFACTORY,
            },
            {
                "subskill": "pronunciation",
                "rating": rating.SATISFACTORY,
            },
        ]
        with self.assertRaises(ValidationError):
            analyse_speaking_profile(items)


class TermAssessmentDraftTests(TestCase):
    """Tests for independent formal Term Assessment draft creation."""
    @classmethod
    def setUpTestData(cls):
        cls.student = get_user_model().objects.create_user(
            username="term_test_student",
            email="term-test@example.com",
            password="TestPassword123!",
        )
        cls.course_type = CourseType.objects.create(
            name="Term Assessment Test Course Type",
        )
        cls.course = Course.objects.create(
            name="Term Assessment Test Course",
            course_type=cls.course_type,
        )
        cls.enrollment = CourseEnrollment.objects.create(
            student=cls.student,
            course=cls.course,
        )
        # Populate the ongoing Skills Assessment with all 14 ratings.
        for skill, subskills in SUBSKILLS.items():
            skill_assessment = StudentSkillAssessment.objects.create(
                student=cls.student,
                course=cls.course,
                skill=skill,
            )
            for subskill, _ in subskills:
                StudentSubSkillAssessment.objects.create(
                    skill_assessment=skill_assessment,
                    subskill=subskill,
                    rating="satisfactory",
                )
    def create_draft(self, term_label="Test Term 1"):
        return get_or_create_term_assessment_draft(
            enrollment=self.enrollment,
            term_label=term_label,
        )
    def get_formal_fluency(self, assessment):
        return StudentTermSubSkillAssessment.objects.get(
            skill_snapshot__term_assessment=assessment,
            skill_snapshot__skill="speaking",
            subskill="fluency",
        )
    def get_ongoing_fluency(self):
        return StudentSubSkillAssessment.objects.get(
            skill_assessment__student=self.student,
            skill_assessment__course=self.course,
            skill_assessment__skill="speaking",
            subskill="fluency",
        )
    # ---------------------------------------------------------
    # DRAFT CREATION
    # ---------------------------------------------------------
    def test_creates_draft_with_correct_enrollment_and_term(self):
        assessment, created = self.create_draft()
        self.assertTrue(created)
        self.assertEqual(assessment.enrollment, self.enrollment)
        self.assertEqual(assessment.term_label, "Test Term 1")
        self.assertEqual(assessment.status, StudentTermAssessment.Status.DRAFT)
        self.assertEqual(StudentTermAssessment.objects.count(), 1)
    def test_creates_exactly_four_skill_snapshots(self):
        assessment, _ = self.create_draft()
        actual_skills = set(
            assessment.skill_snapshots.values_list("skill", flat=True)
        )
        self.assertEqual(actual_skills, set(SUBSKILLS))
        self.assertEqual(assessment.skill_snapshots.count(), 4)
    def test_creates_all_fourteen_expected_subskills(self):
        assessment, _ = self.create_draft()
        actual = {
            (item.skill_snapshot.skill, item.subskill)
            for item in StudentTermSubSkillAssessment.objects.filter(
                skill_snapshot__term_assessment=assessment,
            )
        }
        expected = {
            (skill, subskill)
            for skill, subskills in SUBSKILLS.items()
            for subskill, _ in subskills
        }
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 14)
    def test_copies_all_ongoing_ratings_exactly(self):
        assessment, _ = self.create_draft()
        ongoing = {
            (item.skill_assessment.skill, item.subskill): item.rating
            for item in StudentSubSkillAssessment.objects.filter(
                skill_assessment__student=self.student,
                skill_assessment__course=self.course,
            )
        }
        formal = {
            (item.skill_snapshot.skill, item.subskill): item.rating
            for item in StudentTermSubSkillAssessment.objects.filter(
                skill_snapshot__term_assessment=assessment,
            )
        }
        self.assertEqual(len(ongoing), 14)
        self.assertEqual(formal, ongoing)
    def test_missing_ongoing_ratings_remain_unrated(self):
        ongoing_fluency = self.get_ongoing_fluency()
        ongoing_fluency.rating = None
        ongoing_fluency.save(update_fields=["rating"])
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        self.assertIsNone(formal_fluency.rating)
        self.assertEqual(
            StudentTermSubSkillAssessment.objects.filter(
                skill_snapshot__term_assessment=assessment,
                rating__isnull=True,
            ).count(),
            1,
        )
    def test_creates_complete_structure_without_ongoing_assessments(self):
        StudentSkillAssessment.objects.filter(
            student=self.student,
            course=self.course,
        ).delete()
        assessment, created = self.create_draft()
        self.assertTrue(created)
        self.assertEqual(assessment.skill_snapshots.count(), 4)
        formal_subskills = StudentTermSubSkillAssessment.objects.filter(
            skill_snapshot__term_assessment=assessment,
        )
        self.assertEqual(formal_subskills.count(), 14)
        self.assertEqual(
            formal_subskills.filter(rating__isnull=True).count(),
            14,
        )
    def test_rejects_blank_term_label(self):
        with self.assertRaises(ValueError):
            self.create_draft("   ")
        self.assertFalse(StudentTermAssessment.objects.exists())
    def test_strips_term_label_whitespace(self):
        assessment, _ = self.create_draft("  Test Term 1  ")
        self.assertEqual(assessment.term_label, "Test Term 1")
    # ---------------------------------------------------------
    # INDEPENDENCE FROM ONGOING SKILLS ASSESSMENT
    # ---------------------------------------------------------
    def test_editing_formal_rating_does_not_change_ongoing_rating(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        ongoing_fluency = self.get_ongoing_fluency()
        original_rating = ongoing_fluency.rating
        formal_fluency.rating = "strong"
        formal_fluency.save(update_fields=["rating"])
        ongoing_fluency.refresh_from_db()
        self.assertEqual(formal_fluency.rating, "strong")
        self.assertEqual(ongoing_fluency.rating, original_rating)
    def test_editing_ongoing_rating_does_not_change_formal_rating(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        ongoing_fluency = self.get_ongoing_fluency()
        original_rating = formal_fluency.rating
        ongoing_fluency.rating = "strong"
        ongoing_fluency.save(update_fields=["rating"])
        formal_fluency.refresh_from_db()
        self.assertEqual(ongoing_fluency.rating, "strong")
        self.assertEqual(formal_fluency.rating, original_rating)
    # ---------------------------------------------------------
    # DUPLICATE PREVENTION AND EDIT PRESERVATION
    # ---------------------------------------------------------
    def test_reopening_returns_existing_assessment(self):
        first, first_created = self.create_draft()
        second, second_created = self.create_draft()
        self.assertTrue(first_created)
        self.assertFalse(second_created)
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(StudentTermAssessment.objects.count(), 1)
    def test_reopening_does_not_duplicate_snapshots_or_subskills(self):
        assessment, _ = self.create_draft()
        self.create_draft()
        self.assertEqual(
            StudentSkillTermSnapshot.objects.filter(
                term_assessment=assessment,
            ).count(),
            4,
        )
        self.assertEqual(
            StudentTermSubSkillAssessment.objects.filter(
                skill_snapshot__term_assessment=assessment,
            ).count(),
            14,
        )
    def test_reopening_preserves_formal_teacher_edits(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        formal_fluency.rating = "strong"
        formal_fluency.save(update_fields=["rating"])
        self.create_draft()
        formal_fluency.refresh_from_db()
        self.assertEqual(formal_fluency.rating, "strong")
    def test_existing_submitted_assessment_is_not_recreated(self):
        assessment, _ = self.create_draft()
        assessment.status = StudentTermAssessment.Status.SUBMITTED
        assessment.save(update_fields=["status"])
        same_assessment, created = self.create_draft()
        self.assertFalse(created)
        self.assertEqual(same_assessment.pk, assessment.pk)
        self.assertEqual(
            same_assessment.status,
            StudentTermAssessment.Status.SUBMITTED,
        )
        self.assertEqual(assessment.skill_snapshots.count(), 4)
    def test_different_terms_create_independent_assessments(self):
        first, _ = self.create_draft("Term 1")
        second, _ = self.create_draft("Term 2")
        self.assertNotEqual(first.pk, second.pk)
        self.assertEqual(StudentTermAssessment.objects.count(), 2)
        self.assertEqual(first.skill_snapshots.count(), 4)
        self.assertEqual(second.skill_snapshots.count(), 4)
    # ---------------------------------------------------------
    # TRANSACTION SAFETY
    # ---------------------------------------------------------
    def test_failed_creation_rolls_back_entire_draft(self):
        with patch(
            "profiles.utils.term_assessments."
            "StudentTermSubSkillAssessment.objects.bulk_create",
            side_effect=RuntimeError("Simulated creation failure"),
        ):
            with self.assertRaises(RuntimeError):
                self.create_draft()
        self.assertFalse(StudentTermAssessment.objects.exists())
        self.assertFalse(StudentSkillTermSnapshot.objects.exists())
        self.assertFalse(StudentTermSubSkillAssessment.objects.exists())
        # ---------------------------------------------------------
    # FORMAL SCORE CALCULATIONS
    # ---------------------------------------------------------
    def test_formal_skill_score_uses_its_own_subskills(self):
        assessment, _ = self.create_draft()
        speaking = assessment.skill_snapshots.get(skill="speaking")
        ratings = {
            "fluency": "confident",
            "accuracy_and_range": "satisfactory",
            "pronunciation": "developing",
            "interaction": "strong",
        }
        for subskill, rating in ratings.items():
            speaking.subskill_assessments.filter(
                subskill=subskill,
            ).update(rating=rating)
        self.assertEqual(speaking.calculated_score, Decimal("7.1"))
    def test_unrated_subskills_are_excluded_from_provisional_average(self):
        assessment, _ = self.create_draft()
        speaking = assessment.skill_snapshots.get(skill="speaking")
        speaking.subskill_assessments.filter(
            subskill="fluency",
        ).update(rating=None)
        self.assertEqual(speaking.calculated_score, Decimal("6.0"))
    def test_completely_unrated_skill_has_no_calculated_score(self):
        assessment, _ = self.create_draft()
        speaking = assessment.skill_snapshots.get(skill="speaking")
        speaking.subskill_assessments.update(rating=None)
        self.assertIsNone(speaking.calculated_score)
    def test_overall_score_weights_four_skills_equally(self):
        assessment, _ = self.create_draft()
        ratings = {
            "listening": "confident",
            "reading": "satisfactory",
            "speaking": "strong",
            "writing": "developing",
        }
        for skill, rating in ratings.items():
            assessment.skill_snapshots.get(
                skill=skill,
            ).subskill_assessments.update(rating=rating)
        # (7.5 + 6.0 + 10.0 + 5.0) / 4 = 7.125 -> 7.1
        self.assertEqual(
            assessment.calculated_overall_score,
            Decimal("7.1"),
        )
    def test_overall_score_requires_all_four_skill_scores(self):
        assessment, _ = self.create_draft()
        assessment.skill_snapshots.get(
            skill="listening",
        ).subskill_assessments.update(rating=None)
        self.assertIsNone(assessment.calculated_overall_score)
    def test_calculation_does_not_submit_or_store_results(self):
        assessment, _ = self.create_draft()
        self.assertEqual(
            assessment.calculated_overall_score,
            Decimal("6.0"),
        )
        assessment.refresh_from_db()
        self.assertEqual(assessment.status, StudentTermAssessment.Status.DRAFT)
        self.assertIsNone(assessment.overall_score)
        for snapshot in assessment.skill_snapshots.all():
            self.assertIsNone(snapshot.score)
    # ---------------------------------------------------------
    # FORMAL ASSESSMENT SUBMISSION
    # ---------------------------------------------------------
    def test_submission_stores_final_scores_and_metadata(self):
        assessment, _ = self.create_draft()
        submitted = submit_term_assessment(assessment, self.student)
        submitted.refresh_from_db()
        self.assertEqual(submitted.status, StudentTermAssessment.Status.SUBMITTED)
        self.assertEqual(submitted.teacher, self.student)
        self.assertEqual(submitted.overall_score, Decimal("6.0"))
        self.assertIsNotNone(submitted.assessment_date)
        self.assertIsNotNone(submitted.submitted_at)
        for snapshot in submitted.skill_snapshots.all():
            self.assertEqual(snapshot.score, Decimal("6.0"))
    def test_submission_rejects_missing_rating(self):
        assessment, _ = self.create_draft()
        self.get_formal_fluency(assessment).delete()
        with self.assertRaises(ValidationError):
            assessment = submit_term_assessment(assessment, self.student)
        assessment.refresh_from_db()
        self.assertEqual(assessment.status, StudentTermAssessment.Status.DRAFT)
        self.assertIsNone(assessment.overall_score)
    def test_submission_rejects_unrated_subskill(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        formal_fluency.rating = None
        formal_fluency.save(update_fields=["rating"])
        with self.assertRaises(ValidationError):
            assessment = submit_term_assessment(assessment, self.student)
        assessment.refresh_from_db()
        self.assertEqual(assessment.status, StudentTermAssessment.Status.DRAFT)
        self.assertIsNone(assessment.overall_score)
    def test_submission_rejects_missing_skill(self):
        assessment, _ = self.create_draft()
        assessment.skill_snapshots.filter(skill="speaking").delete()
        with self.assertRaises(ValidationError):
            assessment = submit_term_assessment(assessment, self.student)
        assessment.refresh_from_db()
        self.assertEqual(assessment.status, StudentTermAssessment.Status.DRAFT)
    def test_submission_rejects_missing_teacher(self):
        assessment, _ = self.create_draft()
        with self.assertRaises(ValidationError):
            submit_term_assessment(assessment, None)
        assessment.refresh_from_db()
        self.assertEqual(assessment.status, StudentTermAssessment.Status.DRAFT)
    def test_submitted_assessment_cannot_be_submitted_again(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        with self.assertRaises(ValidationError):
            assessment = submit_term_assessment(assessment, self.student)
        self.assertEqual(StudentTermAssessment.objects.count(), 1)
    def test_submission_does_not_modify_ongoing_ratings(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        formal_fluency.rating = "strong"
        formal_fluency.save(update_fields=["rating"])
        assessment = submit_term_assessment(assessment, self.student)
        ongoing_fluency = self.get_ongoing_fluency()
        ongoing_fluency.refresh_from_db()
        self.assertEqual(ongoing_fluency.rating, "satisfactory")
    def test_failed_submission_does_not_store_partial_scores(self):
        assessment, _ = self.create_draft()
        self.get_formal_fluency(assessment).delete()
        with self.assertRaises(ValidationError):
            assessment = submit_term_assessment(assessment, self.student)
        self.assertFalse(
            assessment.skill_snapshots.filter(score__isnull=False).exists()
        )
        assessment.refresh_from_db()
        self.assertIsNone(assessment.overall_score)
        self.assertIsNone(assessment.submitted_at)
        self.assertEqual(assessment.status, StudentTermAssessment.Status.DRAFT)
    # ---------------------------------------------------------
    # FORMAL ASSESSMENT EDIT PROTECTION
    # ---------------------------------------------------------
    def test_draft_rating_can_be_edited(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        updated = update_term_subskill_rating(formal_fluency, "strong")
        self.assertEqual(updated.rating, "strong")
        formal_fluency.refresh_from_db()
        self.assertEqual(formal_fluency.rating, "strong")
        assessment.refresh_from_db()
        self.assertEqual(assessment.status, StudentTermAssessment.Status.DRAFT)
        self.assertIsNone(assessment.overall_score)
    def test_draft_rating_can_be_cleared(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        updated = update_term_subskill_rating(formal_fluency, None)
        self.assertIsNone(updated.rating)
    def test_invalid_draft_rating_is_rejected(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        with self.assertRaises(ValidationError):
            update_term_subskill_rating(formal_fluency, "invalid_rating")
        formal_fluency.refresh_from_db()
        self.assertEqual(formal_fluency.rating, "satisfactory")
    def test_submitted_rating_cannot_be_edited_through_helper(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        assessment = submit_term_assessment(assessment, self.student)
        with self.assertRaises(ValidationError):
            update_term_subskill_rating(formal_fluency, "strong")
        formal_fluency.refresh_from_db()
        self.assertEqual(formal_fluency.rating, "satisfactory")
    def test_submitted_rating_cannot_be_saved_directly(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        assessment = submit_term_assessment(assessment, self.student)
        formal_fluency.rating = "strong"
        with self.assertRaises(ValidationError):
            formal_fluency.save()
        formal_fluency.refresh_from_db()
        self.assertEqual(formal_fluency.rating, "satisfactory")
    def test_submitted_rating_cannot_be_deleted_directly(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        assessment = submit_term_assessment(assessment, self.student)
        with self.assertRaises(ValidationError):
            formal_fluency.delete()
        self.assertTrue(
            type(formal_fluency).objects.filter(pk=formal_fluency.pk).exists()
        )
    def test_submitted_skill_score_cannot_be_modified(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        speaking = assessment.skill_snapshots.get(skill="speaking")
        speaking.score = Decimal("10.0")
        with self.assertRaises(ValidationError):
            speaking.save()
        speaking.refresh_from_db()
        self.assertEqual(speaking.score, Decimal("6.0"))
    def test_submitted_skill_snapshot_cannot_be_deleted_directly(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        speaking = assessment.skill_snapshots.get(skill="speaking")
        with self.assertRaises(ValidationError):
            speaking.delete()
        self.assertTrue(
            assessment.skill_snapshots.filter(skill="speaking").exists()
        )
    def test_submitted_assessment_cannot_be_modified(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        assessment.overall_feedback = "Modified after submission"
        with self.assertRaises(ValidationError):
            assessment.save()
        assessment.refresh_from_db()
        self.assertEqual(assessment.overall_feedback, "")
    def test_submitted_assessment_cannot_be_reopened(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        assessment.status = StudentTermAssessment.Status.DRAFT
        with self.assertRaises(ValidationError):
            assessment.save()
        assessment.refresh_from_db()
        self.assertEqual(
            assessment.status,
            StudentTermAssessment.Status.SUBMITTED,
        )
    def test_formal_edit_does_not_change_ongoing_rating(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        update_term_subskill_rating(formal_fluency, "strong")
        ongoing_fluency = self.get_ongoing_fluency()
        ongoing_fluency.refresh_from_db()
        self.assertEqual(ongoing_fluency.rating, "satisfactory")
    # ---------------------------------------------------------
    # FORMAL TERM ASSESSMENT REPORT GENERATION
    # ---------------------------------------------------------
    def test_report_rejects_draft_assessment(self):
        assessment, _ = self.create_draft()
        with self.assertRaises(ValidationError):
            generate_term_assessment_report(assessment)
    def test_report_contains_correct_assessment_information(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        report = generate_term_assessment_report(assessment)
        self.assertEqual(report["assessment_id"], assessment.pk)
        self.assertEqual(report["term_label"], assessment.term_label)
        self.assertEqual(report["overall_score"], Decimal("6.0"))
        self.assertEqual(report["assessment_date"], assessment.assessment_date)
        self.assertEqual(report["course"], str(self.course))
        self.assertEqual(len(report["skills"]), 4)
    def test_report_uses_stored_skill_scores(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        report = generate_term_assessment_report(assessment)
        actual = {
            item["key"]: item["score"]
            for item in report["skills"]
        }
        self.assertEqual(set(actual), set(SUBSKILLS))
        self.assertTrue(
            all(score == Decimal("6.0") for score in actual.values())
        )
    def test_report_selects_lowest_rated_subskills_first(self):
        assessment, _ = self.create_draft()
        ratings = {
            ("speaking", "fluency"): "needs_work",
            ("reading", "scanning"): "developing",
            ("listening", "gist"): "needs_work",
            ("writing", "organization"): "developing",
        }
        for (skill, subskill), rating in ratings.items():
            StudentTermSubSkillAssessment.objects.filter(
                skill_snapshot__term_assessment=assessment,
                skill_snapshot__skill=skill,
                subskill=subskill,
            ).update(rating=rating)
        assessment = submit_term_assessment(assessment, self.student)
        report = generate_term_assessment_report(assessment)
        priorities = report["next_term_priorities"]
        self.assertEqual(len(priorities), 3)
        self.assertEqual(
            [(item["skill"], item["subskill"]) for item in priorities],
            [
                ("speaking", "fluency"),
                ("listening", "gist"),
                ("reading", "scanning"),
            ],
        )
        self.assertEqual(
            [item["rating"] for item in priorities],
            ["needs_work", "needs_work", "developing"],
        )
    def test_equal_ratings_follow_existing_subskills_order(self):
        assessment, _ = self.create_draft()
        for skill, subskill in [
            ("speaking", "fluency"),
            ("speaking", "pronunciation"),
            ("reading", "scanning"),
            ("listening", "gist"),
        ]:
            StudentTermSubSkillAssessment.objects.filter(
                skill_snapshot__term_assessment=assessment,
                skill_snapshot__skill=skill,
                subskill=subskill,
            ).update(rating="needs_work")
        assessment = submit_term_assessment(assessment, self.student)
        report = generate_term_assessment_report(assessment)
        self.assertEqual(
            [
                (item["skill"], item["subskill"])
                for item in report["next_term_priorities"]
            ],
            [
                ("speaking", "fluency"),
                ("speaking", "pronunciation"),
                ("reading", "scanning"),
            ],
        )
    def test_report_does_not_invent_weaknesses(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        report = generate_term_assessment_report(assessment)
        self.assertEqual(len(report["development_priorities"]), 4)
        self.assertEqual(len(report["next_term_priorities"]), 3)
        for skill in ("speaking", "reading", "listening", "writing"):
            self.assertIn(
                "Performance is satisfactory",
                report["development_priorities"][skill],
            )
            self.assertNotIn(
                "Targeted development is recommended",
                report["development_priorities"][skill],
            )
        self.assertTrue(
            all(
                item["focus_type"] == "consolidation"
                for item in report["next_term_priorities"]
            )
        )
    def test_report_identifies_recorded_strengths(self):
        assessment, _ = self.create_draft()
        StudentTermSubSkillAssessment.objects.filter(
            skill_snapshot__term_assessment=assessment,
            skill_snapshot__skill="speaking",
            subskill="fluency",
        ).update(rating="strong")
        assessment = submit_term_assessment(assessment, self.student)
        report = generate_term_assessment_report(assessment)
        self.assertIn(
            "fluency stands out as a particular strength",
            report["performance_summary"]["speaking"],
        )
    def test_report_rejects_missing_subskill_rating(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        # Simulate incomplete persisted data without modifying
        # the submitted record through its protected save() method.
        StudentTermSubSkillAssessment.objects.filter(
            skill_snapshot__term_assessment=assessment,
            skill_snapshot__skill="speaking",
            subskill="fluency",
        ).update(rating=None)
        with self.assertRaises(ValidationError):
            generate_term_assessment_report(assessment)
    def test_report_rejects_missing_skill_score(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        StudentSkillTermSnapshot.objects.filter(
            term_assessment=assessment,
            skill="speaking",
        ).update(score=None)
        with self.assertRaises(ValidationError):
            generate_term_assessment_report(assessment)
    def test_report_generation_does_not_modify_assessment(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        original_score = assessment.overall_score
        original_submitted_at = assessment.submitted_at
        original_updated_at = assessment.updated_at
        original_ratings = list(
            StudentTermSubSkillAssessment.objects.filter(
                skill_snapshot__term_assessment=assessment,
            ).order_by("pk").values_list("pk", "rating")
        )
        generate_term_assessment_report(assessment)
        assessment.refresh_from_db()
        current_ratings = list(
            StudentTermSubSkillAssessment.objects.filter(
                skill_snapshot__term_assessment=assessment,
            ).order_by("pk").values_list("pk", "rating")
        )
        self.assertEqual(assessment.overall_score, original_score)
        self.assertEqual(assessment.submitted_at, original_submitted_at)
        self.assertEqual(assessment.updated_at, original_updated_at)
        self.assertEqual(current_ratings, original_ratings)
    def test_report_generation_does_not_modify_ongoing_assessment(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        update_term_subskill_rating(formal_fluency, "strong")
        assessment = submit_term_assessment(assessment, self.student)
        ongoing_before = self.get_ongoing_fluency().rating
        generate_term_assessment_report(assessment)
        ongoing_after = self.get_ongoing_fluency().rating
        self.assertEqual(ongoing_before, ongoing_after)
        self.assertEqual(ongoing_after, "satisfactory")
    def test_report_generation_is_deterministic(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        first_report = generate_term_assessment_report(assessment)
        second_report = generate_term_assessment_report(assessment)
        self.assertEqual(first_report, second_report)
    # ---------------------------------------------------------
    # PERSISTENT FORMAL TERM ASSESSMENT REPORTS
    # ---------------------------------------------------------
    def test_creates_persistent_report_for_submitted_assessment(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        report = create_term_assessment_report(assessment, self.student)
        self.assertEqual(report.assessment, assessment)
        self.assertEqual(report.generated_by, self.student)
        self.assertIsNotNone(report.generated_at)
        self.assertEqual(StudentTermAssessmentReport.objects.count(), 1)
    def test_persistent_report_contains_generated_content(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        report = create_term_assessment_report(assessment, self.student)
        report.refresh_from_db()
        self.assertEqual(report.content["assessment_id"], assessment.pk)
        self.assertEqual(report.content["overall_score"], "6.0")
        self.assertEqual(len(report.content["skills"]), 4)
        self.assertEqual(len(report.content["development_priorities"]), 4)
        self.assertEqual(len(report.content["next_term_priorities"]), 3)
        for skill in ("speaking", "reading", "listening", "writing"):
            self.assertTrue(report.content["development_priorities"][skill])
        self.assertIn("performance_summary", report.content)
        self.assertIn("next_term_focus", report.content)
    def test_persistent_report_serializes_date(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        report = create_term_assessment_report(assessment, self.student)
        self.assertEqual(
            report.content["assessment_date"],
            assessment.assessment_date.isoformat(),
        )
    def test_draft_cannot_have_persistent_report(self):
        assessment, _ = self.create_draft()
        with self.assertRaises(ValidationError):
            create_term_assessment_report(assessment, self.student)
        self.assertFalse(StudentTermAssessmentReport.objects.exists())
    def test_report_requires_generating_user(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        with self.assertRaises(ValidationError):
            create_term_assessment_report(assessment, None)
        self.assertFalse(StudentTermAssessmentReport.objects.exists())
    def test_report_cannot_be_generated_twice(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        first = create_term_assessment_report(assessment, self.student)
        with self.assertRaises(ValidationError):
            create_term_assessment_report(assessment, self.student)
        self.assertEqual(StudentTermAssessmentReport.objects.count(), 1)
        self.assertEqual(assessment.report.pk, first.pk)
    def test_database_prevents_duplicate_reports(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        first = create_term_assessment_report(assessment, self.student)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                StudentTermAssessmentReport.objects.bulk_create([
                    StudentTermAssessmentReport(
                        assessment=assessment,
                        content={"test": "duplicate"},
                        generated_by=self.student,
                    )
                ])
        # Verify the original report remains intact in the database.
        reports = StudentTermAssessmentReport.objects.filter(
            assessment_id=assessment.pk
        )
        self.assertEqual(reports.count(), 1)
        self.assertEqual(reports.get().pk, first.pk)
    def test_generated_report_cannot_be_modified(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        report = create_term_assessment_report(assessment, self.student)
        original_content = report.content.copy()
        report.content = {"modified": True}
        with self.assertRaises(ValidationError):
            report.save()
        report.refresh_from_db()
        self.assertEqual(report.content, original_content)
    def test_generated_report_cannot_be_deleted_directly(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        report = create_term_assessment_report(assessment, self.student)
        with self.assertRaises(ValidationError):
            report.delete()
        self.assertTrue(
            StudentTermAssessmentReport.objects.filter(pk=report.pk).exists()
        )
    def test_report_generation_does_not_modify_submitted_assessment(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        original_score = assessment.overall_score
        original_submitted_at = assessment.submitted_at
        original_updated_at = assessment.updated_at
        create_term_assessment_report(assessment, self.student)
        assessment.refresh_from_db()
        self.assertEqual(assessment.overall_score, original_score)
        self.assertEqual(assessment.submitted_at, original_submitted_at)
        self.assertEqual(assessment.updated_at, original_updated_at)
        self.assertEqual(
            assessment.status,
            StudentTermAssessment.Status.SUBMITTED,
        )
    def test_report_generation_does_not_modify_ongoing_assessment(self):
        assessment, _ = self.create_draft()
        formal_fluency = self.get_formal_fluency(assessment)
        update_term_subskill_rating(formal_fluency, "strong")
        assessment = submit_term_assessment(assessment, self.student)
        ongoing_before = self.get_ongoing_fluency().rating
        create_term_assessment_report(assessment, self.student)
        ongoing_after = self.get_ongoing_fluency().rating
        self.assertEqual(ongoing_before, ongoing_after)
        self.assertEqual(ongoing_after, "satisfactory")
    def test_report_creation_rolls_back_on_generation_failure(self):
        assessment, _ = self.create_draft()
        assessment = submit_term_assessment(assessment, self.student)
        with patch(
            "profiles.utils.term_assessment_reports.generate_term_assessment_report",
            side_effect=RuntimeError("Simulated generation failure"),
        ):
            with self.assertRaises(RuntimeError):
                create_term_assessment_report(assessment, self.student)
        self.assertFalse(StudentTermAssessmentReport.objects.exists())


class TermAssessmentDetailViewTests(TestCase):
    """HTTP tests for the teacher's formal Term Assessment editor."""
    @classmethod
    def setUpTestData(cls):
        cls.student = get_user_model().objects.create_user(
            username="term_view_student",
            email="term-view-student@example.com",
            password="TestPassword123!",
        )
        cls.teacher = get_user_model().objects.create_user(
            username="term_view_teacher",
            email="term-view-teacher@example.com",
            password="TestPassword123!",
        )
        cls.other_teacher = get_user_model().objects.create_user(
            username="term_view_other_teacher",
            email="term-view-other-teacher@example.com",
            password="TestPassword123!",
        )
        for teacher in (cls.teacher, cls.other_teacher):
            UserProfile.objects.update_or_create(
                user=teacher,
                defaults={"role": UserProfile.ROLE_TEACHER},
            )
        cls.course_type = CourseType.objects.create(
            name="Term Assessment View Test Course Type",
        )
        cls.course = Course.objects.create(
            name="Term Assessment View Test Course",
            course_type=cls.course_type,
            teacher=cls.teacher,
        )
        cls.enrollment = CourseEnrollment.objects.create(
            student=cls.student,
            course=cls.course,
        )
        for skill, subskills in SUBSKILLS.items():
            skill_assessment = StudentSkillAssessment.objects.create(
                student=cls.student,
                course=cls.course,
                skill=skill,
            )
            for subskill, _ in subskills:
                StudentSubSkillAssessment.objects.create(
                    skill_assessment=skill_assessment,
                    subskill=subskill,
                    rating="satisfactory",
                )
    def setUp(self):
        self.client.force_login(self.teacher)
        self.assessment, _ = get_or_create_term_assessment_draft(
            enrollment=self.enrollment,
            term_label="Test Term 1",
        )
        self.formal_fluency = self.get_formal_fluency(self.assessment)
        self.url = reverse(
            "profiles:teacher_term_assessment_detail",
            kwargs={
                "course_id": self.course.pk,
                "enrollment_id": self.enrollment.pk,
                "assessment_id": self.assessment.pk,
            },
        )
    def get_formal_fluency(self, assessment):
        return StudentTermSubSkillAssessment.objects.get(
            skill_snapshot__term_assessment=assessment,
            skill_snapshot__skill="speaking",
            subskill="fluency",
        )
    def get_ongoing_fluency(self):
        return StudentSubSkillAssessment.objects.get(
            skill_assessment__student=self.student,
            skill_assessment__course=self.course,
            skill_assessment__skill="speaking",
            subskill="fluency",
        )
    def create_draft(self, term_label="Test Term 1"):
        return get_or_create_term_assessment_draft(
            enrollment=self.enrollment,
            term_label=term_label,
        )
    def post_rating(self, rating, subskill=None):
        return self.client.post(
            self.url,
            {
                "subskill_id": (
                    subskill.pk if subskill is not None
                    else self.formal_fluency.pk
                ),
                "rating": rating,
            },
        )
    # ---------------------------------------------------------
    # VALID DRAFT EDITING
    # ---------------------------------------------------------
    def test_teacher_can_open_assessment_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["assessment"], self.assessment)
        self.assertEqual(response.context["total_subskills"], 14)
        self.assertEqual(response.context["assessed_subskills"], 14)
    def test_teacher_can_save_valid_rating(self):
        response = self.post_rating("strong")
        self.assertRedirects(response, self.url)
        self.formal_fluency.refresh_from_db()
        self.assertEqual(self.formal_fluency.rating, "strong")
    def test_teacher_can_clear_rating(self):
        response = self.post_rating("")
        self.assertRedirects(response, self.url)
        self.formal_fluency.refresh_from_db()
        self.assertIsNone(self.formal_fluency.rating)
    def test_saving_rating_does_not_submit_assessment(self):
        self.post_rating("strong")
        self.assessment.refresh_from_db()
        self.assertEqual(
            self.assessment.status,
            StudentTermAssessment.Status.DRAFT,
        )
        self.assertIsNone(self.assessment.overall_score)
        self.assertIsNone(self.assessment.submitted_at)
        self.assertFalse(
            self.assessment.skill_snapshots.filter(
                score__isnull=False,
            ).exists()
        )
    def test_formal_edit_does_not_change_ongoing_rating(self):
        ongoing_fluency = self.get_ongoing_fluency()
        original_rating = ongoing_fluency.rating
        self.post_rating("strong")
        self.formal_fluency.refresh_from_db()
        ongoing_fluency.refresh_from_db()
        self.assertEqual(self.formal_fluency.rating, "strong")
        self.assertEqual(ongoing_fluency.rating, original_rating)
    # ---------------------------------------------------------
    # INVALID INPUT
    # ---------------------------------------------------------
    def test_invalid_rating_is_rejected(self):
        response = self.post_rating("invalid_rating")
        self.assertRedirects(response, self.url)
        self.formal_fluency.refresh_from_db()
        self.assertEqual(
            self.formal_fluency.rating,
            "satisfactory",
        )
    def test_subskill_from_another_assessment_is_rejected(self):
        other_assessment, _ = self.create_draft("Different Term")
        other_subskill = self.get_formal_fluency(other_assessment)
        response = self.post_rating("strong", subskill=other_subskill)
        self.assertEqual(response.status_code, 404)
        other_subskill.refresh_from_db()
        self.formal_fluency.refresh_from_db()
        self.assertEqual(other_subskill.rating, "satisfactory")
        self.assertEqual(self.formal_fluency.rating, "satisfactory")
    def test_nonexistent_subskill_is_rejected(self):
        response = self.client.post(
            self.url,
            {"subskill_id": 999999999, "rating": "strong"},
        )
        self.assertEqual(response.status_code, 404)
        self.formal_fluency.refresh_from_db()
        self.assertEqual(
            self.formal_fluency.rating,
            "satisfactory",
        )
    # ---------------------------------------------------------
    # TEACHER OWNERSHIP AND ACCESS
    # ---------------------------------------------------------
    def test_other_teacher_cannot_view_assessment(self):
        self.client.force_login(self.other_teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
    def test_other_teacher_cannot_update_assessment(self):
        self.client.force_login(self.other_teacher)
        response = self.post_rating("strong")
        self.assertEqual(response.status_code, 404)
        self.formal_fluency.refresh_from_db()
        self.assertEqual(
            self.formal_fluency.rating,
            "satisfactory",
        )
    def test_student_cannot_update_assessment(self):
        self.client.force_login(self.student)
        response = self.post_rating("strong")
        self.assertRedirects(response, reverse("home"))
        self.formal_fluency.refresh_from_db()
        self.assertEqual(
            self.formal_fluency.rating,
            "satisfactory",
        )
    def test_anonymous_user_cannot_access_assessment(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)
    # ---------------------------------------------------------
    # SUBMITTED ASSESSMENT PROTECTION
    # ---------------------------------------------------------
    def test_submitted_assessment_is_read_only(self):
        submit_term_assessment(self.assessment, self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assessment.refresh_from_db()
        self.assertEqual(
            self.assessment.status,
            StudentTermAssessment.Status.SUBMITTED,
        )
    def test_submitted_assessment_rejects_manual_post(self):
        submit_term_assessment(self.assessment, self.teacher)
        response = self.post_rating("strong")
        self.assertRedirects(response, self.url)
        self.formal_fluency.refresh_from_db()
        self.assessment.refresh_from_db()
        self.assertEqual(
            self.formal_fluency.rating,
            "satisfactory",
        )
        self.assertEqual(
            self.assessment.status,
            StudentTermAssessment.Status.SUBMITTED,
        )
        self.assertEqual(
            self.assessment.overall_score,
            Decimal("6.0"),
        )
    # ---------------------------------------------------------
    # HTTP ASSESSMENT SUBMISSION
    # ---------------------------------------------------------
    def test_teacher_can_submit_complete_assessment(self):
        response = self.client.post(self.url, {"action": "submit"})
        self.assertRedirects(response, self.url)
        self.assessment.refresh_from_db()
        self.assertEqual(
            self.assessment.status,
            StudentTermAssessment.Status.SUBMITTED,
        )
        self.assertEqual(self.assessment.teacher, self.teacher)
        self.assertEqual(self.assessment.overall_score, Decimal("6.0"))
        self.assertIsNotNone(self.assessment.assessment_date)
        self.assertIsNotNone(self.assessment.submitted_at)
        for snapshot in self.assessment.skill_snapshots.all():
            self.assertEqual(snapshot.score, Decimal("6.0"))
    def test_incomplete_assessment_cannot_be_submitted(self):
        self.post_rating("")
        response = self.client.post(self.url, {"action": "submit"})
        self.assertRedirects(response, self.url)
        self.assessment.refresh_from_db()
        self.assertEqual(
            self.assessment.status,
            StudentTermAssessment.Status.DRAFT,
        )
        self.assertIsNone(self.assessment.overall_score)
        self.assertIsNone(self.assessment.submitted_at)
        self.assertFalse(
            self.assessment.skill_snapshots.filter(
                score__isnull=False,
            ).exists()
        )
    def test_submitted_assessment_cannot_be_submitted_again(self):
        self.client.post(self.url, {"action": "submit"})
        self.assessment.refresh_from_db()
        original_submitted_at = self.assessment.submitted_at
        response = self.client.post(self.url, {"action": "submit"})
        self.assertRedirects(response, self.url)
        self.assessment.refresh_from_db()
        self.assertEqual(
            self.assessment.status,
            StudentTermAssessment.Status.SUBMITTED,
        )
        self.assertEqual(self.assessment.submitted_at, original_submitted_at)
        self.assertEqual(self.assessment.overall_score, Decimal("6.0"))
    def test_other_teacher_cannot_submit_assessment(self):
        self.client.force_login(self.other_teacher)
        response = self.client.post(self.url, {"action": "submit"})
        self.assertEqual(response.status_code, 404)
        self.assessment.refresh_from_db()
        self.assertEqual(
            self.assessment.status,
            StudentTermAssessment.Status.DRAFT,
        )
        self.assertIsNone(self.assessment.submitted_at)
    def test_student_cannot_submit_assessment(self):
        self.client.force_login(self.student)
        response = self.client.post(self.url, {"action": "submit"})
        self.assertRedirects(response, reverse("home"))
        self.assessment.refresh_from_db()
        self.assertEqual(
            self.assessment.status,
            StudentTermAssessment.Status.DRAFT,
        )
    def test_unknown_action_does_not_submit_assessment(self):
        response = self.client.post(
            self.url,
            {"action": "invalid_action"},
        )
        self.assertRedirects(response, self.url)
        self.assessment.refresh_from_db()
        self.assertEqual(
            self.assessment.status,
            StudentTermAssessment.Status.DRAFT,
        )
        self.assertIsNone(self.assessment.overall_score)
    def test_submitted_assessment_displays_read_only_ratings(self):
        self.client.post(self.url, {"action": "submit"})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submitted")
        self.assertNotContains(response, 'name="rating"')
        self.assertNotContains(response, 'name="action" value="submit"')

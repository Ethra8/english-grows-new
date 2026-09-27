
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from courses.models import Course, CourseEnrollment, CourseType
from profiles.forms import StudentSubSkillAssessmentFormSet
from profiles.models import (
    Company,
    StudentSkillAssessment,
    StudentSkillAssessmentSnapshot,
    StudentSkillTermSnapshot,
    StudentSubSkillAssessment,
    UserProfile,
    SUBSKILLS,
)

from profiles.utils.skills import build_student_skill_cards
from profiles.views import (
    build_skill_note_display,
    build_skill_progress_chart_data,
    build_overall_skill_progress_chart_data,
)


User = get_user_model()
Rating = StudentSubSkillAssessment.Rating


class SkillAssessmentTestMixin:
    @classmethod
    def setUpTestData(cls):
        cls.teacher = User.objects.create_user(
            username="skills_teacher",
            password="TestPassword123!",
        )
        cls.other_teacher = User.objects.create_user(
            username="skills_other_teacher",
            password="TestPassword123!",
        )
        cls.student = User.objects.create_user(
            username="skills_student",
            password="TestPassword123!",
        )

        # Profiles may already be created by the project's user signal.
        for user, role in (
            (cls.teacher, UserProfile.ROLE_TEACHER),
            (cls.other_teacher, UserProfile.ROLE_TEACHER),
            (cls.student, UserProfile.ROLE_INDIVIDUAL_LEARNER),
        ):
            UserProfile.objects.update_or_create(
                user=user,
                defaults={"role": role},
            )

        cls.course_type = CourseType.objects.create(
            name="Skills Assessment Test Course",
            is_for_individual=True,
        )
        cls.course = Course.objects.create(
            course_type=cls.course_type,
            name="Skills Assessment Test",
            teacher=cls.teacher,
            status="active",
        )
        cls.enrollment = CourseEnrollment.objects.create(
            course=cls.course,
            student=cls.student,
            status=CourseEnrollment.STATUS_ACTIVE,
        )
        cls.assessment = StudentSkillAssessment.objects.create(
            student=cls.student,
            course=cls.course,
            skill="speaking",
        )

        # Use the actual model choices rather than inventing subskill codes.
        cls.subskill_codes = [
            value
            for value, label in StudentSubSkillAssessment._meta.get_field(
                "subskill"
            ).choices
            if value
        ]

        cls.subskills = [
            StudentSubSkillAssessment.objects.create(
                skill_assessment=cls.assessment,
                subskill=code,
                rating=None,
            )
            for code in cls.subskill_codes[:3]
        ]

    def set_rating(self, index, rating):
        subskill = self.subskills[index]
        subskill.rating = rating
        subskill.save(update_fields=["rating", "updated_at"])
        return subskill

    def snapshot_scores(self):
        return list(
            StudentSkillAssessmentSnapshot.objects.filter(
                skill_assessment=self.assessment
            )
            .order_by("pk")
            .values_list("score", flat=True)
        )


class SkillAssessmentModelTests(SkillAssessmentTestMixin, TestCase):
    def test_unrated_subskill_has_no_score(self):
        self.assertIsNone(self.subskills[0].score)
        self.assertIsNone(self.assessment.average_score)

    def test_blank_rating_has_no_score(self):
        self.set_rating(0, "")
        self.assertIsNone(self.subskills[0].score)
        self.assertIsNone(self.assessment.average_score)

    def test_rating_score_mapping(self):
        expected = {
            Rating.NEEDS_WORK: Decimal("4.0"),
            Rating.DEVELOPING: Decimal("5.0"),
            Rating.REQUIRED_STANDARD: Decimal("6.0"),
            Rating.CONFIDENT: Decimal("7.5"),
            Rating.STRONG: Decimal("10.0"),
        }

        for rating, score in expected.items():
            with self.subTest(rating=rating):
                self.subskills[0].rating = rating
                self.assertEqual(self.subskills[0].score, score)

    def test_average_excludes_unrated_subskills(self):
        self.set_rating(0, Rating.STRONG)
        self.set_rating(1, Rating.DEVELOPING)

        self.assertEqual(
            self.assessment.average_score,
            Decimal("7.5"),
        )

    def test_average_rounds_half_up_to_one_decimal(self):
        self.set_rating(0, Rating.STRONG)
        self.set_rating(1, Rating.STRONG)
        self.set_rating(2, Rating.REQUIRED_STANDARD)

        # 26 / 3 = 8.666... -> 8.7
        self.assertEqual(
            self.assessment.average_score,
            Decimal("8.7"),
        )

    def test_clearing_all_ratings_removes_current_average(self):
        self.set_rating(0, Rating.STRONG)
        self.assertEqual(self.assessment.average_score, Decimal("10.0"))

        self.set_rating(0, None)
        self.assertIsNone(self.assessment.average_score)

    def test_saving_individual_subskill_does_not_create_snapshot(self):
        self.set_rating(0, Rating.STRONG)
        self.set_rating(1, Rating.CONFIDENT)

        self.assertEqual(self.snapshot_scores(), [])

    def test_assessment_has_no_retired_teacher_notes_field(self):
        field_names = {
            field.name
            for field in StudentSkillAssessment._meta.get_fields()
        }
        self.assertNotIn("teacher_notes", field_names)

    def test_student_course_skill_combination_is_unique(self):
        from django.db import IntegrityError, transaction

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                StudentSkillAssessment.objects.create(
                    student=self.student,
                    course=self.course,
                    skill="speaking",
                )


class SkillAssessmentFormsetTests(SkillAssessmentTestMixin, TestCase):
    def test_existing_subskills_are_included(self):
        formset = StudentSubSkillAssessmentFormSet(
            instance=self.assessment
        )

        self.assertEqual(
            formset.initial_form_count(),
            len(self.subskills),
        )

    def test_rating_is_optional(self):
        formset = StudentSubSkillAssessmentFormSet(
            instance=self.assessment
        )

        for form in formset.forms:
            self.assertFalse(form.fields["rating"].required)

    def test_all_rating_choices_are_available(self):
        formset = StudentSubSkillAssessmentFormSet(
            instance=self.assessment
        )
        available = {
            value
            for value, label in formset.forms[0].fields["rating"].choices
        }

        self.assertTrue(
            {
                Rating.NEEDS_WORK,
                Rating.DEVELOPING,
                Rating.REQUIRED_STANDARD,
                Rating.CONFIDENT,
                Rating.STRONG,
            }.issubset(available)
        )


class TeacherSkillAssessmentViewTests(SkillAssessmentTestMixin, TestCase):
    def setUp(self):
        self.url = reverse(
            "profiles:teacher_edit_student_skill",
            args=[self.assessment.pk],
        )
        self.client.force_login(self.teacher)

    def post_ratings(self, ratings):
        """
        Construct POST data from the actual Django formset.

        This avoids guessing the formset prefix or management-form
        field names and includes every existing subskill.
        """
        formset = StudentSubSkillAssessmentFormSet(
            instance=self.assessment
        )
        data = {
            key: str(value)
            for key, value in formset.management_form.initial.items()
        }
        prefix = formset.prefix

        data = {
            f"{prefix}-{key}": value
            for key, value in data.items()
        }

        for index, form in enumerate(formset.initial_forms):
            subskill = form.instance
            data[f"{prefix}-{index}-id"] = str(subskill.pk)
            data[f"{prefix}-{index}-rating"] = ratings.get(
                subskill.pk,
                subskill.rating or "",
            )

        return self.client.post(self.url, data)

    def test_teacher_can_open_assessment_form(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("formset", response.context)

    def test_valid_submission_saves_ratings_and_one_snapshot(self):
        response = self.post_ratings({
            self.subskills[0].pk: Rating.STRONG,
            self.subskills[1].pk: Rating.DEVELOPING,
        })

        self.assertEqual(response.status_code, 302)

        self.subskills[0].refresh_from_db()
        self.subskills[1].refresh_from_db()

        self.assertEqual(self.subskills[0].rating, Rating.STRONG)
        self.assertEqual(self.subskills[1].rating, Rating.DEVELOPING)
        self.assertEqual(
            self.assessment.average_score,
            Decimal("7.5"),
        )
        self.assertEqual(
            self.snapshot_scores(),
            [Decimal("7.5")],
        )

    def test_unchanged_submission_creates_another_snapshot(self):
        ratings = {
            self.subskills[0].pk: Rating.STRONG,
            self.subskills[1].pk: Rating.DEVELOPING,
        }

        self.assertEqual(self.post_ratings(ratings).status_code, 302)
        self.assertEqual(self.post_ratings(ratings).status_code, 302)

        self.assertEqual(
            self.snapshot_scores(),
            [Decimal("7.5"), Decimal("7.5")],
        )

    def test_later_submission_preserves_previous_snapshot(self):
        self.post_ratings({
            self.subskills[0].pk: Rating.STRONG,
            self.subskills[1].pk: Rating.DEVELOPING,
        })
        self.post_ratings({
            self.subskills[0].pk: Rating.STRONG,
            self.subskills[1].pk: Rating.CONFIDENT,
        })

        self.assertEqual(
            self.snapshot_scores(),
            [Decimal("7.5"), Decimal("8.8")],
        )

    def test_completely_unrated_submission_creates_no_snapshot(self):
        response = self.post_ratings({})

        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.assessment.average_score)
        self.assertEqual(self.snapshot_scores(), [])

    def test_clearing_all_ratings_does_not_create_new_snapshot(self):
        self.post_ratings({
            self.subskills[0].pk: Rating.STRONG,
        })

        response = self.post_ratings({
            subskill.pk: ""
            for subskill in self.subskills
        })

        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.assessment.average_score)

        # Historical assessment remains intact.
        self.assertEqual(
            self.snapshot_scores(),
            [Decimal("10.0")],
        )

    def test_invalid_rating_saves_nothing(self):
        response = self.post_ratings({
            self.subskills[0].pk: Rating.STRONG,
            self.subskills[1].pk: "invalid_rating",
        })

        self.assertEqual(response.status_code, 200)

        self.subskills[0].refresh_from_db()
        self.subskills[1].refresh_from_db()

        self.assertFalse(self.subskills[0].rating)
        self.assertFalse(self.subskills[1].rating)
        self.assertEqual(self.snapshot_scores(), [])

    def test_submission_does_not_create_formal_term_snapshot(self):
        before = StudentSkillTermSnapshot.objects.count()

        self.post_ratings({
            self.subskills[0].pk: Rating.STRONG,
        })

        self.assertEqual(
            StudentSkillTermSnapshot.objects.count(),
            before,
        )

    def test_unassigned_teacher_cannot_access_assessment(self):
        self.client.force_login(self.other_teacher)

        self.assertEqual(
            self.client.get(self.url).status_code,
            404,
        )

    def test_unassigned_teacher_cannot_submit_assessment(self):
        self.client.force_login(self.other_teacher)

        response = self.post_ratings({
            self.subskills[0].pk: Rating.STRONG,
        })

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.snapshot_scores(), [])

    def test_student_cannot_access_teacher_assessment(self):
        self.client.force_login(self.student)

        self.assertEqual(
            self.client.get(self.url).status_code,
            404,
        )

    def test_anonymous_user_is_redirected_to_login(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)




# =========================================================
# SHARED SKILL CARD HELPER
# =========================================================

class SkillCardHelperTests(SkillAssessmentTestMixin, TestCase):

    def build_cards(self):
        return build_student_skill_cards(
            student=self.student,
            course=self.course,
            build_skill_note_display=build_skill_note_display,
        )

    def test_returns_all_four_skills(self):
        assessments, skills = self.build_cards()

        self.assertEqual(len(skills), 4)
        self.assertEqual(
            [skill["skill_value"] for skill in skills],
            ["listening", "reading", "speaking", "writing"],
        )

    def test_missing_assessments_have_empty_cards(self):
        _, skills = self.build_cards()

        for skill in skills:
            if skill["skill_value"] == "speaking":
                continue

            self.assertIsNone(skill["assessment"])
            self.assertIsNone(skill["assessment_id"])
            self.assertIsNone(skill["score"])
            self.assertEqual(skill["assessed_subskills_count"], 0)
            self.assertEqual(skill["strengths"], [])
            self.assertEqual(skill["confident"], [])
            self.assertEqual(skill["required_standard"], [])
            self.assertEqual(skill["developing"], [])
            self.assertEqual(skill["needs_work"], [])

    def test_cards_include_canonical_subskills(self):
        _, skills = self.build_cards()

        for skill in skills:
            expected = SUBSKILLS[skill["skill_value"]]

            self.assertEqual(
                skill["total_subskills_count"],
                len(expected),
            )
            self.assertEqual(
                [item["value"] for item in skill["subskills"]],
                [value for value, label in expected],
            )

    def test_unrated_subskills_are_not_assessed(self):
        _, skills = self.build_cards()
        speaking = next(
            skill for skill in skills
            if skill["skill_value"] == "speaking"
        )

        self.assertIsNone(speaking["score"])
        self.assertEqual(speaking["assessed_subskills_count"], 0)

        for subskill in speaking["subskills"]:
            self.assertFalse(subskill["is_assessed"])
            self.assertIsNone(subskill["rating"])

    def test_rated_subskills_update_count_and_score(self):
        self.set_rating(0, Rating.STRONG)
        self.set_rating(1, Rating.DEVELOPING)

        _, skills = self.build_cards()
        speaking = next(
            skill for skill in skills
            if skill["skill_value"] == "speaking"
        )

        self.assertEqual(speaking["assessed_subskills_count"], 2)
        self.assertEqual(speaking["score"], Decimal("7.5"))

        assessed = [
            item for item in speaking["subskills"]
            if item["is_assessed"]
        ]
        self.assertEqual(len(assessed), 2)

    def test_helper_does_not_create_database_records(self):
        before_assessments = StudentSkillAssessment.objects.count()
        before_subskills = StudentSubSkillAssessment.objects.count()

        self.build_cards()

        self.assertEqual(
            StudentSkillAssessment.objects.count(),
            before_assessments,
        )
        self.assertEqual(
            StudentSubSkillAssessment.objects.count(),
            before_subskills,
        )

    def test_helper_does_not_expose_retired_teacher_notes(self):
        _, skills = self.build_cards()

        for skill in skills:
            self.assertNotIn("teacher_notes", skill)


# =========================================================
# STRUCTURED RATING CATEGORIES
# =========================================================

class SkillRatingDisplayTests(SkillAssessmentTestMixin, TestCase):

    def test_all_five_rating_categories(self):
        expected = {
            "strengths": Rating.STRONG,
            "confident": Rating.CONFIDENT,
            "required_standard": Rating.REQUIRED_STANDARD,
            "developing": Rating.DEVELOPING,
            "needs_work": Rating.NEEDS_WORK,
        }

        for category, rating in expected.items():
            with self.subTest(category=category):
                self.subskills[0].rating = rating
                self.subskills[0].save(update_fields=["rating"])

                display = build_skill_note_display(self.assessment)

                self.assertIn(
                    self.subskills[0].get_subskill_display(),
                    display[category],
                )

    def test_unrated_subskills_are_excluded(self):
        display = build_skill_note_display(self.assessment)

        for category in (
            "strengths",
            "confident",
            "required_standard",
            "developing",
            "needs_work",
        ):
            self.assertEqual(display[category], [])

    def test_display_contains_current_average(self):
        self.set_rating(0, Rating.STRONG)
        self.set_rating(1, Rating.DEVELOPING)

        display = build_skill_note_display(self.assessment)

        self.assertEqual(display["score"], Decimal("7.5"))
        self.assertEqual(display["skill"], "Speaking")

    def test_display_does_not_contain_obsolete_plain_notes(self):
        display = build_skill_note_display(self.assessment)

        self.assertNotIn("plain_notes", display)
        self.assertNotIn("teacher_notes", display)


# =========================================================
# HISTORICAL SKILL PROGRESS GRAPHS
# =========================================================

class SkillProgressChartTests(SkillAssessmentTestMixin, TestCase):

    def create_snapshot(self, score, recorded_at=None):
        snapshot = StudentSkillAssessmentSnapshot.objects.create(
            skill_assessment=self.assessment,
            score=Decimal(str(score)),
        )

        if recorded_at is not None:
            StudentSkillAssessmentSnapshot.objects.filter(
                pk=snapshot.pk
            ).update(recorded_at=recorded_at)

        return snapshot

    def test_empty_history_has_no_chart_points(self):
        chart = build_skill_progress_chart_data(
            self.student,
            self.course,
        )

        self.assertEqual(chart["labels"], [])
        self.assertTrue(
            all(not dataset["data"] for dataset in chart["datasets"])
        )

    def test_snapshot_appears_in_correct_skill_dataset(self):
        self.create_snapshot("7.5")

        chart = build_skill_progress_chart_data(
            self.student,
            self.course,
        )
        datasets = {
            dataset["label"].lower(): dataset["data"]
            for dataset in chart["datasets"]
        }

        self.assertEqual(len(chart["labels"]), 1)
        self.assertEqual(datasets["speaking"], [7.5])

        for skill in ("listening", "reading", "writing"):
            self.assertEqual(datasets[skill], [None])

    def test_last_snapshot_on_same_day_is_used(self):
        self.create_snapshot("5.0")
        self.create_snapshot("7.5")
        self.create_snapshot("10.0")

        chart = build_skill_progress_chart_data(
            self.student,
            self.course,
        )
        datasets = {
            dataset["label"].lower(): dataset["data"]
            for dataset in chart["datasets"]
        }

        self.assertEqual(len(chart["labels"]), 1)
        self.assertEqual(datasets["speaking"], [10.0])

    def test_snapshots_on_different_days_are_chronological(self):
        now = timezone.now()

        self.create_snapshot("5.0", now - timedelta(days=2))
        self.create_snapshot("7.5", now - timedelta(days=1))
        self.create_snapshot("10.0", now)

        chart = build_skill_progress_chart_data(
            self.student,
            self.course,
        )
        datasets = {
            dataset["label"].lower(): dataset["data"]
            for dataset in chart["datasets"]
        }

        self.assertEqual(len(chart["labels"]), 3)
        self.assertEqual(
            datasets["speaking"],
            [5.0, 7.5, 10.0],
        )

    def test_other_student_history_is_excluded(self):
        other_student = User.objects.create_user(
            username="other_skills_student",
            password="TestPassword123!",
        )
        other_assessment = StudentSkillAssessment.objects.create(
            student=other_student,
            course=self.course,
            skill="speaking",
        )
        StudentSkillAssessmentSnapshot.objects.create(
            skill_assessment=other_assessment,
            score=Decimal("10.0"),
        )

        chart = build_skill_progress_chart_data(
            self.student,
            self.course,
        )

        self.assertEqual(chart["labels"], [])

    def test_overall_chart_requires_all_four_skill_scores(self):
        self.create_snapshot("7.5")

        chart = build_overall_skill_progress_chart_data(
            self.student,
            self.course,
        )

        self.assertEqual(chart["labels"], [])




# =========================================================
# SKILLS PAGE INTEGRATION TESTS
# =========================================================

class LearnerSkillsPageTests(SkillAssessmentTestMixin, TestCase):

    def setUp(self):
        self.client.force_login(self.student)
        self.url = reverse("profiles:my_skills")

    def test_learner_can_access_skills_page(self):
        response = self.client.get(
            self.url,
            {"course": self.course.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "profiles/student/my_skills.html",
        )
        self.assertEqual(response.context["course"], self.course)
        self.assertEqual(len(response.context["skills"]), 4)

    def test_learner_without_enrollment_sees_four_empty_cards(self):
        self.enrollment.delete()

        before = StudentSkillAssessment.objects.count()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["course"])
        self.assertIsNone(response.context["enrollment"])
        self.assertFalse(response.context["has_skill_assessment"])
        self.assertEqual(len(response.context["skills"]), 4)
        self.assertEqual(
            StudentSkillAssessment.objects.count(),
            before,
        )

        for skill in response.context["skills"]:
            self.assertIsNone(skill["score"])
            self.assertEqual(skill["assessed_subskills_count"], 0)

    def test_unrated_assessment_does_not_count_as_assessed(self):
        response = self.client.get(
            self.url,
            {"course": self.course.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["has_skill_assessment"])

    def test_rated_assessment_appears_in_learner_context(self):
        self.set_rating(0, Rating.STRONG)
        self.set_rating(1, Rating.DEVELOPING)

        response = self.client.get(
            self.url,
            {"course": self.course.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["has_skill_assessment"])

        speaking = next(
            skill for skill in response.context["skills"]
            if skill["skill_value"] == "speaking"
        )

        self.assertEqual(speaking["score"], Decimal("7.5"))
        self.assertEqual(speaking["assessed_subskills_count"], 2)

    def test_learner_cannot_select_another_students_course(self):
        other_student = User.objects.create_user(
            username="unrelated_learner",
            password="TestPassword123!",
        )
        other_course = Course.objects.create(
            course_type=self.course_type,
            name="Unrelated Learner Course",
            teacher=self.teacher,
            status="active",
        )
        CourseEnrollment.objects.create(
            course=other_course,
            student=other_student,
            status=CourseEnrollment.STATUS_ACTIVE,
        )

        response = self.client.get(
            self.url,
            {"course": other_course.pk},
        )

        self.assertEqual(response.status_code, 404)

    def test_learner_page_does_not_create_assessments(self):
        before = StudentSkillAssessment.objects.count()

        self.client.get(
            self.url,
            {"course": self.course.pk},
        )

        self.assertEqual(
            StudentSkillAssessment.objects.count(),
            before,
        )


# =========================================================
# TEACHER SKILLS OVERVIEW
# =========================================================

class TeacherSkillsOverviewTests(SkillAssessmentTestMixin, TestCase):

    def setUp(self):
        self.client.force_login(self.teacher)
        self.url = reverse(
            "profiles:student_skills_overview",
            args=[self.course.pk, self.enrollment.pk],
        )

    def test_teacher_can_access_student_skills(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "profiles/teacher/student_skills_overview.html",
        )
        self.assertEqual(response.context["student"], self.student)
        self.assertEqual(response.context["course"], self.course)
        self.assertEqual(len(response.context["skills"]), 4)

    def test_teacher_creates_missing_canonical_assessments(self):
        StudentSkillAssessment.objects.filter(
            student=self.student,
            course=self.course,
        ).exclude(pk=self.assessment.pk).delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        assessments = StudentSkillAssessment.objects.filter(
            student=self.student,
            course=self.course,
        )

        self.assertEqual(assessments.count(), 4)

        for assessment in assessments:
            self.assertEqual(
                assessment.subskill_assessments.count(),
                len(SUBSKILLS[assessment.skill]),
            )

        self.assertFalse(
            StudentSkillAssessmentSnapshot.objects.filter(
                skill_assessment__student=self.student,
                skill_assessment__course=self.course,
            ).exists()
        )

    def test_teacher_overall_average_requires_all_four_skills(self):
        self.set_rating(0, Rating.STRONG)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(
            response.context["overall_average_score"]
        )

    def test_teacher_overall_average_with_four_assessed_skills(self):
        for skill in ("listening", "reading", "writing"):
            assessment, _ = StudentSkillAssessment.objects.get_or_create(
                student=self.student,
                course=self.course,
                skill=skill,
            )
            code = SUBSKILLS[skill][0][0]

            StudentSubSkillAssessment.objects.update_or_create(
                skill_assessment=assessment,
                subskill=code,
                defaults={"rating": Rating.STRONG},
            )

        self.set_rating(0, Rating.STRONG)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["overall_average_score"],
            Decimal("10.0"),
        )

    def test_unassigned_teacher_cannot_access_overview(self):
        self.client.force_login(self.other_teacher)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_student_cannot_access_teacher_overview(self):
        self.client.force_login(self.student)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)


# =========================================================
# COMPANY ADMIN SKILLS OVERVIEW
# =========================================================

class CompanyAdminSkillsOverviewTests(SkillAssessmentTestMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.company = Company.objects.create(
            name="Skills Test Company",
        )
        cls.other_company = Company.objects.create(
            name="Unrelated Test Company",
        )

        cls.admin_user = User.objects.create_user(
            username="skills_company_admin",
            password="TestPassword123!",
        )
        cls.other_admin = User.objects.create_user(
            username="skills_other_company_admin",
            password="TestPassword123!",
        )

        UserProfile.objects.update_or_create(
            user=cls.admin_user,
            defaults={
                "role": UserProfile.ROLE_COMPANY_ADMIN,
                "company": cls.company,
            },
        )
        UserProfile.objects.update_or_create(
            user=cls.other_admin,
            defaults={
                "role": UserProfile.ROLE_COMPANY_ADMIN,
                "company": cls.other_company,
            },
        )
        UserProfile.objects.filter(user=cls.student).update(
            role=UserProfile.ROLE_EMPLOYEE,
            company=cls.company,
        )

        cls.course.company = cls.company
        cls.course.save(update_fields=["company"])

    def setUp(self):
        self.client.force_login(self.admin_user)
        self.url = reverse(
            "profiles:company_admin_student_skills_overview",
            args=[self.student.pk],
        )

    def test_company_admin_can_access_employee_skills(self):
        response = self.client.get(
            self.url,
            {"course": self.course.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "profiles/company_admin/company_admin_student_skills_overview.html",
        )
        self.assertEqual(response.context["student"], self.student)
        self.assertEqual(response.context["course"], self.course)
        self.assertEqual(len(response.context["skills"]), 4)

    def test_company_admin_sees_current_assessment(self):
        self.set_rating(0, Rating.STRONG)
        self.set_rating(1, Rating.DEVELOPING)

        response = self.client.get(
            self.url,
            {"course": self.course.pk},
        )

        self.assertEqual(response.status_code, 200)

        speaking = next(
            skill for skill in response.context["skills"]
            if skill["skill_value"] == "speaking"
        )

        self.assertEqual(speaking["score"], Decimal("7.5"))
        self.assertEqual(speaking["assessed_subskills_count"], 2)

    def test_employee_without_enrollment_sees_four_empty_cards(self):
        self.enrollment.delete()

        before = StudentSkillAssessment.objects.count()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["course"])
        self.assertIsNone(response.context["enrollment"])
        self.assertEqual(len(response.context["skills"]), 4)

        for skill in response.context["skills"]:
            self.assertIsNone(skill["score"])
            self.assertEqual(skill["assessed_subskills_count"], 0)

        self.assertEqual(
            StudentSkillAssessment.objects.count(),
            before,
        )

    def test_admin_from_another_company_cannot_access_employee(self):
        self.client.force_login(self.other_admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_company_admin_cannot_select_unrelated_course(self):
        unrelated_course = Course.objects.create(
            course_type=self.course_type,
            name="Unrelated Company Course",
            teacher=self.teacher,
            company=self.other_company,
            status="active",
        )
        CourseEnrollment.objects.create(
            course=unrelated_course,
            student=self.student,
            status=CourseEnrollment.STATUS_ACTIVE,
        )

        response = self.client.get(
            self.url,
            {"course": unrelated_course.pk},
        )

        self.assertEqual(response.status_code, 404)

    def test_company_admin_page_does_not_create_assessments(self):
        before = StudentSkillAssessment.objects.count()

        response = self.client.get(
            self.url,
            {"course": self.course.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            StudentSkillAssessment.objects.count(),
            before,
        )

    def test_teacher_cannot_access_company_admin_page(self):
        self.client.force_login(self.teacher)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from ..models import PlacementAttempt, PlacementQuestion, TEST_VERSION


class PlacementPublicFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_placement_questions", stdout=StringIO())

    def setUp(self):
        # Simulate successful Turnstile verification without external requests.
        self.turnstile_patcher = patch("placement.views.verify_turnstile", return_value=True)
        self.mock_turnstile = self.turnstile_patcher.start()
        self.addCleanup(self.turnstile_patcher.stop)

        # Keep email delivery separate from public placement flow tests.
        self.email_patcher = patch("placement.views.send_placement_result_emails")
        self.mock_send_emails = self.email_patcher.start()
        self.addCleanup(self.email_patcher.stop)

    def start(self):
        response = self.client.get(reverse("placement:test"))
        self.assertEqual(response.status_code, 200)
        return response

    def valid_data(self, correct=True):
        data = {
            "name": "Example Learner",
            "email": "learner@example.com",
            "acknowledge": "on",
            "token": self.client.session["placement_test_token"],
            "cf-turnstile-response": "test-turnstile-token",
        }
        if correct:
            data.update({
                f"q_{q.number}": q.correct_answer
                for q in PlacementQuestion.objects.filter(version=TEST_VERSION)
            })
        return data

    def test_public_page_does_not_expose_answer_key(self):
        response = self.start()
        self.assertNotContains(response, 'name="correct_answer"')
        self.assertNotContains(response, '"correct_answer"')
        self.assertContains(response, 'name="q_50"')
        self.assertEqual(PlacementAttempt.objects.count(), 0)
        self.mock_send_emails.assert_not_called()

    def test_full_score_and_private_result(self):
        self.start()
        response = self.client.post(reverse("placement:test"), self.valid_data())

        self.assertRedirects(response, reverse("placement:result"))

        attempt = PlacementAttempt.objects.get()
        self.assertEqual(attempt.score, 50)
        self.assertEqual(
            (attempt.recommended_level, attempt.cefr_reference),
            ("proficiency", "C2"),
        )
        self.assertIsNone(attempt.user_id)
        self.mock_send_emails.assert_called_once_with(attempt)

        self.assertContains(self.client.get(reverse("placement:result")), "Proficiency")
        self.mock_send_emails.assert_called_once_with(attempt)

    def test_blank_answers_are_allowed(self):
        self.start()
        self.client.post(reverse("placement:test"), self.valid_data(correct=False))

        attempt = PlacementAttempt.objects.get()
        self.assertEqual(
            (attempt.score, attempt.recommended_level, attempt.cefr_reference),
            (0, "elementary", "A1"),
        )
        self.mock_send_emails.assert_called_once_with(attempt)

    def test_invalid_answer_does_not_create_attempt(self):
        self.start()
        data = self.valid_data()
        data["q_1"] = "E"

        response = self.client.post(reverse("placement:test"), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PlacementAttempt.objects.count(), 0)
        self.mock_send_emails.assert_not_called()

    def test_missing_contact_acknowledgement_does_not_create_attempt(self):
        self.start()
        data = self.valid_data()
        data.pop("acknowledge")

        self.client.post(reverse("placement:test"), data)
        self.assertEqual(PlacementAttempt.objects.count(), 0)
        self.mock_send_emails.assert_not_called()

    def test_honeypot_does_not_create_attempt(self):
        self.start()
        data = self.valid_data()
        data["website"] = "automated-spam"

        self.client.post(reverse("placement:test"), data)
        self.assertEqual(PlacementAttempt.objects.count(), 0)
        self.mock_send_emails.assert_not_called()

    def test_forged_form_token_does_not_create_attempt(self):
        self.start()
        data = self.valid_data()
        data["token"] = "invalid-token"

        self.client.post(reverse("placement:test"), data)
        self.assertEqual(PlacementAttempt.objects.count(), 0)
        self.mock_send_emails.assert_not_called()

    def test_replay_does_not_create_another_attempt(self):
        self.start()
        data = self.valid_data()

        self.client.post(reverse("placement:test"), data)
        attempt = PlacementAttempt.objects.get()
        self.mock_send_emails.assert_called_once_with(attempt)

        response = self.client.post(reverse("placement:test"), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PlacementAttempt.objects.count(), 1)
        self.mock_send_emails.assert_called_once()

    def test_another_browser_cannot_see_result(self):
        self.start()
        self.client.post(reverse("placement:test"), self.valid_data())

        attempt = PlacementAttempt.objects.get()
        self.mock_send_emails.assert_called_once_with(attempt)

        other = Client()
        self.assertRedirects(
            other.get(reverse("placement:result")),
            reverse("placement:test"),
        )
        self.mock_send_emails.assert_called_once()

    def test_incomplete_question_bank_disables_test(self):
        PlacementQuestion.objects.filter(
            version=TEST_VERSION,
            number=50,
        ).update(is_active=False)

        self.assertEqual(
            self.client.get(reverse("placement:test")).status_code,
            503,
        )
        self.mock_send_emails.assert_not_called()

    def test_failed_turnstile_does_not_create_attempt(self):
        self.start()
        self.mock_turnstile.return_value = False

        response = self.client.post(reverse("placement:test"), self.valid_data())

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["turnstile_failed"])
        self.assertEqual(PlacementAttempt.objects.count(), 0)
        self.mock_turnstile.assert_called_once()
        self.mock_send_emails.assert_not_called()

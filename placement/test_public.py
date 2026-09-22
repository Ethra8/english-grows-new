from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import PlacementAttempt, PlacementQuestion, TEST_VERSION


class PlacementPublicFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_placement_questions", stdout=StringIO())

    def start(self):
        response = self.client.get(reverse("placement:test"))
        self.assertEqual(response.status_code, 200)
        return response

    def valid_data(self, correct=True):
        data = {
            "name": "Example Learner", "email": "learner@example.com",
            "acknowledge": "on", "token": self.client.session["placement_test_token"],
        }
        if correct:
            data.update({f"q_{q.number}": q.correct_answer for q in PlacementQuestion.objects.filter(version=TEST_VERSION)})
        return data

    def test_public_page_does_not_expose_answer_key(self):
        response = self.start()
        self.assertNotContains(response, 'name="correct_answer"')
        self.assertNotContains(response, '"correct_answer"')
        self.assertContains(response, 'name="q_50"')
        self.assertEqual(PlacementAttempt.objects.count(), 0)

    def test_full_score_and_private_result(self):
        self.start()
        response = self.client.post(reverse("placement:test"), self.valid_data())
        self.assertRedirects(response, reverse("placement:result"))
        attempt = PlacementAttempt.objects.get()
        self.assertEqual(attempt.score, 50)
        self.assertEqual((attempt.recommended_level, attempt.cefr_reference), ("advanced", "C1"))
        self.assertIsNone(attempt.user_id)
        self.assertContains(self.client.get(reverse("placement:result")), "Advanced")

    def test_blank_answers_are_allowed(self):
        self.start()
        self.client.post(reverse("placement:test"), self.valid_data(correct=False))
        self.assertEqual(PlacementAttempt.objects.get().score, 0)
        self.assertEqual(PlacementAttempt.objects.get().recommended_level, "foundation")

    def test_invalid_answer_does_not_create_attempt(self):
        self.start()
        data = self.valid_data()
        data["q_1"] = "E"
        response = self.client.post(reverse("placement:test"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PlacementAttempt.objects.count(), 0)

    def test_missing_contact_acknowledgement_does_not_create_attempt(self):
        self.start()
        data = self.valid_data()
        data.pop("acknowledge")
        self.client.post(reverse("placement:test"), data)
        self.assertEqual(PlacementAttempt.objects.count(), 0)

    def test_honeypot_does_not_create_attempt(self):
        self.start()
        data = self.valid_data()
        data["website"] = "automated-spam"
        self.client.post(reverse("placement:test"), data)
        self.assertEqual(PlacementAttempt.objects.count(), 0)

    def test_forged_form_token_does_not_create_attempt(self):
        self.start()
        data = self.valid_data()
        data["token"] = "invalid-token"
        self.client.post(reverse("placement:test"), data)
        self.assertEqual(PlacementAttempt.objects.count(), 0)

    def test_replay_does_not_create_another_attempt(self):
        self.start()
        data = self.valid_data()
        self.client.post(reverse("placement:test"), data)
        response = self.client.post(reverse("placement:test"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PlacementAttempt.objects.count(), 1)

    def test_another_browser_cannot_see_result(self):
        self.start()
        self.client.post(reverse("placement:test"), self.valid_data())
        from django.test import Client
        other = Client()
        self.assertRedirects(other.get(reverse("placement:result")), reverse("placement:test"))

    def test_incomplete_question_bank_disables_test(self):
        PlacementQuestion.objects.filter(version=TEST_VERSION, number=50).update(is_active=False)
        self.assertEqual(self.client.get(reverse("placement:test")).status_code, 503)

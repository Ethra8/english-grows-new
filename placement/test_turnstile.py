
import json
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import parse_qs

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from communications.models import MarketingSubscriber
from .models import PlacementAttempt
from .views import RESULT_KEY, TOKEN_KEY


TEST_SITEKEY = "1x00000000000000000000AA"
TEST_SECRET = "1x0000000000000000000000000000000AA"
TEST_TOKEN = "XXXX.DUMMY.TOKEN.XXXX"


@override_settings(
    TURNSTILE_SITEKEY=TEST_SITEKEY,
    TURNSTILE_SECRET_KEY=TEST_SECRET,
    SITE_URL="https://englishgrows.com",
)
class PlacementTurnstileTests(TestCase):
    def setUp(self):
        self.url = reverse("placement:test")
        self.questions = [
            SimpleNamespace(
                number=i, text=f"Question {i}",
                option_a="Option A", option_b="Option B",
                option_c="Option C", option_d="Option D",
            )
            for i in range(1, 51)
        ]

        question_patch = patch("placement.views._questions", return_value=self.questions)
        question_patch.start()
        self.addCleanup(question_patch.stop)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.session_token = self.client.session[TOKEN_KEY]
        self.initial_subscribers = MarketingSubscriber.objects.count()

    def submission(self, **changes):
        data = {
            "token": self.session_token,
            "email": "placement-test@example.com",
            "acknowledge": "on",
            "marketing_opt_in": "on",
            "cf-turnstile-response": TEST_TOKEN,
            "q_1": "B",
            "q_50": "D",
        }
        data.update(changes)
        return data

    @staticmethod
    def save_test_grade(attempt):
        """Save a real attempt while isolating the existing grading algorithm."""
        attempt.answer_snapshot = {}
        attempt.score = 0
        attempt.recommended_level = "Elementary"
        attempt.cefr_reference = "A1"
        attempt.completed_at = timezone.now()
        attempt.save()
        return attempt

    def post_with_verification(self, verification, data=None):
        """Mock only Cloudflare's HTTP response and external side effects."""
        response_body = BytesIO(json.dumps(verification).encode("utf-8"))

        with (
            patch("config.turnstile.urlopen", return_value=response_body) as siteverify,
            patch.object(
                PlacementAttempt, "grade", autospec=True,
                side_effect=self.save_test_grade,
            ) as grade,
            patch("placement.views.send_placement_result_emails") as send_email,
            patch("placement.views.MarketingSubscriber.subscribe") as subscribe,
        ):
            response = self.client.post(self.url, data or self.submission())

        return response, siteverify, grade, send_email, subscribe

    def assert_no_submission(self, grade, send_email, subscribe):
        self.assertEqual(PlacementAttempt.objects.count(), 0)
        self.assertEqual(MarketingSubscriber.objects.count(), self.initial_subscribers)
        grade.assert_not_called()
        send_email.assert_not_called()
        subscribe.assert_not_called()
        self.assertEqual(self.client.session[TOKEN_KEY], self.session_token)

    def test_valid_token_creates_one_attempt_and_sends_result(self):
        response, siteverify, grade, send_email, subscribe = self.post_with_verification({
            "success": True,
            "hostname": "test",
            "action": "test",
        })

        self.assertRedirects(response, reverse("placement:result"), fetch_redirect_response=False)
        self.assertEqual(PlacementAttempt.objects.count(), 1)

        attempt = PlacementAttempt.objects.get()
        self.assertEqual(attempt.answers["1"], "B")
        self.assertEqual(attempt.answers["50"], "D")
        self.assertEqual(self.client.session[RESULT_KEY], attempt.pk)
        self.assertNotIn(TOKEN_KEY, self.client.session)

        grade.assert_called_once()
        send_email.assert_called_once_with(attempt)
        subscribe.assert_called_once()

        request = siteverify.call_args.args[0]
        payload = parse_qs(request.data.decode("utf-8"))
        self.assertEqual(payload["secret"], [TEST_SECRET])
        self.assertEqual(payload["response"], [TEST_TOKEN])

    def test_valid_token_without_marketing_consent(self):
        data = self.submission()
        data.pop("marketing_opt_in")

        response, _, grade, send_email, subscribe = self.post_with_verification(
            {"success": True, "hostname": "test", "action": "test"},
            data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(PlacementAttempt.objects.count(), 1)
        grade.assert_called_once()
        send_email.assert_called_once()
        subscribe.assert_not_called()

    def test_missing_token_is_rejected_without_contacting_cloudflare(self):
        response, siteverify, grade, send_email, subscribe = self.post_with_verification(
            {"success": True},
            self.submission(**{"cf-turnstile-response": ""}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["turnstile_failed"])
        siteverify.assert_not_called()
        self.assert_no_submission(grade, send_email, subscribe)

    def test_invalid_token_is_rejected(self):
        response, siteverify, grade, send_email, subscribe = self.post_with_verification({
            "success": False,
            "error-codes": ["invalid-input-response"],
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["turnstile_failed"])
        siteverify.assert_called_once()
        self.assert_no_submission(grade, send_email, subscribe)

    def test_expired_or_reused_token_is_rejected(self):
        response, _, grade, send_email, subscribe = self.post_with_verification({
            "success": False,
            "error-codes": ["timeout-or-duplicate"],
        })

        self.assertEqual(response.status_code, 200)
        self.assert_no_submission(grade, send_email, subscribe)

    def test_failed_verification_preserves_answers_and_allows_retry(self):
        failed, _, grade, send_email, subscribe = self.post_with_verification({
            "success": False,
            "error-codes": ["invalid-input-response"],
        })

        self.assert_no_submission(grade, send_email, subscribe)
        self.assertEqual(failed.context["form"]["q_1"].value(), "B")
        self.assertEqual(failed.context["form"]["q_50"].value(), "D")
        self.assertEqual(failed.context["form"]["email"].value(), "placement-test@example.com")
        self.assertContains(failed, 'data-turnstile-failed="true"')

        # Retry with the same placement session, but a fresh successful verification.
        response, _, grade, send_email, subscribe = self.post_with_verification({
            "success": True,
            "hostname": "test",
            "action": "test",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(PlacementAttempt.objects.count(), 1)
        grade.assert_called_once()
        send_email.assert_called_once()
        subscribe.assert_called_once()

    def test_invalid_placement_session_never_calls_cloudflare(self):
        response, siteverify, grade, send_email, subscribe = self.post_with_verification(
            {"success": True},
            self.submission(token="incorrect-session-token"),
        )

        self.assertEqual(response.status_code, 200)
        siteverify.assert_not_called()
        self.assert_no_submission(grade, send_email, subscribe)

    @override_settings(
        TURNSTILE_SITEKEY="production-like-sitekey-for-testing",
        TURNSTILE_SECRET_KEY="production-like-secret-for-testing",
    )
    def test_both_authorised_production_hostnames_are_accepted(self):
        for index, hostname in enumerate(("englishgrows.com", "www.englishgrows.com"), 1):
            with self.subTest(hostname=hostname):
                response, _, grade, send_email, _ = self.post_with_verification({
                    "success": True,
                    "hostname": hostname,
                    "action": "placement",
                })

                self.assertEqual(response.status_code, 302)
                self.assertEqual(PlacementAttempt.objects.count(), index)
                grade.assert_called_once()
                send_email.assert_called_once()

                if index == 1:
                    self.client.get(self.url)
                    self.session_token = self.client.session[TOKEN_KEY]

    @override_settings(
        TURNSTILE_SITEKEY="production-like-sitekey-for-testing",
        TURNSTILE_SECRET_KEY="production-like-secret-for-testing",
    )
    def test_unauthorised_hostname_is_rejected(self):
        response, _, grade, send_email, subscribe = self.post_with_verification({
            "success": True,
            "hostname": "another-website.example",
            "action": "placement",
        })

        self.assertEqual(response.status_code, 200)
        self.assert_no_submission(grade, send_email, subscribe)

    @override_settings(
        TURNSTILE_SITEKEY="production-like-sitekey-for-testing",
        TURNSTILE_SECRET_KEY="production-like-secret-for-testing",
    )
    def test_wrong_action_is_rejected(self):
        response, _, grade, send_email, subscribe = self.post_with_verification({
            "success": True,
            "hostname": "www.englishgrows.com",
            "action": "signup",
        })

        self.assertEqual(response.status_code, 200)
        self.assert_no_submission(grade, send_email, subscribe)
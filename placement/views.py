import secrets

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from communications.models import MarketingSubscriber
from communications.services import send_placement_result_emails
from config.turnstile import verify_turnstile

from .forms import PlacementTestForm
from .models import PlacementAttempt, PlacementQuestion, TEST_VERSION, TOTAL_QUESTIONS


TOKEN_KEY = "placement_test_token"
RESULT_KEY = "placement_last_attempt_id"


def _questions():
    questions = list(PlacementQuestion.objects.filter(version=TEST_VERSION, is_active=True).order_by("number"))
    if [q.number for q in questions] != list(range(1, TOTAL_QUESTIONS + 1)) or any(
        not all((q.option_a, q.option_b, q.option_c, q.option_d)) for q in questions
    ):
        return None
    return questions


def _private(response):
    response["Cache-Control"] = "private, no-store"
    return response


def _placement_route(request, page):
    """Return the placement URL name matching the current language."""
    language = getattr(request, "LANGUAGE_CODE", "en")
    return f"placement:{page}_es" if language == "es" else f"placement:{page}"


@never_cache
@require_http_methods(["GET", "POST"])
def placement_test(request):
    questions = _questions()
    if questions is None:
        return HttpResponse(_("The placement test is temporarily unavailable. Please try again later."), status=503)

    turnstile_failed = False

    if request.method == "GET":
        request.session[TOKEN_KEY] = secrets.token_urlsafe(24)
        initial = {"token": request.session[TOKEN_KEY]}

        if request.user.is_authenticated:
            initial.update(
                name=request.user.get_full_name() or request.user.get_username(),
                email=request.user.email,
            )

        form = PlacementTestForm(questions=questions, initial=initial)

    else:
        form = PlacementTestForm(request.POST, questions=questions)

        if form.is_valid():
            if not secrets.compare_digest(form.cleaned_data["token"], request.session.get(TOKEN_KEY, "")):
                form.add_error(None, _("This test session has expired. Reload the page and try again."))

            else:
                is_test_key = settings.TURNSTILE_SITEKEY == "1x00000000000000000000AA"

                if not verify_turnstile(
                    request.POST.get("cf-turnstile-response", ""),
                    expected_hostname=None if is_test_key else ("englishgrows.com", "www.englishgrows.com"),
                    expected_action=None if is_test_key else "placement",
                ):
                    turnstile_failed = True
                    form.add_error(None, _("Security verification failed. Please try again."))

                else:
                    answers = {str(q.number): form.cleaned_data.get(f"q_{q.number}") or None for q in questions}

                    name = (
                        request.user.get_full_name() or request.user.get_username()
                        if request.user.is_authenticated else ""
                    )

                    email = (
                        request.user.email or form.cleaned_data["email"]
                        if request.user.is_authenticated else form.cleaned_data["email"]
                    )

                    try:
                        with transaction.atomic():
                            attempt = PlacementAttempt(
                                user=request.user if request.user.is_authenticated else None,
                                name=name,
                                email=email,
                                test_version=TEST_VERSION,
                                answers=answers,
                            ).grade()

                            # Optional single opt-in: activate immediately without a confirmation email.
                            if form.cleaned_data["marketing_opt_in"]:
                                MarketingSubscriber.subscribe(
                                    email=email,
                                    source=MarketingSubscriber.Source.PLACEMENT_TEST,
                                    consent_text=str(form.fields["marketing_opt_in"].label),
                                    user=request.user if request.user.is_authenticated else None,
                                )

                    except ValidationError:
                        form.add_error(None, _("We could not grade your answers. Please try again later."))

                    else:
                        request.session.pop(TOKEN_KEY, None)
                        request.session[RESULT_KEY] = attempt.pk

                        # The grading transaction has committed. Email delivery cannot
                        # undo the saved result, and refreshing the result page won't resend.
                        send_placement_result_emails(attempt)

                        return redirect(_placement_route(request, "result"))

    rows = [{"number": q.number, "field": form[f"q_{q.number}"]} for q in questions]
    pages = [rows[i:i + 10] for i in range(0, TOTAL_QUESTIONS, 10)]

    site_url = settings.SITE_URL.rstrip("/")
    english_url = f"{site_url}{reverse('placement:test')}"
    spanish_url = f"{site_url}{reverse('placement:test_es')}"

    context = {
        "form": form,
        "pages": pages,
        "question_count": TOTAL_QUESTIONS,
        "privacy_url": getattr(settings, "PLACEMENT_PRIVACY_URL", ""),
        "placement_is_result": False,
        "english_url": english_url,
        "spanish_url": spanish_url,
        "canonical_url": spanish_url if getattr(request, "LANGUAGE_CODE", "en") == "es" else english_url,
        "turnstile_sitekey": settings.TURNSTILE_SITEKEY,
        "turnstile_failed": turnstile_failed,
    }

    return _private(render(request, "placement/test.html", context))


@never_cache
@require_http_methods(["GET"])
def placement_result(request):
    attempt_id = request.session.get(RESULT_KEY)

    if not attempt_id:
        return redirect(_placement_route(request, "test"))

    attempt = PlacementAttempt.objects.filter(pk=attempt_id, completed_at__isnull=False).first()

    if attempt is None or (
        attempt.user_id and (
            not request.user.is_authenticated or request.user.pk != attempt.user_id
        )
    ):
        request.session.pop(RESULT_KEY, None)
        return redirect(_placement_route(request, "test"))

    return _private(render(request, "placement/result.html", {
        "attempt": attempt,
        "total": TOTAL_QUESTIONS,
        "placement_is_result": True,
    }))
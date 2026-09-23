from functools import wraps

from django.urls import path
from django.utils import translation

from . import views


app_name = "placement"


def in_language(view, language):
    """Render a placement page in the language assigned to its URL."""
    @wraps(view)
    def localized(request, *args, **kwargs):
        with translation.override(language):
            request.LANGUAGE_CODE = language
            response = view(request, *args, **kwargs)
            response["Content-Language"] = language
            return response
    return localized


urlpatterns = [
    # English
    path("placement-test/", in_language(views.placement_test, "en"), name="test"),
    path("placement-test/result/", in_language(views.placement_result, "en"), name="result"),

    # Spanish
    path("es/placement-test/", in_language(views.placement_test, "es"), name="test_es"),
    path("es/placement-test/result/", in_language(views.placement_result, "es"), name="result_es"),
]
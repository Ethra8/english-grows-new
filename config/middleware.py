from django.conf import settings
from django.utils import translation


class ExplicitLanguageMiddleware:
    """
    Use only an explicitly selected site language.

    Rules:
    - If the django_language cookie exists and is supported,
      activate that language.
    - Otherwise always use settings.LANGUAGE_CODE.
    - Ignore the browser Accept-Language header completely.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        supported_languages = {
            code
            for code, name in settings.LANGUAGES
        }

        language_code = request.COOKIES.get(
            settings.LANGUAGE_COOKIE_NAME
        )

        if language_code not in supported_languages:
            language_code = settings.LANGUAGE_CODE

        translation.activate(language_code)

        request.LANGUAGE_CODE = language_code

        response = self.get_response(request)

        translation.deactivate()

        return response
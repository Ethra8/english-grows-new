import json
import logging

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings


logger = logging.getLogger(__name__)

SITEVERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def verify_turnstile(token, *, expected_hostname=None, expected_action=None):
    """Validate a Turnstile token against Cloudflare's Siteverify API."""

    if not token or len(token) > 2048:
        return False

    payload = urlencode({
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token,
    }).encode("utf-8")

    request = Request(
        SITEVERIFY_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    try:
        with urlopen(request, timeout=10) as response:
            result = json.load(response)
    except (OSError, ValueError) as exc:
        logger.warning("Turnstile verification request failed: %s", exc)
        return False

    if not isinstance(result, dict) or not result.get("success"):
        logger.info("Turnstile verification rejected: %s", result.get("error-codes", []) if isinstance(result, dict) else [])
        return False

    if expected_hostname:
        allowed_hostnames = (expected_hostname,) if isinstance(expected_hostname, str) else expected_hostname

        if result.get("hostname") not in allowed_hostnames:
            logger.warning("Turnstile hostname mismatch: %s", result.get("hostname"))
            return False
    
    if expected_action and result.get("action") != expected_action:
        logger.warning("Turnstile action mismatch.")
        return False

    return True
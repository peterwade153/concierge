"""OpenAI client configuration helpers.

Centralizes construction-time concerns (timeout resolution) so the
``RestaurantAgent`` stays focused on orchestration.
"""

import logging
import os

logger = logging.getLogger(__name__)

DEFAULT_REQUEST_TIMEOUT_SECONDS = 30  # default when OPENROUTER_REQUEST_TIMEOUT is unset


def resolve_request_timeout() -> float:
    """Return the request timeout in seconds from the environment.

    Reads ``OPENROUTER_REQUEST_TIMEOUT`` (integer seconds). Returns the
    configured value, or the default when the variable is unset. An invalid
    value is logged and falls back to the default rather than crashing
    agent construction.
    """
    raw = os.environ.get("OPENROUTER_REQUEST_TIMEOUT")
    if not raw:
        return float(DEFAULT_REQUEST_TIMEOUT_SECONDS)
    try:
        return float(int(raw))
    except (TypeError, ValueError):
        logger.warning(
            "Invalid OPENROUTER_REQUEST_TIMEOUT=%r; falling back to %ss",
            raw,
            DEFAULT_REQUEST_TIMEOUT_SECONDS,
        )
        return float(DEFAULT_REQUEST_TIMEOUT_SECONDS)

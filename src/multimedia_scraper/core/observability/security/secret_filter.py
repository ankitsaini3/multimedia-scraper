# src/multimedia_scraper/core/observability/security/secret_filter.py

from __future__ import annotations

from multimedia_scraper.core.observability.security.secret_patterns import (
    SECRET_PATTERNS,
)

REDACTION_TOKEN = "[REDACTED]"


def filter_secrets(
    value: str,
) -> str:
    """
    Deterministically redact secret-like payloads.

    Guarantees:
    - stable replacement semantics
    - non-leaking telemetry
    - serialization-safe output
    """

    sanitized = value

    for pattern in SECRET_PATTERNS:
        sanitized = pattern.sub(
            REDACTION_TOKEN,
            sanitized,
        )

    return sanitized

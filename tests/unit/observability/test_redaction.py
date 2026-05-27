# tests/core/observability/test_redaction.py

from __future__ import annotations

from multimedia_scraper.core.observability.security.automatic_redaction import (
    automatically_redact_fields,
)
from multimedia_scraper.core.observability.security.secret_filter import (
    filter_secrets,
)


def test_secret_filter_redacts_tokens() -> None:
    payload = "Authorization=Bearer abc123"

    sanitized = filter_secrets(
        payload,
    )

    assert "abc123" not in sanitized

    assert "[REDACTED]" in sanitized


def test_structured_field_redaction() -> None:
    fields = {
        "token": "super-secret",
        "message": ("api_key=abcdef"),
    }

    sanitized = automatically_redact_fields(
        fields,
    )

    assert sanitized["token"] == "****"

    assert "abcdef" not in str(
        sanitized["message"],
    )

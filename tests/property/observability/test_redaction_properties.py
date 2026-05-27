# tests/property/observability/test_redaction_properties.py

from __future__ import annotations

from hypothesis import given, strategies as st

from multimedia_scraper.core.observability.security.secret_filter import (
    filter_secrets,
)


@given(
    st.text(
        min_size=1,
        max_size=128,
    ),
)
def test_redaction_never_returns_none(
    payload: str,
) -> None:
    sanitized = filter_secrets(
        payload,
    )

    assert sanitized is not None

    assert isinstance(
        sanitized,
        str,
    )

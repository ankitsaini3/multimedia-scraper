# src/multimedia_scraper/core/observability/security/masking.py

from __future__ import annotations


def mask_value(value: str) -> str:
    """
    Deterministically mask sensitive values.

    Avoids accidental credential disclosure while
    preserving minimal debugging visibility.
    """

    if not value:
        return "****"

    if len(value) <= 4:
        return "****"

    return f"{value[:2]}****{value[-2:]}"

# src/multimedia_scraper/core/observability/security/automatic_redaction.py

from __future__ import annotations

from collections.abc import Mapping

from multimedia_scraper.core.observability.dto.structured_fields import (
    StructuredValue,
)
from multimedia_scraper.core.observability.security.redaction import (
    redact_fields,
)
from multimedia_scraper.core.observability.security.secret_filter import (
    filter_secrets,
)


def automatically_redact_fields(
    fields: Mapping[
        str,
        StructuredValue,
    ],
) -> dict[str, StructuredValue]:
    """
    Apply deterministic automatic redaction pipeline.

    Guarantees:
    - secret filtering
    - structured field redaction
    - transport-safe output
    """

    sanitized: dict[
        str,
        StructuredValue,
    ] = {}

    for key, value in redact_fields(
        fields,
    ).items():
        sanitized[key] = _sanitize_value(
            value,
        )

    return sanitized


def _sanitize_value(
    value: StructuredValue,
) -> StructuredValue:
    if isinstance(value, str):
        return filter_secrets(
            value,
        )

    if isinstance(value, tuple):
        return tuple(_sanitize_value(item) for item in value)

    if isinstance(value, dict):
        return {
            key: _sanitize_value(
                item,
            )
            for key, item in value.items()
        }

    return value

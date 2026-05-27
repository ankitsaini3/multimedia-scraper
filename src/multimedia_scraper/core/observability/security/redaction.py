# src/multimedia_scraper/core/observability/security/redaction.py

from __future__ import annotations

from collections.abc import Mapping

from strenum import StrEnum

from multimedia_scraper.core.observability.dto.structured_fields import (
    StructuredValue,
)
from multimedia_scraper.core.observability.security.sensitive_fields import (
    SENSITIVE_FIELD_NAMES,
)


class RedactionPolicy(StrEnum):
    MASK = "mask"
    DROP = "drop"


def redact_fields(
    fields: Mapping[str, StructuredValue],
    *,
    policy: RedactionPolicy = RedactionPolicy.MASK,
) -> dict[str, StructuredValue]:
    """
    Apply deterministic structured field redaction.
    """

    redacted: dict[str, StructuredValue] = {}

    for key, value in fields.items():
        normalized = key.lower()

        if normalized not in SENSITIVE_FIELD_NAMES:
            redacted[key] = value
            continue

        if policy == RedactionPolicy.DROP:
            continue

        redacted[key] = _redact_value(value)

    return redacted


def _redact_value(
    value: StructuredValue,
) -> StructuredValue:
    # if isinstance(value, str):
    #     return mask_value(value)    # only for diagnostic purpose

    return "****"

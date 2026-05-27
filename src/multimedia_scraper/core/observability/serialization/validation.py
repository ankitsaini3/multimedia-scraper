# src/multimedia_scraper/core/observability/serialization/validation.py

from __future__ import annotations

from collections.abc import Mapping

from multimedia_scraper.core.errors.observability import (
    TelemetryValidationError,
)
from multimedia_scraper.core.observability.dto.structured_fields import (
    StructuredValue,
)


def validate_structured_value(
    value: StructuredValue,
) -> None:
    """
    Recursively validate transport-safe structured values.
    """

    if value is None:
        return

    if isinstance(
        value,
        (str, int, float, bool),
    ):
        return

    if isinstance(value, tuple):
        for item in value:
            validate_structured_value(item)

        return

    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TelemetryValidationError(
                    "structured field mapping keys must be strings",
                )

            validate_structured_value(item)

        return

    raise TelemetryValidationError(
        f"unsupported structured value type: {type(value)!r}",
    )

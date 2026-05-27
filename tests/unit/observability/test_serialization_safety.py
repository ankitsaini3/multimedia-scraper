# tests/core/observability/test_serialization_safety.py

from __future__ import annotations

import pytest

from multimedia_scraper.core.errors.observability import (
    TelemetryValidationError,
)
from multimedia_scraper.core.observability.serialization.validation import (
    validate_structured_value,
)


def test_invalid_runtime_object_rejected() -> None:
    class RuntimeHandle:
        pass

    with pytest.raises(
        TelemetryValidationError,
    ):
        validate_structured_value(
            RuntimeHandle(),
        )

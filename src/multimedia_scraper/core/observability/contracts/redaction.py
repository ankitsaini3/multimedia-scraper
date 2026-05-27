# src/multimedia_scraper/core/observability/contracts/redaction.py

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from multimedia_scraper.core.observability.dto.structured_fields import (
    StructuredValue,
)


class StructuredFieldRedactor(Protocol):
    """
    Sensitive telemetry redaction contract.
    """

    def redact(
        self,
        fields: Mapping[str, StructuredValue],
    ) -> Mapping[str, StructuredValue]: ...

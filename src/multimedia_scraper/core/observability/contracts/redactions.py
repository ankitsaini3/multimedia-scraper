# src/multimedia_scraper/core/observability/contracts/redaction.py

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.dto.structured_fields import (
    StructuredValue,
)


class StructuredFieldRedactor(
    Protocol,
):
    """
    Structured field redaction contract.
    """

    def redact_fields(
        self,
        fields: Mapping[
            str,
            StructuredValue,
        ],
    ) -> Mapping[
        str,
        StructuredValue,
    ]: ...


class StructuredEventRedactor(
    Protocol,
):
    """
    Immutable telemetry event redaction contract.

    Redaction MUST:
    - preserve immutability
    - avoid partial mutation
    - remain deterministic
    """

    def redact_event(
        self,
        event: LogEventDTO,
    ) -> LogEventDTO: ...

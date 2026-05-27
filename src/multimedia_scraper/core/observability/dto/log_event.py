# src/multimedia_scraper/core/observability/dto/log_event.py

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime

from multimedia_scraper.core.observability.dto.correlation import (
    CorrelationMetadataDTO,
)
from multimedia_scraper.core.observability.dto.event_category import (
    EventCategory,
)
from multimedia_scraper.core.observability.dto.severity import (
    LogSeverity,
)
from multimedia_scraper.core.observability.dto.structured_fields import (
    StructuredValue,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class LogEventDTO:
    """
    Canonical immutable structured telemetry event.

    Must remain:
    - deterministic
    - serialization-safe
    - replay-safe
    - transport-safe
    """

    timestamp_utc: datetime
    monotonic_ns: int

    severity: LogSeverity
    event_category: EventCategory

    subsystem: str
    operation: str

    message: str

    correlation: CorrelationMetadataDTO

    fields: Mapping[str, StructuredValue]

    exception_type: str | None = None
    exception_message: str | None = None

    schema_version: int = 1

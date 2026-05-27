# src/multimedia_scraper/core/observability/contracts/serializer.py

from __future__ import annotations

from typing import Protocol

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)


class LogEventSerializer(Protocol):
    """
    Structured telemetry serializer contract.
    """

    def serialize(
        self,
        event: LogEventDTO,
    ) -> bytes: ...

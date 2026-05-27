# src/multimedia_scraper/core/observability/formatters/json_formatter.py

from __future__ import annotations

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.serialization.canonical_json import (
    serialize_log_event,
)


class JsonTelemetryFormatter:
    """
    Deterministic JSON telemetry formatter.

    Infrastructure-isolated formatting layer.
    """

    def format(
        self,
        event: LogEventDTO,
    ) -> bytes:
        return serialize_log_event(
            event,
        )

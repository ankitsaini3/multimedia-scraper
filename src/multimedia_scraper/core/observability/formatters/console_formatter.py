# src/multimedia_scraper/core/observability/formatters/console_formatter.py

from __future__ import annotations

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)


class ConsoleTelemetryFormatter:
    """
    Human-readable structured console formatter.

    This formatter exists ONLY for operator visibility.
    Structured DTOs remain canonical.
    """

    def format(
        self,
        event: LogEventDTO,
    ) -> bytes:
        rendered = (
            f"[{event.timestamp_utc.isoformat()}] "
            f"[{event.severity.value}] "
            f"[{event.subsystem}] "
            f"[{event.operation}] "
            f"{event.message}"
        )

        return rendered.encode(
            "utf-8",
        )

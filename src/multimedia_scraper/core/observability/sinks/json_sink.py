# src/multimedia_scraper/core/observability/sinks/json_sink.py

from __future__ import annotations

import asyncio
import sys
from typing import Any

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.formatters.json_formatter import (
    JsonTelemetryFormatter,
)
from multimedia_scraper.core.observability.sinks.base import (
    BaseTelemetrySink,
)


class JsonTelemetrySink(
    BaseTelemetrySink,
):
    """
    Structured JSON stdout sink.

    Machine-readable telemetry transport.
    """

    def __init__(
        self,
        *,
        formatter: (JsonTelemetryFormatter | None) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            **kwargs,
        )

        self._formatter = formatter or JsonTelemetryFormatter()

    async def _write_event(
        self,
        event: LogEventDTO,
    ) -> None:
        payload = self._formatter.format(
            event,
        )

        await asyncio.to_thread(
            self._write_sync,
            payload,
        )

    def _write_sync(
        self,
        payload: bytes,
    ) -> None:
        sys.stdout.buffer.write(
            payload + b"\n",
        )

        sys.stdout.flush()

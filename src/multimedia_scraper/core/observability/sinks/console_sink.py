# src/multimedia_scraper/core/observability/sinks/console_sink.py

from __future__ import annotations

import asyncio
import sys
from typing import Any

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.formatters.console_formatter import (
    ConsoleTelemetryFormatter,
)
from multimedia_scraper.core.observability.sinks.base import (
    BaseTelemetrySink,
)


class ConsoleTelemetrySink(
    BaseTelemetrySink,
):
    """
    Async structured console sink.

    Scheduling guarantees:
    - non-blocking emit path
    - bounded buffering
    - isolated writer execution
    """

    def __init__(
        self,
        *,
        formatter: (ConsoleTelemetryFormatter | None) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            **kwargs,
        )

        self._formatter = formatter or ConsoleTelemetryFormatter()

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

# src/multimedia_scraper/core/observability/sinks/file_sink.py

from __future__ import annotations

import asyncio
from pathlib import Path
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


class FileTelemetrySink(
    BaseTelemetrySink,
):
    """
    Structured append-only telemetry file sink.

    Guarantees:
    - append-only writes
    - bounded buffering
    - async-safe emission
    - isolated blocking IO
    """

    def __init__(
        self,
        *,
        path: Path,
        formatter: (JsonTelemetryFormatter | None) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            **kwargs,
        )

        self._path = path

        self._formatter = formatter or JsonTelemetryFormatter()

    async def start(self) -> None:
        self._path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        await super().start()

    async def _write_event(
        self,
        event: LogEventDTO,
    ) -> None:
        payload = self._formatter.format(
            event,
        )

        await asyncio.to_thread(
            self._append_sync,
            payload,
        )

    def _append_sync(
        self,
        payload: bytes,
    ) -> None:
        with self._path.open(
            "ab",
        ) as file:
            file.write(
                payload + b"\n",
            )

            file.flush()

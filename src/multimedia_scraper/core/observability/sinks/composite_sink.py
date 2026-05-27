# src/multimedia_scraper/core/observability/sinks/composite_sink.py

from __future__ import annotations

from collections.abc import Sequence
from contextlib import suppress

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.sinks.base import (
    BaseTelemetrySink,
)


class CompositeTelemetrySink:
    """
    Runtime-owned sink fanout coordinator.

    Guarantees:
    - sink isolation
    - deterministic fanout ordering
    - bounded downstream behavior
    """

    def __init__(
        self,
        *,
        sinks: Sequence[
            BaseTelemetrySink
        ],
    ) -> None:
        self._sinks = tuple(
            sinks,
        )

        self._degraded = False

    async def start(self) -> None:
        for sink in self._sinks:
            await sink.start()

    async def emit(
        self,
        event: LogEventDTO,
    ) -> None:
        degraded = False

        for sink in self._sinks:
            try:
                await sink.emit(
                    event,
                )

            except Exception:
                # intentional sink isolation
                degraded = True
                continue

        self._degraded = degraded

    async def flush(self) -> None:
        for sink in self._sinks:
            try:
                await sink.flush()

            except Exception:
                continue

    async def shutdown(self) -> None:
        for sink in self._sinks:
            with suppress(Exception):
                await sink.shutdown()


    @property
    def degraded(self) -> bool:
        return any(
            not sink.is_healthy()
            for sink in self._sinks
        )

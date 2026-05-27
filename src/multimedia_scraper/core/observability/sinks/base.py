# src/multimedia_scraper/core/observability/sinks/base.py

from __future__ import annotations

import asyncio

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.sinks.async_queue import (
    BoundedTelemetryQueue,
)
from multimedia_scraper.core.observability.sinks.overflow_policy import (
    OverflowPolicy,
)


class BaseTelemetrySink:
    """
    Runtime-owned async telemetry sink base.

    Guarantees:
    - bounded buffering
    - deterministic shutdown
    - isolated infrastructure failure
    - cancellation-safe flushing
    """

    def __init__(
        self,
        *,
        capacity: int = 1024,
        overflow_policy: OverflowPolicy = (OverflowPolicy.DROP_OLDEST),
    ) -> None:
        self._queue = BoundedTelemetryQueue(
            capacity=capacity,
            overflow_policy=overflow_policy,
        )

        self._worker_task: asyncio.Task[None] | None = None

        self._shutdown = False

        self._healthy = True

    async def start(self) -> None:
        if self._worker_task is not None:
            return

        self._worker_task = asyncio.create_task(
            self._run_worker(),
            name=(f"{self.__class__.__name__}-worker"),
        )

    async def emit(
        self,
        event: LogEventDTO,
    ) -> None:
        await self._queue.put(
            event,
        )

    async def flush(self) -> None:
        await self._queue.wait_until_empty()

    async def shutdown(self) -> None:
        if self._shutdown:
            return

        self._shutdown = True

        await self._queue.close()

        if self._worker_task is not None:
            await self._worker_task

    def is_healthy(self) -> bool:
        return self._healthy

    async def _run_worker(self) -> None:
        try:
            async for event in self._queue.drain_iter():
                await self._write_event(
                    event,
                )

        except Exception:
            self._healthy = False

    async def _write_event(
        self,
        event: LogEventDTO,
    ) -> None:
        raise NotImplementedError

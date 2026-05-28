# src/multimedia_scraper/core/observability/sinks/async_queue.py

from __future__ import annotations

import asyncio
from collections import deque
from collections.abc import AsyncIterator

from multimedia_scraper.core.errors.concurrency import (
    QueueOverflowError,
)
from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.sinks.overflow_policy import (
    OverflowPolicy,
)
from multimedia_scraper.core.observability.sinks.queue_statistics import (
    QueueStatistics,
)


class BoundedTelemetryQueue:
    """
    Runtime-owned bounded async telemetry queue.

    Guarantees:
    - bounded memory usage
    - deterministic overflow behavior
    - async-safe coordination
    - cancellation-safe waiting
    - observable queue state

    This queue intentionally avoids:
    - hidden background tasks
    - unbounded buffering
    - implicit retries
    """

    def __init__(
        self,
        *,
        capacity: int,
        overflow_policy: OverflowPolicy,
    ) -> None:
        if capacity <= 0:
            raise ValueError(
                "queue capacity must be > 0",
            )

        self._capacity = capacity

        self._overflow_policy = overflow_policy

        self._queue: deque[LogEventDTO] = deque()

        self._condition = asyncio.Condition()

        self._closed = False

        self._dropped_events = 0
        self._rejected_events = 0

        self._empty_event = asyncio.Event()
        self._empty_event.set()

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def overflow_policy(
        self,
    ) -> OverflowPolicy:
        return self._overflow_policy

    def depth(self) -> int:
        return len(self._queue)

    def statistics(
        self,
    ) -> QueueStatistics:
        return QueueStatistics(
            capacity=self._capacity,
            current_depth=len(self._queue),
            dropped_events=self._dropped_events,
            rejected_events=self._rejected_events,
        )

    async def put(
        self,
        event: LogEventDTO,
    ) -> None:
        """
        Enqueue immutable telemetry event.

        Overflow behavior is explicit and deterministic.
        """

        async with self._condition:
            if self._closed:
                raise RuntimeError(
                    "telemetry queue closed",
                )

            if len(self._queue) < self._capacity:
                self._queue.append(event)
                self._empty_event.clear()

                self._condition.notify()

                return

            await self._handle_overflow(
                event,
            )

    async def get(
        self,
    ) -> LogEventDTO:
        """
        Await next telemetry event.
        """

        async with self._condition:
            while not self._queue and not self._closed:
                await self._condition.wait()

            if not self._queue:
                raise RuntimeError(
                    "telemetry queue drained",
                )

            event = self._queue.popleft()
            if not self._queue:
                self._empty_event.set()

            self._condition.notify()

            return event

    async def close(self) -> None:
        """
        Deterministically close queue ingestion.
        """

        async with self._condition:
            self._closed = True

            self._condition.notify_all()

    async def drain_iter(
        self,
    ) -> AsyncIterator[LogEventDTO]:
        """
        Drain remaining queued telemetry events.
        """

        while True:
            try:
                yield await self.get()

            except RuntimeError:
                return

    async def wait_until_empty(
        self,
    ) -> None:
        await self._empty_event.wait()

    async def _handle_overflow(
        self,
        event: LogEventDTO,
    ) -> None:
        policy = self._overflow_policy

        if policy == OverflowPolicy.DROP_OLDEST:
            self._queue.popleft()

            self._queue.append(event)

            self._dropped_events += 1

            self._condition.notify()

            return

        if policy == OverflowPolicy.DROP_NEWEST:
            self._dropped_events += 1

            return

        if policy == OverflowPolicy.REJECT:
            self._rejected_events += 1

            raise QueueOverflowError(
                "telemetry queue capacity exceeded",
            )

        if policy == OverflowPolicy.BLOCK:
            while len(self._queue) >= self._capacity and not self._closed:
                await self._condition.wait()

            if self._closed:
                raise RuntimeError(
                    "telemetry queue closed",
                )

            self._queue.append(event)

            self._condition.notify()

            return

        raise RuntimeError(
            f"unsupported overflow policy: {policy!r}",
        )

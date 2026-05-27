# tests/stress/observability/test_cancellation_storm.py

from __future__ import annotations

import asyncio

import pytest

from multimedia_scraper.core.observability.sinks.async_queue import (
    BoundedTelemetryQueue,
)
from multimedia_scraper.core.observability.sinks.overflow_policy import (
    OverflowPolicy,
)


@pytest.mark.asyncio
async def test_queue_survives_cancellation_storm() -> None:
    queue = BoundedTelemetryQueue(
        capacity=16,
        overflow_policy=(OverflowPolicy.DROP_NEWEST),
    )

    async def blocked_put() -> None:
        await queue.put(
            object(),  # type: ignore[arg-type]
        )

    tasks = [
        asyncio.create_task(
            blocked_put(),
        )
        for _ in range(100)
    ]

    for task in tasks:
        task.cancel()

    await asyncio.gather(
        *tasks,
        return_exceptions=True,
    )

    assert queue.depth() <= 16

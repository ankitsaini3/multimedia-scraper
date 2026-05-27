# tests/integration/observability/test_pipeline_backpressure.py

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
async def test_blocking_overflow_policy_applies_backpressure() -> None:
    queue = BoundedTelemetryQueue(
        capacity=1,
        overflow_policy=(OverflowPolicy.BLOCK),
    )

    await queue.put(
        object(),  # type: ignore[arg-type]
    )

    blocked = False

    async def producer() -> None:
        nonlocal blocked

        blocked = True

        await queue.put(
            object(),  # type: ignore[arg-type]
        )

        blocked = False

    task = asyncio.create_task(
        producer(),
    )

    await asyncio.sleep(0.1)

    assert blocked is True

    await queue.get()

    await asyncio.wait_for(
        task,
        timeout=1,
    )

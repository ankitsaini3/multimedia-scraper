from __future__ import annotations

import pytest

from multimedia_scraper.runtime.events import (
    create_runtime_event,
)


@pytest.mark.asyncio
async def test_failing_event_handler_does_not_break_dispatch(
    event_bus,
):
    received = []

    async def failing_handler(event):
        raise RuntimeError("boom")

    async def healthy_handler(event):
        received.append(event)

    event = create_runtime_event(
        event_type="test-event",
    )

    event_bus.subscribe(
        type(event),
        failing_handler,
    )

    event_bus.subscribe(
        type(event),
        healthy_handler,
    )

    await event_bus.publish(event)

    assert len(received) == 1

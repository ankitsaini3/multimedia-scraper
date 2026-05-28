from __future__ import annotations

import pytest

from multimedia_scraper.runtime.events import (
    create_runtime_event,
)


@pytest.mark.asyncio
async def test_event_bus_dispatches_events(
    event_bus,
):
    received = []

    async def handler(event):
        received.append(event)

    event = create_runtime_event(
        event_type="test-event",
    )

    event_bus.subscribe(
        type(event),
        handler,
    )

    await event_bus.publish(event)

    assert len(received) == 1


@pytest.mark.asyncio
async def test_event_bus_unsubscribe(
    event_bus,
):
    received = []

    async def handler(event):
        received.append(event)

    event = create_runtime_event(
        event_type="test-event",
    )

    event_bus.subscribe(
        type(event),
        handler,
    )

    event_bus.unsubscribe(
        type(event),
        handler,
    )

    await event_bus.publish(event)

    assert received == []

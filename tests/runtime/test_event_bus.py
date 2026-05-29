from __future__ import annotations

import asyncio

import pytest

from multimedia_scraper.runtime.cancellation import (
    RuntimeCancellationError,
    create_root_cancellation_scope,
)
from multimedia_scraper.runtime.event_bus import (
    RuntimeEventBus,
)
from multimedia_scraper.runtime.events import (
    RuntimeEvent,
    create_runtime_event,
)
from multimedia_scraper.runtime.supervisor import (
    TaskSupervisor,
)

pytestmark = pytest.mark.asyncio


async def test_event_handlers_execute() -> None:
    scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="root",
        cancellation_scope=scope,
    )

    bus = RuntimeEventBus(
        supervisor=supervisor,
        cancellation_scope=scope,
    )

    received = asyncio.Event()

    async def handler(
        event: RuntimeEvent,
    ) -> None:
        received.set()

    bus.subscribe(
        RuntimeEvent,
        handler,
    )

    await bus.publish(
        create_runtime_event(
            event_type="test",
        ),
    )

    await asyncio.sleep(0)
    assert received.is_set()


async def test_publish_respects_cancellation() -> None:
    scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="root",
        cancellation_scope=scope,
    )

    bus = RuntimeEventBus(
        supervisor=supervisor,
        cancellation_scope=scope,
    )

    scope.cancel()

    with pytest.raises(
        RuntimeCancellationError,
    ):
        await bus.publish(
            create_runtime_event(
                event_type="cancelled",
            ),
        )


async def test_event_bus_shutdown_is_idempotent() -> None:
    scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="root",
        cancellation_scope=scope,
    )

    bus = RuntimeEventBus(
        supervisor=supervisor,
        cancellation_scope=scope,
    )

    await bus.shutdown()
    await bus.shutdown()

    assert bus.is_closed is True


async def test_handler_failures_are_isolated() -> None:
    scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="root",
        cancellation_scope=scope,
    )

    bus = RuntimeEventBus(
        supervisor=supervisor,
        cancellation_scope=scope,
    )

    successful = asyncio.Event()

    async def failing(
        event: RuntimeEvent,
    ) -> None:
        raise RuntimeError("boom")

    async def succeeding(
        event: RuntimeEvent,
    ) -> None:
        successful.set()

    bus.subscribe(
        RuntimeEvent,
        failing,
    )

    bus.subscribe(
        RuntimeEvent,
        succeeding,
    )

    await bus.publish(
        create_runtime_event(
            event_type="failure-test",
        ),
    )

    await asyncio.sleep(0)
    assert successful.is_set()


async def test_publish_does_not_leave_orphan_tasks() -> None:
    scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="root",
        cancellation_scope=scope,
    )

    bus = RuntimeEventBus(
        supervisor=supervisor,
        cancellation_scope=scope,
    )

    async def handler(
        event: RuntimeEvent,
    ) -> None:
        return None

    bus.subscribe(
        RuntimeEvent,
        handler,
    )

    await bus.publish(
        create_runtime_event(
            event_type="test",
        ),
    )

    await asyncio.sleep(0)

    assert supervisor._children == set()
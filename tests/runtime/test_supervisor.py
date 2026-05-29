from __future__ import annotations

import asyncio

import pytest

from multimedia_scraper.runtime.cancellation import (
    RuntimeCancellationError,
    create_root_cancellation_scope,
)
from multimedia_scraper.runtime.exceptions import (
    SupervisorClosedError,
)
from multimedia_scraper.runtime.supervisor import (
    TaskSupervisor,
)
from multimedia_scraper.runtime.context import (
    RuntimeContext
)

pytestmark = pytest.mark.asyncio


async def test_supervisor_tracks_spawned_tasks() -> None:
    scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="root",
        cancellation_scope=scope,
    )

    async def work() -> int:
        return 42

    task = supervisor.spawn(
        name="work",
        coroutine=work(),
    )

    assert len(supervisor._children) == 1

    result = await task.wait()

    assert result == 42

    await asyncio.sleep(0)

    assert len(supervisor._children) == 0


async def test_closed_supervisor_rejects_spawn() -> None:
    scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="root",
        cancellation_scope=scope,
    )

    await supervisor.shutdown()

    async def work() -> None:
        return None

    coroutine = work()

    try:
        with pytest.raises(
            SupervisorClosedError,
        ):
            supervisor.spawn(
                name="work",
                coroutine=coroutine,
            )

    finally:
        coroutine.close()


async def test_supervisor_shutdown_propagates_cancellation() -> None:
    scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="root",
        cancellation_scope=scope,
    )

    started = asyncio.Event()

    cancelled = asyncio.Event()

    async def worker() -> None:
        started.set()

        try:
            while True:
                scope.raise_if_cancelled()

                await asyncio.sleep(0.01)

        except RuntimeCancellationError:
            cancelled.set()

    supervisor.spawn(
        name="worker",
        coroutine=worker(),
    )

    await started.wait()

    await supervisor.shutdown()

    assert cancelled.is_set()


async def test_supervisor_shutdown_is_idempotent() -> None:
    scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="root",
        cancellation_scope=scope,
    )

    await supervisor.shutdown()
    await supervisor.shutdown()
    await supervisor.shutdown()

    assert supervisor.is_closed is True



async def test_supervisor_prevents_orphan_tasks() -> None:
    scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="root",
        cancellation_scope=scope,
    )

    async def work() -> None:
        return None

    task = supervisor.spawn(
        name="work",
        coroutine=work(),
    )

    await task.wait()

    await asyncio.sleep(0)

    assert supervisor._children == set()

async def test_runtime_can_execute_supervised_work(
    fake_runtime_context: RuntimeContext,
) -> None:
    completed = asyncio.Event()

    async def worker() -> None:
        completed.set()

    task = fake_runtime_context.spawn(
        name="worker",
        coroutine=worker(),
    )

    await task.wait()

    assert completed.is_set()
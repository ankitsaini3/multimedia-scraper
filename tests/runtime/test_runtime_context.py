from __future__ import annotations

import asyncio

import pytest

from multimedia_scraper.runtime.context import (
    RuntimeContext,
)

pytestmark = pytest.mark.asyncio


async def test_runtime_context_spawn_delegates_to_supervisor(
    fake_runtime_context: RuntimeContext,
) -> None:
    async def work() -> int:
        return 123

    task = fake_runtime_context.spawn(
        name="work",
        coroutine=work(),
    )

    result = await task.wait()

    assert result == 123


async def test_child_supervisor_inherits_cancellation(
    fake_runtime_context: RuntimeContext,
) -> None:
    child = fake_runtime_context.create_child_supervisor(
        name="child",
    )

    fake_runtime_context.cancellation_scope.cancel()

    assert child.cancellation_scope.is_cancelled is True


async def test_child_supervisor_has_isolated_task_tracking(
    fake_runtime_context: RuntimeContext,
) -> None:
    child = fake_runtime_context.create_child_supervisor(
        name="child",
    )

    async def work() -> None:
        return None

    task = child.spawn(
        name="work",
        coroutine=work(),
    )

    await task.wait()

    await asyncio.sleep(0)

    assert child._children == set()

    assert fake_runtime_context.supervisor._children == set()

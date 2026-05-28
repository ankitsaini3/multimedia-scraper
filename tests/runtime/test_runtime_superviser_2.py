from __future__ import annotations

import asyncio

import pytest


@pytest.mark.asyncio
async def test_all_runtime_tasks_owned_by_supervisor(
    supervisor,
):
    async def worker():
        await asyncio.sleep(0)

    task = supervisor.spawn(
        name="worker",
        coroutine=worker(),
    )

    assert task.task in supervisor._children

    await task.wait()

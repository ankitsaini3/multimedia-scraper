from __future__ import annotations

import asyncio

import pytest


@pytest.mark.asyncio
async def test_supervisor_tracks_spawned_tasks(
    supervisor,
):
    async def worker():
        await asyncio.sleep(0)

    task = supervisor.spawn(
        name="worker",
        coroutine=worker(),
    )

    assert task.done is False

    await task.wait()


@pytest.mark.asyncio
async def test_supervisor_shutdown_drains_tasks(
    supervisor,
):
    async def worker():
        await asyncio.sleep(0.01)

    supervisor.spawn(
        name="worker",
        coroutine=worker(),
    )

    await supervisor.shutdown()

    assert supervisor.is_closed is True

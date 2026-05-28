from __future__ import annotations

import asyncio

import pytest


@pytest.mark.asyncio
async def test_supervisor_cleanup_completes(
    supervisor,
):
    cleaned = False

    async def worker():
        nonlocal cleaned

        try:
            await asyncio.sleep(10)
        finally:
            cleaned = True

    supervisor.spawn(
        name="cleanup-worker",
        coroutine=worker(),
    )

    await supervisor.shutdown()

    assert cleaned is True

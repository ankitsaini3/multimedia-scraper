from __future__ import annotations

import asyncio

import pytest

from multimedia_scraper.runtime.bootstrap import (
    RuntimeBootstrapCoordinator,
)


@pytest.mark.asyncio
async def test_shutdown_is_idempotent(
    runtime_context,
    observability,
    diagnostics,
):
    coordinator = RuntimeBootstrapCoordinator(
        configuration=None,
        observability=observability,
        diagnostics=diagnostics,
    )

    await asyncio.gather(
        coordinator.shutdown(runtime_context),
        coordinator.shutdown(runtime_context),
        coordinator.shutdown(runtime_context),
    )

    assert observability.shutdown_called is True

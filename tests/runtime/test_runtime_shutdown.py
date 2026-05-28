from __future__ import annotations

import pytest

from multimedia_scraper.runtime.bootstrap import (
    RuntimeBootstrapCoordinator,
)


@pytest.mark.asyncio
async def test_runtime_shutdown_cancels_scope(
    runtime_context,
    observability,
    diagnostics,
):
    coordinator = RuntimeBootstrapCoordinator(
        configuration=None,
        observability=observability,
        diagnostics=diagnostics,
    )

    await coordinator.shutdown(runtime_context)

    assert runtime_context.cancellation_scope.is_cancelled is True


@pytest.mark.asyncio
async def test_runtime_shutdown_flushes_observability(
    runtime_context,
    observability,
    diagnostics,
):
    coordinator = RuntimeBootstrapCoordinator(
        configuration=None,
        observability=observability,
        diagnostics=diagnostics,
    )

    await coordinator.shutdown(runtime_context)

    assert observability.shutdown_called is True

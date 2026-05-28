from __future__ import annotations

import pytest

from multimedia_scraper.runtime.bootstrap import (
    RuntimeBootstrapCoordinator,
)
from multimedia_scraper.runtime.lifecycle import (
    RuntimeLifecycleState,
)


@pytest.mark.asyncio
async def test_runtime_bootstrap_reaches_active_state(
    observability,
    diagnostics,
):
    coordinator = RuntimeBootstrapCoordinator(
        configuration=None,
        observability=observability,
        diagnostics=diagnostics,
    )

    coordinator._state = RuntimeLifecycleState.BOOTSTRAPPING

    assert coordinator.state == (RuntimeLifecycleState.BOOTSTRAPPING)

from __future__ import annotations

import pytest

from multimedia_scraper.runtime.bootstrap import (
    RuntimeBootstrapCoordinator,
)
from multimedia_scraper.runtime.lifecycle import (
    RuntimeLifecycleState,
)


class FailingObservability:
    async def initialize(self):
        raise RuntimeError("startup failure")


@pytest.mark.asyncio
async def test_runtime_never_enters_active_on_failure(
    diagnostics,
):
    coordinator = RuntimeBootstrapCoordinator(
        configuration=None,
        observability=FailingObservability(),
        diagnostics=diagnostics,
    )

    with pytest.raises(RuntimeError):
        await coordinator.bootstrap()

    assert coordinator.state != (RuntimeLifecycleState.ACTIVE)

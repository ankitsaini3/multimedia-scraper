from __future__ import annotations

import pytest

from multimedia_scraper.runtime.context import (
    RuntimeContext,
)
from multimedia_scraper.runtime.lifecycle import (
    RuntimeLifecycleState,
)

pytestmark = pytest.mark.asyncio


async def test_runtime_bootstrap_activates_runtime(
    runtime_bootstrap_coordinator,
) -> None:
    context = await runtime_bootstrap_coordinator.bootstrap()

    assert isinstance(
        context,
        RuntimeContext,
    )

    assert (
        runtime_bootstrap_coordinator.state
        is RuntimeLifecycleState.ACTIVE
    )


async def test_runtime_shutdown_transitions_lifecycle(
    runtime_bootstrap_coordinator,
) -> None:
    context = await runtime_bootstrap_coordinator.bootstrap()

    await runtime_bootstrap_coordinator.shutdown(
        context,
    )

    assert (
        runtime_bootstrap_coordinator.state
        is RuntimeLifecycleState.TERMINATED
    )


async def test_runtime_shutdown_is_idempotent(
    runtime_bootstrap_coordinator,
) -> None:
    context = await runtime_bootstrap_coordinator.bootstrap()

    await runtime_bootstrap_coordinator.shutdown(
        context,
    )

    await runtime_bootstrap_coordinator.shutdown(
        context,
    )

    assert (
        runtime_bootstrap_coordinator.state
        is RuntimeLifecycleState.TERMINATED
    )


async def test_runtime_registry_contains_primitives(
    runtime_bootstrap_coordinator,
) -> None:
    context = await runtime_bootstrap_coordinator.bootstrap()

    resolved = context.registry.resolve(
        type(context.supervisor),
    )

    assert resolved is context.supervisor
# tests/stress/observability/test_concurrent_logging.py

from __future__ import annotations

import asyncio

import pytest

from multimedia_scraper.core.observability.context.propagation import (
    bind_telemetry_context,
    get_telemetry_context,
)
from multimedia_scraper.core.observability.internal.context_builders import (
    create_root_telemetry_context,
)


@pytest.mark.asyncio
async def test_concurrent_context_isolation() -> None:
    async def worker(
        index: int,
    ) -> str:
        context = create_root_telemetry_context(
            runtime_scope_id=(f"scope-{index}"),
            runtime_id="runtime",
            subsystem="worker",
            operation="concurrent",
            supervisor_id="root",
        )

        with bind_telemetry_context(
            context,
        ):
            await asyncio.sleep(0)

            current = get_telemetry_context()

            assert current is not None

            return current.correlation.correlation_id

    results = await asyncio.gather(
        *[worker(index) for index in range(50)],
    )

    assert len(results) == len(set(results))

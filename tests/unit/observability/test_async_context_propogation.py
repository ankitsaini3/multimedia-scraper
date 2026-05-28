# tests/core/observability/test_async_context_propagation.py

from __future__ import annotations

import asyncio

import pytest

from multimedia_scraper.core.observability.context.propagation import (
    bind_telemetry_context,
    child_telemetry_context,
    get_telemetry_context,
)
from multimedia_scraper.core.observability.internal.context_builders import (
    create_root_telemetry_context,
)


@pytest.mark.asyncio
async def test_context_propagation_is_deterministic() -> None:
    root = create_root_telemetry_context(
        runtime_scope_id="scope",
        runtime_id="runtime",
        subsystem="runtime",
        operation="startup",
        supervisor_id="root",
    )

    async def child_task() -> str:
        context = get_telemetry_context()

        assert context is not None

        return context.correlation.trace.trace_id

    with bind_telemetry_context(
        root,
    ):
        async with asyncio.TaskGroup() as tg:
            task_1 = tg.create_task(
                child_task(),
            )

            task_2 = tg.create_task(
                child_task(),
            )

        assert task_1.result() == task_2.result()


@pytest.mark.asyncio
async def test_child_context_preserves_trace_lineage() -> None:
    root = create_root_telemetry_context(
        runtime_scope_id="scope",
        runtime_id="runtime",
        subsystem="runtime",
        operation="startup",
        supervisor_id="root",
    )

    with (
        bind_telemetry_context(
            root,
        ),
        child_telemetry_context(
            operation="worker",
        ) as child,
    ):
        assert child.correlation.trace.trace_id == root.correlation.trace.trace_id

        assert child.correlation.trace.parent_span_id == root.correlation.trace.span_id

# tests/stress/observability/test_queue_pressure.py

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest

from multimedia_scraper.core.observability.dto.correlation import (
    CorrelationMetadataDTO,
)
from multimedia_scraper.core.observability.dto.event_category import (
    EventCategory,
)
from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.dto.operation_trace import (
    OperationTraceDTO,
)
from multimedia_scraper.core.observability.dto.severity import (
    LogSeverity,
)
from multimedia_scraper.core.observability.dto.supervision_lineage import (
    SupervisionLineageDTO,
)
from multimedia_scraper.core.observability.sinks.async_queue import (
    BoundedTelemetryQueue,
)
from multimedia_scraper.core.observability.sinks.overflow_policy import (
    OverflowPolicy,
)


def _event(
    index: int,
) -> LogEventDTO:
    trace = OperationTraceDTO(
        trace_id=f"trace-{index}",
        span_id=f"span-{index}",
        parent_span_id=None,
        operation_id=f"op-{index}",
        operation_name="pressure",
        started_at_utc=datetime.now(
            tz=UTC,
        ),
    )

    supervision = SupervisionLineageDTO(
        runtime_id="runtime",
        root_supervisor_id="root",
        supervisor_id="root",
        parent_supervisor_id=None,
        supervisor_depth=0,
    )

    correlation = CorrelationMetadataDTO(
        correlation_id=f"corr-{index}",
        causation_id=None,
        runtime_scope_id="scope",
        trace=trace,
        supervision=supervision,
    )

    return LogEventDTO(
        timestamp_utc=datetime.now(
            tz=UTC,
        ),
        monotonic_ns=index,
        severity=LogSeverity.INFO,
        event_category=(EventCategory.RUNTIME),
        subsystem="runtime",
        operation="pressure",
        message=f"event-{index}",
        correlation=correlation,
        fields={},
    )


@pytest.mark.asyncio
async def test_queue_remains_bounded_under_pressure() -> None:
    queue = BoundedTelemetryQueue(
        capacity=32,
        overflow_policy=(OverflowPolicy.DROP_OLDEST),
    )

    async def producer(
        offset: int,
    ) -> None:
        for index in range(100):
            await queue.put(
                _event(
                    offset + index,
                ),
            )

    await asyncio.gather(
        producer(0),
        producer(1000),
        producer(2000),
    )

    assert queue.depth() <= 32

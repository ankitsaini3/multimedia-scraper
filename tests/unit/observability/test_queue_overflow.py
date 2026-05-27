# tests/core/observability/test_queue_overflow.py

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from multimedia_scraper.core.errors.concurrency import (
    QueueOverflowError,
)
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
        operation_name="overflow",
        started_at_utc=datetime.now(
            tz=timezone.utc,
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
            tz=timezone.utc,
        ),
        monotonic_ns=index,
        severity=LogSeverity.INFO,
        event_category=(EventCategory.RUNTIME),
        subsystem="runtime",
        operation="overflow",
        message=f"event-{index}",
        correlation=correlation,
        fields={},
    )


@pytest.mark.asyncio
async def test_queue_reject_policy() -> None:
    queue = BoundedTelemetryQueue(
        capacity=1,
        overflow_policy=(OverflowPolicy.REJECT),
    )

    await queue.put(
        _event(1),
    )

    with pytest.raises(
        QueueOverflowError,
    ):
        await queue.put(
            _event(2),
        )


@pytest.mark.asyncio
async def test_queue_drop_oldest_policy() -> None:
    queue = BoundedTelemetryQueue(
        capacity=1,
        overflow_policy=(OverflowPolicy.DROP_OLDEST),
    )

    await queue.put(
        _event(1),
    )

    await queue.put(
        _event(2),
    )

    item = await queue.get()

    assert item.message == "event-2"

    stats = queue.statistics()

    assert stats.dropped_events == 1

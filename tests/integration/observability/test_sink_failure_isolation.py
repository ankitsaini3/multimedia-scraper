# tests/core/observability/test_sink_failure_isolation.py

from __future__ import annotations

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
from multimedia_scraper.core.observability.sinks.base import (
    BaseTelemetrySink,
)
from multimedia_scraper.core.observability.sinks.composite_sink import (
    CompositeTelemetrySink,
)


class FailingSink(
    BaseTelemetrySink,
):
    async def _write_event(
        self,
        event: LogEventDTO,
    ) -> None:
        raise RuntimeError(
            "sink failure",
        )


class HealthySink(
    BaseTelemetrySink,
):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.events: list[LogEventDTO] = []

    async def _write_event(
        self,
        event: LogEventDTO,
    ) -> None:
        self.events.append(
            event,
        )


def _event() -> LogEventDTO:
    trace = OperationTraceDTO(
        trace_id="trace",
        span_id="span",
        parent_span_id=None,
        operation_id="op",
        operation_name="runtime",
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
        correlation_id="corr",
        causation_id=None,
        runtime_scope_id="scope",
        trace=trace,
        supervision=supervision,
    )

    return LogEventDTO(
        timestamp_utc=datetime.now(
            tz=UTC,
        ),
        monotonic_ns=1,
        severity=LogSeverity.INFO,
        event_category=(EventCategory.RUNTIME),
        subsystem="runtime",
        operation="runtime",
        message="event",
        correlation=correlation,
        fields={},
    )


@pytest.mark.asyncio
async def test_sink_failures_are_isolated() -> None:
    failing = FailingSink()

    healthy = HealthySink()

    composite = CompositeTelemetrySink(
        sinks=[
            failing,
            healthy,
        ],
    )

    await composite.start()

    await composite.emit(
        _event(),
    )

    await composite.shutdown()

    assert len(healthy.events) == 1

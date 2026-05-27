# tests/core/observability/test_shutdown_flush.py

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


class InMemorySink(
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
        operation_name="startup",
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
        operation="shutdown",
        message="flush",
        correlation=correlation,
        fields={},
    )


@pytest.mark.asyncio
async def test_shutdown_flushes_events() -> None:
    sink = InMemorySink()

    await sink.start()

    await sink.emit(
        _event(),
    )

    await sink.shutdown()

    assert len(sink.events) == 1

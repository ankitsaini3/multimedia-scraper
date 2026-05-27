# tests/core/observability/test_canonical_json.py

from __future__ import annotations

from datetime import datetime, timezone

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
from multimedia_scraper.core.observability.serialization.canonical_json import (
    serialize_log_event,
)


def test_log_serialization_is_deterministic() -> None:
    trace = OperationTraceDTO(
        trace_id="trace-1",
        span_id="span-1",
        parent_span_id=None,
        operation_id="op-1",
        operation_name="startup",
        started_at_utc=datetime(
            2026,
            1,
            1,
            tzinfo=timezone.utc,
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
        correlation_id="corr-1",
        causation_id=None,
        runtime_scope_id="scope",
        trace=trace,
        supervision=supervision,
    )

    event = LogEventDTO(
        timestamp_utc=datetime(
            2026,
            1,
            1,
            tzinfo=timezone.utc,
        ),
        monotonic_ns=123,
        severity=LogSeverity.INFO,
        event_category=(EventCategory.RUNTIME),
        subsystem="runtime",
        operation="bootstrap",
        message="startup complete",
        correlation=correlation,
        fields={
            "a": 1,
            "b": "two",
        },
    )

    first = serialize_log_event(
        event,
    )

    second = serialize_log_event(
        event,
    )

    assert first == second

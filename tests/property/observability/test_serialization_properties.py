# tests/property/observability/test_serialization_properties.py

from __future__ import annotations

from datetime import UTC, datetime

from hypothesis import given, strategies as st

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


@given(
    st.text(
        min_size=1,
        max_size=32,
    ),
)
def test_serialization_is_stable(
    message: str,
) -> None:
    trace = OperationTraceDTO(
        trace_id="trace",
        span_id="span",
        parent_span_id=None,
        operation_id="op",
        operation_name="property",
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

    event = LogEventDTO(
        timestamp_utc=datetime.now(
            tz=UTC,
        ),
        monotonic_ns=1,
        severity=LogSeverity.INFO,
        event_category=(EventCategory.RUNTIME),
        subsystem="runtime",
        operation="property",
        message=message,
        correlation=correlation,
        fields={},
    )

    first = serialize_log_event(
        event,
    )

    second = serialize_log_event(
        event,
    )

    assert first == second

# src/multimedia_scraper/core/observability/internal/context_builders.py

from __future__ import annotations

from datetime import UTC, datetime

from multimedia_scraper.core.observability.dto.correlation import (
    CorrelationMetadataDTO,
)
from multimedia_scraper.core.observability.dto.operation_trace import (
    OperationTraceDTO,
)
from multimedia_scraper.core.observability.dto.supervision_lineage import (
    SupervisionLineageDTO,
)
from multimedia_scraper.core.observability.dto.telemetry_context import (
    TelemetryContextDTO,
)
from multimedia_scraper.core.observability.internal.ids import (
    new_correlation_id,
    new_span_id,
    new_trace_id,
)


def create_root_telemetry_context(
    *,
    runtime_scope_id: str,
    runtime_id: str,
    subsystem: str,
    operation: str,
    supervisor_id: str,
    task_id: str | None = None,
) -> TelemetryContextDTO:
    """
    Create root runtime telemetry context.
    """

    trace_id = new_trace_id()
    child_span_id = new_span_id()

    return TelemetryContextDTO(
        correlation=CorrelationMetadataDTO(
            correlation_id=new_correlation_id(),
            causation_id=None,
            runtime_scope_id=runtime_scope_id,
            trace=OperationTraceDTO(
                trace_id=trace_id,
                span_id=child_span_id,
                parent_span_id=None,
                operation_id=new_correlation_id(),
                operation_name=operation,
                started_at_utc=datetime.now(
                    tz=UTC,
                ),
            ),
            supervision=SupervisionLineageDTO(
                runtime_id=runtime_id,
                root_supervisor_id=supervisor_id,
                supervisor_id=supervisor_id,
                parent_supervisor_id=None,
                supervisor_depth=0,
                task_id=task_id,
            ),
        ),
        subsystem=subsystem,
        operation=operation,
    )


def create_child_telemetry_context(
    parent: TelemetryContextDTO,
    *,
    subsystem: str | None = None,
    operation: str | None = None,
    supervisor_id: str | None = None,
    task_id: str | None = None,
) -> TelemetryContextDTO:
    """
    Create immutable child telemetry context.

    Guarantees:
    - deterministic lineage propagation
    - immutable ancestry
    - explicit child ownership
    - async-safe propagation
    """

    parent_trace = parent.correlation.trace
    parent_supervision = parent.correlation.supervision

    child_span_id = new_span_id()

    return TelemetryContextDTO(
        correlation=CorrelationMetadataDTO(
            correlation_id=parent.correlation.correlation_id,
            causation_id=parent_trace.span_id,
            runtime_scope_id=parent.correlation.runtime_scope_id,
            trace=OperationTraceDTO(
                trace_id=parent_trace.trace_id,
                span_id=child_span_id,
                parent_span_id=parent_trace.span_id,
                operation_id=new_correlation_id(),
                operation_name=(operation or parent.operation),
                started_at_utc=datetime.now(
                    tz=UTC,
                ),
            ),
            supervision=SupervisionLineageDTO(
                runtime_id=parent_supervision.runtime_id,
                root_supervisor_id=(parent_supervision.root_supervisor_id),
                supervisor_id=(supervisor_id or parent_supervision.supervisor_id),
                parent_supervisor_id=(parent_supervision.supervisor_id),
                supervisor_depth=(parent_supervision.supervisor_depth + 1),
                task_id=task_id,
            ),
        ),
        subsystem=subsystem or parent.subsystem,
        operation=operation or parent.operation,
    )

# src/multimedia_scraper/core/observability/failures/failure_correlation.py

from __future__ import annotations

from dataclasses import dataclass

from multimedia_scraper.core.observability.dto.telemetry_context import (
    TelemetryContextDTO,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class FailureCorrelationSnapshot:
    """
    Immutable correlated runtime failure snapshot.

    Guarantees:
    - supervision lineage preservation
    - trace continuity
    - deterministic diagnostics
    """

    correlation_id: str

    trace_id: str

    span_id: str

    supervisor_id: str

    task_id: str | None

    operation: str

    subsystem: str


def correlate_failure(
    context: TelemetryContextDTO,
) -> FailureCorrelationSnapshot:
    """
    Extract deterministic failure lineage.
    """

    return FailureCorrelationSnapshot(
        correlation_id=(context.correlation.correlation_id),
        trace_id=(context.correlation.trace.trace_id),
        span_id=(context.correlation.trace.span_id),
        supervisor_id=(context.correlation.supervision.supervisor_id),
        task_id=(context.correlation.supervision.task_id),
        operation=(context.operation),
        subsystem=(context.subsystem),
    )

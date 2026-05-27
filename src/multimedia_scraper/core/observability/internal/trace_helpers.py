# src/multimedia_scraper/core/observability/internal/trace_helpers.py

from __future__ import annotations

from multimedia_scraper.core.observability.dto.telemetry_context import (
    TelemetryContextDTO,
)


def trace_id(
    context: TelemetryContextDTO,
) -> str:
    return context.correlation.trace.trace_id


def span_id(
    context: TelemetryContextDTO,
) -> str:
    return context.correlation.trace.span_id


def correlation_id(
    context: TelemetryContextDTO,
) -> str:
    return context.correlation.correlation_id


def supervisor_id(
    context: TelemetryContextDTO,
) -> str:
    return context.correlation.supervision.supervisor_id

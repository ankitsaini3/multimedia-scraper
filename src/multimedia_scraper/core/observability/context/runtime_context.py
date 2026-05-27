# src/multimedia_scraper/core/observability/context/runtime_context.py

from __future__ import annotations

from contextvars import ContextVar

from multimedia_scraper.core.observability.dto.telemetry_context import (
    TelemetryContextDTO,
)

current_telemetry_context: ContextVar[TelemetryContextDTO | None] = ContextVar(
    "current_telemetry_context",
    default=None,
)

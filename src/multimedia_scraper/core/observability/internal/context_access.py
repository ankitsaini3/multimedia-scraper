# src/multimedia_scraper/core/observability/internal/context_access.py

from __future__ import annotations

from multimedia_scraper.core.errors.observability import (
    CorrelationPropagationError,
)
from multimedia_scraper.core.observability.context.runtime_context import (
    current_telemetry_context,
)
from multimedia_scraper.core.observability.dto.telemetry_context import (
    TelemetryContextDTO,
)


def require_telemetry_context(
    *,
    reason: str,
) -> TelemetryContextDTO:
    """
    Require active telemetry context.

    Used at runtime ownership boundaries where
    correlation propagation is mandatory.
    """

    context = current_telemetry_context.get()

    if context is None:
        raise CorrelationPropagationError(
            f"missing telemetry context: {reason}",
        )

    return context

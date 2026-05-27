# src/multimedia_scraper/core/observability/dto/telemetry_context.py

from __future__ import annotations

from dataclasses import dataclass

from multimedia_scraper.core.observability.dto.correlation import (
    CorrelationMetadataDTO,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TelemetryContextDTO:
    """
    Immutable task-local observability context.

    Context propagation MUST remain:
    - deterministic
    - task-local
    - async-safe
    - supervision-safe

    This context MUST NEVER:
    - contain runtime services
    - contain mutable state
    - contain live task handles
    """

    correlation: CorrelationMetadataDTO

    subsystem: str

    operation: str

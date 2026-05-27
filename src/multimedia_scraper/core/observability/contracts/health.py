# src/multimedia_scraper/core/observability/contracts/health.py

from __future__ import annotations

from dataclasses import dataclass

from strenum import StrEnum


class TelemetryHealthStatus(
    StrEnum,
):
    HEALTHY = "healthy"

    DEGRADED = "degraded"

    UNHEALTHY = "unhealthy"


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TelemetryHealthSnapshot:
    """
    Immutable telemetry infrastructure health snapshot.
    """

    status: TelemetryHealthStatus

    queue_depth: int

    dropped_events: int

    last_failure_unix_ns: int | None

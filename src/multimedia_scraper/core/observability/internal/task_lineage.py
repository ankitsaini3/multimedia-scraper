# src/multimedia_scraper/core/observability/internal/task_lineage.py

from __future__ import annotations

from multimedia_scraper.core.observability.dto.telemetry_context import (
    TelemetryContextDTO,
)


def task_lineage_path(
    context: TelemetryContextDTO,
) -> str:
    """
    Deterministic supervision lineage representation.

    Useful for:
    - diagnostics
    - structured telemetry
    - failure reconstruction
    """

    supervision = context.correlation.supervision

    return (
        f"{supervision.root_supervisor_id}"
        f"/{supervision.supervisor_id}"
        f"/depth:{supervision.supervisor_depth}"
    )

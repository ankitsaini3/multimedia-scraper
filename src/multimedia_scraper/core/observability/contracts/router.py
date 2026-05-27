# src/multimedia_scraper/core/observability/contracts/router.py

from __future__ import annotations

from typing import Protocol

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)


class TelemetryRouter(
    Protocol,
):
    """
    Infrastructure-isolated telemetry routing contract.

    Routers MUST:
    - avoid event mutation
    - preserve ordering semantics
    - remain bounded
    """

    async def route(
        self,
        event: LogEventDTO,
    ) -> None:
        """
        Route immutable telemetry event.
        """

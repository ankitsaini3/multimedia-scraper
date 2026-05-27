# src/multimedia_scraper/core/observability/contracts/pipeline.py

from __future__ import annotations

from typing import Protocol

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)


class TelemetryPipeline(
    Protocol,
):
    """
    Runtime-owned telemetry processing pipeline.

    Pipelines MUST:
    - define bounded behavior
    - define overflow policy
    - define shutdown semantics
    """

    async def enqueue(
        self,
        event: LogEventDTO,
    ) -> None:
        """
        Enqueue immutable telemetry event.
        """

    async def drain(self) -> None:
        """
        Drain pending telemetry deterministically.
        """

    def queue_depth(self) -> int:
        """
        Current bounded queue depth.
        """

    def capacity(self) -> int:
        """
        Maximum bounded capacity.
        """

# src/multimedia_scraper/core/observability/contracts/emitter.py

from __future__ import annotations

from typing import Protocol

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)


class StructuredEventEmitter(
    Protocol,
):
    """
    Runtime-owned telemetry emission contract.

    Emission MUST remain:
    - bounded
    - async-safe
    - cancellation-safe
    - supervision-safe
    """

    async def emit(
        self,
        event: LogEventDTO,
    ) -> None:
        """
        Emit immutable telemetry event.
        """


class StructuredEventPublisher(
    Protocol,
):
    """
    Structured telemetry publication coordinator.

    Infrastructure-independent publication boundary.
    """

    async def publish(
        self,
        event: LogEventDTO,
    ) -> None:
        """
        Publish structured telemetry event.
        """

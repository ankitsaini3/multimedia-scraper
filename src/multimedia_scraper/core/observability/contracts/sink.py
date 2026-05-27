# src/multimedia_scraper/core/observability/contracts/sink.py

from __future__ import annotations

from typing import Protocol

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)


class TelemetrySink(Protocol):
    """
    Structured telemetry sink contract.

    Infrastructure isolation boundary.

    Sinks MUST:
    - remain bounded
    - remain failure-isolated
    - remain async-safe
    - support deterministic shutdown
    """

    async def start(self) -> None:
        """
        Initialize sink infrastructure.
        """

    async def emit(
        self,
        event: LogEventDTO,
    ) -> None:
        """
        Consume immutable structured telemetry event.
        """

    async def flush(self) -> None:
        """
        Flush buffered telemetry deterministically.
        """

    async def shutdown(self) -> None:
        """
        Deterministic sink shutdown.
        """

    def is_healthy(self) -> bool:
        """
        Return infrastructure health state.
        """

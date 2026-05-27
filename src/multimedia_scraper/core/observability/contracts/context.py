# src/multimedia_scraper/core/observability/contracts/context.py

from __future__ import annotations

from typing import Protocol

from multimedia_scraper.core.observability.dto.telemetry_context import (
    TelemetryContextDTO,
)


class TelemetryContextProvider(
    Protocol,
):
    """
    Task-local telemetry context provider.
    """

    def get_context(
        self,
    ) -> TelemetryContextDTO | None: ...


class TelemetryContextBinder(
    Protocol,
):
    """
    Runtime-owned telemetry context binder.
    """

    def bind(
        self,
        context: TelemetryContextDTO,
    ) -> None: ...

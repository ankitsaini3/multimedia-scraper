# src/multimedia_scraper/core/observability/contracts/formatter.py

from __future__ import annotations

from typing import Protocol

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)


class StructuredEventFormatter(
    Protocol,
):
    """
    Structured event formatting contract.

    Formatters MUST:
    - remain deterministic
    - avoid event mutation
    - preserve causality
    - preserve correlation metadata
    """

    def format(
        self,
        event: LogEventDTO,
    ) -> bytes:
        """
        Format immutable telemetry event into transport payload.
        """

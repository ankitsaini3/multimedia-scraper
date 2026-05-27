# src/multimedia_scraper/core/observability/contracts/filtering.py

from __future__ import annotations

from typing import Protocol

from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)


class StructuredEventFilter(
    Protocol,
):
    """
    Structured telemetry filtering contract.

    Filtering MUST:
    - remain deterministic
    - avoid event mutation
    - preserve runtime isolation
    """

    def should_emit(
        self,
        event: LogEventDTO,
    ) -> bool:
        """
        Return True if event should propagate.
        """

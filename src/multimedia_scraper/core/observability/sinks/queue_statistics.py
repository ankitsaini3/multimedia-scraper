# src/multimedia_scraper/core/observability/sinks/queue_statistics.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class QueueStatistics:
    """
    Immutable bounded queue statistics snapshot.
    """

    capacity: int

    current_depth: int

    dropped_events: int

    rejected_events: int

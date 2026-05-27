# src/multimedia_scraper/core/observability/sinks/overflow_policy.py

from __future__ import annotations

from strenum import StrEnum


class OverflowPolicy(StrEnum):
    """
    Canonical bounded telemetry overflow behavior.
    """

    DROP_OLDEST = "drop_oldest"

    DROP_NEWEST = "drop_newest"

    BLOCK = "block"

    REJECT = "reject"

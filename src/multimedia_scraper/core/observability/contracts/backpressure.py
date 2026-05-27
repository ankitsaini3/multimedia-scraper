# src/multimedia_scraper/core/observability/contracts/backpressure.py

from __future__ import annotations

from strenum import StrEnum


class OverflowPolicy(
    StrEnum,
):
    """
    Canonical bounded telemetry overflow semantics.
    """

    DROP_OLDEST = "drop_oldest"

    DROP_NEWEST = "drop_newest"

    BLOCK = "block"

    REJECT = "reject"

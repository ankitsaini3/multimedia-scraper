# src/multimedia_scraper/core/observability/bootstrap/degraded_mode.py

from __future__ import annotations

from strenum import StrEnum


class DegradedObservabilityReason(
    StrEnum,
):
    SINK_FAILURE = "sink_failure"

    QUEUE_PRESSURE = "queue_pressure"

    SERIALIZATION_FAILURE = "serialization_failure"

    BOOTSTRAP_FAILURE = "bootstrap_failure"

    FLUSH_FAILURE = "flush_failure"

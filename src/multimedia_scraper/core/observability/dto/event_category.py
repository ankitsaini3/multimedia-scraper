# src/multimedia_scraper/core/observability/dto/event_category.py

from __future__ import annotations

from strenum import StrEnum


class EventCategory(StrEnum):
    """
    Semantic event classification taxonomy.
    """

    RUNTIME = "runtime"
    LIFECYCLE = "lifecycle"
    SUPERVISION = "supervision"
    CANCELLATION = "cancellation"
    RESOURCE = "resource"
    NETWORK = "network"
    PLUGIN = "plugin"
    SECURITY = "security"
    TELEMETRY = "telemetry"
    FAILURE = "failure"

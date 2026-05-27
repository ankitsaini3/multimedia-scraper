# src/multimedia_scraper/core/observability/contracts/events.py

from __future__ import annotations

from typing import Protocol


class StructuredTelemetryEvent(
    Protocol,
):
    """
    Canonical structured telemetry event contract.
    """

    @property
    def schema_version(self) -> int: ...

    def serialize(self) -> bytes:
        """
        Deterministic serialization contract.
        """


class ReplayableTelemetryEvent(
    StructuredTelemetryEvent,
    Protocol,
):
    """
    Replay-safe telemetry event contract.
    """

    @property
    def event_id(self) -> str: ...

    @property
    def occurred_at_unix_ns(self) -> int: ...

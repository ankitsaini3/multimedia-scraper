# src/multimedia_scraper/core/observability/contracts/lifecycle.py

from __future__ import annotations

from typing import Protocol

from strenum import StrEnum


class ObservabilityLifecycleState(
    StrEnum,
):
    CREATED = "created"

    INITIALIZED = "initialized"

    ACTIVE = "active"

    DRAINING = "draining"

    FLUSHING = "flushing"

    SHUTDOWN = "shutdown"


class LifecycleManagedTelemetryComponent(
    Protocol,
):
    """
    Lifecycle-aware telemetry infrastructure contract.

    Required by bootstrap + shutdown semantics.
    """

    async def initialize(self) -> None: ...

    async def start(self) -> None: ...

    async def drain(self) -> None: ...

    async def flush(self) -> None: ...

    async def shutdown(self) -> None: ...

    def lifecycle_state(
        self,
    ) -> ObservabilityLifecycleState: ...

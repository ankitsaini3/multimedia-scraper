# src/multimedia_scraper/core/observability/bootstrap/bootstrap_observability.py

from __future__ import annotations

from multimedia_scraper.core.observability.bootstrap.bootstrap_state import (
    ObservabilityBootstrapState,
)
from multimedia_scraper.core.observability.bootstrap.degraded_logger import (
    DegradedObservabilityLogger,
)
from multimedia_scraper.core.observability.bootstrap.degraded_mode import (
    DegradedObservabilityReason,
)
from multimedia_scraper.core.observability.bootstrap.early_bootstrap_buffer import (
    EarlyBootstrapBuffer,
)
from multimedia_scraper.core.observability.bootstrap.startup_diagnostics import (
    StartupDiagnosticsRegistry,
)
from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.sinks.composite_sink import (
    CompositeTelemetrySink,
)


class BootstrapObservabilityController:
    """
    Runtime-owned observability bootstrap coordinator.

    Integrates:
    - early bootstrap telemetry
    - startup diagnostics
    - degraded mode handling
    - deterministic shutdown flushing

    This controller is the ONLY authority for:
    - observability activation
    - degraded mode transition
    - startup telemetry replay
    """

    def __init__(
        self,
        *,
        early_buffer: (EarlyBootstrapBuffer),
        sink: CompositeTelemetrySink,
        degraded_logger: (DegradedObservabilityLogger),
        diagnostics: (StartupDiagnosticsRegistry),
    ) -> None:
        self._early_buffer = early_buffer

        self._sink = sink

        self._degraded_logger = degraded_logger

        self._diagnostics = diagnostics

        self._state = ObservabilityBootstrapState.PRE_BOOTSTRAP

        self._degraded = False

        self._dropped_events = 0

    @property
    def state(
        self,
    ) -> ObservabilityBootstrapState:
        return self._state

    @property
    def degraded_mode(
        self,
    ) -> bool:
        return (
            self._degraded
            or self._sink.degraded
        )

    async def initialize(
        self,
    ) -> None:
        self._state = ObservabilityBootstrapState.INITIALIZING

        try:
            await self._sink.start()

            await self._replay_early_events()

            self._state = ObservabilityBootstrapState.ACTIVE

        except Exception:
            self._degraded = True

            self._state = ObservabilityBootstrapState.DEGRADED

            raise

    async def emit(
        self,
        event: LogEventDTO,
    ) -> None:
        if self._degraded:
            await self._degraded_logger.emit_degraded_event(
                event=event,
                reason=(DegradedObservabilityReason.SINK_FAILURE),
            )

            return

        try:
            await self._sink.emit(
                event,
            )

            if self._sink.degraded:
                self._degraded = True

                self._state = (
                    ObservabilityBootstrapState
                    .DEGRADED
                )

        except Exception:
            self._degraded = True

            self._state = ObservabilityBootstrapState.DEGRADED

            self._dropped_events += 1

            await self._degraded_logger.emit_degraded_event(
                event=event,
                reason=(DegradedObservabilityReason.SINK_FAILURE),
            )

    async def shutdown(
        self,
    ) -> None:
        self._state = ObservabilityBootstrapState.DRAINING

        try:
            self._state = ObservabilityBootstrapState.FLUSHING

            await self._sink.flush()

        finally:
            self._state = ObservabilityBootstrapState.SHUTDOWN

            await self._sink.shutdown()

    async def _replay_early_events(
        self,
    ) -> None:
        events = self._early_buffer.drain()

        for event in events:
            await self._sink.emit(
                event,
            )

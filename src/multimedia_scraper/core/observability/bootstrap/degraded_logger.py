# src/multimedia_scraper/core/observability/bootstrap/degraded_logger.py

from __future__ import annotations

from collections.abc import Mapping

from multimedia_scraper.core.observability.bootstrap.degraded_mode import (
    DegradedObservabilityReason,
)
from multimedia_scraper.core.observability.dto.event_category import (
    EventCategory,
)
from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.dto.structured_fields import (
    StructuredValue,
)
from multimedia_scraper.core.observability.sinks.console_sink import (
    ConsoleTelemetrySink,
)


class DegradedObservabilityLogger:
    """
    Emergency degraded observability path.

    Used ONLY when:
    - normal routing fails
    - pipelines become unhealthy
    - sink infrastructure partially collapses

    Guarantees:
    - runtime survival
    - observability isolation
    - emergency visibility
    """

    def __init__(
        self,
        *,
        sink: ConsoleTelemetrySink,
    ) -> None:
        self._sink = sink

    async def emit_degraded_event(
        self,
        *,
        event: LogEventDTO,
        reason: (DegradedObservabilityReason),
        metadata: Mapping[
            str,
            StructuredValue,
        ]
        | None = None,
    ) -> None:
        degraded_event = LogEventDTO(
            timestamp_utc=(event.timestamp_utc),
            monotonic_ns=(event.monotonic_ns),
            severity=event.severity,
            event_category=(EventCategory.TELEMETRY),
            subsystem=("observability"),
            operation=("degraded-mode"),
            message=("observability entered degraded mode"),
            correlation=(event.correlation),
            fields={
                "reason": reason.value,
                "original_message": (event.message),
                **(metadata or {}),
            },
        )

        await self._sink.emit(
            degraded_event,
        )

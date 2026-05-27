# src/multimedia_scraper/core/observability/bootstrap/bootstrap_logger.py

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime

from multimedia_scraper.core.observability.bootstrap.early_bootstrap_buffer import (
    EarlyBootstrapBuffer,
)
from multimedia_scraper.core.observability.dto.event_category import (
    EventCategory,
)
from multimedia_scraper.core.observability.dto.log_event import (
    LogEventDTO,
)
from multimedia_scraper.core.observability.dto.severity import (
    LogSeverity,
)
from multimedia_scraper.core.observability.dto.structured_fields import (
    StructuredValue,
)
from multimedia_scraper.core.observability.internal.clocks import (
    monotonic_time_ns,
)
from multimedia_scraper.core.observability.internal.context_access import (
    require_telemetry_context,
)


class EarlyBootstrapLogger:
    """
    Bootstrap-safe emergency telemetry logger.

    Exists before:
    - full sink activation
    - pipeline activation
    - runtime ACTIVE state

    This logger intentionally:
    - avoids background scheduling
    - avoids worker startup
    - avoids runtime dependencies
    """

    def __init__(
        self,
        *,
        buffer: (EarlyBootstrapBuffer),
    ) -> None:
        self._buffer = buffer

    def log(
        self,
        *,
        severity: LogSeverity,
        event_category: EventCategory,
        message: str,
        fields: Mapping[
            str,
            StructuredValue,
        ]
        | None = None,
        exception: BaseException | None = None,
    ) -> None:
        context = require_telemetry_context(
            reason=("bootstrap logging requires telemetry context"),
        )

        event = LogEventDTO(
            timestamp_utc=datetime.now(
                tz=UTC,
            ),
            monotonic_ns=(monotonic_time_ns()),
            severity=severity,
            event_category=(event_category),
            subsystem=(context.subsystem),
            operation=(context.operation),
            message=message,
            correlation=(context.correlation),
            fields=fields or {},
            exception_type=(
                type(exception).__name__ if exception is not None else None
            ),
            exception_message=(str(exception) if exception is not None else None),
        )

        self._buffer.append(
            event,
        )

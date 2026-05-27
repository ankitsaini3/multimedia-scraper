# src/multimedia_scraper/core/observability/security/secure_event_factory.py

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime

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
from multimedia_scraper.core.observability.dto.telemetry_context import (
    TelemetryContextDTO,
)
from multimedia_scraper.core.observability.failures.exception_formatter import (
    format_exception,
)
from multimedia_scraper.core.observability.internal.clocks import (
    monotonic_time_ns,
)
from multimedia_scraper.core.observability.security.automatic_redaction import (
    automatically_redact_fields,
)


def create_secure_log_event(
    *,
    context: TelemetryContextDTO,
    severity: LogSeverity,
    event_category: EventCategory,
    message: str,
    fields: Mapping[
        str,
        StructuredValue,
    ]
    | None = None,
    exception: BaseException | None = None,
) -> LogEventDTO:
    """
    Create fully sanitized structured telemetry event.

    Guarantees:
    - immutable output
    - automatic redaction
    - deterministic serialization safety
    - secret filtering
    """

    sanitized_message = automatically_redact_fields(
        {
            "message": message,
        },
    )["message"]

    formatted_exception = (
        format_exception(
            exception,
        )
        if exception is not None
        else None
    )

    return LogEventDTO(
        timestamp_utc=datetime.now(
            tz=UTC,
        ),
        monotonic_ns=(monotonic_time_ns()),
        severity=severity,
        event_category=(event_category),
        subsystem=context.subsystem,
        operation=context.operation,
        message=str(
            sanitized_message,
        ),
        correlation=(context.correlation),
        fields=(
            automatically_redact_fields(
                fields or {},
            )
        ),
        exception_type=(
            formatted_exception.exception_type if formatted_exception else None
        ),
        exception_message=(
            formatted_exception.message if formatted_exception else None
        ),
    )

# src/multimedia_scraper/core/observability/security/plugin_safe_event_factory.py

from __future__ import annotations

from collections.abc import Mapping

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
from multimedia_scraper.core.observability.security.plugin_telemetry_policy import (
    PluginTelemetryPolicy,
)
from multimedia_scraper.core.observability.security.plugin_telemetry_redaction import (
    sanitize_plugin_fields,
)
from multimedia_scraper.core.observability.security.secure_event_factory import (
    create_secure_log_event,
)


def create_plugin_safe_event(
    *,
    context: TelemetryContextDTO,
    severity: LogSeverity,
    event_category: EventCategory,
    message: str,
    policy: PluginTelemetryPolicy,
    fields: Mapping[
        str,
        StructuredValue,
    ]
    | None = None,
    exception: BaseException | None = None,
) -> LogEventDTO:
    """
    Create plugin-isolated telemetry event.

    Guarantees:
    - plugin boundary isolation
    - host secret protection
    - deterministic field filtering
    """

    plugin_fields = sanitize_plugin_fields(
        fields or {},
        policy=policy,
    )

    sanitized_exception: BaseException | None

    if exception is not None and not policy.allow_exception_messages:
        sanitized_exception = RuntimeError(
            type(
                exception,
            ).__name__,
        )

    else:
        sanitized_exception = exception

    return create_secure_log_event(
        context=context,
        severity=severity,
        event_category=event_category,
        message=message,
        fields=plugin_fields,
        exception=sanitized_exception,
    )

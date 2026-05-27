# src/multimedia_scraper/core/observability/security/plugin_telemetry_redaction.py

from __future__ import annotations

from collections.abc import Mapping

from multimedia_scraper.core.observability.dto.structured_fields import (
    StructuredValue,
)
from multimedia_scraper.core.observability.security.plugin_telemetry_policy import (
    PluginTelemetryPolicy,
)

PLUGIN_RESTRICTED_FIELDS = frozenset(
    {
        "host_path",
        "filesystem_path",
        "environment",
        "env",
        "process",
        "subprocess",
        "token",
        "secret",
        "api_key",
    },
)


def sanitize_plugin_fields(
    fields: Mapping[
        str,
        StructuredValue,
    ],
    *,
    policy: PluginTelemetryPolicy,
) -> dict[str, StructuredValue]:
    """
    Produce plugin-safe structured telemetry payload.

    Guarantees:
    - host isolation
    - secret isolation
    - plugin-safe boundaries
    """

    if not (policy.allow_structured_fields):
        return {}

    sanitized: dict[
        str,
        StructuredValue,
    ] = {}

    for key, value in fields.items():
        normalized = key.lower()

        if normalized in PLUGIN_RESTRICTED_FIELDS:
            continue

        sanitized[key] = value

    return sanitized

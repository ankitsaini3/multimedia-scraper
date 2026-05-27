# src/multimedia_scraper/core/observability/security/plugin_telemetry_policy.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PluginTelemetryPolicy:
    """
    Immutable plugin telemetry isolation policy.

    Guarantees:
    - plugin-safe telemetry
    - boundary-safe diagnostics
    - capability-safe exposure
    """

    allow_exception_messages: bool

    allow_structured_fields: bool

    allow_host_paths: bool

    allow_environment_metadata: bool

# src/multimedia_scraper/core/errors/observability.py

from __future__ import annotations

from multimedia_scraper.core.errors.runtime import (
    RuntimeSystemError,
)


class ObservabilityError(
    RuntimeSystemError,
):
    """
    Base observability subsystem failure.
    """


class TelemetrySerializationError(
    ObservabilityError,
):
    """
    Structured telemetry serialization failure.
    """


class TelemetryValidationError(
    ObservabilityError,
):
    """
    Structured telemetry validation failure.
    """


class CorrelationPropagationError(
    ObservabilityError,
):
    """
    Correlation propagation integrity failure.
    """


class TelemetryBackpressureError(
    ObservabilityError,
):
    """
    Telemetry queue/buffer pressure violation.
    """


class TelemetryFlushError(
    ObservabilityError,
):
    """
    Deterministic telemetry flush failure.
    """


class RedactionFailureError(
    ObservabilityError,
):
    """
    Sensitive telemetry redaction failure.
    """

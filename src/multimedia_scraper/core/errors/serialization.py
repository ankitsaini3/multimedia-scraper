# src/multimedia_scraper/core/errors/serialization.py

from __future__ import annotations

from multimedia_scraper.core.errors.base import (
    InfrastructureError,
)


class SerializationError(
    InfrastructureError,
):
    """
    Base serialization failure.
    """


class DTOValidationError(
    SerializationError,
):
    """
    DTO schema validation failure.
    """


class DTOCompatibilityError(
    SerializationError,
):
    """
    DTO version compatibility failure.
    """


class DeserializationError(
    SerializationError,
):
    """
    Safe deserialization failure.
    """


class SchemaMigrationError(
    SerializationError,
):
    """
    DTO schema migration failure.
    """


class CanonicalEncodingError(
    SerializationError,
):
    """
    Canonical deterministic encoding failure.
    """

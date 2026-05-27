# src/multimedia_scraper/core/errors/configuration.py

from __future__ import annotations

from multimedia_scraper.core.errors.base import (
    ConfigurationError,
)


class ConfigurationValidationError(
    ConfigurationError,
):
    """
    Configuration schema validation failure.
    """


class ConfigurationResolutionError(
    ConfigurationError,
):
    """
    Configuration source resolution failure.
    """


class ConfigurationOverrideError(
    ConfigurationError,
):
    """
    Invalid configuration override semantics.
    """


class MissingConfigurationError(
    ConfigurationError,
):
    """
    Required configuration missing.
    """


class FrozenConfigurationMutationError(
    ConfigurationError,
):
    """
    Illegal mutation of frozen runtime configuration.
    """

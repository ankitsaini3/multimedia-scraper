# src/multimedia_scraper/core/errors/base.py

from __future__ import annotations


class MultimediaScraperError(Exception):
    """
    Canonical root runtime exception.

    All public runtime exceptions MUST derive from this root.
    """


class RuntimeSystemError(
    MultimediaScraperError,
):
    """
    Runtime coordination failure.

    Examples:
    - lifecycle corruption
    - supervision corruption
    - runtime invariant violation
    - cancellation corruption
    """


class InfrastructureError(
    MultimediaScraperError,
):
    """
    Infrastructure interaction failure.

    Examples:
    - filesystem failure
    - subprocess failure
    - network failure
    - serialization failure
    """


class IntegrationError(
    MultimediaScraperError,
):
    """
    External integration incompatibility.

    Examples:
    - plugin incompatibility
    - provider incompatibility
    - capability mismatch
    """


class DomainError(
    MultimediaScraperError,
):
    """
    Domain semantic failure.

    Examples:
    - invalid metadata
    - malformed DTO state
    - unsupported media structure
    """


class UserInputError(
    MultimediaScraperError,
):
    """
    Invalid user-provided input.
    """


class ConfigurationError(
    MultimediaScraperError,
):
    """
    Configuration validation or resolution failure.
    """

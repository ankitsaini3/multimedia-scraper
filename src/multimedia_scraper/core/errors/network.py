# src/multimedia_scraper/core/errors/network.py

from __future__ import annotations

from multimedia_scraper.core.errors.base import (
    InfrastructureError,
)


class NetworkError(
    InfrastructureError,
):
    """
    Base network infrastructure failure.
    """


class RequestTimeoutError(
    NetworkError,
):
    """
    Network timeout condition.
    """


class ConnectionFailureError(
    NetworkError,
):
    """
    Network connection establishment failure.
    """


class ResponseValidationError(
    NetworkError,
):
    """
    Invalid or malformed network response.
    """


class SSRFProtectionError(
    NetworkError,
):
    """
    SSRF protection rule violation.
    """

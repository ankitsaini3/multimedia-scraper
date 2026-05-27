# src/multimedia_scraper/core/errors/resources.py

from __future__ import annotations

from multimedia_scraper.core.errors.base import (
    RuntimeSystemError,
)


class ResourceError(
    RuntimeSystemError,
):
    """
    Base runtime resource failure.
    """


class ResourceLeakError(
    ResourceError,
):
    """
    Resource cleanup or ownership leak detected.
    """


class ResourceOwnershipError(
    ResourceError,
):
    """
    Invalid resource ownership semantics.
    """


class ResourceInitializationError(
    ResourceError,
):
    """
    Resource initialization failure.
    """


class ResourceCleanupError(
    ResourceError,
):
    """
    Resource cleanup failure.
    """


class ResourceExhaustedError(
    ResourceError,
):
    """
    Runtime resource exhaustion condition.
    """

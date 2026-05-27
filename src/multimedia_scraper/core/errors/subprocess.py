# src/multimedia_scraper/core/errors/subprocess.py

from __future__ import annotations

from multimedia_scraper.core.errors.base import (
    InfrastructureError,
)


class SubprocessError(
    InfrastructureError,
):
    """
    Base subprocess execution failure.
    """


class SubprocessLaunchError(
    SubprocessError,
):
    """
    Subprocess launch failure.
    """


class SubprocessTerminationError(
    SubprocessError,
):
    """
    Subprocess termination or reconciliation failure.
    """


class SubprocessTimeoutError(
    SubprocessError,
):
    """
    Subprocess execution timeout.
    """


class UnsupportedExecutableError(
    SubprocessError,
):
    """
    Unapproved executable invocation attempt.
    """

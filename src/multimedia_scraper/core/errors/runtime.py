# src/multimedia_scraper/core/errors/runtime.py

from __future__ import annotations

from multimedia_scraper.core.errors.base import (
    RuntimeSystemError as RuntimeSystemError,
)


class RuntimeInvariantViolationError(
    RuntimeSystemError,
):
    """
    Core runtime invariant violation.
    """


class RuntimeStateError(
    RuntimeSystemError,
):
    """
    Illegal runtime lifecycle transition or invalid runtime state.
    """


class RuntimeBootstrapError(
    RuntimeSystemError,
):
    """
    Runtime bootstrap failure.
    """


class RuntimeShutdownError(
    RuntimeSystemError,
):
    """
    Runtime shutdown failure.
    """


class RuntimeCancellationError(
    RuntimeSystemError,
):
    """
    Runtime cancellation propagation failure.
    """


class RuntimeHealthError(
    RuntimeSystemError,
):
    """
    Runtime health integrity failure.
    """

class CancellationScopeClosedError(RuntimeSystemError):
    """
    Raised when attempting to create children
    from a closed cancellation scope.
    """
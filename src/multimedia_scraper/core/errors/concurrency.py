# src/multimedia_scraper/core/errors/concurrency.py

from __future__ import annotations

from multimedia_scraper.core.errors.base import (
    RuntimeSystemError,
)


class ConcurrencyError(
    RuntimeSystemError,
):
    """
    Base concurrency semantics failure.
    """


class EventLoopBlockedError(
    ConcurrencyError,
):
    """
    Event loop blocking violation detected.
    """


class AsyncBoundaryViolationError(
    ConcurrencyError,
):
    """
    Illegal async/sync boundary behavior.
    """


class TaskOwnershipError(
    ConcurrencyError,
):
    """
    Invalid task ownership semantics.
    """


class ConcurrencyLimitExceededError(
    ConcurrencyError,
):
    """
    Bounded concurrency limit exceeded.
    """


class QueueOverflowError(
    ConcurrencyError,
):
    """
    Bounded queue overflow condition.
    """


class DeadlockRiskError(
    ConcurrencyError,
):
    """
    Potential deadlock condition detected.
    """

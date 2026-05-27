# src/multimedia_scraper/core/errors/supervision.py

from __future__ import annotations

from multimedia_scraper.core.errors.base import (
    RuntimeSystemError,
)


class SupervisionError(
    RuntimeSystemError,
):
    """
    Base supervision failure.
    """


class SupervisorCorruptionError(
    SupervisionError,
):
    """
    Supervision ownership graph corruption.
    """


class OrphanTaskError(
    SupervisionError,
):
    """
    Detached or unowned task detected.
    """


class RestartPolicyViolationError(
    SupervisionError,
):
    """
    Invalid restart behavior or restart storm condition.
    """


class TaskSupervisionError(
    SupervisionError,
):
    """
    Supervised task reconciliation failure.
    """


class ChildTaskEscapeError(
    SupervisionError,
):
    """
    Child task escaped parent lifecycle boundary.
    """

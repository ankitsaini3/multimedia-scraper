# src/multimedia_scraper/core/errors/security.py

from __future__ import annotations

from multimedia_scraper.core.errors.base import (
    RuntimeSystemError,
)


class SecurityBoundaryError(
    RuntimeSystemError,
):
    """
    Base security boundary violation.
    """


class SandboxViolationError(
    SecurityBoundaryError,
):
    """
    Sandbox isolation violation.
    """


class CapabilityDeniedError(
    SecurityBoundaryError,
):
    """
    Unauthorized capability access attempt.
    """


class PathTraversalError(
    SecurityBoundaryError,
):
    """
    Filesystem traversal attack attempt detected.
    """


class UnsafeSubprocessError(
    SecurityBoundaryError,
):
    """
    Unsafe subprocess execution attempt.
    """


class SecretExposureError(
    SecurityBoundaryError,
):
    """
    Sensitive credential exposure detected.
    """


class PluginIsolationError(
    SecurityBoundaryError,
):
    """
    Plugin isolation boundary violation.
    """

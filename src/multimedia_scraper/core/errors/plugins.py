# src/multimedia_scraper/core/errors/plugins.py

from __future__ import annotations

from multimedia_scraper.core.errors.base import (
    IntegrationError,
)


class PluginError(
    IntegrationError,
):
    """
    Base plugin integration failure.
    """


class PluginInitializationError(
    PluginError,
):
    """
    Plugin initialization failure.
    """


class PluginCompatibilityError(
    PluginError,
):
    """
    Plugin compatibility validation failure.
    """


class PluginCapabilityError(
    PluginError,
):
    """
    Plugin capability declaration violation.
    """


class PluginExecutionError(
    PluginError,
):
    """
    Plugin runtime execution failure.
    """


class PluginContractViolationError(
    PluginError,
):
    """
    Plugin contract semantic violation.
    """



class PluginShutdownError(
    PluginError,
):
    """Plugin shutdown reconciliation failure."""


class PluginTaskLeakError(
    PluginError,
):
    """Plugin leaked runtime-owned tasks."""



class PluginDiscoveryError(
    PluginError,
):
    """Plugin discovery failure."""


class PluginImportError(
    PluginError,
):
    """Plugin import failure."""


class InvalidPluginModuleError(
    PluginError,
):
    """Invalid plugin module contract."""


class DuplicatePluginError(PluginError):
    """Raised when a duplicate plugin ID is registered."""


class PluginValidationError(PluginError):
    """Raised when plugin validation fails."""


class PluginRegistryFrozenError(PluginError):
    """Raised when attempting mutation after freeze."""


class UnknownPluginError(PluginError):
    """Raised when plugin cannot be resolved."""


class DuplicateCapabilityProviderError(
    PluginError,
):
    """Capability provider already registered."""


class UnknownCapabilityProviderError(
    PluginError,
):
    """Capability provider not registered."""
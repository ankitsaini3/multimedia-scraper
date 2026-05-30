from __future__ import annotations


class PluginRegistryError(Exception):
    """Base plugin registry exception."""


class DuplicatePluginError(PluginRegistryError):
    """Raised when a duplicate plugin ID is registered."""


class PluginValidationError(PluginRegistryError):
    """Raised when plugin validation fails."""


class PluginRegistryFrozenError(PluginRegistryError):
    """Raised when attempting mutation after freeze."""


class UnknownPluginError(PluginRegistryError):
    """Raised when plugin cannot be resolved."""


class DuplicateCapabilityProviderError(
    PluginRegistryError,
):
    """Capability provider already registered."""


class UnknownCapabilityProviderError(
    PluginRegistryError,
):
    """Capability provider not registered."""

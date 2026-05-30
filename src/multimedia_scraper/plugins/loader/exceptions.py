from __future__ import annotations


class PluginLoaderError(Exception):
    """Base plugin loader error."""


class PluginDiscoveryError(
    PluginLoaderError,
):
    """Plugin discovery failure."""


class PluginImportError(
    PluginLoaderError,
):
    """Plugin import failure."""


class InvalidPluginModuleError(
    PluginLoaderError,
):
    """Invalid plugin module contract."""


class PluginCompatibilityError(
    PluginLoaderError,
):
    """Plugin compatibility validation failure."""

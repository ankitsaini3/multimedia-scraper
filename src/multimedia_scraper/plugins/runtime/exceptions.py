from __future__ import annotations


class PluginRuntimeError(Exception):
    """Base plugin runtime exception."""


class PluginShutdownError(
    PluginRuntimeError,
):
    """Plugin shutdown reconciliation failure."""


class PluginTaskLeakError(
    PluginRuntimeError,
):
    """Plugin leaked runtime-owned tasks."""

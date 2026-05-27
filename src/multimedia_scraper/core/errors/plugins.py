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

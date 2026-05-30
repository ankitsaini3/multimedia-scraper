from __future__ import annotations

import re

from multimedia_scraper.core.errors.plugins import (
    PluginValidationError,
)
from multimedia_scraper.plugins.contracts.plugin import RuntimePlugin
from multimedia_scraper.plugins.dto.capability import PluginCapabilityDTO

PLUGIN_ID_PATTERN = re.compile(r"^[a-z0-9._-]+$")
CAPABILITY_PATTERN = re.compile(r"^[a-z0-9._-]+$")


def validate_plugin(plugin: RuntimePlugin) -> None:
    manifest = plugin.manifest
    metadata = manifest.metadata

    _validate_plugin_id(metadata.plugin_id)
    _validate_capabilities(manifest.capabilities)
    _validate_entrypoint(manifest.entrypoint)


def _validate_plugin_id(plugin_id: str) -> None:
    if not plugin_id:
        raise PluginValidationError(
            "Plugin ID cannot be empty.",
        )

    if not PLUGIN_ID_PATTERN.fullmatch(plugin_id):
        raise PluginValidationError(
            f"Invalid plugin ID: {plugin_id}",
        )


def _validate_capabilities(
    capabilities: tuple[PluginCapabilityDTO, ...],
) -> None:
    for capability in capabilities:
        if not CAPABILITY_PATTERN.fullmatch(
            capability.capability_name,
        ):
            raise PluginValidationError(
                (f"Invalid capability name: {capability.capability_name}"),
            )


def _validate_entrypoint(entrypoint: str) -> None:
    if not entrypoint:
        raise PluginValidationError(
            "Plugin entrypoint cannot be empty.",
        )

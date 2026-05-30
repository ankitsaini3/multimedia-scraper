from __future__ import annotations

from multimedia_scraper.plugins.dto.manifest import (
    PluginManifestDTO,
)
from multimedia_scraper.plugins.loader.exceptions import (
    PluginCompatibilityError,
)

SUPPORTED_PLUGIN_API_VERSION = 1


def validate_plugin_compatibility(
    manifest: PluginManifestDTO,
) -> None:
    if manifest.api_version != (SUPPORTED_PLUGIN_API_VERSION):
        raise PluginCompatibilityError(
            (f"Unsupported plugin API version: {manifest.api_version}"),
        )

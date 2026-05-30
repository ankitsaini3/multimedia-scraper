from __future__ import annotations

from dataclasses import dataclass

from multimedia_scraper.plugins.dto.capability import PluginCapabilityDTO
from multimedia_scraper.plugins.dto.plugin_metadata import (
    PluginMetadataDTO,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PluginManifestDTO:
    metadata: PluginMetadataDTO
    capabilities: tuple[PluginCapabilityDTO, ...]
    api_version: int
    entrypoint: str

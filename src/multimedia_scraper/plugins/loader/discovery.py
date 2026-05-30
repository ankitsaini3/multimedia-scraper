from __future__ import annotations

from pathlib import Path

from multimedia_scraper.plugins.dto.discovery import (
    PluginDiscoveryRecordDTO,
)
from multimedia_scraper.plugins.loader.filesystem import (
    discover_plugin_directories,
)


def discover_local_plugins(
    *,
    root: Path,
) -> tuple[PluginDiscoveryRecordDTO, ...]:
    discoveries: list[PluginDiscoveryRecordDTO] = []

    for directory in discover_plugin_directories(root):
        plugin_id = directory.name

        discoveries.append(
            PluginDiscoveryRecordDTO(
                plugin_id=plugin_id,
                module_name=f"{plugin_id}.plugin",
                filesystem_path=directory,
            ),
        )

    return tuple(discoveries)

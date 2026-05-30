from __future__ import annotations

from multimedia_scraper.plugins.dto.diagnostics import (
    PluginRegistrySnapshotDTO,
)


def create_registry_snapshot(
    *,
    plugin_ids: tuple[str, ...],
    frozen: bool,
) -> PluginRegistrySnapshotDTO:
    return PluginRegistrySnapshotDTO(
        plugin_count=len(plugin_ids),
        registered_plugins=plugin_ids,
        frozen=frozen,
    )

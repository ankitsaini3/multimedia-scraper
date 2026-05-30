from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PluginRegistrySnapshotDTO:
    plugin_count: int
    registered_plugins: tuple[str, ...]
    frozen: bool

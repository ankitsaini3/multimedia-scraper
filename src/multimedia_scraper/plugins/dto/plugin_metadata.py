from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PluginMetadataDTO:
    plugin_id: str
    display_name: str
    version: str
    description: str
    author: str | None = None
    homepage: str | None = None
    license: str | None = None

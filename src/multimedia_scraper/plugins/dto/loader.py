from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PluginLoadResultDTO:
    plugin_id: str
    loaded: bool
    failure_reason: str | None = None

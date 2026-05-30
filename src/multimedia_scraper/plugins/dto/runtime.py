from __future__ import annotations

from dataclasses import dataclass

from multimedia_scraper.plugins.contracts.states import (
    PluginLifecycleState,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PluginRuntimeStateDTO:
    plugin_id: str
    state: PluginLifecycleState
    initialized: bool
    active: bool

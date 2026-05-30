from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True, kw_only=True)
class PluginDiscoveryRecordDTO:
    plugin_id: str
    module_name: str
    filesystem_path: Path

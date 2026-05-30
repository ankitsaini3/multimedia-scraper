from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PluginCapabilityDTO:
    capability_name: str

    provider_type: type[object]

    version: int

    optional: bool = False

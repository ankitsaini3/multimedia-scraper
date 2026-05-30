from __future__ import annotations

from dataclasses import dataclass

from multimedia_scraper.plugins.types import (
    CapabilityName,
    PluginId,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class CapabilityProviderRegistrationDTO:
    capability_name: CapabilityName

    plugin_id: PluginId

    provider_type: type[object]

    version: int

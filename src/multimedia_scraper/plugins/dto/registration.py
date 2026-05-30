from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from multimedia_scraper.plugins.dto.manifest import PluginManifestDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class PluginRegistrationDTO:
    manifest: PluginManifestDTO
    registered_at_utc: datetime
    source: str

    @staticmethod
    def create(
        *,
        manifest: PluginManifestDTO,
        source: str,
    ) -> PluginRegistrationDTO:
        return PluginRegistrationDTO(
            manifest=manifest,
            registered_at_utc=datetime.now(tz=UTC),
            source=source,
        )

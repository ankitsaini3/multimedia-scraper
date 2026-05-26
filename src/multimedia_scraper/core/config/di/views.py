from __future__ import annotations

from dataclasses import dataclass

from multimedia_scraper.core.config.dto.cache import (
    CacheConfigDTO,
)


@dataclass(frozen=True, slots=True)
class CacheConfigView:
    config: CacheConfigDTO
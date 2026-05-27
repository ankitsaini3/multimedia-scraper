from __future__ import annotations

from typing import Protocol

from multimedia_scraper.core.config.dto.cache import (
    CacheConfigDTO,
)


class CacheConfigProvider(
    Protocol,
):
    @property
    def cache(self) -> CacheConfigDTO: ...

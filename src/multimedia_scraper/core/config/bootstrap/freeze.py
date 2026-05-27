from __future__ import annotations

from dataclasses import dataclass

from multimedia_scraper.core.config.dto.runtime import (
    RuntimeConfigDTO,
)


@dataclass(frozen=True, slots=True)
class FrozenRuntimeConfig:
    """
    Authoritative immutable runtime config.

    After activation:
    - mutation forbidden
    - replacement forbidden
    - env access forbidden
    """

    config: RuntimeConfigDTO

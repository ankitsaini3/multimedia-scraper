from dataclasses import dataclass

from .base import ConfigDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class CacheConfigDTO(ConfigDTO):
    enabled: bool
    root_directory: str
    max_size_mb: int

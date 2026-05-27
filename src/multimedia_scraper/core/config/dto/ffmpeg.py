from dataclasses import dataclass

from .base import ConfigDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class FFmpegConfigDTO(ConfigDTO):
    executable_path: str
    hwaccel_enabled: bool
    max_parallel_jobs: int

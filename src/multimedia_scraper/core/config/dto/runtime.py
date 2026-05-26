from dataclasses import dataclass

from .base import ConfigDTO
from .cache import CacheConfigDTO
from .ffmpeg import FFmpegConfigDTO
from .logging import LoggingConfigDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class RuntimeConfigDTO(ConfigDTO):
    logging: LoggingConfigDTO
    cache: CacheConfigDTO
    ffmpeg: FFmpegConfigDTO
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from multimedia_scraper.core.config.dto.cache import (
    CacheConfigDTO,
)
from multimedia_scraper.core.config.dto.ffmpeg import (
    FFmpegConfigDTO,
)
from multimedia_scraper.core.config.dto.logging import (
    LoggingConfigDTO,
)
from multimedia_scraper.core.config.dto.runtime import (
    RuntimeConfigDTO,
)


class RuntimeConfigDTOFactory:
    @staticmethod
    def create(
        payload: Mapping[str, Any],
    ) -> RuntimeConfigDTO:

        return RuntimeConfigDTO(
            logging=LoggingConfigDTO(
                level=payload["logging.level"],
                json_logs=payload["logging.json_logs"],
                correlation_ids=True,
            ),
            cache=CacheConfigDTO(
                enabled=payload["cache.enabled"],
                root_directory=payload["cache.root_directory"],
                max_size_mb=payload["cache.max_size_mb"],
            ),
            ffmpeg=FFmpegConfigDTO(
                executable_path=payload["ffmpeg.executable_path"],
                hwaccel_enabled=payload["ffmpeg.hwaccel_enabled"],
                max_parallel_jobs=payload["ffmpeg.max_parallel_jobs"],
            ),
        )

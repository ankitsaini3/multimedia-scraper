from multimedia_scraper.core.config.dto.runtime import (
    RuntimeConfigDTO,
)
from multimedia_scraper.core.config.validators.runtime import (
    RuntimeConfigDTOFactory,
)


def test_validation_pipeline_returns_runtime_dto() -> None:

    payload = {
        "logging.level": "INFO",
        "logging.json_logs": True,
        "cache.enabled": True,
        "cache.root_directory": "/tmp/cache",
        "cache.max_size_mb": 1024,
        "ffmpeg.executable_path": "/usr/bin/ffmpeg",
        "ffmpeg.hwaccel_enabled": False,
        "ffmpeg.max_parallel_jobs": 2,
    }

    dto = RuntimeConfigDTOFactory.create(
        payload,
    )

    assert isinstance(
        dto,
        RuntimeConfigDTO,
    )

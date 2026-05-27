from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from multimedia_scraper.core.config.bootstrap.coordinator import (
    ConfigurationBootstrapCoordinator,
)
from multimedia_scraper.core.config.bootstrap.state import (
    ConfigBootstrapState,
)
from multimedia_scraper.core.config.dto.runtime import (
    RuntimeConfigDTO,
)
from multimedia_scraper.core.config.sources.models import (
    ConfigSource,
)
from multimedia_scraper.core.config.sources.resolver import (
    ConfigResolver,
)
from multimedia_scraper.core.config.sources.types import (
    ConfigSourceType,
)
from multimedia_scraper.core.config.validators.pipeline import (
    ValidationPipeline,
)


class FakeSourceProvider:
    def load(self) -> ConfigSource:
        return ConfigSource(
            source_type=ConfigSourceType.DEFAULT,
            source_name="defaults",
            precedence=0,
            payload={
                "logging.level": "INFO",
                "logging.json_logs": True,
                "cache.enabled": True,
                "cache.root_directory": "/tmp/cache",
                "cache.max_size_mb": 1024,
                "ffmpeg.executable_path": "/usr/bin/ffmpeg",
                "ffmpeg.hwaccel_enabled": False,
                "ffmpeg.max_parallel_jobs": 2,
            },
        )


def test_full_bootstrap_flow() -> None:

    coordinator = ConfigurationBootstrapCoordinator(
        resolver=ConfigResolver(),
        validator=ValidationPipeline(),
        providers=[
            FakeSourceProvider(),
        ],
    )

    frozen = coordinator.bootstrap()

    assert coordinator.state == (ConfigBootstrapState.ACTIVE)

    assert isinstance(
        frozen.config,
        RuntimeConfigDTO,
    )

    assert frozen.config.logging.level == "INFO"

    assert frozen.config.cache.max_size_mb == 1024

    with pytest.raises(
        FrozenInstanceError,
    ):
        frozen.config.cache.max_size_mb = 2048

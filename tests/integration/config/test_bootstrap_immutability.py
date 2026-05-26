from __future__ import annotations

import pytest
from dataclasses import FrozenInstanceError

from multimedia_scraper.core.config.bootstrap.coordinator import (
    ConfigurationBootstrapCoordinator,
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
from multimedia_scraper.core.runtime.di import (
    ServiceCollection,
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


def test_runtime_config_is_frozen_after_bootstrap(
) -> None:

    coordinator = (
        ConfigurationBootstrapCoordinator(
            resolver=ConfigResolver(),
            validator=ValidationPipeline(),
            providers=[
                FakeSourceProvider(),
            ],
        )
    )

    frozen = coordinator.bootstrap()

    with pytest.raises(
        FrozenInstanceError,
    ):
        frozen.config.logging.level = "DEBUG"


def test_service_collection_freeze_prevents_mutation(
) -> None:

    services = ServiceCollection()

    services.freeze()

    with pytest.raises(RuntimeError):
        services.register_instance(
            interface=str,
            implementation="test",
            scope="application",
        )
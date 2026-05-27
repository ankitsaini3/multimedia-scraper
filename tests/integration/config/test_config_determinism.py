from __future__ import annotations

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


def build_config():

    coordinator = ConfigurationBootstrapCoordinator(
        resolver=ConfigResolver(),
        validator=ValidationPipeline(),
        providers=[
            FakeSourceProvider(),
        ],
    )

    return coordinator.bootstrap()


def test_bootstrap_is_deterministic() -> None:

    config_1 = build_config()

    config_2 = build_config()

    assert config_1 == config_2

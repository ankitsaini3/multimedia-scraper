from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

from .base import ConfigSourceProvider
from .models import ConfigSource
from .types import ConfigSourceType

ENV_MAPPINGS: dict[
    str,
    tuple[str, Callable[[str], Any]],
] = {
    "MULTIMEDIA_SCRAPER_LOG_LEVEL": ("logging.level", str),
    "MULTIMEDIA_SCRAPER_CACHE_DIR": ("cache.root_directory", str),
}


class EnvironmentConfigSourceProvider(
    ConfigSourceProvider,
):
    def load(self) -> ConfigSource:
        payload: dict[str, Any] = {}

        for env_key in sorted(ENV_MAPPINGS):
            mapping_key, parser = ENV_MAPPINGS[env_key]

            raw = os.getenv(env_key)

            if raw is None:
                continue

            payload[mapping_key] = parser(raw)

        return ConfigSource(
            source_type=ConfigSourceType.ENVIRONMENT,
            source_name="environment",
            precedence=2,
            payload=payload,
        )

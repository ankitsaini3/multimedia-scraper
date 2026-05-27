from dataclasses import FrozenInstanceError

import pytest

from multimedia_scraper.core.config.dto.cache import (
    CacheConfigDTO,
)


def test_cache_config_is_immutable() -> None:

    config = CacheConfigDTO(
        enabled=True,
        root_directory="/tmp/cache",
        max_size_mb=1024,
    )

    with pytest.raises(FrozenInstanceError):
        config.max_size_mb = 2048

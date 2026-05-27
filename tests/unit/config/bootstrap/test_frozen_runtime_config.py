from dataclasses import FrozenInstanceError

import pytest

from multimedia_scraper.core.config.bootstrap.freeze import (
    FrozenRuntimeConfig,
)
from multimedia_scraper.core.config.dto.runtime import (
    RuntimeConfigDTO,
)


def test_frozen_runtime_config_is_immutable() -> None:

    frozen = FrozenRuntimeConfig(
        config=RuntimeConfigDTO(
            logging=None,
            cache=None,
            ffmpeg=None,
        ),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        frozen.config = None

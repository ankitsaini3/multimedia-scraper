import pytest

from multimedia_scraper.core.config.validators.pipeline import (
    ValidationPipeline,
)
from multimedia_scraper.core.errors.configuration import (
    ConfigurationValidationError,
)


def test_cache_requires_directory() -> None:

    pipeline = ValidationPipeline()

    payload = {
        "cache.enabled": True,
        "cache.root_directory": "",
    }

    with pytest.raises(
        ConfigurationValidationError,
    ):
        pipeline.validate(payload)

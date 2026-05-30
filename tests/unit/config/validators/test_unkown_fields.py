import pytest

from multimedia_scraper.core.config.validators.pipeline import (
    ValidationPipeline,
)
from multimedia_scraper.core.errors.configuration import (
    ConfigurationValidationError,
)


def test_unknown_fields_fail_validation() -> None:

    pipeline = ValidationPipeline()

    payload = {
        "logging.level": "INFO",
        "invalid.field": True,
    }

    with pytest.raises(
        ConfigurationValidationError,
    ):
        pipeline.validate(payload)

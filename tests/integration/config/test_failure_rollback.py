import pytest

from multimedia_scraper.core.config.bootstrap.coordinator import (
    ConfigurationBootstrapCoordinator,
)
from multimedia_scraper.core.config.bootstrap.state import (
    ConfigBootstrapState,
)
from multimedia_scraper.core.config.exceptions import (
    ConfigurationValidationError,
)


class FakeResolver:
    def resolve(self, sources):
        return {}


class FailingValidator:
    def validate(self, payload):
        raise ConfigurationValidationError(
            "validation failed",
        )


def test_failed_bootstrap_rolls_back() -> None:

    coordinator = ConfigurationBootstrapCoordinator(
        resolver=FakeResolver(),
        validator=FailingValidator(),
        providers=[],
    )

    with pytest.raises(
        ConfigurationValidationError,
    ):
        coordinator.bootstrap()

    assert coordinator.state == (ConfigBootstrapState.TERMINATED)

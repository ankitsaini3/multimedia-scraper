import pytest

from multimedia_scraper.core.config.bootstrap.coordinator import (
    ConfigurationBootstrapCoordinator,
)


def test_bootstrap_requires_explicit_dependencies() -> None:

    with pytest.raises(TypeError):
        ConfigurationBootstrapCoordinator(
            resolver=None,
            validator=None,
            providers=[],
        )

import pytest

from multimedia_scraper.core.runtime.di import (
    ServiceCollection,
)


def test_service_collection_disallows_mutation_after_freeze() -> None:

    services = ServiceCollection()

    services.freeze()

    with pytest.raises(RuntimeError):
        services.register_instance(
            interface=str,
            implementation="test",
            scope="application",
        )

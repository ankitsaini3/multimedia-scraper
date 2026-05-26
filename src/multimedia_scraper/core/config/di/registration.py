from __future__ import annotations

from multimedia_scraper.core.config.bootstrap.freeze import (
    FrozenRuntimeConfig,
)

from multimedia_scraper.core.runtime.di import (
    ServiceCollection,
)


def register_configuration(
    services: ServiceCollection,
    config: FrozenRuntimeConfig,
) -> None:
    """
    Register authoritative immutable runtime config.
    """

    services.register_instance(
        FrozenRuntimeConfig,
        config,
        scope="application",
    )
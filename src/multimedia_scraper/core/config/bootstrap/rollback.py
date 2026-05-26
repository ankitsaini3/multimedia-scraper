from __future__ import annotations

from typing import Protocol

from multimedia_scraper.core.config.bootstrap.state import (
    ConfigBootstrapState,
)


class BootstrapStateController(
    Protocol,
):
    _state: ConfigBootstrapState


class ConfigBootstrapRollbackManager:

    def rollback(
        self,
        coordinator: BootstrapStateController,
    ) -> None:

        coordinator._state = (
            ConfigBootstrapState.ROLLING_BACK
        )

        coordinator._state = (
            ConfigBootstrapState.TERMINATED
        )
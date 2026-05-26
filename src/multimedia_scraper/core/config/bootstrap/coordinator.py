from __future__ import annotations

from collections.abc import Sequence

from multimedia_scraper.core.config.bootstrap.freeze import (
    FrozenRuntimeConfig,
)
from multimedia_scraper.core.config.bootstrap.state import (
    ConfigBootstrapState,
)
from multimedia_scraper.core.config.dto.runtime import (
    RuntimeConfigDTO,
)
from multimedia_scraper.core.config.sources.base import (
    ConfigSourceProvider,
)
from multimedia_scraper.core.config.sources.resolver import (
    ConfigResolver,
)
from multimedia_scraper.core.config.validators.pipeline import (
    ValidationPipeline,
)

from multimedia_scraper.core.config.bootstrap.rollback import (
    ConfigBootstrapRollbackManager,
)


class ConfigurationBootstrapCoordinator:

    def __init__(
        self,
        *,
        resolver: ConfigResolver,
        validator: ValidationPipeline,
        providers: Sequence[ConfigSourceProvider],
    ) -> None:
        
        if resolver is None:
            raise TypeError(
                "resolver cannot be None"
            )
        
        if validator is None:
            raise TypeError(
                "validator cannot be None"
            )
        
        self._resolver = resolver
        self._validator = validator
        self._providers = tuple(providers)

        self._state = (
            ConfigBootstrapState.PRE_BOOTSTRAP
        )

    @property
    def state(
        self,
    ) -> ConfigBootstrapState:
        return self._state

    def bootstrap(
        self,
    ) -> FrozenRuntimeConfig:
        
        try:
            self._transition(
                ConfigBootstrapState.RESOLVING,
            )

            sources = tuple(
                provider.load()
                for provider in self._providers
            )

            merged = self._resolver.resolve(
                sources,
            )

            self._transition(
                ConfigBootstrapState.VALIDATING,
            )

            validated = self._validator.validate(
                merged,
            )

            self._transition(
                ConfigBootstrapState.FREEZING,
            )

            frozen = FrozenRuntimeConfig(
                config=validated,
            )

            self._transition(
                ConfigBootstrapState.ACTIVATING,
            )

            self._transition(
                ConfigBootstrapState.ACTIVE,
            )

            return frozen
        except Exception as e:
            self._state = (
                ConfigBootstrapState.FAILED
            )

            rollback = (
                    ConfigBootstrapRollbackManager()
                )

            rollback.rollback(self)

            raise


    def _transition(
        self,
        state: ConfigBootstrapState,
    ) -> None:
        self._state = state
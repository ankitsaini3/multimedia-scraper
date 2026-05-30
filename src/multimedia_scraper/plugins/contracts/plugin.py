from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from multimedia_scraper.plugins.dto.manifest import (
    PluginManifestDTO,
)

if TYPE_CHECKING:
    from multimedia_scraper.plugins.runtime.context import (
        PluginRuntimeContext,
    )


class RuntimePlugin(Protocol):
    @property
    def manifest(self) -> PluginManifestDTO: ...

    async def initialize(
        self,
        context: PluginRuntimeContext,
    ) -> None: ...

    async def activate(self) -> None: ...

    async def shutdown(self) -> None: ...

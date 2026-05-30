from __future__ import annotations

import asyncio

from multimedia_scraper.plugins.contracts.plugin import (
    RuntimePlugin,
)
from multimedia_scraper.plugins.dto.capability import (
    PluginCapabilityDTO,
)
from multimedia_scraper.plugins.dto.manifest import (
    PluginManifestDTO,
)
from multimedia_scraper.plugins.dto.plugin_metadata import (
    PluginMetadataDTO,
)
from multimedia_scraper.plugins.runtime.context import (
    PluginRuntimeContext,
)


class SearchProvider:
    async def search(
        self,
        query: str,
    ) -> list[str]:
        return [query]


class ValidTestPlugin(RuntimePlugin):
    def __init__(self) -> None:
        self.initialized = False
        self.activated = False
        self.shutdown_called = False

    @property
    def manifest(self) -> PluginManifestDTO:
        return PluginManifestDTO(
            metadata=PluginMetadataDTO(
                plugin_id="valid-plugin",
                display_name="Valid Plugin",
                version="1.0.0",
                description="Test plugin",
            ),
            capabilities=(
                PluginCapabilityDTO(
                    capability_name="search",
                    provider_type=SearchProvider,
                    version=1,
                ),
            ),
            api_version=1,
            entrypoint="valid.plugin",
        )

    async def initialize(
        self,
        context: PluginRuntimeContext,
    ) -> None:
        self.initialized = True

    async def activate(self) -> None:
        self.activated = True

    async def shutdown(self) -> None:
        self.shutdown_called = True


class FailingInitializePlugin(
    ValidTestPlugin,
):
    @property
    def manifest(self) -> PluginManifestDTO:
        manifest = super().manifest

        return PluginManifestDTO(
            metadata=PluginMetadataDTO(
                plugin_id="failing-init",
                display_name="Failing Init",
                version="1.0.0",
                description="Fail init",
            ),
            capabilities=manifest.capabilities,
            api_version=1,
            entrypoint="failing.init",
        )

    async def initialize(
        self,
        context: PluginRuntimeContext,
    ) -> None:
        raise RuntimeError(
            "Initialization failure",
        )


class FailingActivatePlugin(
    ValidTestPlugin,
):
    @property
    def manifest(self) -> PluginManifestDTO:
        manifest = super().manifest

        return PluginManifestDTO(
            metadata=PluginMetadataDTO(
                plugin_id="failing-activate",
                display_name="Fail Activate",
                version="1.0.0",
                description="Fail activate",
            ),
            capabilities=manifest.capabilities,
            api_version=1,
            entrypoint="failing.activate",
        )

    async def activate(self) -> None:
        raise RuntimeError(
            "Activation failure",
        )


class LeakingPlugin(
    ValidTestPlugin,
):
    @property
    def manifest(self) -> PluginManifestDTO:
        manifest = super().manifest

        return PluginManifestDTO(
            metadata=PluginMetadataDTO(
                plugin_id="leaking-plugin",
                display_name="Leaking Plugin",
                version="1.0.0",
                description="Leaks tasks",
            ),
            capabilities=manifest.capabilities,
            api_version=1,
            entrypoint="leaking.plugin",
        )

    async def activate(self) -> None:
        task = asyncio.create_task(
            asyncio.sleep(60),
        )

        _ = task

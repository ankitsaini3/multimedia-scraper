from __future__ import annotations

from pathlib import Path

from multimedia_scraper.plugins.dto.loader import (
    PluginLoadResultDTO,
)
from multimedia_scraper.plugins.loader.compatibility import (
    validate_plugin_compatibility,
)
from multimedia_scraper.plugins.loader.discovery import (
    discover_local_plugins,
)
from multimedia_scraper.plugins.loader.importer import (
    import_plugin_module,
)
from multimedia_scraper.plugins.loader.parser import (
    parse_plugin_module,
)
from multimedia_scraper.plugins.registry.registry import (
    RuntimePluginRegistry,
)
from multimedia_scraper.runtime.context import (
    RuntimeContext,
)


class LocalPluginLoader:
    """
    Deterministic local plugin loader.

    Responsibilities:
    - local filesystem discovery
    - deterministic import ordering
    - compatibility validation
    - manifest parsing
    - runtime-owned plugin registration

    Explicitly excluded:
    - remote plugins
    - package systems
    - marketplaces
    - hot reload
    """

    def __init__(
        self,
        *,
        plugin_registry: RuntimePluginRegistry,
        runtime_context: RuntimeContext,
    ) -> None:
        self._plugin_registry = plugin_registry

        self._runtime_context = runtime_context

    def load_from_path(
        self,
        root: Path,
    ) -> tuple[PluginLoadResultDTO, ...]:
        results: list[PluginLoadResultDTO] = []

        discoveries = discover_local_plugins(
            root=root,
        )

        for discovery in discoveries:
            try:
                module = import_plugin_module(
                    discovery.module_name,
                )

                manifest, plugin_class = parse_plugin_module(
                    module,
                )

                validate_plugin_compatibility(
                    manifest,
                )

                plugin = plugin_class()

                self._plugin_registry.register(
                    plugin,
                    runtime_context=(self._runtime_context),
                    source=str(discovery.filesystem_path),
                )

                results.append(
                    PluginLoadResultDTO(
                        plugin_id=(manifest.metadata.plugin_id),
                        loaded=True,
                    ),
                )

            except Exception as exc:
                results.append(
                    PluginLoadResultDTO(
                        plugin_id=(discovery.plugin_id),
                        loaded=False,
                        failure_reason=str(exc),
                    ),
                )

        return tuple(results)

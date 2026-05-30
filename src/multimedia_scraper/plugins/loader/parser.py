from __future__ import annotations

from multimedia_scraper.plugins.contracts.plugin import (
    RuntimePlugin,
)
from multimedia_scraper.plugins.dto.manifest import (
    PluginManifestDTO,
)
from multimedia_scraper.core.errors.plugins import (
    InvalidPluginModuleError,
)


def parse_plugin_module(
    module: object,
) -> tuple[
    PluginManifestDTO,
    type[RuntimePlugin],
]:
    manifest = getattr(
        module,
        "PLUGIN_MANIFEST",
        None,
    )

    plugin_class = getattr(
        module,
        "PLUGIN_CLASS",
        None,
    )

    if manifest is None:
        raise InvalidPluginModuleError(
            "Plugin module missing PLUGIN_MANIFEST.",
        )

    if plugin_class is None:
        raise InvalidPluginModuleError(
            "Plugin module missing PLUGIN_CLASS.",
        )

    return manifest, plugin_class

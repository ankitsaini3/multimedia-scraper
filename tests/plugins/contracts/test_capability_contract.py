from __future__ import annotations

from multimedia_scraper.plugins.registry.registry import (
    RuntimePluginRegistry,
)
from tests.plugins.fixtures.plugins import (
    SearchProvider,
    ValidTestPlugin,
)
from tests.plugins.fixtures.runtime import (
    create_test_runtime_context,
)


def test_typed_provider_lookup():
    registry = RuntimePluginRegistry()

    plugin = ValidTestPlugin()

    registry.register(
        plugin,
        runtime_context=(create_test_runtime_context()),
        source="test",
    )

    provider = registry._capability_registry.resolve_provider(
        SearchProvider,
    )

    assert provider is plugin

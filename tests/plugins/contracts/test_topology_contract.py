from __future__ import annotations

from multimedia_scraper.plugins.registry.registry import (
    RuntimePluginRegistry,
)
from tests.plugins.fixtures.plugins import (
    ValidTestPlugin,
)
from tests.plugins.fixtures.runtime import (
    create_test_runtime_context,
)


def test_registry_topology_snapshot():
    registry = RuntimePluginRegistry()

    registry.register(
        ValidTestPlugin(),
        runtime_context=(create_test_runtime_context()),
        source="test",
    )

    snapshot = registry.snapshot()

    assert snapshot.plugin_count == 1

    assert snapshot.frozen is False

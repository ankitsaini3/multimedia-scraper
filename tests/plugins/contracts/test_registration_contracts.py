from __future__ import annotations

import pytest

from multimedia_scraper.plugins.registry.exceptions import (
    DuplicatePluginError,
    PluginRegistryFrozenError,
)
from multimedia_scraper.plugins.registry.registry import (
    RuntimePluginRegistry,
)
from tests.plugins.fixtures.plugins import (
    ValidTestPlugin,
)
from tests.plugins.fixtures.runtime import (
    create_test_runtime_context,
)


def test_duplicate_plugin_registration_fails():
    registry = RuntimePluginRegistry()

    context = create_test_runtime_context()

    plugin = ValidTestPlugin()

    registry.register(
        plugin,
        runtime_context=context,
        source="test",
    )

    with pytest.raises(
        DuplicatePluginError,
    ):
        registry.register(
            plugin,
            runtime_context=context,
            source="test",
        )


def test_frozen_registry_rejects_registration():
    registry = RuntimePluginRegistry()

    context = create_test_runtime_context()

    registry.freeze()

    with pytest.raises(
        PluginRegistryFrozenError,
    ):
        registry.register(
            ValidTestPlugin(),
            runtime_context=context,
            source="test",
        )

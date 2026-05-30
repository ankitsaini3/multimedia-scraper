from __future__ import annotations

import pytest

from multimedia_scraper.plugins.registry.registry import (
    RuntimePluginRegistry,
)
from tests.plugins.fixtures.plugins import (
    FailingActivatePlugin,
    FailingInitializePlugin,
    ValidTestPlugin,
)
from tests.plugins.fixtures.runtime import (
    create_test_runtime_context,
)


@pytest.mark.asyncio
async def test_plugin_initialize():
    registry = RuntimePluginRegistry()

    plugin = ValidTestPlugin()

    registry.register(
        plugin,
        runtime_context=(create_test_runtime_context()),
        source="test",
    )

    await registry.initialize_all()

    assert plugin.initialized is True


@pytest.mark.asyncio
async def test_plugin_activate():
    registry = RuntimePluginRegistry()

    plugin = ValidTestPlugin()

    registry.register(
        plugin,
        runtime_context=(create_test_runtime_context()),
        source="test",
    )

    await registry.initialize_all()

    await registry.activate_all()

    assert plugin.activated is True


@pytest.mark.asyncio
async def test_initialize_failure_propagates():
    registry = RuntimePluginRegistry()

    registry.register(
        FailingInitializePlugin(),
        runtime_context=(create_test_runtime_context()),
        source="test",
    )

    with pytest.raises(RuntimeError):
        await registry.initialize_all()


@pytest.mark.asyncio
async def test_activation_failure_propagates():
    registry = RuntimePluginRegistry()

    registry.register(
        FailingActivatePlugin(),
        runtime_context=(create_test_runtime_context()),
        source="test",
    )

    await registry.initialize_all()

    with pytest.raises(RuntimeError):
        await registry.activate_all()

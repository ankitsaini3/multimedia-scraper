from __future__ import annotations

import pytest

from multimedia_scraper.plugins.registry.registry import (
    RuntimePluginRegistry,
)
from tests.plugins.fixtures.plugins import (
    ValidTestPlugin,
)
from tests.plugins.fixtures.runtime import (
    create_test_runtime_context,
)


@pytest.mark.asyncio
async def test_plugin_shutdown():
    registry = RuntimePluginRegistry()

    plugin = ValidTestPlugin()

    registry.register(
        plugin,
        runtime_context=(create_test_runtime_context()),
        source="test",
    )

    await registry.initialize_all()

    await registry.activate_all()

    await registry.shutdown_all()

    assert plugin.shutdown_called is True

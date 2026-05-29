from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from multimedia_scraper.runtime.bootstrap import (
    RuntimeBootstrapCoordinator,
)
from multimedia_scraper.runtime.cancellation import (
    create_root_cancellation_scope,
)
from multimedia_scraper.runtime.context import (
    RuntimeContext,
)
from multimedia_scraper.runtime.event_bus import (
    RuntimeEventBus,
)
from multimedia_scraper.runtime.metadata import (
    RuntimeId,
    RuntimeMetadata,
)
from multimedia_scraper.runtime.registry import (
    RuntimeRegistry,
)
from multimedia_scraper.runtime.supervisor import (
    TaskSupervisor,
)


@pytest.fixture
def fake_runtime_context() -> RuntimeContext:
    scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="root",
        cancellation_scope=scope,
    )

    event_bus = RuntimeEventBus(
        supervisor=supervisor,
        cancellation_scope=scope,
    )

    return RuntimeContext(
        runtime_id=RuntimeId(value=uuid4()),
        config=Mock(),
        observability=Mock(),
        diagnostics=Mock(),
        metadata=RuntimeMetadata(
            runtime_version="0.1.0",
            created_at=datetime.now(UTC),
            bootstrap_completed_at=datetime.now(UTC),
        ),
        cancellation_scope=scope,
        supervisor=supervisor,
        event_bus=event_bus,
        registry=RuntimeRegistry(),
    )


@pytest.fixture
def runtime_bootstrap_coordinator():
    observability = Mock()

    observability.initialize = AsyncMock()
    observability.shutdown = AsyncMock()

    configuration = Mock()

    configuration.bootstrap.return_value = Mock()

    diagnostics = Mock()

    return RuntimeBootstrapCoordinator(
        configuration=configuration,
        observability=observability,
        diagnostics=diagnostics,
    )
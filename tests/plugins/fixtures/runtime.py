from __future__ import annotations

from unittest.mock import MagicMock

from multimedia_scraper.core.config.bootstrap.freeze import (
    FrozenRuntimeConfig,
)
from multimedia_scraper.core.observability.bootstrap.bootstrap_observability import (
    BootstrapObservabilityController,
)
from multimedia_scraper.core.observability.bootstrap.startup_diagnostics import (
    StartupDiagnosticsRegistry,
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


def create_test_runtime_context() -> RuntimeContext:
    cancellation_scope = create_root_cancellation_scope()

    supervisor = TaskSupervisor(
        name="test-root",
        cancellation_scope=(cancellation_scope),
    )

    return RuntimeContext(
        runtime_id=MagicMock(spec=RuntimeId),
        config=MagicMock(
            spec=FrozenRuntimeConfig,
        ),
        observability=MagicMock(
            spec=BootstrapObservabilityController,
        ),
        diagnostics=MagicMock(
            spec=StartupDiagnosticsRegistry,
        ),
        metadata=MagicMock(
            spec=RuntimeMetadata,
        ),
        cancellation_scope=(cancellation_scope),
        supervisor=supervisor,
        event_bus=RuntimeEventBus(
            supervisor=supervisor,
            cancellation_scope=(cancellation_scope),
        ),
        registry=RuntimeRegistry(),
    )

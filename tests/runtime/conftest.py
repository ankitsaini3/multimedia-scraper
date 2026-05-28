from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from multimedia_scraper.core.config.bootstrap.freeze import FrozenRuntimeConfig
from multimedia_scraper.core.observability.bootstrap.bootstrap_observability import (
    BootstrapObservabilityController,
)
from multimedia_scraper.core.observability.bootstrap.startup_diagnostics import (
    StartupDiagnosticsRegistry,
)
from multimedia_scraper.runtime.cancellation import (
    create_root_cancellation_scope,
)
from multimedia_scraper.runtime.context import RuntimeContext
from multimedia_scraper.runtime.event_bus import RuntimeEventBus
from multimedia_scraper.runtime.metadata import RuntimeId, RuntimeMetadata
from multimedia_scraper.runtime.registry import RuntimeRegistry
from multimedia_scraper.runtime.supervisor import TaskSupervisor


class FakeFrozenRuntimeConfig(FrozenRuntimeConfig):
    pass


class FakeObservabilityController(
    BootstrapObservabilityController,
):
    def __init__(self) -> None:
        self.initialized = False
        self.shutdown_called = False

    async def initialize(self) -> None:
        self.initialized = True

    async def shutdown(self) -> None:
        self.shutdown_called = True


@pytest.fixture
def diagnostics() -> StartupDiagnosticsRegistry:
    return StartupDiagnosticsRegistry()


@pytest.fixture
def observability(
    diagnostics: StartupDiagnosticsRegistry,
) -> FakeObservabilityController:
    return FakeObservabilityController()


@pytest.fixture
def cancellation_scope():
    return create_root_cancellation_scope()


@pytest.fixture
def supervisor(cancellation_scope):
    return TaskSupervisor(
        name="runtime-root",
        cancellation_scope=cancellation_scope,
    )


@pytest.fixture
def event_bus(
    supervisor: TaskSupervisor,
    cancellation_scope,
) -> RuntimeEventBus:
    return RuntimeEventBus(
        supervisor=supervisor,
        cancellation_scope=cancellation_scope,
    )


@pytest.fixture
def registry() -> RuntimeRegistry:
    return RuntimeRegistry()


@pytest.fixture
def runtime_context(
    observability,
    diagnostics,
    cancellation_scope,
    supervisor,
    event_bus,
    registry,
):
    return RuntimeContext(
        runtime_id=RuntimeId(value=uuid4()),
        config=FakeFrozenRuntimeConfig(
            config=None,
        ),
        observability=observability,
        diagnostics=diagnostics,
        metadata=RuntimeMetadata(
            runtime_version="0.1.0",
            created_at=datetime.now(UTC),
            bootstrap_completed_at=datetime.now(UTC),
        ),
        cancellation_scope=cancellation_scope,
        supervisor=supervisor,
        event_bus=event_bus,
        registry=registry,
    )

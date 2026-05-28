from __future__ import annotations

from typing import Protocol

from multimedia_scraper.core.config.bootstrap.freeze import FrozenRuntimeConfig
from multimedia_scraper.core.observability.bootstrap.bootstrap_observability import (
    BootstrapObservabilityController,
)
from multimedia_scraper.core.observability.bootstrap.startup_diagnostics import (
    StartupDiagnosticsRegistry,
)
from multimedia_scraper.runtime.cancellation import CancellationScope, CancellationToken
from multimedia_scraper.runtime.event_bus import (
    RuntimeEventBus,
)
from multimedia_scraper.runtime.lifecycle import (
    RuntimeLifecycleState,
)
from multimedia_scraper.runtime.registry import (
    RuntimeRegistry,
)
from multimedia_scraper.runtime.supervisor import (
    TaskSupervisor,
)


class LifecycleStateProvider(Protocol):
    state: RuntimeLifecycleState


class RegistryProvider(Protocol):
    registry: RuntimeRegistry


class EventBusProvider(Protocol):
    event_bus: RuntimeEventBus


class SupervisorProvider(Protocol):
    supervisor: TaskSupervisor


class RuntimeConfigProvider(Protocol):
    config: FrozenRuntimeConfig


class RuntimeObservabilityProvider(Protocol):
    observability: BootstrapObservabilityController


class RuntimeDiagnosticsProvider(Protocol):
    diagnostics: StartupDiagnosticsRegistry


class CancellationTokenProvider(Protocol):
    cancellation_token: CancellationToken


class CancellationScopeProvider(Protocol):
    cancellation_scope: CancellationScope

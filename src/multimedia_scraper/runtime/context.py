from __future__ import annotations

from dataclasses import dataclass

from multimedia_scraper.core.config.bootstrap.freeze import FrozenRuntimeConfig
from multimedia_scraper.core.observability.bootstrap.bootstrap_observability import (
    BootstrapObservabilityController,
)
from multimedia_scraper.core.observability.bootstrap.startup_diagnostics import (
    StartupDiagnosticsRegistry,
)
from multimedia_scraper.runtime.cancellation import (
    CancellationScope,
)
from multimedia_scraper.runtime.event_bus import (
    RuntimeEventBus,
)
from multimedia_scraper.runtime.metadata import RuntimeId, RuntimeMetadata
from multimedia_scraper.runtime.protocols import (
    CancellationScopeProvider,
    EventBusProvider,
    RegistryProvider,
    RuntimeConfigProvider,
    RuntimeDiagnosticsProvider,
    RuntimeObservabilityProvider,
    SupervisorProvider,
)
from multimedia_scraper.runtime.registry import (
    RuntimeRegistry,
)
from multimedia_scraper.runtime.supervisor import (
    TaskSupervisor,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class RuntimeContext(
    RuntimeConfigProvider,
    RuntimeObservabilityProvider,
    RuntimeDiagnosticsProvider,
    CancellationScopeProvider,
    SupervisorProvider,
    EventBusProvider,
    RegistryProvider,
):
    """
    Immutable runtime dependency root.
    """

    runtime_id: RuntimeId

    config: FrozenRuntimeConfig

    observability: BootstrapObservabilityController

    diagnostics: StartupDiagnosticsRegistry

    metadata: RuntimeMetadata

    cancellation_scope: CancellationScope

    supervisor: TaskSupervisor

    event_bus: RuntimeEventBus

    registry: RuntimeRegistry

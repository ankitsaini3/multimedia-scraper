from __future__ import annotations

from collections.abc import Coroutine
from dataclasses import dataclass
from typing import TypeVar

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
from multimedia_scraper.runtime.task import (
    RuntimeTask,
)

T = TypeVar("T")


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

    RuntimeContext is the operational ownership root for:
    - structured execution
    - supervision
    - runtime cancellation
    - lifecycle-bound task ownership
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

    def spawn(
        self,
        *,
        name: str,
        coroutine: Coroutine[object, object, T],
    ) -> RuntimeTask[T]:
        """
        Spawn a structured runtime-owned task.

        Delegates execution ownership to the root supervisor.

        Guarantees:
        - no detached execution
        - runtime-bound lifecycle ownership
        - structured cancellation propagation
        """

        return self.supervisor.spawn(
            name=name,
            coroutine=coroutine,
        )

    def create_child_scope(
        self,
        *,
        name: str,
    ) -> CancellationScope:
        """
        Create a child runtime cancellation scope.

        Child scope remains runtime-owned through
        hierarchical cancellation propagation.
        """

        return self.cancellation_scope.create_child(
            name=name,
        )

    def create_child_supervisor(
        self,
        *,
        name: str,
    ) -> TaskSupervisor:
        """
        Create a child structured concurrency supervisor.

        Child supervisors inherit:
        - runtime cancellation
        - structured ownership
        - deterministic shutdown semantics
        """

        child_scope = self.create_child_scope(
            name=f"{name}-scope",
        )

        return TaskSupervisor(
            name=name,
            cancellation_scope=child_scope,
            parent=self.supervisor,
        )

    @property
    def cancellation_token(self) -> CancellationToken:
        """
        Read-only cooperative cancellation surface.
        """

        return self.cancellation_scope.token

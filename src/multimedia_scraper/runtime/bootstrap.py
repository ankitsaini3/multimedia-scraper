from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from multimedia_scraper.core.config.bootstrap.coordinator import (
    ConfigurationBootstrapCoordinator,
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
from multimedia_scraper.runtime.context import RuntimeContext
from multimedia_scraper.runtime.event_bus import (
    RuntimeEventBus,
)
from multimedia_scraper.runtime.lifecycle import (
    RuntimeLifecycleState,
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


@dataclass(slots=True, kw_only=True)
class RuntimeBootstrapCoordinator:
    """
    Deterministic runtime bootstrap integration.

    Responsibilities:

    - startup ordering
    - shutdown ordering
    - cleanup coordination
    - runtime primitive ownership

    Explicitly excluded:

    - orchestration
    - restart policies
    - retry systems
    - workflow engines
    """

    configuration: ConfigurationBootstrapCoordinator

    observability: BootstrapObservabilityController

    diagnostics: StartupDiagnosticsRegistry

    _state: RuntimeLifecycleState = field(
        default=RuntimeLifecycleState.CREATED,
        init=False,
    )

    @property
    def state(self) -> RuntimeLifecycleState:
        return self._state

    async def bootstrap(self) -> RuntimeContext:
        """
        Deterministic runtime startup ordering.

        Ordering:

        1. configuration bootstrap
        2. observability initialization
        3. runtime primitive creation
        4. runtime activation
        """

        self._state = RuntimeLifecycleState.BOOTSTRAPPING

        try:
            config = self.configuration.bootstrap()

            await self.observability.initialize()

            cancellation_scope = create_root_cancellation_scope()

            supervisor = TaskSupervisor(
                name="runtime-root",
                cancellation_scope=cancellation_scope,
            )

            event_bus = RuntimeEventBus(
                supervisor=supervisor,
                cancellation_scope=cancellation_scope,
            )

            registry = RuntimeRegistry()

            context = RuntimeContext(
                runtime_id=RuntimeId(value=uuid4()),
                config=config,
                observability=self.observability,
                diagnostics=self.diagnostics,
                metadata=RuntimeMetadata(
                    runtime_version="0.1.0",
                    created_at=self._utc_now(),
                    bootstrap_completed_at=self._utc_now(),
                ),
                cancellation_scope=cancellation_scope,
                supervisor=supervisor,
                event_bus=event_bus,
                registry=registry,
            )

            self._state = RuntimeLifecycleState.ACTIVE

            return context
        except Exception:
            self._state = RuntimeLifecycleState.FAILED

        raise

    async def shutdown(
        self,
        context: RuntimeContext,
    ) -> None:
        """
        Deterministic structured runtime shutdown.

        Ordering:

        1. runtime cancellation
        2. supervisor drain
        3. observability flush/shutdown
        4. runtime termination
        """

        if self._state in (
            RuntimeLifecycleState.SHUTTING_DOWN,
            RuntimeLifecycleState.TERMINATED,
        ):
            return

        self._state = RuntimeLifecycleState.SHUTTING_DOWN

        context.cancellation_scope.cancel()

        await context.supervisor.shutdown()

        await context.observability.shutdown()

        self._state = RuntimeLifecycleState.TERMINATED

    @staticmethod
    def _utc_now() -> datetime:
        from datetime import UTC, datetime

        return datetime.now(UTC)

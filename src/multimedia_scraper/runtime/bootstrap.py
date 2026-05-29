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
    create_root_cancellation_scope, CancellationScope
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
    - lifecycle reconciliation

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

        Failure semantics:
        - no partial runtime activation
        - deterministic cleanup on failure
        """

        if self._state is not RuntimeLifecycleState.CREATED:
            raise RuntimeError(
                "Runtime bootstrap already executed",
            )

        self._state = RuntimeLifecycleState.BOOTSTRAPPING
        observability_initialized = False

        try:
            config = self.configuration.bootstrap()

            await self.observability.initialize()

            observability_initialized = True

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

            runtime_id = RuntimeId(
                value=uuid4(),
            )

            metadata = RuntimeMetadata(
                runtime_version="0.1.0",
                created_at=self._utc_now(),
                bootstrap_completed_at=self._utc_now(),
            )

            context = RuntimeContext(
                runtime_id=runtime_id,
                config=config,
                observability=self.observability,
                diagnostics=self.diagnostics,
                metadata=metadata,
                cancellation_scope=cancellation_scope,
                supervisor=supervisor,
                event_bus=event_bus,
                registry=registry,
            )

            self._register_runtime_components(
                context=context,
            )

            self._state = RuntimeLifecycleState.ACTIVE

            return context
        
        except Exception:
            self._state = RuntimeLifecycleState.FAILED

            if observability_initialized:
                await self._safe_shutdown_observability()

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

        Guarantees:
        - idempotent shutdown
        - deterministic cleanup
        - bounded task reconciliation
        """

        if self._state in (
            RuntimeLifecycleState.SHUTTING_DOWN,
            RuntimeLifecycleState.TERMINATED,
        ):
            return

        self._state = RuntimeLifecycleState.SHUTTING_DOWN

        try:
            context.cancellation_scope.cancel()

            await context.event_bus.shutdown()
            await context.supervisor.shutdown()
        finally:
            await self._safe_shutdown_observability()

            self._state = RuntimeLifecycleState.TERMINATED

    @staticmethod
    def _utc_now() -> datetime:
        from datetime import UTC, datetime

        return datetime.now(UTC)

    async def _safe_shutdown_observability(
        self,
    ) -> None:
        """
        Failure-isolated observability shutdown.

        Runtime termination must never fail because
        observability teardown fails.
        """

        try:
            await self.observability.shutdown()

        except Exception:
            pass

    def _register_runtime_components(
        self,
        *,
        context: RuntimeContext,
    ) -> None:
        """
        Explicit runtime ownership registration.

        No reflection.
        No auto-wiring.
        No DI container behavior.
        """

        context.registry.register(
            RuntimeContext,
            context,
        )

        context.registry.register(
            TaskSupervisor,
            context.supervisor,
        )

        context.registry.register(
            CancellationScope,
            context.cancellation_scope,
        )

        context.registry.register(
            RuntimeEventBus,
            context.event_bus,
        )
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType

from multimedia_scraper.plugins.contracts.plugin import (
    RuntimePlugin,
)
from multimedia_scraper.plugins.dto.capability_registration import (
    CapabilityRegistrationDTO,
)
from multimedia_scraper.plugins.dto.diagnostics import (
    PluginRegistrySnapshotDTO,
)
from multimedia_scraper.plugins.dto.registration import (
    PluginRegistrationDTO,
)
from multimedia_scraper.plugins.registry.capabilities import (
    CapabilityRegistry,
)
from multimedia_scraper.plugins.registry.exceptions import (
    DuplicatePluginError,
    PluginRegistryFrozenError,
    UnknownPluginError,
)
from multimedia_scraper.plugins.registry.snapshots import (
    create_registry_snapshot,
)
from multimedia_scraper.plugins.registry.validation import (
    validate_plugin,
)
from multimedia_scraper.plugins.runtime.container import (
    PluginContainer,
)
from multimedia_scraper.plugins.runtime.context import (
    PluginRuntimeContext,
)
from multimedia_scraper.plugins.runtime.supervision import PluginSupervisor
from multimedia_scraper.plugins.runtime.tasks import PluginTaskTracker
from multimedia_scraper.plugins.types import (
    CapabilityName,
    PluginId,
)
from multimedia_scraper.runtime.context import (
    RuntimeContext,
)
from multimedia_scraper.runtime.supervisor import (
    TaskSupervisor,
)


@dataclass(slots=True, kw_only=True)
class RuntimePluginRegistry:
    """
    Runtime-owned plugin registry.

    Responsibilities:
    - deterministic plugin registration
    - plugin lifecycle ownership
    - capability ownership registration
    - plugin execution domain ownership
    - deterministic lifecycle ordering

    Explicitly excluded:
    - dependency graphs
    - hot reload
    - plugin marketplaces
    - remote plugins
    - orchestration
    """

    _containers: dict[str, PluginContainer] = field(
        default_factory=dict,
        init=False,
    )

    _registrations: dict[str, PluginRegistrationDTO] = field(
        default_factory=dict,
        init=False,
    )

    _capability_registry: CapabilityRegistry = field(
        default_factory=CapabilityRegistry,
        init=False,
    )

    _frozen: bool = field(
        default=False,
        init=False,
    )

    @property
    def is_frozen(self) -> bool:
        return self._frozen

    @property
    def plugins(
        self,
    ) -> MappingProxyType[str, RuntimePlugin]:
        return MappingProxyType(
            {
                plugin_id: container.plugin
                for plugin_id, container in (self._containers.items())
            },
        )

    def register(
        self,
        plugin: RuntimePlugin,
        *,
        runtime_context: RuntimeContext,
        source: str,
    ) -> None:
        """
        Deterministic runtime-owned plugin registration.
        """

        if self._frozen:
            raise PluginRegistryFrozenError(
                "Plugin registry is frozen.",
            )

        validate_plugin(plugin)

        plugin_id = plugin.manifest.metadata.plugin_id

        if plugin_id in self._containers:
            raise DuplicatePluginError(
                (f"Plugin already registered: {plugin_id}"),
            )

        plugin_scope = runtime_context.cancellation_scope.create_child(
            name=f"{plugin_id}-scope",
        )

        plugin_supervisor = TaskSupervisor(
            name=f"{plugin_id}-supervisor",
            cancellation_scope=plugin_scope,
            parent=runtime_context.supervisor,
        )

        plugin_runtime_context = PluginRuntimeContext(
            plugin_id=plugin_id,
            runtime=runtime_context,
            supervisor=PluginSupervisor(_supervisor=plugin_supervisor),
            cancellation_scope=plugin_scope,
        )

        container = PluginContainer(
            plugin=plugin,
            context=plugin_runtime_context,
            task_tracker=PluginTaskTracker(),
        )

        self._containers[plugin_id] = container

        registration = PluginRegistrationDTO.create(
            manifest=plugin.manifest,
            source=source,
        )

        self._registrations[plugin_id] = registration

        self._capability_registry.register_manifest(
            plugin.manifest,
            provider=plugin,
        )

    def resolve(
        self,
        plugin_id: PluginId,
    ) -> RuntimePlugin:
        container = self._containers.get(
            plugin_id,
        )

        if container is None:
            raise UnknownPluginError(
                f"Unknown plugin: {plugin_id}",
            )

        return container.plugin

    def registrations(
        self,
    ) -> tuple[PluginRegistrationDTO, ...]:
        return tuple(
            sorted(
                self._registrations.values(),
                key=lambda registration: registration.manifest.metadata.plugin_id,
            ),
        )

    def capabilities(
        self,
        capability_name: CapabilityName,
    ) -> tuple[CapabilityRegistrationDTO, ...]:
        return self._capability_registry.resolve(
            capability_name,
        )

    def snapshot(self) -> PluginRegistrySnapshotDTO:
        return create_registry_snapshot(
            plugin_ids=tuple(
                sorted(
                    self._containers.keys(),
                ),
            ),
            frozen=self._frozen,
        )

    def freeze(self) -> None:
        self._frozen = True

    async def initialize_all(self) -> None:
        """
        Deterministic plugin initialization ordering.
        """

        for plugin_id in sorted(
            self._containers.keys(),
        ):
            container = self._containers[plugin_id]

            await container.initialize()

    async def activate_all(self) -> None:
        """
        Deterministic plugin activation ordering.
        """

        for plugin_id in sorted(
            self._containers.keys(),
        ):
            container = self._containers[plugin_id]

            await container.activate()

    async def shutdown_all(self) -> None:
        """
        Deterministic reverse-order shutdown.
        """

        for plugin_id in sorted(self._containers.keys(), reverse=True):
            container = self._containers[plugin_id]

            await container.shutdown()

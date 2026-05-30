from __future__ import annotations

from dataclasses import dataclass, field

from multimedia_scraper.plugins.contracts.plugin import (
    RuntimePlugin,
)
from multimedia_scraper.plugins.contracts.states import PluginLifecycleState
from multimedia_scraper.plugins.runtime.context import (
    PluginRuntimeContext,
)
from multimedia_scraper.plugins.runtime.exceptions import PluginTaskLeakError
from multimedia_scraper.plugins.runtime.tasks import (
    PluginTaskTracker,
)


@dataclass(slots=True, kw_only=True)
class PluginContainer:
    plugin: RuntimePlugin

    context: PluginRuntimeContext

    task_tracker: PluginTaskTracker

    _state: PluginLifecycleState = field(
        default=PluginLifecycleState.LOADED,
        init=False,
    )

    @property
    def state(self) -> PluginLifecycleState:
        return self._state

    async def initialize(self) -> None:
        self._state = PluginLifecycleState.INITIALIZING

        await self.plugin.initialize(
            self.context,
        )

        self._state = PluginLifecycleState.INITIALIZED

    async def activate(self) -> None:
        self._state = PluginLifecycleState.ACTIVATING

        await self.plugin.activate()

        self._state = PluginLifecycleState.ACTIVE

    async def shutdown(self) -> None:
        self._state = PluginLifecycleState.SHUTTING_DOWN

        self.context.cancellation_scope.cancel()

        await self.plugin.shutdown()

        if self.task_tracker.active_count > 0:
            raise PluginTaskLeakError("leaked task error")

        await self.context.supervisor.shutdown()

        self._state = PluginLifecycleState.TERMINATED

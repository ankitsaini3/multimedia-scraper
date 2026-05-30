from __future__ import annotations

from dataclasses import dataclass

from multimedia_scraper.plugins.runtime.supervision import (
    PluginSupervisor,
)
from multimedia_scraper.runtime.cancellation import (
    CancellationScope,
)
from multimedia_scraper.runtime.context import (
    RuntimeContext,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class PluginRuntimeContext:
    plugin_id: str

    runtime: RuntimeContext

    supervisor: PluginSupervisor

    cancellation_scope: CancellationScope

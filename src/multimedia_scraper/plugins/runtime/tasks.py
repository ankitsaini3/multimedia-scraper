from __future__ import annotations

from dataclasses import dataclass, field

from multimedia_scraper.runtime.task import (
    RuntimeTask,
)


@dataclass(slots=True, kw_only=True)
class PluginTaskTracker:
    _tasks: set[RuntimeTask[object]] = field(
        default_factory=set,
        init=False,
    )

    def track(
        self,
        task: RuntimeTask[object],
    ) -> None:
        self._tasks.add(task)

    def discard(
        self,
        task: RuntimeTask[object],
    ) -> None:
        self._tasks.discard(task)

    @property
    def active_count(self) -> int:
        return len(self._tasks)

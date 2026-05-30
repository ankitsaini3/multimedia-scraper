from __future__ import annotations

from collections.abc import Coroutine
from dataclasses import dataclass
from typing import TypeVar

from multimedia_scraper.runtime.supervisor import (
    TaskSupervisor,
)
from multimedia_scraper.runtime.task import (
    RuntimeTask,
)

T = TypeVar("T")


@dataclass(frozen=True, slots=True, kw_only=True)
class PluginSupervisor:
    """
    Scoped plugin supervision boundary.

    Plugins MUST NOT receive raw runtime supervisors.
    """

    _supervisor: TaskSupervisor

    def spawn(
        self,
        *,
        name: str,
        coroutine: Coroutine[object, object, T],
    ) -> RuntimeTask[T]:
        return self._supervisor.spawn(
            name=name,
            coroutine=coroutine,
        )

    async def shutdown(self) -> None:
        await self._supervisor.shutdown()

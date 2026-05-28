from __future__ import annotations

import asyncio
from collections.abc import Coroutine
from dataclasses import dataclass, field
from typing import TypeVar
from uuid import UUID, uuid4

from multimedia_scraper.runtime.cancellation import (
    CancellationScope,
)
from multimedia_scraper.runtime.exceptions import (
    SupervisorClosedError,
)
from multimedia_scraper.runtime.task import RuntimeTask, create_runtime_task

T = TypeVar("T")


@dataclass(slots=True, kw_only=True)
class TaskSupervisor:
    """
    Minimal structured concurrency supervisor.
    """

    name: str

    cancellation_scope: CancellationScope

    parent: TaskSupervisor | None = None

    _supervisor_id: UUID = field(
        default_factory=uuid4,
        init=False,
    )

    _children: set[asyncio.Task[object]] = field(
        default_factory=set,
        init=False,
        repr=False,
    )

    _closed: bool = field(
        default=False,
        init=False,
        repr=False,
    )

    @property
    def supervisor_id(self) -> UUID:
        return self._supervisor_id

    @property
    def is_closed(self) -> bool:
        return self._closed

    def spawn(
        self,
        *,
        name: str,
        coroutine: Coroutine[object, object, T],
    ) -> RuntimeTask[T]:
        if self._closed:
            raise SupervisorClosedError(
                f"Supervisor '{self.name}' is closed",
            )

        self.cancellation_scope.raise_if_cancelled()

        runtime_task = create_runtime_task(
            name=name,
            coroutine=coroutine,
        )

        self._children.add(runtime_task.task)

        runtime_task.task.add_done_callback(
            lambda completed: self._children.discard(completed),
        )

        return runtime_task

    async def shutdown(self) -> None:
        if self._closed:
            return

        self._closed = True

        self.cancellation_scope.cancel()

        children = tuple(self._children)

        if not children:
            return

        await asyncio.gather(
            *children,
            return_exceptions=True,
        )

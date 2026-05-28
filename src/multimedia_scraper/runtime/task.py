from __future__ import annotations

import asyncio
from collections.abc import Coroutine
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID, uuid4

T = TypeVar("T")


@dataclass(frozen=True, slots=True, kw_only=True)
class RuntimeTask(Generic[T]):
    """
    Immutable runtime-owned task handle.
    """

    task_id: UUID

    name: str

    task: asyncio.Task[T]

    async def wait(self) -> T:
        return await self.task

    @property
    def done(self) -> bool:
        return self.task.done()

    @property
    def cancelled(self) -> bool:
        return self.task.cancelled()


def create_runtime_task(
    *,
    name: str,
    coroutine: Coroutine[object, object, T],
) -> RuntimeTask[T]:
    task = asyncio.create_task(
        coroutine,
        name=name,
    )

    return RuntimeTask(
        task_id=uuid4(),
        name=name,
        task=task,
    )

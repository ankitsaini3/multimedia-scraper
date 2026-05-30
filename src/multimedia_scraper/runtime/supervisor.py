from __future__ import annotations

import asyncio
from collections.abc import Coroutine
from dataclasses import dataclass, field
from typing import TypeVar
from uuid import UUID, uuid4

from multimedia_scraper.core.errors.runtime import (
    RuntimeCancellationError,
)
from multimedia_scraper.core.errors.supervision import SupervisorClosedError
from multimedia_scraper.runtime.cancellation import (
    CancellationScope,
)
from multimedia_scraper.runtime.task import RuntimeTask, create_runtime_task

T = TypeVar("T")

DEFAULT_SHUTDOWN_TIMEOUT_SECONDS = 5.0


@dataclass(slots=True, kw_only=True)
class TaskSupervisor:
    """
    Minimal structured concurrency supervisor.

    Responsibilities:
    - structured spawning
    - task ownership
    - cooperative cancellation propagation
    - deterministic shutdown
    - orphan prevention
    """

    name: str

    cancellation_scope: CancellationScope

    parent: TaskSupervisor | None = None

    shutdown_timeout_seconds: float = DEFAULT_SHUTDOWN_TIMEOUT_SECONDS

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
            coroutine=self._run_structured(
                coroutine=coroutine,
            ),
        )

        self._children.add(runtime_task.task)

        runtime_task.task.add_done_callback(
            self._on_task_done,
        )

        return runtime_task

    async def shutdown(self) -> None:
        """
        Deterministic graceful supervisor shutdown.

        Shutdown flow:
        1. close spawning
        2. propagate cooperative cancellation
        3. await graceful completion
        4. force asyncio cancellation if bounded wait expires
        """
        if self._closed:
            return

        self._closed = True

        self.cancellation_scope.cancel()

        children = tuple(self._children)

        if not children:
            return

        try:
            await asyncio.wait_for(
                asyncio.gather(
                    *children,
                    return_exceptions=True,
                ),
                timeout=self.shutdown_timeout_seconds,
            )

        except TimeoutError:
            for task in children:
                task.cancel()

    async def _run_structured(
        self,
        *,
        coroutine: Coroutine[object, object, T],
    ) -> T:
        """
        Structured execution wrapper.

        Ensures:
        - cooperative cancellation awareness
        - scope-bound execution
        - cancellation propagation consistency
        """

        if self.cancellation_scope.is_cancelled:
            raise RuntimeCancellationError()

        try:
            return await coroutine

        except asyncio.CancelledError as exc:
            self.cancellation_scope.cancel()

            raise RuntimeCancellationError() from exc

    def _on_task_done(
        self,
        completed: asyncio.Task[object],
    ) -> None:
        """
        Deterministic ownership cleanup.

        Prevents orphan tracking retention.
        """

        self._children.discard(completed)

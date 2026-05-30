from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from typing import TypeVar, cast

from multimedia_scraper.runtime.cancellation import (
    CancellationScope,
)
from multimedia_scraper.runtime.events import RuntimeEvent
from multimedia_scraper.core.errors.supervision import SupervisorClosedError
from multimedia_scraper.runtime.supervisor import (
    TaskSupervisor,
)
from multimedia_scraper.runtime.task import RuntimeTask

TEvent = TypeVar(
    "TEvent",
    bound=RuntimeEvent,
)

EventHandler = Callable[
    [TEvent],
    Coroutine[object, object, None],
]

_InternalHandler = Callable[
    [RuntimeEvent],
    Coroutine[object, object, None],
]


@dataclass(slots=True, kw_only=True)
class RuntimeEventBus:
    """
    Minimal supervised in-memory runtime event bus.

    Guarantees:
    - structured handler execution
    - cancellation-aware dispatch
    - deterministic publish semantics
    - lifecycle-bound coordination
    """

    supervisor: TaskSupervisor

    cancellation_scope: CancellationScope

    _subscribers: dict[
        type[RuntimeEvent],
        set[_InternalHandler],
    ] = field(
        default_factory=lambda: defaultdict(set),
        init=False,
        repr=False,
    )

    _closed: bool = field(
        default=False,
        init=False,
        repr=False,
    )

    @property
    def is_closed(self) -> bool:
        return self._closed

    def subscribe(
        self,
        event_type: type[TEvent],
        handler: EventHandler[TEvent],
    ) -> None:
        """
        Registers a typed async subscriber.
        """
        if self._closed:
            raise RuntimeError(
                "RuntimeEventBus is closed",
            )

        erased_handler = cast(
            _InternalHandler,
            handler,
        )

        handlers = self._subscribers[event_type]

        handlers.add(erased_handler)

    def unsubscribe(
        self,
        event_type: type[TEvent],
        handler: EventHandler[TEvent],
    ) -> None:

        erased_handler = cast(
            _InternalHandler,
            handler,
        )

        handlers = self._subscribers.get(event_type)

        if handlers is None:
            return

        handlers.discard(erased_handler)

    async def publish(
        self,
        event: RuntimeEvent,
    ) -> None:
        """
        Deterministic structured event dispatch.

        Guarantees:
        - cancellation-aware execution
        - supervised handler ownership
        - deterministic handler snapshotting
        - failure isolation
        """
        if self._closed:
            return

        self.cancellation_scope.raise_if_cancelled()

        handlers = tuple(
            self._subscribers.get(type(event), ()),
        )

        if not handlers:
            return

        runtime_tasks = tuple(
            self._spawn_handler(
                event=event,
                handler=handler,
            )
            for handler in handlers
        )

        await asyncio.gather(
            *(task.wait() for task in runtime_tasks),
            return_exceptions=True,
        )

    async def shutdown(self) -> None:
        """
        Deterministic event bus shutdown.

        Event bus owns no independent workers,
        queues, or detached execution.

        Shutdown only prevents future publications
        and subscriptions.
        """

        if self._closed:
            return

        self._closed = True

        self._subscribers.clear()

    def _spawn_handler(
        self,
        *,
        event: RuntimeEvent,
        handler: _InternalHandler,
    ) -> RuntimeTask[None]:
        """
        Spawn a supervised handler execution.

        Ensures all handler execution remains
        lifecycle-bound to the runtime supervisor.
        """

        try:
            return self.supervisor.spawn(
                name=(f"event-handler:{event.event_type}"),
                coroutine=self._run_handler(
                    event=event,
                    handler=handler,
                ),
            )

        except SupervisorClosedError:
            raise

    async def _run_handler(
        self,
        *,
        event: RuntimeEvent,
        handler: _InternalHandler,
    ) -> None:
        """
        Structured handler execution wrapper.

        Failure isolation intentionally occurs
        at gather(return_exceptions=True).
        """

        self.cancellation_scope.raise_if_cancelled()

        await handler(event)

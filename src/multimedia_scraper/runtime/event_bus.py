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
from multimedia_scraper.runtime.supervisor import (
    TaskSupervisor,
)

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
    Minimal async in-memory runtime event bus.
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

    def subscribe(
        self,
        event_type: type[TEvent],
        handler: EventHandler[TEvent],
    ) -> None:
        """
        Registers a typed async subscriber.
        """

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
        Deterministic cancellation-safe event dispatch.
        """

        self.cancellation_scope.raise_if_cancelled()

        handlers = tuple(
            self._subscribers.get(type(event), ()),
        )

        if not handlers:
            return

        tasks = tuple(
            self.supervisor.spawn(
                name=(f"event-handler:{event.event_type}"),
                coroutine=handler(event),
            )
            for handler in handlers
        )

        await asyncio.gather(
            *(task.wait() for task in tasks),
            return_exceptions=True,
        )

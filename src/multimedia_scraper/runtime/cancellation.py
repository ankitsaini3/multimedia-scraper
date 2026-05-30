from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Final
from uuid import UUID, uuid4

from multimedia_scraper.runtime.exceptions import (
    CancellationScopeClosedError,
    RuntimeCancellationError,
)

ROOT_CANCELLATION_SCOPE_NAME: Final[str] = "runtime-root"


@dataclass(frozen=True, slots=True, kw_only=True)
class CancellationToken:
    """
    Immutable cooperative cancellation view.

    Tokens never own cancellation state.

    Ownership belongs exclusively to CancellationScope.
    """

    scope_id: UUID

    _cancel_event: asyncio.Event = field(
        repr=False,
        compare=False,
    )

    @property
    def is_cancelled(self) -> bool:
        return self._cancel_event.is_set()

    async def wait_cancelled(self) -> None:
        await self._cancel_event.wait()

    def raise_if_cancelled(self) -> None:
        if self.is_cancelled:
            raise RuntimeCancellationError(
                f"Cancellation requested for scope {self.scope_id}",
            )


@dataclass(slots=True, kw_only=True)
class CancellationScope:
    """
    Minimal structured cancellation primitive.

    Responsibilities:

    - cooperative cancellation
    - deterministic propagation
    - explicit ownership
    - downward cancellation hierarchy

    Explicitly excluded:

    - supervision
    - retries
    - scheduling
    - orchestration
    - worker management
    """

    name: str

    parent: CancellationScope | None = None

    _scope_id: UUID = field(
        default_factory=uuid4,
        init=False,
    )

    _cancel_event: asyncio.Event = field(
        default_factory=asyncio.Event,
        init=False,
        repr=False,
    )

    _children: set[CancellationScope] = field(
        default_factory=set,
        init=False,
        repr=False,
    )

    _closed: bool = field(
        default=False,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        if self.parent is not None:
            self.parent._register_child(self)

            if self.parent.is_cancelled:
                self.cancel()

    @property
    def scope_id(self) -> UUID:
        return self._scope_id

    @property
    def token(self) -> CancellationToken:
        return CancellationToken(
            scope_id=self._scope_id,
            _cancel_event=self._cancel_event,
        )

    @property
    def is_cancelled(self) -> bool:
        return self._cancel_event.is_set()

    @property
    def is_closed(self) -> bool:
        return self._closed

    def create_child(
        self,
        *,
        name: str,
    ) -> CancellationScope:
        """
        Creates a deterministic child scope.
        """

        if self._closed:
            raise CancellationScopeClosedError(
                f"Scope '{self.name}' is closed",
            )

        return CancellationScope(
            name=name,
            parent=self,
        )

    def cancel(self) -> None:
        """
        Deterministic cooperative cancellation.

        Cancellation propagates downward only.
        """

        if self.is_cancelled:
            return

        self._cancel_event.set()

        for child in tuple(self._children):
            child.cancel()

    async def wait_cancelled(self) -> None:
        await self._cancel_event.wait()

    def close(self) -> None:
        """
        Prevents future child creation.

        Does NOT cancel the scope.
        """

        self._closed = True

    def raise_if_cancelled(self) -> None:
        self.token.raise_if_cancelled()

    def _register_child(
        self,
        child: CancellationScope,
    ) -> None:
        self._children.add(child)

    def __hash__(self) -> int:
        return hash(self._scope_id)


def create_root_cancellation_scope() -> CancellationScope:
    """
    Creates the root structured cancellation scope.
    """

    return CancellationScope(
        name=ROOT_CANCELLATION_SCOPE_NAME,
    )


async def cancel_after(
    scope: CancellationScope,
    timeout_seconds: float,
) -> None:
    try:
        await asyncio.sleep(timeout_seconds)

    except asyncio.CancelledError:
        return

    if not scope.is_cancelled:
        scope.cancel()

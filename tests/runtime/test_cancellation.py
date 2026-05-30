from __future__ import annotations

import asyncio

import pytest

from multimedia_scraper.runtime.cancellation import (
    CancellationScopeClosedError,
    RuntimeCancellationError,
    cancel_after,
    create_root_cancellation_scope,
)

pytestmark = pytest.mark.asyncio


async def test_token_reflects_scope_cancellation() -> None:
    scope = create_root_cancellation_scope()

    token = scope.token

    assert token.is_cancelled is False

    scope.cancel()

    assert token.is_cancelled is True


async def test_parent_cancellation_propagates_downward() -> None:
    root = create_root_cancellation_scope()

    child = root.create_child(
        name="child",
    )

    grandchild = child.create_child(
        name="grandchild",
    )

    root.cancel()

    assert root.is_cancelled is True
    assert child.is_cancelled is True
    assert grandchild.is_cancelled is True


async def test_child_cancellation_does_not_propagate_upward() -> None:
    root = create_root_cancellation_scope()

    child = root.create_child(
        name="child",
    )

    child.cancel()

    assert child.is_cancelled is True
    assert root.is_cancelled is False


async def test_closed_scope_rejects_children() -> None:
    scope = create_root_cancellation_scope()

    scope.close()

    with pytest.raises(
        CancellationScopeClosedError,
    ):
        scope.create_child(name="child")


async def test_close_does_not_cancel_scope() -> None:
    scope = create_root_cancellation_scope()

    scope.close()

    assert scope.is_closed is True
    assert scope.is_cancelled is False


async def test_child_created_after_parent_cancelled_auto_cancels() -> None:
    root = create_root_cancellation_scope()

    root.cancel()

    child = root.create_child(
        name="child",
    )

    assert child.is_cancelled is True


async def test_cancel_is_idempotent() -> None:
    scope = create_root_cancellation_scope()

    scope.cancel()
    scope.cancel()
    scope.cancel()

    assert scope.is_cancelled is True


async def test_wait_cancelled_unblocks() -> None:
    scope = create_root_cancellation_scope()

    waiter = asyncio.create_task(
        scope.wait_cancelled(),
    )

    await asyncio.sleep(0)

    scope.cancel()

    await waiter


async def test_raise_if_cancelled_raises() -> None:
    scope = create_root_cancellation_scope()

    scope.cancel()

    with pytest.raises(
        RuntimeCancellationError,
    ):
        scope.raise_if_cancelled()


async def test_cancel_after_cancels_scope() -> None:
    scope = create_root_cancellation_scope()

    await cancel_after(
        scope,
        timeout_seconds=0.01,
    )

    assert scope.is_cancelled is True


async def test_cancel_after_respects_existing_cancellation() -> None:
    scope = create_root_cancellation_scope()

    scope.cancel()

    await cancel_after(
        scope,
        timeout_seconds=0.01,
    )

    assert scope.is_cancelled is True

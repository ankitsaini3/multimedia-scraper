from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest


def test_runtime_context_is_immutable(
    runtime_context,
) -> None:
    with pytest.raises(FrozenInstanceError):
        runtime_context.registry = object()


def test_runtime_dependencies_cannot_be_replaced(
    runtime_context,
) -> None:
    with pytest.raises(FrozenInstanceError):
        runtime_context.event_bus = object()


def test_runtime_context_dependency_identity_stable(
    runtime_context,
) -> None:
    registry_before = runtime_context.registry

    registry_after = runtime_context.registry

    assert registry_before is registry_after

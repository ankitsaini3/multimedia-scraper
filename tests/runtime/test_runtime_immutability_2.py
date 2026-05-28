from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest


def test_runtime_context_freeze_boundary(
    runtime_context,
):
    with pytest.raises(FrozenInstanceError):
        runtime_context.metadata = object()

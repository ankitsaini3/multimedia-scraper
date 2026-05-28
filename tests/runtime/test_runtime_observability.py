from __future__ import annotations


def test_runtime_uses_explicit_observability_dependency(
    runtime_context,
):
    assert runtime_context.observability is not None

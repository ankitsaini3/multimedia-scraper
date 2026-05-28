from __future__ import annotations


def test_runtime_registries_are_isolated():
    from multimedia_scraper.runtime.registry import (
        RuntimeRegistry,
    )

    registry_a = RuntimeRegistry()

    registry_b = RuntimeRegistry()

    registry_a.register(str, "a")

    assert registry_b.try_resolve(str) is None

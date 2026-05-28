from __future__ import annotations


def test_cancellation_propagates_to_children():
    from multimedia_scraper.runtime.cancellation import (
        create_root_cancellation_scope,
    )

    root = create_root_cancellation_scope()

    child = root.create_child(
        name="child",
    )

    root.cancel()

    assert root.is_cancelled is True

    assert child.is_cancelled is True

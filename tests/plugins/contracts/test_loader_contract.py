from __future__ import annotations

from pathlib import Path

from multimedia_scraper.plugins.loader.discovery import (
    discover_local_plugins,
)


def test_discovery_ordering(
    tmp_path: Path,
):
    (tmp_path / "plugin_b").mkdir()

    (tmp_path / "plugin_a").mkdir()

    (tmp_path / "plugin_c").mkdir()

    discoveries = discover_local_plugins(
        root=tmp_path,
    )

    assert tuple(discovery.plugin_id for discovery in discoveries) == (
        "plugin_a",
        "plugin_b",
        "plugin_c",
    )

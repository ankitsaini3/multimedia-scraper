from __future__ import annotations

from pathlib import Path


def discover_plugin_directories(
    root: Path,
) -> tuple[Path, ...]:
    if not root.exists():
        return ()

    return tuple(
        sorted(path for path in root.iterdir() if path.is_dir()),
    )

from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
from collections.abc import Callable

CACHE_PATHS = [
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "build",
    "dist",
    "htmlcov",
    ".coverage",
]


def clean() -> None:
    for path_str in CACHE_PATHS:
        path = pathlib.Path(path_str)

        # Safely handle symlinks, directories, and files
        if path.is_symlink():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        elif path.exists():
            path.unlink()


def run_commands(commands: list[list[str]]) -> None:
    for cmd in commands:
        print(f"\n>>> Running: {' '.join(cmd)}\n")
        subprocess.run(cmd, check=True)


def ci() -> None:
    clean()

    commands = [
        ["ruff", "format", ".", "--check"],
        ["ruff", "check", "."],
        ["mypy", "src/multimedia_scraper"],
        [
            "pytest",
            "--cov=multimedia_scraper",
            "--cov-report=term-missing",
            "-n",
            "auto",
        ],
    ]

    run_commands(commands)


TASKS: dict[str, Callable[[], None]] = {
    "clean": clean,
    "ci": ci,
}


def main() -> int:
    if len(sys.argv) < 2:
        print("Available tasks:")
        for task_name in TASKS:
            print(f"  - {task_name}")
        return 1

    task_name = sys.argv[1]
    task = TASKS.get(task_name)

    if task is None:
        print(f"Unknown task: {task_name}")
        return 1

    try:
        task()
    except subprocess.CalledProcessError as e:
        print(f"\nCommand failed with exit code {e.returncode}: {' '.join(e.cmd)}")
        return e.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

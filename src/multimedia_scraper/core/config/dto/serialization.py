from __future__ import annotations

import json
from dataclasses import asdict

from .runtime import RuntimeConfigDTO


def serialize_runtime_config(
    config: RuntimeConfigDTO,
) -> str:
    return json.dumps(
        asdict(config),
        sort_keys=True,
        separators=(",", ":"),
    )

from __future__ import annotations

import importlib
from types import ModuleType


def import_plugin_module(
    module_name: str,
) -> ModuleType:
    return importlib.import_module(module_name)

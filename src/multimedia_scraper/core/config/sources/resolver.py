from __future__ import annotations

from collections.abc import Iterable

from .merge import merge_sources
from .models import ConfigSource


class ConfigResolver:

    def resolve(
        self,
        sources: Iterable[ConfigSource],
    ) -> dict[str, object]:

        return merge_sources(sources)
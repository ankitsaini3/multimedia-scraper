from multimedia_scraper.core.config.sources.merge import (
    merge_sources,
)
from multimedia_scraper.core.config.sources.models import (
    ConfigSource,
)
from multimedia_scraper.core.config.sources.types import (
    ConfigSourceType,
)


def test_merge_is_deterministic() -> None:

    source_a = ConfigSource(
        source_type=ConfigSourceType.DEFAULT,
        source_name="defaults",
        precedence=0,
        payload={
            "logging.level": "INFO",
        },
    )

    source_b = ConfigSource(
        source_type=ConfigSourceType.ENVIRONMENT,
        source_name="env",
        precedence=1,
        payload={
            "logging.level": "DEBUG",
        },
    )

    result_1 = merge_sources(
        [source_a, source_b],
    )

    result_2 = merge_sources(
        [source_a, source_b],
    )

    assert result_1 == result_2

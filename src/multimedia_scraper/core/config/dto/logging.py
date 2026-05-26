from dataclasses import dataclass

from .base import ConfigDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class LoggingConfigDTO(ConfigDTO):
    level: str
    json_logs: bool
    correlation_ids: bool
from enum import Enum


class ConfigSourceType(str, Enum):
    DEFAULT = "default"
    FILE = "file"
    ENVIRONMENT = "environment"
    SECRET = "secret"
    CLI = "cli"

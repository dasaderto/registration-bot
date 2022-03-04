import logging
from enum import Enum
from pathlib import Path
from typing import List


class Environment(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    PRODUCTION_CONSOLE = "production console"
    STAGING = "staging"


class BaseConfig:
    BOT_TOKEN: str
    DEFAULT_LOGGING_LEVEL = logging.DEBUG
    LOGS_FORMAT = '%(asctime)s - %(name)s[%(process)d] - %(threadName)s - %(levelname)s - %(message)s'

    # FILESYSTEM
    ROOT_PATH = Path()
    RUNTIME_PATH = ROOT_PATH / "runtime"
    LOGS_PATH = RUNTIME_PATH / "logs"
    RESOURCES_PATH = ROOT_PATH / "resources"
    LOCALIZATIONS_PATH = RESOURCES_PATH / "localization"
    ENVIRONMENT: Environment
    DEFAULT_LANGUAGE = "ru"

    # DB
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str

    REGISTERED_MODELS: List[str]
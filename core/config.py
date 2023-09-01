import logging
import os
from typing import Union

from pydantic_settings import BaseSettings

from core.utils.config_helpers import build_database_uri, get_database_uri_from_secret

log = logging.getLogger(__name__)


class Config(BaseSettings):
    APP_ENV: str = os.environ.get("APP_ENV", "dev")
    DEBUG: bool = True
    APP_HOST: str = "localhost"
    APP_PORT: int = os.environ.get("APP_PORT", 8000) # type: ignore
    LOG_LEVEL: str = "DEBUG"

    DB_SECRETS_MANAGER_KEY: Union[str, None] = os.environ.get(
        "DB_SECRETS_MANAGER_KEY", None
    )

    if DB_SECRETS_MANAGER_KEY:
        DB_CONNECTION_URI: str = get_database_uri_from_secret(DB_SECRETS_MANAGER_KEY)
    else:
        # The reason to override the default value is to make it easier to run the app locally from alembic perspective, where env might not be set
        DB_CONNECTION_URI: str = build_database_uri(
            DB_DRIVER=os.environ.get("DB_DRIVER", "postgresql"),
            DB_HOST=os.environ.get("DB_HOST", "db"),
            DB_PORT=os.environ.get("DB_PORT", 5432),
            DB_NAME=os.environ.get("DB_NAME", "postgres"),
            DB_USER=os.environ.get("DB_USER", "postgres"),
            DB_PASSWORD=os.environ.get("DB_PASSWORD", "postgres"),
        )
    # DBConfig, where there will be placeholders for read and write DB URIs
    WRITER_DB_URI: str = DB_CONNECTION_URI
    READER_DB_URI: str = DB_CONNECTION_URI
    DB_ENGINE_POOL_SIZE: int = os.environ.get("DB_ENGINE_POOL_SIZE", 20) # type: ignore
    DB_ENGINE_MAX_OVERFLOW: int = os.environ.get("DB_ENGINE_MAX_OVERFLOW", 0) # type: ignore


class TestingConfig(Config):
    APP_ENV: str = "test"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"


class DevelopmentConfig(Config):
    APP_ENV: str = "dev"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"


class ProductionConfig(Config):
    APP_ENV: str = "prod"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"


def get_config():
    APP_ENV = os.environ.get("APP_ENV", "dev")
    config_type = {
        "dev": DevelopmentConfig(),
        "test": TestingConfig(),
        "prod": ProductionConfig(),
    }

    log.debug(f"APP_ENV: {APP_ENV}")
    return config_type[APP_ENV]


config = get_config()

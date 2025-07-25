from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLL_BACK: bool = False


class ProdConfig(GlobalConfig):
    SettingsConfigDict(env_prefix="PROD_")


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True

    SettingsConfigDict(env_prefix="TEST_")


@lru_cache()
def get_config(env_state: str):
    config = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return config[env_state]()


config = get_config(BaseConfig().ENV_STATE)

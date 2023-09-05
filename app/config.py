""" Enviroment Variables Utilities """
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Enviroment Variable Class"""

    model_config = SettingsConfigDict(env_file=".env")

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOSTNAME: str
    DB_PORT: int
    DB_NAME: str
    DB_TEST_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()

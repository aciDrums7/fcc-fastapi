""" Enviroment Variables Utilities """
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Enviroment Variable Class"""

    model_config = SettingsConfigDict(env_file=".env")

    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_HOSTNAME: str = "freecodecamp"
    DB_PORT: int = 5432
    DB_NAME: str = "fastapi"
    DB_TEST_NAME: str = "fastapi_test"
    SECRET_KEY: str = "SecretKey123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 21


settings = Settings()

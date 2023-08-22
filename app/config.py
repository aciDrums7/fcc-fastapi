""" Enviroment Variables Utilities """
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Enviroment Variable Class"""

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOSTNAME: str
    DB_PORT: int
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        """Pydantic Config Class"""

        env_file = ".env"


settings = Settings()

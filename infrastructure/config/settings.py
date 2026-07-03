from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Configurações do banco de dados
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Configurações do JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    # Configurações do email
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    # Aliases para manter compatibilidade no código
    @property
    def EMAIL_HOST(self) -> str:
        return self.SMTP_HOST

    @property
    def EMAIL_PORT(self) -> int:
        return self.SMTP_PORT

    @property
    def EMAIL_USER(self) -> str:
        return self.SMTP_USER

    @property
    def EMAIL_PASSWORD(self) -> str:
        return self.SMTP_PASSWORD

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()

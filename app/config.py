from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore") # extra позволяет игнорировать переменные окружения, которые есть в .env файле, но отсутсвуют в config.py


settings = Settings()

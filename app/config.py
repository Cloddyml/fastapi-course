from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_NAME: str

    model_config = SettingsConfigDict(
        # pathlib позволяет формировать путь
        # с помощью оператора "/", аналогично os.path.join()
        env_file=BASE_DIR / ".env"
        # extra="ignore # extra позволяет игнорировать переменные окружения, которые есть в .env файле, но отсутсвуют в config.py
    )

settings = Settings()

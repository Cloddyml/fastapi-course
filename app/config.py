from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        # pathlib позволяет формировать путь
        # с помощью оператора "/", аналогично os.path.join()
        env_file=BASE_DIR / ".env"
        # extra="ignore # extra позволяет игнорировать переменные окружения, которые есть в .env файле, но отсутсвуют в config.py
    )

settings = Settings()

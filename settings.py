from pydantic_settings import BaseSettings, SettingsConfigDict

SECRET_KEY: str = "safpfsdakfjsadkqwofiqoiwfhoiqwhfi12oi3421oihfoqihfpqoiwhfopi12hfphpqhwfpasfhjpajfs"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
REFRESH_TOKEN_EXPIRE_DAYS: int = 14


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    db_name: str
    db_user: str
    db_host: str
    db_port: str
    db_pass: str

    superuser_password: str
    superuser_name: str
    superuser_email: str
    superuser_tg_id: int

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    def get_db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}/{self.db_name}"


settings = Settings()

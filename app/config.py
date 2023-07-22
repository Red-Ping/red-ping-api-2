from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Red Ping"
    secret_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env")
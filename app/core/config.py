from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "LLM app"
    ENV: str = "local"

    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    SQLITE_PATH: str

    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL:str
    OPENROUTER_MODEL: str
    OPENROUTER_SITE_URL: str
    OPENROUTER_APP_NAME: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
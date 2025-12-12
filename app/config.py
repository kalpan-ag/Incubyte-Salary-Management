from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./salary_kata.db"
    app_title: str = "Incubyte Salary API"
    app_version: str = "1.0.0"

    # extra="ignore" tells Pydantic to ignore PYTHONPATH and other system vars
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
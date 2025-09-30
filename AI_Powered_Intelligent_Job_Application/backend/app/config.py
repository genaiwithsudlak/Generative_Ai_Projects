# backend/app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    LLM_MODEL: str = "gpt-4o-mini"   # change to your preferred model
    LINKEDIN_EMAIL: str | None = None
    LINKEDIN_PASSWORD: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

from pydantic import BaseSettings
from openai import OpenAI

class Settings(BaseSettings):
    openai_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

client = OpenAI(api_key=settings.openai_api_key)

from openai import OpenAI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    tmp_dir: str = "/tmp"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

client = OpenAI(api_key=settings.openai_api_key)

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_api_key: str = ""
    model_base_url: str = "https://api.meta.ai/v1"
    model_name: str = "your-model-name"
    database_url: str = "sqlite:///./documentor.db"

    class Config:
        env_file = ".env"

settings = Settings()

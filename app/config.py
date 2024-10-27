from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MINIO_BUCKET_NAME: str
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_URL: str
    DATABASE_URL: str
    SECRET_KEY: str = "helloworld"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 180

    class Config:
        env_file = ".env"


settings = Settings()

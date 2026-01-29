import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "GitHub Clone"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # GCS Configuration
    BUCKET_NAME: str = os.getenv("BUCKET_NAME", "my-github-clone-bucket")
    MOUNT_POINT: str = os.getenv("MOUNT_POINT", "/mnt/gcs")

    class Config:
        case_sensitive = True

settings = Settings()

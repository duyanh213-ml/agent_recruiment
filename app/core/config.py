import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Agent Recruitment App"

    default_HR_role: str = "HR"
    default_admin_role: str = "HR_admin"
    default_hr_active: bool = False
    default_admin_active: bool = True

    DATABASE_NAME: str = os.getenv('POSTGRES_DB', "recruitment")
    DATABASE_USER: str = os.getenv('POSTGRES_USER', "postgres")
    DATABASE_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', "recruitment")
    DATABASE_HOST: str = os.getenv('POSTGRES_HOST', "127.0.0.1")
    DATABASE_PORT: str = os.getenv('POSTGRES_PORT', "5432")

    HR_ADMIN_USERNAME: str = os.getenv('HR_ADMIN_USERNAME', '')
    HR_ADMIN_PASSWORD: str = os.getenv('HR_ADMIN_PASSWORD', '')
    
    MINIO_ENDPOINT: str = os.getenv('MINIO_ENDPOINT')
    MINIO_ACCESS_KEY: str = os.getenv('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY: str = os.getenv('MINIO_SECRET_KEY')
    MINIO_BUCKET_NAME: str = os.getenv('MINIO_BUCKET_NAME')
    
    TMP_CANDIDATE_FILE: str = os.getenv('TMP_CANDIDATE_FILE')

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql+psycopg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


settings = Settings()


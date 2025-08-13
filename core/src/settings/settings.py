import os

from dotenv import load_dotenv

load_dotenv()


def display_startup_message():
    """Display a rectangle message on app startup."""
    print(
        "########################################\n"
        "#                                      #\n"
        "#  Agent Recruitment Core Application  #\n"
        "#                                      #\n"
        "########################################"
    )


class PDFExtractorSettings:

    ZOOM_CONST = 2


class GeneralCoreSettings:

    PREFIX: str = "/recruitment_agent/core"
    TOKEN: str = os.getenv("TOKEN", "")
    TMP_CANDIDATE_FOLDER: str = "tmp_candidate_folder"

    EXTRACT_OBJECTIVE: str = "extract_objective"
    EXTRACT_EXPERIENCES: str = "extract_experiences"
    EXTRACT_SKILLS: str = "extract_skills"
    EXTRACT_EDUCATION: str = "extract_education"
    EXTRACT_CERTIFICATE: str = "extract_certificate"
    SCORE: str = "score"
    SUMMARY_REASON = "summary_reason"
    
    APP_TITLE: str = "Agent Recruitment Core Application"


class MinioSettings:

    MINIO_ENDPOINT: str = os.getenv('MINIO_ENDPOINT')
    MINIO_ACCESS_KEY: str = os.getenv('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY: str = os.getenv('MINIO_SECRET_KEY')
    MINIO_BUCKET_NAME: str = os.getenv('MINIO_BUCKET_NAME')


class OpenAISettings:

    MODEL: str = "gpt-4o"
    LLM_API_KEY: str = os.getenv("LLM_API_KEY")

    SYSTEM_ROLE: str = "assistant"
    SYSTEM_CONTENT_FOR_PARAGRAPH_CORRECTION_PROMPT: str = "You are a helpful assistant specializing in spelling and grammar correction."
    SYSTEM_CONTENT_FOR_EXTRACTION: str = "You are an assistant that extracts candidate information from their CV/resume."
    SYSTEM_CONTENT_FOR_EVALUATION: str = "You are a strict HR assistant who evaluates job candidates on a scale from 0 to 100, based on the candidate’s information and the job they are applying for."


class PostgresSettings:

    DATABASE_NAME: str = os.getenv('POSTGRES_DB', "recruitment")
    DATABASE_USER: str = os.getenv('POSTGRES_USER', "postgres")
    DATABASE_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', "recruitment")
    DATABASE_HOST: str = os.getenv('POSTGRES_HOST', "127.0.0.1")
    DATABASE_PORT: str = os.getenv('POSTGRES_PORT', "5432")

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql+psycopg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

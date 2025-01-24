import logging

from minio import Minio
from minio.error import S3Error

from app.core.config import settings

logger = logging.getLogger(__name__)


class MinioForAgentRecruiment:

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        secure=False,
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.bucket_name = bucket_name

        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    def upload_file(self, file_path: str, object_name: str):
        try:
            self.client.fput_object(self.bucket_name, object_name, file_path)
        except S3Error as e:
            logger.error("Error when upload file to Minio", e)

    def download_file(self, file_path: str, object_name: str):
        try:
            self.client.fget_object(self.bucket_name, object_name, file_path)
        except S3Error as e:
            logger.error("Error when upload file to Minio", e)

    def delete_file(self, object_name: str):
        try:
            self.client.remove_object(self.bucket_name, object_name)
        except S3Error as e:
            logger.error("Error when delete file in Minio", e)


minio_agent_recruiment = MinioForAgentRecruiment(
    settings.MINIO_ENDPOINT, 
    settings.MINIO_ACCESS_KEY,
    settings.MINIO_SECRET_KEY,
    settings.MINIO_BUCKET_NAME
)
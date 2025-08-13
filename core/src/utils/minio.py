import logging
import os

from minio import Minio
from minio.error import S3Error

from src.settings.settings import MinioSettings


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

    def download_file(self, folder_prefix: str, download_path: str):
        try:
            os.makedirs(os.path.dirname(download_path), exist_ok=True)
            
            objects = self.client.list_objects(self.bucket_name, prefix=folder_prefix, recursive=True)
            
            for object in objects:
                self.client.fget_object(self.bucket_name, object.object_name, download_path)
                logger.info(f"Downloaded: {object.object_name} -> {download_path}")

        except S3Error as err:
            logger.info(f"Error downloading: {err}")


minio_agent_recruiment = MinioForAgentRecruiment(
    MinioSettings.MINIO_ENDPOINT, 
    MinioSettings.MINIO_ACCESS_KEY,
    MinioSettings.MINIO_SECRET_KEY,
    MinioSettings.MINIO_BUCKET_NAME
)

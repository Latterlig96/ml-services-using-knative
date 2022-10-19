from minio import Minio
from minio.error import S3Error
import os
from typing import Any
import io
from loguru import logger


class MinioClient:

    def __init__(self,
                 endpoint: str,
                 access_key: str,
                 secret_key: str):
        self._client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )

    @classmethod
    def build_from_env(cls):
        endpoint = os.getenv("MLFLOW_S3_ENDPOINT_URL", "localhost")
        access_key = os.getenv("AWS_ACCESS_KEY_ID", "admin")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY", "admin123")
        return MinioClient(endpoint.replace("http://", ""), access_key, secret_key)

    def _bucket_exists(self, bucket_name: str) -> bool:
        return True if self._client.bucket_exists(bucket_name) else False

    def create_bucket(self,
                      bucket_name: str,
                      **kwargs) -> bool:
        if self._bucket_exists(bucket_name):
            logger.info(
                f"Bucket name {bucket_name} already exists, creating bucket operation skipped")
            return True
        if "_" in bucket_name:
            logger.info(
                "Replacing all '_' characters with '-' to avoid unappropriate bucket creation")
            bucket_name = bucket_name.replace("_", "-")
        self._client.make_bucket(bucket_name, **kwargs)
        return True

    def get_object_from_bucket(self, bucket_name: str, object_name: str):
        try:
            response = self._client.get_object(bucket_name, object_name)
            return response.read()
        except S3Error as e:
            logger.exception(e)

    def put_object_to_bucket(self, bucket_name: str, object_name: str, object_data: Any):
        if isinstance(object_data, str):
            try:
                with open(object_data, 'rb') as f:
                    object_data = io.BytesIO(f.read())
            except FileNotFoundError as e:
                raise FileNotFoundError(e)
        try:
            if isinstance(object_data, io.BytesIO):
                pass
            else:
                object_data = io.BytesIO(object_data)
            self._client.put_object(bucket_name=bucket_name,
                                    object_name=object_name,
                                    data=object_data,
                                    length=object_data.getbuffer().nbytes)
        except (TypeError, AttributeError) as e:
            logger.exception(e)

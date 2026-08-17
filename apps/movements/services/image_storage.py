from __future__ import annotations

import os
import uuid
from typing import Any, BinaryIO, Union

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class ImageStorageError(RuntimeError):
    """Raised when the image upload to S3 fails."""


class S3ImageStorageService:
    def __init__(self, bucket_name: str | None = None, region_name: str | None = None, client: Any | None = None):
        self.bucket_name = bucket_name or os.environ.get("AWS_IMPORT_BUCKET_NAME", "finance-imports-dev")
        self.region_name = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self.client = client or boto3.client("s3", region_name=self.region_name)

    def upload_file(self, file_obj: Union[BinaryIO, bytes], filename: str | None = None, content_type: str = "application/octet-stream") -> str:
        payload = file_obj.read() if hasattr(file_obj, "read") else file_obj
        if not payload:
            raise ImageStorageError("Import image is empty")

        safe_name = filename or f"{uuid.uuid4()}.bin"
        key = f"imports/{uuid.uuid4()}/{safe_name}"

        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=payload,
                ContentType=content_type,
                ACL="private",
            )
        except (BotoCoreError, ClientError, ValueError) as exc:
            raise ImageStorageError("Failed to upload import image to S3") from exc

        return key

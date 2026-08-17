from __future__ import annotations

import os
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class TextractServiceError(RuntimeError):
    """Raised when the OCR provider cannot process the image."""


class TextractClient:
    def __init__(self, region_name: str | None = None, client: Any | None = None):
        self.region_name = region_name or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self.client = client or boto3.client("textract", region_name=self.region_name)

    def extract_movement_candidates(self, image_bytes: bytes) -> list[dict[str, Any]]:
        if not image_bytes:
            return []

        try:
            response = self.client.detect_document_text(Document={"Bytes": image_bytes})
        except (BotoCoreError, ClientError, ValueError) as exc:
            raise TextractServiceError("OCR service unavailable: image could not be processed") from exc

        lines = [
            block.get("Text", "")
            for block in response.get("Blocks", [])
            if block.get("BlockType") == "LINE" and block.get("Text")
        ]

        if not lines:
            return []

        description = " ".join(lines[:3]).strip()
        return [{
            "description": description or "Imported movement",
            "date": None,
            "amount": None,
            "currency": None,
            "source_confidence": 0.6,
        }]

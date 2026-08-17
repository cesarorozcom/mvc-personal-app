from __future__ import annotations

import logging
from decimal import Decimal
from typing import Any

from apps.movements.services.duplicate_guard import build_duplicate_signature, is_duplicate_proposal
from apps.movements.services.proposal_validation import validate_proposal

logger = logging.getLogger(__name__)


class ImageImportPipeline:
    def __init__(self, storage_service: Any | None = None, ocr_client: Any | None = None):
        self.storage_service = storage_service
        self.ocr_client = ocr_client

    def start_import(self, image_bytes: bytes, filename: str | None = None, default_currency: str | None = None) -> dict[str, Any]:
        if not image_bytes:
            raise ValueError("Image bytes are required")

        key = None
        if self.storage_service is not None:
            key = self.storage_service.upload_file(image_bytes, filename=filename, content_type="image/jpeg")

        proposals = []
        if self.ocr_client is not None:
            raw_candidates = self.ocr_client.extract_movement_candidates(image_bytes)
            for candidate in raw_candidates:
                try:
                    proposal = validate_proposal(candidate, default_currency=default_currency)
                    proposal["source_confidence"] = candidate.get("source_confidence", 0.0)
                    proposal["requires_review"] = bool(proposal.get("requires_review", False)) or bool(candidate.get("source_confidence", 0.0) < 0.85)
                    proposals.append(proposal)
                except ValueError as exc:
                    logger.warning("Ignoring invalid OCR proposal: %s", exc)

        if not proposals:
            logger.info("OCR produced no proposals for import; manual review required")

        return {
            "image_key": key,
            "proposals": proposals,
            "status": "review",
        }

    def mark_duplicates(self, proposals: list[dict[str, Any]], existing_history: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for proposal in proposals:
            duplicate = is_duplicate_proposal(proposal, existing_history)
            proposal["is_duplicate"] = duplicate
            proposal["duplicate_reason"] = "duplicate exact match with historical transaction" if duplicate else ""
        return proposals

    def confirm_valid_proposals(self, proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
        confirmed = []
        for proposal in proposals:
            if proposal.get("is_duplicate"):
                continue
            if proposal.get("requires_review") and not proposal.get("confirmed"):
                continue
            if proposal.get("discarded"):
                continue
            confirmed.append({
                "date": proposal["date"],
                "description": proposal["description"],
                "amount": Decimal(str(proposal["amount"])),
                "currency": proposal["currency"],
            })
        return confirmed

    def build_duplicate_signature(self, proposal: dict[str, Any]) -> str:
        return build_duplicate_signature(proposal)

from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation


class ProposalValidationError(ValueError):
    """Raised when a movement proposal does not conform to the expected schema."""


def normalize_description(value: str | None) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def coerce_date(value: str | None) -> str:
    if value in (None, ""):
        raise ProposalValidationError("date is required")

    try:
        if isinstance(value, str):
            date_value = datetime.strptime(value, "%Y-%m-%d")
            return date_value.strftime("%Y-%m-%d")
        return value.isoformat()
    except (TypeError, ValueError) as exc:
        raise ProposalValidationError("date must be in ISO 8601 format YYYY-MM-DD") from exc


def coerce_amount(value: str | Decimal | int | float | None) -> Decimal:
    if value in (None, ""):
        raise ProposalValidationError("amount is required")

    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ProposalValidationError("amount must be numeric") from exc

    return amount.quantize(Decimal("0.01"))


def validate_proposal(payload: dict, default_currency: str | None = None) -> dict:
    normalized = {
        "date": payload.get("date"),
        "description": normalize_description(payload.get("description")),
        "amount": payload.get("amount"),
        "currency": str(payload.get("currency") or "").strip().upper(),
    }

    if not normalized["description"]:
        raise ProposalValidationError("description is required")

    normalized["date"] = coerce_date(normalized["date"])
    normalized["amount"] = float(coerce_amount(normalized["amount"]))

    if not normalized["currency"]:
        if default_currency:
            normalized["currency"] = str(default_currency).strip().upper()
            normalized["requires_review"] = True
        else:
            raise ProposalValidationError("currency is required")
    else:
        normalized["requires_review"] = False

    if normalized["currency"] and len(normalized["currency"]) != 3:
        raise ProposalValidationError("currency must be a valid ISO 4217 code")

    return normalized

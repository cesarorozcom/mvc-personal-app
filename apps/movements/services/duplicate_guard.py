from __future__ import annotations

from decimal import Decimal


def canonicalize_text(value: str | None) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().lower().split())


def build_duplicate_signature(payload: dict) -> str:
    date_value = str(payload.get("date") or "")
    description = canonicalize_text(payload.get("description"))
    amount = Decimal(str(payload.get("amount") or "0")).quantize(Decimal("0.01"))
    currency = str(payload.get("currency") or "").upper()
    return f"{date_value}|{description}|{amount}|{currency}"


def is_duplicate_proposal(candidate: dict, existing_entries: list[dict]) -> bool:
    candidate_signature = build_duplicate_signature(candidate)
    return any(build_duplicate_signature(existing) == candidate_signature for existing in existing_entries)

import pytest

from apps.movements.services.proposal_validation import ProposalValidationError, validate_proposal


def test_validate_proposal_accepts_valid_payload():
    payload = {
        "date": "2026-08-15",
        "description": "  Rent payment  ",
        "amount": "-125.50",
        "currency": "usd",
    }

    validated = validate_proposal(payload)

    assert validated["date"] == "2026-08-15"
    assert validated["description"] == "Rent payment"
    assert validated["amount"] == -125.5
    assert validated["currency"] == "USD"
    assert validated["requires_review"] is False


def test_validate_proposal_uses_default_currency_when_missing():
    payload = {
        "date": "2026-08-15",
        "description": "Transfer",
        "amount": "750.00",
        "currency": "",
    }

    validated = validate_proposal(payload, default_currency="cop")

    assert validated["currency"] == "COP"
    assert validated["requires_review"] is True


def test_validate_proposal_raises_for_missing_description():
    payload = {
        "date": "2026-08-15",
        "description": "   ",
        "amount": "15.00",
        "currency": "ARS",
    }

    with pytest.raises(ProposalValidationError, match="description is required"):
        validate_proposal(payload)


def test_validate_proposal_raises_for_invalid_date():
    payload = {
        "date": "15/08/2026",
        "description": "Coffee",
        "amount": "25.00",
        "currency": "ARS",
    }

    with pytest.raises(ProposalValidationError, match="date must be in ISO 8601"):
        validate_proposal(payload)

from apps.movements.services.duplicate_guard import build_duplicate_signature, is_duplicate_proposal


def test_build_duplicate_signature_normalizes_fields():
    payload = {
        "date": "2026-08-15",
        "description": "  Groceries  Purchase  ",
        "amount": "123.40",
        "currency": "ars",
    }

    signature = build_duplicate_signature(payload)

    assert signature == "2026-08-15|groceries purchase|123.40|ARS"


def test_is_duplicate_proposal_detects_exact_duplicate():
    candidate = {
        "date": "2026-08-15",
        "description": "Groceries Purchase",
        "amount": "123.40",
        "currency": "ARS",
    }
    history = [{
        "date": "2026-08-15",
        "description": " groceries purchase ",
        "amount": "123.40",
        "currency": "ars",
    }]

    assert is_duplicate_proposal(candidate, history) is True


def test_is_duplicate_proposal_returns_false_for_different_amount():
    candidate = {
        "date": "2026-08-15",
        "description": "Groceries Purchase",
        "amount": "123.40",
        "currency": "ARS",
    }
    history = [{
        "date": "2026-08-15",
        "description": "Groceries Purchase",
        "amount": "123.41",
        "currency": "ARS",
    }]

    assert is_duplicate_proposal(candidate, history) is False

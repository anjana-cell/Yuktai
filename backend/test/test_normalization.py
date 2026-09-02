from decimal import Decimal

from app.services.normalization_service import (
    normalize_text,
    normalize_amount,
)


def test_normalize_text():
    assert normalize_text("  Rahul   Kumar ") == "rahul kumar"
    assert normalize_text("RAHUL KUMAR") == "rahul kumar"


def test_normalize_amount():
    assert normalize_amount("₹2,500") == Decimal("2500.00")
    assert normalize_amount("2500") == Decimal("2500.00")
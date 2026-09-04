from app.services.matching_service import (
    amount_similarity,
    customer_similarity,
    date_similarity,
    currency_similarity,
    calculate_confidence,
    confidence_level,
)
def test_exact_amount():
    assert amount_similarity(1999, 1999) == 1.0


def test_amount_difference():
    score = amount_similarity(1999, 1990)

    assert 0 < score < 1


def test_exact_customer():
    assert customer_similarity(
        "Rahul Sharma",
        "Rahul Sharma"
    ) == 1.0


def test_fuzzy_customer():
    score = customer_similarity(
        "Rahul Sharma",
        "Rahul S"
    )

    assert 0 < score < 1


def test_different_customer():
    score = customer_similarity(
        "Rahul Sharma",
        "Ananya Rao"
    )

    assert score < 0.8


def test_same_date():
    assert date_similarity(
        "2026-08-20",
        "2026-08-20"
    ) == 1.0


def test_one_day_difference():
    score = date_similarity(
        "2026-08-20",
        "2026-08-21"
    )

    assert 0 < score < 1


def test_same_currency():
    assert currency_similarity(
        "INR",
        "INR"
    ) == 1.0


def test_different_currency():
    assert currency_similarity(
        "INR",
        "USD"
    ) == 0.0


def test_high_confidence():
    score = calculate_confidence(
        1.0,
        1.0,
        1.0,
        1.0
    )

    assert score == 1.0
    assert confidence_level(score) == "HIGH"


def test_medium_confidence():
    level = confidence_level(0.80)

    assert level == "MEDIUM"


def test_low_confidence():
    level = confidence_level(0.50)

    assert level == "LOW"
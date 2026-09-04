from app.services.matching_service import find_best_candidate


def test_missing_order_id_payment_matches_using_all_similarity_fields():
    order = {
        "order_id": "ORD-1",
        "amount": 1999,
        "customer_name": "Rahul Sharma",
        "order_date": "2026-08-20",
        "currency": "INR",
    }
    payments = [{
        "payment_id": "PAY-1",
        "amount": 1999,
        "customer_name": "Rahul Sharma",
        "payment_date": "2026-08-20",
        "currency": "INR",
    }]

    result = find_best_candidate(order, payments)

    assert result["payment_id"] == "PAY-1"
    assert result["amount_score"] == 1.0
    assert result["customer_score"] == 1.0
    assert result["date_score"] == 1.0
    assert result["currency_score"] == 1.0
    assert result["confidence_score"] == 1.0


def test_slightly_different_customer_name_is_best_candidate():
    order = {
        "order_id": "ORD-2",
        "amount": 2499,
        "customer_name": "Ananya Rao",
        "order_date": "2026-08-21",
        "currency": "INR",
    }
    payments = [
        {
            "payment_id": "PAY-FUZZY",
            "amount": 2499,
            "customer_name": "Ananya Raoa",
            "payment_date": "2026-08-21",
            "currency": "INR",
        },
        {
            "payment_id": "PAY-WEAK",
            "amount": 2499,
            "customer_name": "Different Customer",
            "payment_date": "2026-08-21",
            "currency": "INR",
        },
    ]

    result = find_best_candidate(order, payments)

    assert result["payment_id"] == "PAY-FUZZY"
    assert result["confidence_score"] > 0.7


def test_one_day_date_difference_is_best_candidate():
    order = {
        "order_id": "ORD-3",
        "amount": 2999,
        "customer_name": "Meera Nair",
        "order_date": "2026-08-22",
        "currency": "INR",
    }
    payments = [{
        "payment_id": "PAY-DATE",
        "amount": 2999,
        "customer_name": "Meera Nair",
        "payment_date": "2026-08-23",
        "currency": "INR",
    }]

    result = find_best_candidate(order, payments)

    assert result["payment_id"] == "PAY-DATE"
    assert result["confidence_score"] > 0.9


def test_unrelated_payment_is_not_selected_over_stronger_candidate():
    order = {
        "order_id": "ORD-4",
        "amount": 3999,
        "customer_name": "Priya Menon",
        "order_date": "2026-08-24",
        "currency": "INR",
    }
    payments = [
        {
            "payment_id": "PAY-STRONG",
            "amount": 3999,
            "customer_name": "Priya Menon",
            "payment_date": "2026-08-24",
            "currency": "INR",
        },
        {
            "payment_id": "PAY-UNRELATED",
            "amount": 999,
            "customer_name": "Unrelated Customer",
            "payment_date": "2026-08-24",
            "currency": "INR",
        },
    ]

    result = find_best_candidate(order, payments)

    assert result["payment_id"] == "PAY-STRONG"
    assert result["confidence_score"] > 0.9

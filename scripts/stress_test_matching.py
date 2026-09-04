from app.services.matching_service import find_best_candidate


cases = [
    {
        "order": {
            "order_id": "ORD-EXACT",
            "amount": 1999,
            "customer_name": "Rahul Sharma",
            "order_date": "2026-08-20",
            "currency": "INR",
        },
        "payments": [{
            "payment_id": "PAY-EXACT",
            "order_id": "ORD-EXACT",
            "amount": 1999,
            "customer_name": "Rahul Sharma",
            "payment_date": "2026-08-20",
            "currency": "INR",
        }],
        "expected_payment_id": "PAY-EXACT",
    },
    {
        "order": {
            "order_id": "ORD-MISSING-ID",
            "amount": 2499,
            "customer_name": "Ananya Rao",
            "order_date": "2026-08-21",
            "currency": "INR",
        },
        "payments": [{
            "payment_id": "PAY-MISSING-ID",
            "order_id": None,
            "amount": 2499,
            "customer_name": "Ananya Rao",
            "payment_date": "2026-08-21",
            "currency": "INR",
        }],
        "expected_payment_id": "PAY-MISSING-ID",
    },
    {
        "order": {
            "order_id": "ORD-FUZZY",
            "amount": 2999,
            "customer_name": "Meera Nair",
            "order_date": "2026-08-22",
            "currency": "INR",
        },
        "payments": [{
            "payment_id": "PAY-FUZZY",
            "order_id": None,
            "amount": 2999,
            "customer_name": "Meera Nairr",
            "payment_date": "2026-08-23",
            "currency": "INR",
        }],
        "expected_payment_id": "PAY-FUZZY",
    },
    {
        "order": {
            "order_id": "ORD-MULTIPLE",
            "amount": 3999,
            "customer_name": "Priya Menon",
            "order_date": "2026-08-24",
            "currency": "INR",
        },
        "payments": [
            {
                "payment_id": "PAY-CORRECT",
                "order_id": None,
                "amount": 3999,
                "customer_name": "Priya Menon",
                "payment_date": "2026-08-24",
                "currency": "INR",
            },
            {
                "payment_id": "PAY-SIMILAR-AMOUNT",
                "order_id": None,
                "amount": 3999,
                "customer_name": "Karan Patel",
                "payment_date": "2026-08-27",
                "currency": "INR",
            },
        ],
        "expected_payment_id": "PAY-CORRECT",
    },
    {
        "order": {
            "order_id": "ORD-NONE",
            "amount": 4999,
            "customer_name": "Vikram Singh",
            "order_date": "2026-08-25",
            "currency": "INR",
        },
        "payments": [{
            "payment_id": "PAY-OTHER-ORDER",
            "order_id": "ORD-DIFFERENT",
            "amount": 4999,
            "customer_name": "Vikram Singh",
            "payment_date": "2026-08-25",
            "currency": "INR",
        }],
        "expected_payment_id": None,
    },
]


correct_cases = 0

for case in cases:
    order = case["order"]
    expected_payment_id = case["expected_payment_id"]
    prediction = find_best_candidate(order, case["payments"])
    predicted_payment_id = (
        prediction["payment_id"]
        if prediction is not None
        else None
    )
    confidence = (
        prediction["confidence_score"]
        if prediction is not None
        else None
    )
    confidence_level = (
        prediction["confidence_level"]
        if prediction is not None
        else None
    )
    is_correct = predicted_payment_id == expected_payment_id

    if is_correct:
        correct_cases += 1

    print(f"order_id: {order['order_id']}")
    print(f"expected payment_id: {expected_payment_id}")
    print(f"predicted payment_id: {predicted_payment_id}")
    print(f"confidence: {confidence}")
    print(f"confidence level: {confidence_level}")
    print(f"correct: {is_correct}")
    print()


total_cases = len(cases)
accuracy = correct_cases / total_cases if total_cases else 0.0

print(f"total cases: {total_cases}")
print(f"correct cases: {correct_cases}")
print(f"accuracy: {accuracy:.2%}")

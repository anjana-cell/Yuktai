from rapidfuzz.fuzz import ratio
from datetime import datetime
def amount_similarity(order_amount, payment_amount):
    if order_amount is None or payment_amount is None:
        return 0.0

    if order_amount == 0:
        return 1.0 if payment_amount == 0 else 0.0

    difference = abs(order_amount - payment_amount)

    score = 1 - (difference / abs(order_amount))

    return max(0.0, min(1.0, score))

def customer_similarity(order_customer, payment_customer):
    if not order_customer or not payment_customer:
        return 0.0

    order_customer = str(order_customer).strip().lower()
    payment_customer = str(payment_customer).strip().lower()

    return ratio(order_customer, payment_customer) / 100

def date_similarity(order_date, payment_date):
    if not order_date or not payment_date:
        return 0.0

    try:
        if isinstance(order_date, str):
            order_date = datetime.fromisoformat(order_date)

        if isinstance(payment_date, str):
            payment_date = datetime.fromisoformat(payment_date)

        difference = abs((order_date - payment_date).days)

        score = 1 - (difference / 7)

        return max(0.0, min(1.0, score))

    except (ValueError, TypeError):
        return 0.0
def currency_similarity(order_currency, payment_currency):
    if not order_currency or not payment_currency:
        return 0.0

    order_currency = str(order_currency).strip().upper()
    payment_currency = str(payment_currency).strip().upper()

    return 1.0 if order_currency == payment_currency else 0.0
def calculate_confidence(
    amount_score,
    customer_score,
    date_score,
    currency_score
):
    confidence = (
        0.40 * amount_score
        + 0.30 * customer_score
        + 0.20 * date_score
        + 0.10 * currency_score
    )

    return round(confidence, 4)
def confidence_level(confidence):
    if confidence >= 0.90:
        return "HIGH"

    if confidence >= 0.70:
        return "MEDIUM"

    return "LOW"
def score_candidate(order, payment):
    amount_score = amount_similarity(
        order.get("amount"),
        payment.get("amount")
    )

    customer_score = customer_similarity(
        order.get("customer_name"),
        payment.get("customer_name")
    )

    date_score = date_similarity(
        order.get("order_date"),
        payment.get("payment_date")
    )

    currency_score = currency_similarity(
        order.get("currency"),
        payment.get("currency")
    )

    confidence = calculate_confidence(
        amount_score,
        customer_score,
        date_score,
        currency_score
    )

    return {
        "order_id": order.get("order_id"),
        "payment_id": payment.get("payment_id"),
        "amount_score": amount_score,
        "customer_score": customer_score,
        "date_score": date_score,
        "currency_score": currency_score,
        "confidence_score": confidence,
        "confidence_level": confidence_level(confidence)
    }
def generate_candidates(order, payments, date_window=7):
    candidates = []

    for payment in payments:

        if payment.get("order_id") and payment.get("order_id") != order.get("order_id"):
            continue

        if (
            order.get("currency")
            and payment.get("currency")
            and order["currency"].upper() != payment["currency"].upper()
        ):
            continue

        if (
            order.get("order_date")
            and payment.get("payment_date")
        ):
            try:
                order_date = datetime.fromisoformat(
                    str(order["order_date"])
                )
                payment_date = datetime.fromisoformat(
                    str(payment["payment_date"])
                )

                difference = abs(
                    (order_date - payment_date).days
                )

                if difference > date_window:
                    continue

            except (ValueError, TypeError):
                pass

        candidates.append(payment)

    return candidates
def find_best_candidate(order, payments):
    candidates = generate_candidates(order, payments)

    if not candidates:
        return None

    scored_candidates = [
        score_candidate(order, payment)
        for payment in candidates
    ]

    scored_candidates.sort(
        key=lambda x: x["confidence_score"],
        reverse=True
    )

    best = scored_candidates[0]

    if len(scored_candidates) > 1:
        second_best = scored_candidates[1]

        best["second_best_score"] = second_best["confidence_score"]

        best["confidence_margin"] = round(
            best["confidence_score"]
            - second_best["confidence_score"],
            4
        )
    else:
        best["second_best_score"] = None
        best["confidence_margin"] = None

    return best
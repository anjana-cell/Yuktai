import pandas as pd

from app.services.matching_service import find_best_candidate


orders = pd.read_csv("data/raw/orders.csv")
payments = pd.read_csv("data/raw/payments.csv")

orders_records = orders.to_dict("records")
payment_records = payments.to_dict("records")


print("===== CANDIDATE MATCHING TEST =====")

for order in orders_records[:10]:

    result = find_best_candidate(
        order,
        payment_records
    )

    print("\nOrder:", order["order_id"])

    if result is None:
        print("No candidate found")
        continue

    print("Best Payment:", result["payment_id"])
    print("Confidence:", result["confidence_score"])
    print("Level:", result["confidence_level"])
    print("Amount Score:", result["amount_score"])
    print("Customer Score:", result["customer_score"])
    print("Date Score:", result["date_score"])
    print("Currency Score:", result["currency_score"])
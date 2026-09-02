from pathlib import Path

import pandas as pd

from backend.app.services.reconcilation_service import reconcile


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"


orders = pd.read_csv(RAW_DIR / "orders.csv")
payments = pd.read_csv(RAW_DIR / "payments.csv")
settlements = pd.read_csv(RAW_DIR / "settlements.csv")


result = reconcile(
    orders,
    payments,
    settlements
)


print("\n===== RECONCILIATION RESULTS =====\n")

print(
    result[
        [
            "order_id",
            "payment_id",
            "settlement_id",
            "amount_order",
            "amount_payment",
            "settled_amount",
            "fee_amount",
            "status",
        ]
    ].head(20).to_string(index=False)
)


print("\n===== STATUS DISTRIBUTION =====\n")

print(result["status"].value_counts())
import pandas as pd

from .normalization_service import (
    normalize_orders,
    normalize_payments,
    normalize_settlements,
)


def classify_transaction(row):
    if pd.isna(row["payment_id"]):
        return "missing_payment"

    if str(row["payment_id"]).startswith("pay_unmatched_"):
        return "unmatched_transaction"

    if str(row["payment_id"]).endswith("_dup"):
        return "duplicate_payment"

    if pd.isna(row["settlement_id"]):
        return "missing_settlement"

    if row["amount_order"] != row["amount_payment"]:
        return "amount_mismatch"

    if row["settlement_date"] - row["order_date"] > pd.Timedelta(days=1):
        return "date_variation"

    if row["customer_name_order"] != row["customer_name_payment"]:
        return "customer_variation"

    if row["fee_amount"] > 0:
        return "fee_deduction"

    if row["settled_amount"] == row["amount_payment"] / 2:
        return "partial_settlement"

    if row["settled_amount"] < row["amount_payment"]:
        return "amount_mismatch"

    return "exact_match"


def reconcile(orders, payments, settlements):

    orders = normalize_orders(orders)
    payments = normalize_payments(payments)
    settlements = normalize_settlements(settlements)

    # Orders → Payments
    result = orders.merge(
        payments,
        on="order_id",
        how="left",
        suffixes=("_order", "_payment")
    )

    # Payments → Settlements
    result = result.merge(
        settlements,
        on="payment_id",
        how="left"
    )

    result["status"] = result.apply(
        classify_transaction,
        axis=1
    )

    return result
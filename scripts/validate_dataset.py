from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
GROUND_TRUTH_DIR = BASE_DIR / "data" / "ground_truth"


orders = pd.read_csv(RAW_DIR / "orders.csv")
payments = pd.read_csv(RAW_DIR / "payments.csv")
settlements = pd.read_csv(RAW_DIR / "settlements.csv")
truth = pd.read_csv(
    GROUND_TRUTH_DIR / "reconciliation_truth.csv"
)


print("===== DATASET VALIDATION =====")
print()

print("Orders:", len(orders))
print("Payments:", len(payments))
print("Settlements:", len(settlements))
print("Ground Truth:", len(truth))

print()

print("Missing order IDs:")
print(orders["order_id"].isna().sum())

print("Missing payment IDs:")
print(payments["payment_id"].isna().sum())

print("Missing settlement IDs:")
print(settlements["settlement_id"].isna().sum())

print()

print("Duplicate order IDs:")
print(orders["order_id"].duplicated().sum())

print("Duplicate payment IDs:")
print(payments["payment_id"].duplicated().sum())

print("Duplicate settlement IDs:")
print(settlements["settlement_id"].duplicated().sum())

print()

print("Scenario distribution:")
print(truth["scenario"].value_counts())

print()
print("===== VALIDATION COMPLETE =====")
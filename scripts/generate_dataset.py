import random
from datetime import timedelta
from pathlib import Path

import pandas as pd
from faker import Faker


fake = Faker()
random.seed(42)
Faker.seed(42)


# -----------------------------
# Configuration
# -----------------------------

NUM_TRANSACTIONS = 500

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
GROUND_TRUTH_DIR = BASE_DIR / "data" / "ground_truth"

RAW_DIR.mkdir(parents=True, exist_ok=True)
GROUND_TRUTH_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Scenario distribution
# -----------------------------

SCENARIOS = [
    ("exact_match", 300),
    ("date_variation", 40),
    ("customer_variation", 30),
    ("fee_deduction", 30),
    ("amount_mismatch", 25),
    ("missing_settlement", 20),
    ("missing_payment", 15),
    ("duplicate_payment", 15),
    ("partial_settlement", 15),
    ("unmatched_transaction", 10),
]


def random_amount():
    return random.choice([
        499,
        799,
        999,
        1299,
        1499,
        1999,
        2499,
        2999,
        3999,
        4999,
        5999,
        9999,
    ])


def random_date():
    return fake.date_between(
        start_date="-30d",
        end_date="today"
    )


def normalize_customer_name(name):
    return " ".join(name.split())


# -----------------------------
# Generate transactions
# -----------------------------

orders = []
payments = []
settlements = []
ground_truth = []


scenario_pool = []

for scenario, count in SCENARIOS:
    scenario_pool.extend([scenario] * count)

random.shuffle(scenario_pool)


for i in range(NUM_TRANSACTIONS):

    order_id = f"ORD{i + 1001}"
    payment_id = f"PAY{i + 5001}"
    settlement_id = f"SET{i + 9001}"

    order_customer_name = normalize_customer_name(fake.name())
    amount = random_amount()

    order_date = pd.Timestamp(random_date()).date()

    # -----------------------------
    # Order
    # -----------------------------

    orders.append({
        "order_id": order_id,
        "customer_name": order_customer_name,
        "amount": amount,
        "currency": "INR",
        "order_date": order_date,
    })

    scenario = scenario_pool[i]

    # -----------------------------
    # Default payment
    # -----------------------------

    payment_amount = amount
    payment_date = order_date
    payment_status = "captured"
    
    payment_customer_name = order_customer_name

    # -----------------------------
    # Default settlement
    # -----------------------------

    settled_amount = amount
    fee_amount = 0
    settlement_date = order_date + timedelta(days=1)
    settlement_status = "settled"

    # -----------------------------
    # Scenario handling
    # -----------------------------

    if scenario == "exact_match":
        pass

    elif scenario == "date_variation":
        settlement_date = order_date + timedelta(days=3)

    elif scenario == "customer_variation":
        payment_customer_name = order_customer_name.upper()
    

    elif scenario == "fee_deduction":
        fee_amount = round(amount * 0.02, 2)
        settled_amount = round(amount - fee_amount, 2)

    elif scenario == "amount_mismatch":
        difference = random.choice([100, 200, 300, 500])
        settled_amount = amount - difference

    elif scenario == "missing_settlement":
        settlement_status = "missing"

    elif scenario == "missing_payment":
        payment_status = "missing"

    elif scenario == "duplicate_payment":
        pass

    elif scenario == "partial_settlement":
        settled_amount = round(amount * 0.5, 2)

    elif scenario == "unmatched_transaction":
        payment_id = f"PAY_UNMATCHED_{i + 1}"

    # -----------------------------
    # Payment
    # -----------------------------

    if payment_status != "missing":
        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "customer_name": payment_customer_name,
            "amount": payment_amount,
            "currency": "INR",
            "status": payment_status,
            "payment_date": payment_date,
        })

    # -----------------------------
    # Settlement
    # -----------------------------

    if settlement_status != "missing":
        settlements.append({
            "settlement_id": settlement_id,
            "payment_id": payment_id,
            "settled_amount": settled_amount,
            "fee_amount": fee_amount,
            "currency": "INR",
            "settlement_date": settlement_date,
            "status": settlement_status,
        })

    # -----------------------------
    # Duplicate payment
    # -----------------------------

    if scenario == "duplicate_payment":
        payments.append({
            "payment_id": f"{payment_id}_DUP",
            "order_id": order_id,
            "amount": payment_amount,
            "currency": "INR",
            "status": "captured",
            "payment_date": payment_date,
        })

    # -----------------------------
    # Ground truth
    # -----------------------------

    expected_difference = round(
        payment_amount - settled_amount,
        2
    )

    ground_truth.append({
        "order_id": order_id,
        "expected_status": scenario,
        "scenario": scenario,
        "expected_payment": payment_amount,
        "expected_settlement": settled_amount
        if settlement_status != "missing"
        else None,
        "expected_difference": expected_difference
        if settlement_status != "missing"
        else None,
    })


# -----------------------------
# Convert to DataFrames
# -----------------------------

orders_df = pd.DataFrame(orders)
payments_df = pd.DataFrame(payments)
settlements_df = pd.DataFrame(settlements)
truth_df = pd.DataFrame(ground_truth)


# -----------------------------
# Save CSV files
# -----------------------------

orders_df.to_csv(
    RAW_DIR / "orders.csv",
    index=False
)

payments_df.to_csv(
    RAW_DIR / "payments.csv",
    index=False
)

settlements_df.to_csv(
    RAW_DIR / "settlements.csv",
    index=False
)

truth_df.to_csv(
    GROUND_TRUTH_DIR / "reconciliation_truth.csv",
    index=False
)


print("Dataset generation complete.")
print()
print(f"Orders:       {len(orders_df)}")
print(f"Payments:     {len(payments_df)}")
print(f"Settlements:  {len(settlements_df)}")
print(f"Ground truth: {len(truth_df)}")
print()
print("Scenario distribution:")
print(truth_df["scenario"].value_counts())
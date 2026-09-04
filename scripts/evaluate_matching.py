import pandas as pd

from app.services.matching_service import find_best_candidate


orders = pd.read_csv("data/raw/orders.csv")
payments = pd.read_csv("data/raw/payments.csv")
ground_truth = pd.read_csv(
    "data/ground_truth/reconciliation_truth.csv"
)


payment_records = payments.to_dict("records")


correct = 0
total = 0

results = []


for _, truth in ground_truth.iterrows():

    order_id = truth["order_id"]

    order_rows = orders[
        orders["order_id"] == order_id
    ]

    if order_rows.empty:
        continue

    order = order_rows.iloc[0].to_dict()

    predicted = find_best_candidate(
        order,
        payment_records
    )

    predicted_payment_id = (
        predicted["payment_id"]
        if predicted is not None
        else None
    )
    expected_payment_id = truth["expected_payment_id"]
    if pd.isna(expected_payment_id):
        expected_payment_id = None

    is_correct = (
        predicted_payment_id == expected_payment_id
    )

    if is_correct:
        correct += 1

    total += 1

    results.append({
        "order_id": order_id,
        "predicted_payment": predicted_payment_id,
        "expected_payment_id": expected_payment_id,
        "confidence": predicted["confidence_score"]
        if predicted is not None
        else None,
        "confidence_level": predicted["confidence_level"]
        if predicted is not None
        else None,
        "correct": is_correct,
        "scenario": truth["scenario"]
    })


results_df = pd.DataFrame(results)
print("\n===== ACCURACY BY SCENARIO =====")

scenario_accuracy = (
    results_df
    .groupby("scenario")["correct"]
    .mean()
    .sort_values(ascending=False)
)

print(scenario_accuracy)
print("\n===== CONFIDENCE LEVEL DISTRIBUTION =====")

print(
    results_df["confidence_level"]
    .value_counts()
)
print("\n===== ACCURACY BY CONFIDENCE LEVEL =====")

confidence_accuracy = (
    results_df
    .groupby("confidence_level")["correct"]
    .mean()
)

print(confidence_accuracy)
print("\n===== MEDIUM CONFIDENCE RECORDS =====")

print(
    results_df[
        results_df["confidence_level"] == "MEDIUM"
    ].to_string(index=False)
)
print("\n===== MEDIUM CONFIDENCE RECORDS =====")

print(
    results_df[
        results_df["confidence_level"] == "MEDIUM"
    ].to_string(index=False)
)


print("===== MATCHING EVALUATION =====")
print(f"Total evaluated: {total}")
print(f"Correct matches: {correct}")

if total > 0:
    accuracy = correct / total
    print(f"Matching accuracy: {accuracy:.2%}")

print("\n===== SAMPLE RESULTS =====")
print(results_df.head(20).to_string(index=False))
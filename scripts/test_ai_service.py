from app.services.ai_service import investigate_exception


exception = {
    "order_id": "ORD1015",
    "payment_id": "PAY5015",
    "exception_type": "partial_settlement",
    "order_amount": 9999,
    "payment_amount": 9999,
    "settlement_amount": 4999.50,
    "difference": 4999.50
}


result = investigate_exception(exception)

print("\nAI Investigation Result")
print("=======================")

print("Finding:")
print(result.finding)

print("\nLikely Cause:")
print(result.likely_cause)

print("\nEvidence:")
for item in result.evidence:
    print("-", item)

print("\nRecommended Action:")
print(result.recommended_action)

print("\nConfidence:")
print(result.confidence)
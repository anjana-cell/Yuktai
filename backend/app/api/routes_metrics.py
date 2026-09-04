from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

from app.services.reconcilation_service import reconcile


router = APIRouter()

RAW_DIR = Path(__file__).resolve().parents[3] / "data" / "raw"
REQUIRED_FILES = ("orders.csv", "payments.csv", "settlements.csv")


@router.get("/metrics")
def get_metrics():
	missing_files = [filename for filename in REQUIRED_FILES if not (RAW_DIR / filename).is_file()]
	if missing_files:
		raise HTTPException(
			status_code=404,
			detail=f"Required CSV file(s) not found: {', '.join(missing_files)}",
		)

	result = reconcile(
		pd.read_csv(RAW_DIR / "orders.csv"),
		pd.read_csv(RAW_DIR / "payments.csv"),
		pd.read_csv(RAW_DIR / "settlements.csv"),
	)

	total_records = len(result)
	matched_records = int((result["status"] == "exact_match").sum())
	exception_records = total_records - matched_records
	match_rate = matched_records / total_records if total_records else 0
	exception_rate = exception_records / total_records if total_records else 0

	return {
		"total_records": total_records,
		"matched_records": matched_records,
		"exception_records": exception_records,
		"match_rate": match_rate,
		"exception_rate": exception_rate,
		"automation_rate": match_rate,
	}

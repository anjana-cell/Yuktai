import json
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

from app.services.reconcilation_service import reconcile


router = APIRouter()

RAW_DIR = Path(__file__).resolve().parents[3] / "data" / "raw"
REQUIRED_FILES = ("orders.csv", "payments.csv", "settlements.csv")


@router.post("/reconcile")
def reconcile_files():
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

	return json.loads(result.to_json(orient="records", date_format="iso"))

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.ai_service import investigate_exception
from app.services.reconcilation_service import reconcile


router = APIRouter()

RAW_DIR = Path(__file__).resolve().parents[3] / "data" / "raw"
RESOLUTIONS_FILE = RAW_DIR.parent / "resolutions.json"
REQUIRED_FILES = ("orders.csv", "payments.csv", "settlements.csv")
EXCEPTION_STATUSES = {
	"amount_mismatch",
	"partial_settlement",
	"missing_settlement",
	"missing_payment",
	"duplicate_payment",
	"unmatched_transaction",
}


class ResolutionRequest(BaseModel):
	decision: Literal["resolved", "rejected", "needs_review"]
	reason: str = Field(..., min_length=1)


def _load_resolutions():
	if not RESOLUTIONS_FILE.exists():
		RESOLUTIONS_FILE.write_text("[]", encoding="utf-8")

	return json.loads(RESOLUTIONS_FILE.read_text(encoding="utf-8"))


def _save_resolutions(resolutions):
	RESOLUTIONS_FILE.write_text(
		json.dumps(resolutions, indent=2),
		encoding="utf-8",
	)


def _load_reconciliation_result():
	missing_files = [filename for filename in REQUIRED_FILES if not (RAW_DIR / filename).is_file()]
	if missing_files:
		raise HTTPException(
			status_code=404,
			detail=f"Required CSV file(s) not found: {', '.join(missing_files)}",
		)

	return reconcile(
		pd.read_csv(RAW_DIR / "orders.csv"),
		pd.read_csv(RAW_DIR / "payments.csv"),
		pd.read_csv(RAW_DIR / "settlements.csv"),
	)


@router.get("/exceptions")
def get_exceptions():
	result = _load_reconciliation_result()
	exceptions = result[result["status"].isin(EXCEPTION_STATUSES)].copy()
	exceptions["amount"] = exceptions["amount_order"]
	exceptions["settlement_amount"] = exceptions["settled_amount"]
	exceptions["difference"] = exceptions["amount_payment"] - exceptions["settled_amount"]

	return json.loads(
		exceptions[
			[
				"order_id",
				"payment_id",
				"status",
				"amount",
				"settlement_amount",
				"difference",
			]
		].to_json(orient="records")
	)


@router.post("/exceptions/{order_id}/investigate")
def investigate_order_exception(order_id: str):
	result = _load_reconciliation_result()
	matching_rows = result[
		result["order_id"].astype(str).str.lower() == order_id.strip().lower()
	]
	if matching_rows.empty:
		raise HTTPException(status_code=404, detail="Order not found")

	exception_rows = matching_rows[matching_rows["status"].isin(EXCEPTION_STATUSES)]
	if exception_rows.empty:
		raise HTTPException(
			status_code=400,
			detail="The order does not have an exception requiring investigation",
		)

	row = exception_rows.iloc[0]
	exception_data = {
		"order_id": row["order_id"],
		"payment_id": None if pd.isna(row["payment_id"]) else row["payment_id"],
		"exception_type": row["status"],
		"order_amount": None if pd.isna(row["amount_order"]) else row["amount_order"],
		"payment_amount": None if pd.isna(row["amount_payment"]) else row["amount_payment"],
		"settlement_amount": None if pd.isna(row["settled_amount"]) else row["settled_amount"],
		"difference": (
			None
			if pd.isna(row["amount_payment"]) or pd.isna(row["settled_amount"])
			else row["amount_payment"] - row["settled_amount"]
		),
	}

	try:
		return investigate_exception(exception_data)
	except Exception as error:
		raise HTTPException(
			status_code=500,
			detail=f"AI investigation failed: {error}",
		) from error


@router.post("/exceptions/{order_id}/resolve")
def resolve_order_exception(order_id: str, resolution: ResolutionRequest):
	result = _load_reconciliation_result()
	matching_rows = result[
		result["order_id"].astype(str).str.lower() == order_id.strip().lower()
	]
	if matching_rows.empty:
		raise HTTPException(status_code=404, detail="Order not found")

	if not matching_rows["status"].isin(EXCEPTION_STATUSES).any():
		raise HTTPException(
			status_code=400,
			detail="The order does not have an exception requiring review",
		)

	reason = resolution.reason.strip()
	if not reason:
		raise HTTPException(status_code=422, detail="reason must be a non-empty string")

	order_id = str(matching_rows.iloc[0]["order_id"])
	saved_resolution = {
		"order_id": order_id,
		"decision": resolution.decision,
		"reason": reason,
		"timestamp": datetime.now(timezone.utc).isoformat(),
	}
	resolutions = _load_resolutions()
	updated = False
	for index, existing in enumerate(resolutions):
		if str(existing.get("order_id", "")).lower() == order_id.lower():
			resolutions[index] = saved_resolution
			updated = True
			break
	if not updated:
		resolutions.append(saved_resolution)

	_save_resolutions(resolutions)
	return saved_resolution


@router.get("/exceptions/{order_id}/audit")
def get_order_exception_audit(order_id: str):
	result = _load_reconciliation_result()
	matching_rows = result[
		result["order_id"].astype(str).str.lower() == order_id.strip().lower()
	]
	if matching_rows.empty:
		raise HTTPException(status_code=404, detail="Order not found")

	resolutions = _load_resolutions()
	return [
		resolution
		for resolution in resolutions
		if str(resolution.get("order_id", "")).lower() == order_id.strip().lower()
	]

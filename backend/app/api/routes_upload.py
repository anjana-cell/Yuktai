from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile


router = APIRouter()

RAW_DIR = Path(__file__).resolve().parents[3] / "data" / "raw"


@router.post("/upload")
async def upload_files(
	orders: UploadFile = File(...),
	payments: UploadFile = File(...),
	settlements: UploadFile = File(...),
):
	uploads = {
		"orders.csv": orders,
		"payments.csv": payments,
		"settlements.csv": settlements,
	}

	for upload in uploads.values():
		if not upload.filename or not upload.filename.lower().endswith(".csv"):
			raise HTTPException(
				status_code=400,
				detail="All uploaded files must have a .csv extension",
			)

	RAW_DIR.mkdir(parents=True, exist_ok=True)
	for filename, upload in uploads.items():
		(RAW_DIR / filename).write_bytes(await upload.read())

	return {
		"status": "uploaded",
		"filenames": list(uploads),
	}

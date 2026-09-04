from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_exceptions import router as exceptions_router
from app.api.routes_metrics import router as metrics_router
from app.api.routes_reconciliation import router as reconciliation_router
from app.api.routes_upload import router as upload_router


app = FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:5173"],
	allow_methods=["GET", "POST"],
	allow_headers=["*"],
)
app.include_router(exceptions_router, prefix="/api")
app.include_router(metrics_router, prefix="/api")
app.include_router(reconciliation_router, prefix="/api")
app.include_router(upload_router, prefix="/api")


@app.get("/health")
def health():
	return {"status": "ok"}


@app.get("/")
def root():
	return {"message": "AI Finance Controller"}

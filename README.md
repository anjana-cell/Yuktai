# AI Finance Reconciliation Controller

> AI-assisted reconciliation for orders, payments, and settlements.

## Overview

AI Finance Reconciliation Controller automates financial reconciliation by matching orders, payments, and settlements, detecting discrepancies, investigating exceptions with Google Gemini, and keeping humans in control of final decisions.

### Workflow

```text
Orders + Payments + Settlements
              ↓
        Data Normalization
              ↓
       Matching & Reconciliation
              ↓
        Exception Detection
              ↓
       Gemini AI Investigation
              ↓
          Human Review
              ↓
       Resolution + Audit Trail
Key Features
Multi-source order, payment, and settlement reconciliation
Deterministic + fuzzy transaction matching
Confidence-based matching
Automatic exception detection
Gemini-powered exception investigation
Human-in-the-loop resolution
Resolution and audit history
React reconciliation dashboard
REST APIs with FastAPI
Tech Stack

Backend: Python, FastAPI, Pandas, RapidFuzz, Pydantic

AI: Google Gemini, google-genai

Frontend: React, Vite, Axios, Recharts

Data: CSV + JSON persistence

Dataset

Synthetic dataset used for testing:

500 Orders
500 Payments
480 Settlements
500 Ground-truth records

Scenarios include amount mismatches, partial settlements, missing payments, missing settlements, duplicate payments, and other reconciliation variations.

Evaluation

On the controlled synthetic ground-truth dataset:

Records Evaluated: 500
Correct Matches:   500
Accuracy:          100%

This result represents performance on the project's synthetic test dataset and does not imply real-world accuracy.

Run Locally
Backend
python -m venv backend/.venv
Windows
backend\.venv\Scripts\activate
pip install fastapi uvicorn pandas rapidfuzz pydantic python-dotenv python-multipart google-genai
set PYTHONPATH=backend
uvicorn app.main:app --reload
Gemini API Key

Create .env in the project root:

GEMINI_API_KEY=your_gemini_api_key

Never commit .env to GitHub.

Frontend
cd frontend
npm install
npm run dev

Frontend: http://localhost:5173

Backend API: http://127.0.0.1:8000

API Docs: http://127.0.0.1:8000/docs

Core Design Principle

Detect deterministically → Investigate with AI → Decide with humans → Record the decision

Gemini assists with investigation and explanation. The reconciliation engine remains responsible for financial calculations and exception detection, while the final resolution remains with the human reviewer.

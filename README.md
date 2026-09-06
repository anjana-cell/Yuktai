# AI Finance Reconciliation Controller

> **AI-assisted financial reconciliation for orders, payments, and settlements — combining deterministic matching, intelligent exception investigation, and human-in-the-loop decision making.**

## Overview

The **AI Finance Reconciliation Controller** is a financial reconciliation system designed to automate the process of matching **orders, payments, and settlements** across multiple data sources.

Traditional reconciliation systems rely heavily on manual investigation when transactions do not match. This project automates the reconciliation workflow by combining a **deterministic reconciliation engine** with **Google Gemini** for investigating and explaining exceptions.

The system follows a simple principle:

> **Detect deterministically → Investigate with AI → Decide with humans → Record the decision**

The AI does **not** make financial decisions autonomously. Financial calculations and discrepancy detection remain deterministic, while Gemini assists reviewers by analyzing exceptions and providing investigation insights.

---

## Problem Statement

Financial systems often contain inconsistencies between:

* Customer orders
* Payment records
* Settlement records

Common reconciliation problems include:

* Amount mismatches
* Partial settlements
* Missing payments
* Missing settlements
* Duplicate payments
* Transaction/reference variations
* Other transaction-level discrepancies

Manually identifying and investigating these exceptions is time-consuming and error-prone.

This project provides an automated reconciliation pipeline that identifies these inconsistencies and uses AI to assist humans in investigating them.

---

## Solution

The system processes financial records through the following pipeline:

```text
┌─────────────────────────────────────────────┐
│ Orders + Payments + Settlements             │
└──────────────────────┬──────────────────────┘
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
```

### How It Works

1. **Data Ingestion**

   * Loads order, payment, and settlement records from structured CSV/JSON data.

2. **Data Normalization**

   * Standardizes fields and transaction information before comparison.

3. **Transaction Matching**

   * Uses deterministic matching and fuzzy matching to associate related records.
   * Generates confidence scores for potential matches.

4. **Reconciliation**

   * Compares expected and actual financial values.
   * Identifies whether transactions reconcile successfully.

5. **Exception Detection**

   * Automatically categorizes discrepancies such as missing records, amount mismatches, partial settlements, and duplicates.

6. **AI Investigation**

   * Sends relevant exception context to Google Gemini.
   * Gemini analyzes the available information and provides an explanation or investigation summary.

7. **Human Review**

   * A reviewer examines the reconciliation result and AI-generated investigation.
   * The final decision remains under human control.

8. **Resolution & Audit Trail**

   * Stores the reviewer's decision and resolution information for future reference and auditing.

---

# Key Features

### 1. Multi-Source Reconciliation

Reconciles data across:

* Orders
* Payments
* Settlements

### 2. Deterministic + Fuzzy Matching

Uses a combination of:

* Exact transaction/reference matching
* Amount-based matching
* Fuzzy string matching using **RapidFuzz**

This helps handle variations in transaction identifiers and related fields.

### 3. Confidence-Based Matching

Potential matches are assigned confidence scores, allowing the system to distinguish between:

* High-confidence matches
* Possible matches
* Low-confidence matches
* Unmatched records

### 4. Automatic Exception Detection

The reconciliation engine identifies financial inconsistencies such as:

* Amount mismatches
* Partial settlements
* Missing payments
* Missing settlements
* Duplicate payments
* Other reconciliation exceptions

### 5. Gemini-Powered Investigation

Google Gemini is used to investigate detected exceptions and provide contextual explanations to assist the reviewer.

The AI layer is intentionally separated from the core reconciliation logic.

### 6. Human-in-the-Loop Resolution

The system does not automatically finalize financial resolutions.

Instead:

```text
System detects exception
        ↓
AI investigates exception
        ↓
Human reviews evidence
        ↓
Human makes final decision
```

This provides an additional layer of control for financial workflows.

### 7. Resolution & Audit History

Reviewer decisions and resolutions can be recorded to maintain an audit trail of how exceptions were handled.

### 8. Reconciliation Dashboard

A React-based dashboard provides visibility into:

* Reconciliation results
* Exceptions
* Transaction details
* Matching confidence
* Investigation results
* Resolution status

---

# System Architecture

```text
                    ┌──────────────────────┐
                    │   Orders / Payments  │
                    │    / Settlements     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Data Normalization    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Matching Engine       │
                    │                      │
                    │ Exact + Fuzzy Match  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Reconciliation Engine │
                    └──────────┬───────────┘
                               │
                       ┌───────┴────────┐
                       ▼                ▼
                  Reconciled       Exceptions
                                      │
                                      ▼
                           ┌──────────────────┐
                           │ Google Gemini AI │
                           │ Investigation    │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │ Human Reviewer   │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │ Resolution +     │
                           │ Audit Trail      │
                           └──────────────────┘
```

---

# Technology Stack

| Layer             | Technologies                  |
| ----------------- | ----------------------------- |
| Backend           | Python, FastAPI               |
| Data Processing   | Pandas                        |
| Matching          | RapidFuzz                     |
| Validation        | Pydantic                      |
| AI                | Google Gemini, `google-genai` |
| Frontend          | React, Vite                   |
| HTTP Client       | Axios                         |
| Visualization     | Recharts                      |
| Persistence       | CSV + JSON                    |
| API Documentation | FastAPI / OpenAPI             |

---

# Dataset

The project currently uses a **synthetic dataset** designed to simulate common financial reconciliation scenarios.

| Dataset              | Records |
| -------------------- | ------: |
| Orders               |     500 |
| Payments             |     500 |
| Settlements          |     480 |
| Ground-Truth Records |     500 |

### Included Scenarios

The synthetic dataset contains examples of:

* Correctly reconciled transactions
* Amount mismatches
* Partial settlements
* Missing payments
* Missing settlements
* Duplicate payments
* Other transaction-level reconciliation variations

The ground-truth records are used to evaluate the matching and reconciliation engine.

---

# Evaluation

The reconciliation engine was evaluated against the controlled synthetic ground-truth dataset.

### Results

| Metric            |   Result |
| ----------------- | -------: |
| Records Evaluated |  **500** |
| Correct Matches   |  **500** |
| Matching Accuracy | **100%** |

### Important Note

> **The reported 100% accuracy is limited to the project's controlled synthetic test dataset. It should not be interpreted as real-world financial reconciliation accuracy.**

Real-world performance would depend on factors such as:

* Data quality
* Transaction volume
* Identifier consistency
* Matching ambiguity
* Missing or corrupted records
* Financial system integrations
* Domain-specific reconciliation rules

---

# Project Structure

```text
AI-Finance-Reconciliation-Controller/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── ...
│   │
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── data/
│   ├── orders.csv
│   ├── payments.csv
│   ├── settlements.csv
│   └── ...
│
├── .env
├── .gitignore
└── README.md
```

> The exact structure may vary depending on the current implementation.

---

# Getting Started

## Prerequisites

Make sure the following are installed:

* Python 3.x
* Node.js and npm
* Git
* Google Gemini API key

---

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd AI-Finance-Reconciliation-Controller
```

---

# Backend Setup

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv backend/.venv
backend\.venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv backend/.venv
source backend/.venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install fastapi uvicorn pandas rapidfuzz pydantic python-dotenv python-multipart google-genai
```

---

# Configure Gemini

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace `your_gemini_api_key` with your actual API key.

### Security

**Never commit your `.env` file to GitHub.**

Add it to `.gitignore`:

```gitignore
.env
backend/.venv/
__pycache__/
node_modules/
```

---

# Run the Backend

From the project root:

```bash
set PYTHONPATH=backend
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI automatically provides interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

Open another terminal and navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

# API

The backend exposes REST APIs through FastAPI for operations such as:

* Loading reconciliation data
* Running reconciliation
* Retrieving exceptions
* Investigating exceptions with Gemini
* Reviewing and resolving exceptions
* Accessing reconciliation results and history

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# AI Responsibility Boundary

A key design decision in this project is the separation between **financial computation** and **AI reasoning**.

### Deterministic Engine

Responsible for:

* Transaction matching
* Amount comparison
* Reconciliation calculations
* Exception detection
* Confidence scoring

### Gemini AI

Responsible for:

* Investigating detected exceptions
* Explaining possible causes
* Summarizing transaction context
* Assisting the human reviewer

### Human Reviewer

Responsible for:

* Reviewing evidence
* Accepting or rejecting the suggested resolution
* Making the final financial decision

Therefore:

```text
              FINANCIAL TRUTH
                    │
                    ▼
          Deterministic Engine
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
      Reconciled           Exception
                              │
                              ▼
                        Gemini AI
                       Investigation
                              │
                              ▼
                       Human Reviewer
                              │
                              ▼
                     Final Resolution
                              │
                              ▼
                        Audit Trail
```

This architecture prevents the generative AI model from becoming the source of truth for financial calculations.

---

# Core Design Principle

> **Detect deterministically → Investigate with AI → Decide with humans → Record the decision**

The system is designed around three principles:

### 1. Deterministic First

Financial calculations and reconciliation logic should be predictable, reproducible, and testable.

### 2. AI as an Investigator

Gemini is used where natural-language reasoning is useful — primarily for analyzing and explaining exceptions.

### 3. Human-Controlled Decisions

The final resolution of a financial exception remains with a human reviewer.

---



# License



```text
MIT License
```

---

## Summary

The **AI Finance Reconciliation Controller** demonstrates how traditional rule-based financial reconciliation can be combined with generative AI without allowing the AI model to control the financial source of truth.

The system combines:

**Automated Reconciliation + Fuzzy Matching + Exception Detection + Gemini Investigation + Human Review + Auditability**

to create an AI-assisted reconciliation workflow that is both practical and controllable.

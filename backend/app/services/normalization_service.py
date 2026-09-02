import re
from decimal import Decimal, InvalidOperation

import pandas as pd


def normalize_text(value):
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    # Collapse multiple spaces
    value = re.sub(r"\s+", " ", value)

    return value


def normalize_amount(value):
    if pd.isna(value):
        return None

    value = str(value)

    # Remove currency symbols and commas
    value = re.sub(r"[₹,$]", "", value)
    value = value.replace(",", "").strip()

    try:
        return Decimal(value).quantize(Decimal("0.01"))
    except InvalidOperation:
        return None


def normalize_date(value):
    if pd.isna(value):
        return None

    parsed = pd.to_datetime(value, errors="coerce")

    if pd.isna(parsed):
        return None

    return parsed.date()


def normalize_status(value):
    if pd.isna(value):
        return None

    return str(value).strip().lower()
def normalize_orders(df):
    df = df.copy()

    df["order_id"] = df["order_id"].apply(normalize_text)
    df["customer_name"] = df["customer_name"].apply(normalize_text)
    df["amount"] = df["amount"].apply(normalize_amount)
    df["currency"] = df["currency"].apply(normalize_text)
    df["order_date"] = df["order_date"].apply(normalize_date)

    return df
def normalize_payments(df):
    df = df.copy()

    df["payment_id"] = df["payment_id"].apply(normalize_text)
    df["order_id"] = df["order_id"].apply(normalize_text)
    df["customer_name"] = df["customer_name"].apply(normalize_text)
    df["amount"] = df["amount"].apply(normalize_amount)
    df["currency"] = df["currency"].apply(normalize_text)
    df["status"] = df["status"].apply(normalize_status)
    df["payment_date"] = df["payment_date"].apply(normalize_date)

    return df
def normalize_settlements(df):
    df = df.copy()

    df["settlement_id"] = df["settlement_id"].apply(normalize_text)
    df["payment_id"] = df["payment_id"].apply(normalize_text)
    df["settled_amount"] = df["settled_amount"].apply(normalize_amount)
    df["fee_amount"] = df["fee_amount"].apply(normalize_amount)
    df["currency"] = df["currency"].apply(normalize_text)
    df["settlement_date"] = df["settlement_date"].apply(normalize_date)
    df["status"] = df["status"].apply(normalize_status)

    return df
import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "sales.db"
CSV_PATH = BASE_DIR / "ai_bi_assistant_sales_data - GET.csv"


def initialize_database():
    """Create the SQLite database from the source CSV if it doesn't exist."""

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Sales CSV not found: {CSV_PATH}")

    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name='sales_transactions'
        """)

        if cursor.fetchone():
            print("Database already initialized.")
            return

        df = pd.read_csv(CSV_PATH)

        required_columns = [
            "Transaction_Id", "Order_date", "Product", "Category",
            "Region", "Sales_channel", "Quantity", "Unit_price",
            "Discount_amount", "Status"
        ]

        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"CSV is missing columns: {missing}")

        # Convert numeric columns safely
        for col in ["Quantity", "Unit_price", "Discount_amount"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Standardize dates
        df["Order_date"] = (
            pd.to_datetime(df["Order_date"], dayfirst=True, errors="coerce")
            .dt.strftime("%Y-%m-%d")
        )

        def validate_record(row):
            if row["Status"] != "Completed":
                return "RETURNED"

            if pd.isna(row["Quantity"]) or row["Quantity"] <= 0:
                return "INVALID_QUANTITY"

            if pd.isna(row["Unit_price"]):
                return "MISSING_UNIT_PRICE"

            if row["Unit_price"] <= 0:
                return "INVALID_UNIT_PRICE"

            if pd.isna(row["Discount_amount"]):
                return "MISSING_DISCOUNT"

            if row["Discount_amount"] < 0:
                return "INVALID_DISCOUNT"

            if pd.isna(row["Order_date"]):
                return "INVALID_DATE"

            return "VALID"

        df["validation_status"] = df.apply(validate_record, axis=1)

        df["net_revenue"] = 0.0

        valid = df["validation_status"] == "VALID"

        df.loc[valid, "net_revenue"] = (
            df.loc[valid, "Quantity"] * df.loc[valid, "Unit_price"]
            - df.loc[valid, "Discount_amount"]
        )

        df.to_sql(
            "sales_transactions",
            conn,
            if_exists="replace",
            index=False
        )

        conn.commit()
        print(f"Database initialized with {len(df)} records.")

    finally:
        conn.close()


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
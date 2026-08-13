import os
from pathlib import Path

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)

TABLES = {
    "transactions_clean.csv": "TRANSACTIONS",
}


def load_csv_to_snowflake(csv_file, table_name):
    file_path = DATA_DIR / csv_file

    print(f"Loading {csv_file} → RAW.{table_name}")

    df = pd.read_csv(file_path)

    columns = list(df.columns)

    column_names = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    insert_sql = f"""
        INSERT INTO {table_name} ({column_names})
        VALUES ({placeholders})
    """

    cursor = conn.cursor()

    try:
        rows = [tuple(row) for row in df.itertuples(index=False, name=None)]

        cursor.executemany(insert_sql, rows)

        print(f"✓ Loaded {len(rows):,} rows into RAW.{table_name}")

    finally:
        cursor.close()


try:
    print("Starting BankFlow Snowflake loading...")
    print()

    for csv_file, table_name in TABLES.items():
        load_csv_to_snowflake(csv_file, table_name)

    print()
    print("===================================")
    print("BANKFLOW SNOWFLAKE LOAD COMPLETED")
    print("===================================")

finally:
    conn.close()
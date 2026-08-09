import pandas as pd
from pathlib import Path

from src.utils.database import engine


# -----------------------------------
# Configuration
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"


# -----------------------------------
# Load CSV into PostgreSQL
# -----------------------------------

def load_table(file_name, table_name):

    file_path = PROCESSED_DATA_DIR / file_name

    print(f"Loading {file_name}...")

    dataframe = pd.read_csv(file_path)

    dataframe.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(
        f"✓ Loaded {len(dataframe):,} rows "
        f"into {table_name}"
    )


# -----------------------------------
# Main Loading Pipeline
# -----------------------------------

def main():

    print("Starting BankFlow PostgreSQL loading...\n")

    load_table(
        "customers_clean.csv",
        "customers"
    )

    load_table(
        "accounts_clean.csv",
        "accounts"
    )

    load_table(
        "merchants_clean.csv",
        "merchants"
    )

    load_table(
        "transactions_clean.csv",
        "transactions"
    )

    print("\n===================================")
    print("BANKFLOW POSTGRESQL LOAD COMPLETED")
    print("===================================")


if __name__ == "__main__":
    main()
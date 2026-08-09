import pandas as pd
from pathlib import Path


# -----------------------------------
# Configuration
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------
# Load Raw Data
# -----------------------------------

def load_data():

    customers = pd.read_csv(
        RAW_DATA_DIR / "customers.csv"
    )

    accounts = pd.read_csv(
        RAW_DATA_DIR / "accounts.csv"
    )

    merchants = pd.read_csv(
        RAW_DATA_DIR / "merchants.csv"
    )

    transactions = pd.read_csv(
        RAW_DATA_DIR / "transactions.csv"
    )

    return customers, accounts, merchants, transactions


# -----------------------------------
# Transform Customers
# -----------------------------------

def transform_customers(customers):

    customers = customers.copy()

    customers["first_name"] = (
        customers["first_name"]
        .str.strip()
        .str.title()
    )

    customers["last_name"] = (
        customers["last_name"]
        .str.strip()
        .str.title()
    )

    customers["email"] = (
        customers["email"]
        .str.strip()
        .str.lower()
    )

    customers["date_of_birth"] = pd.to_datetime(
        customers["date_of_birth"]
    )

    return customers


# -----------------------------------
# Transform Accounts
# -----------------------------------

def transform_accounts(accounts):

    accounts = accounts.copy()

    accounts["account_type"] = (
        accounts["account_type"]
        .str.strip()
        .str.title()
    )

    accounts["account_status"] = (
        accounts["account_status"]
        .str.strip()
        .str.title()
    )

    accounts["balance"] = accounts["balance"].round(2)

    accounts["opened_date"] = pd.to_datetime(
        accounts["opened_date"]
    )

    return accounts


# -----------------------------------
# Transform Merchants
# -----------------------------------

def transform_merchants(merchants):

    merchants = merchants.copy()

    merchants["merchant_name"] = (
        merchants["merchant_name"]
        .str.strip()
    )

    merchants["merchant_category"] = (
        merchants["merchant_category"]
        .str.strip()
        .str.title()
    )

    merchants["city"] = (
        merchants["city"]
        .str.strip()
        .str.title()
    )

    merchants["country"] = (
        merchants["country"]
        .str.strip()
        .str.title()
    )

    return merchants


# -----------------------------------
# Transform Transactions
# -----------------------------------

def transform_transactions(transactions):

    transactions = transactions.copy()

    transactions["transaction_timestamp"] = pd.to_datetime(
        transactions["transaction_timestamp"]
    )

    transactions["amount"] = (
        transactions["amount"]
        .astype(float)
        .round(2)
    )

    transactions["transaction_type"] = (
        transactions["transaction_type"]
        .str.strip()
        .str.title()
    )

    transactions["payment_method"] = (
        transactions["payment_method"]
        .str.strip()
    )

    transactions["status"] = (
        transactions["status"]
        .str.strip()
        .str.title()
    )

    # Derived date fields for analytics
    transactions["transaction_date"] = (
        transactions["transaction_timestamp"].dt.date
    )

    transactions["transaction_year"] = (
        transactions["transaction_timestamp"].dt.year
    )

    transactions["transaction_month"] = (
        transactions["transaction_timestamp"].dt.month
    )

    transactions["transaction_day"] = (
        transactions["transaction_timestamp"].dt.day
    )

    return transactions


# -----------------------------------
# Save Processed Data
# -----------------------------------

def save_data(
    customers,
    accounts,
    merchants,
    transactions
):

    customers.to_csv(
        PROCESSED_DATA_DIR / "customers_clean.csv",
        index=False
    )

    accounts.to_csv(
        PROCESSED_DATA_DIR / "accounts_clean.csv",
        index=False
    )

    merchants.to_csv(
        PROCESSED_DATA_DIR / "merchants_clean.csv",
        index=False
    )

    transactions.to_csv(
        PROCESSED_DATA_DIR / "transactions_clean.csv",
        index=False
    )


# -----------------------------------
# Main Transformation Pipeline
# -----------------------------------

def main():

    print("Starting BankFlow data transformation...\n")

    customers, accounts, merchants, transactions = load_data()

    print("Raw data loaded successfully")

    customers = transform_customers(customers)
    accounts = transform_accounts(accounts)
    merchants = transform_merchants(merchants)
    transactions = transform_transactions(transactions)

    print("✓ Customers transformed")
    print("✓ Accounts transformed")
    print("✓ Merchants transformed")
    print("✓ Transactions transformed")

    save_data(
        customers,
        accounts,
        merchants,
        transactions
    )

    print("\nProcessed datasets saved successfully.")

    print(f"Customers: {len(customers):,}")
    print(f"Accounts: {len(accounts):,}")
    print(f"Merchants: {len(merchants):,}")
    print(f"Transactions: {len(transactions):,}")

    print("\n===================================")
    print("BANKFLOW TRANSFORMATION COMPLETED")
    print("===================================")


if __name__ == "__main__":
    main()
import pandas as pd
from pathlib import Path


#----------------------
# Configuration
#----------------------

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


#-------------------------
# load data
#--------------------------

def load_data():
    customers  = pd.read_csv(RAW_DATA_DIR / "customers.csv")
    accounts = pd.read_csv(RAW_DATA_DIR / "accounts.csv")
    merchants = pd.read_csv(RAW_DATA_DIR / "merchants.csv")
    transactions = pd.read_csv(RAW_DATA_DIR / "transactions.csv")

    return customers, accounts, merchants, transactions


# -----------------------------------
# Check Required Columns
# -----------------------------------

def validate_columns(customers, accounts, merchants, transactions):

    expected_columns = {
        "customers": [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_birth",
            "city",
            "country"
        ],

        "accounts": [
            "account_id",
            "customer_id",
            "account_type",
            "account_status",
            "balance",
            "opened_date"
        ],

        "merchants": [
            "merchant_id",
            "merchant_name",
            "merchant_category",
            "city",
            "country"
        ],

        "transactions": [
            "transaction_id",
            "account_id",
            "merchant_id",
            "transaction_timestamp",
            "transaction_type",
            "amount",
            "payment_method",
            "status"
        ]
    }

    datasets = {
        "customers": customers,
        "accounts": accounts,
        "merchants": merchants,
        "transactions": transactions
    }

    for name, dataframe in datasets.items():

        missing_columns = set(expected_columns[name]) - set(dataframe.columns)

        if missing_columns:
            raise ValueError(
                f"{name} is missing columns: {missing_columns}"
            )

    print("✓ Column validation passed")


    # -----------------------------------
# Check Missing Values
# -----------------------------------

def validate_missing_values(
    customers,
    accounts,
    merchants,
    transactions
):

    datasets = {
        "customers": customers,
        "accounts": accounts,
        "merchants": merchants,
        "transactions": transactions
    }

    for name, dataframe in datasets.items():

        missing_values = dataframe.isnull().sum().sum()

        if missing_values > 0:
            raise ValueError(
                f"{name} contains {missing_values} missing values"
            )

    print("✓ Missing-value validation passed")


# -----------------------------------
# Check Duplicate IDs
# -----------------------------------

def validate_duplicate_ids(
    customers,
    accounts,
    merchants,
    transactions
):

    datasets = {
        "customers": ("customer_id", customers),
        "accounts": ("account_id", accounts),
        "merchants": ("merchant_id", merchants),
        "transactions": ("transaction_id", transactions)
    }

    for name, (id_column, dataframe) in datasets.items():

        duplicates = dataframe[id_column].duplicated().sum()

        if duplicates > 0:
            raise ValueError(
                f"{name} contains {duplicates} duplicate IDs"
            )

    print("✓ Duplicate-ID validation passed")


# -----------------------------------
# Validate Relationships
# -----------------------------------

def validate_relationships(
    customers,
    accounts,
    merchants,
    transactions
):

    customer_ids = set(customers["customer_id"])
    account_ids = set(accounts["account_id"])
    merchant_ids = set(merchants["merchant_id"])

    invalid_customer_ids = set(accounts["customer_id"]) - customer_ids

    if invalid_customer_ids:
        raise ValueError(
            f"Invalid customer IDs found in accounts: "
            f"{invalid_customer_ids}"
        )

    invalid_account_ids = set(transactions["account_id"]) - account_ids

    if invalid_account_ids:
        raise ValueError(
            f"Invalid account IDs found in transactions: "
            f"{invalid_account_ids}"
        )

    invalid_merchant_ids = set(transactions["merchant_id"]) - merchant_ids

    if invalid_merchant_ids:
        raise ValueError(
            f"Invalid merchant IDs found in transactions: "
            f"{invalid_merchant_ids}"
        )

    print("✓ Relationship validation passed")


# -----------------------------------
# Validate Transaction Amounts
# -----------------------------------

def validate_transaction_amounts(transactions):

    invalid_amounts = transactions[
        transactions["amount"] <= 0
    ]

    if not invalid_amounts.empty:
        raise ValueError(
            f"Found {len(invalid_amounts)} invalid transaction amounts"
        )

    print("✓ Transaction amount validation passed")


# -----------------------------------
# Validate Account Balances
# -----------------------------------

def validate_account_balances(accounts):

    invalid_balances = accounts[
        accounts["balance"] < 0
    ]

    if not invalid_balances.empty:
        raise ValueError(
            f"Found {len(invalid_balances)} negative account balances"
        )

    print("✓ Account balance validation passed")


# -----------------------------------
# Main Validation Pipeline
# -----------------------------------

def main():

    print("Starting BankFlow data validation...\n")

    customers, accounts, merchants, transactions = load_data()

    print("Data loaded successfully")
    print(f"Customers: {len(customers):,}")
    print(f"Accounts: {len(accounts):,}")
    print(f"Merchants: {len(merchants):,}")
    print(f"Transactions: {len(transactions):,}\n")

    validate_columns(
        customers,
        accounts,
        merchants,
        transactions
    )

    validate_missing_values(
        customers,
        accounts,
        merchants,
        transactions
    )

    validate_duplicate_ids(
        customers,
        accounts,
        merchants,
        transactions
    )

    validate_relationships(
        customers,
        accounts,
        merchants,
        transactions
    )

    validate_transaction_amounts(transactions)

    validate_account_balances(accounts)

    print("\n===================================")
    print("BANKFLOW VALIDATION PASSED")
    print("===================================")


if __name__ == "__main__":
    main()
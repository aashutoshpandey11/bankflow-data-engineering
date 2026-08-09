from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------

fake = Faker()

NUM_CUSTOMERS = 1000
NUM_ACCOUNTS = 1500
NUM_MERCHANTS = 200
NUM_TRANSACTIONS = 50000

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Generate Customers
# -----------------------------

def generate_customers():
    customers = []

    for i in range(1, NUM_CUSTOMERS + 1):
        customers.append({
            "customer_id": i,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "phone": fake.phone_number(),
            "date_of_birth": fake.date_of_birth(
                minimum_age=18,
                maximum_age=80
            ),
            "city": fake.city(),
            "country": fake.country()
        })

    return pd.DataFrame(customers)



# -----------------------------
# Generate Accounts
# -----------------------------

def generate_accounts():
    accounts = []

    account_types = [
        "Savings",
        "Checking",
        "Business"
    ]

    account_statuses = [
        "Active",
        "Inactive",
        "Suspended"
    ]

    for i in range(1, NUM_ACCOUNTS + 1):
        accounts.append({
            "account_id": i,
            "customer_id": random.randint(1, NUM_CUSTOMERS),
            "account_type": random.choice(account_types),
            "account_status": random.choice(account_statuses),
            "balance": round(random.uniform(100, 50000), 2),
            "opened_date": fake.date_between(
                start_date="-10y",
                end_date="today"
            )
        })

    return pd.DataFrame(accounts)



# -----------------------------
# Generate Merchants
# -----------------------------

def generate_merchants():
    merchants = []

    merchant_categories = [
        "Groceries",
        "Restaurants",
        "Electronics",
        "Travel",
        "Healthcare",
        "Entertainment",
        "Clothing",
        "Utilities",
        "Education",
        "Fuel"
    ]

    for i in range(1, NUM_MERCHANTS + 1):
        merchants.append({
            "merchant_id": i,
            "merchant_name": fake.company(),
            "merchant_category": random.choice(merchant_categories),
            "city": fake.city(),
            "country": fake.country()
        })

    return pd.DataFrame(merchants)


# -----------------------------
# Generate Transactions
# -----------------------------

def generate_transactions():
    transactions = []

    transaction_types = [
        "Purchase",
        "Withdrawal",
        "Deposit",
        "Transfer"
    ]

    payment_methods = [
        "Debit Card",
        "Credit Card",
        "Bank Transfer",
        "Mobile Banking"
    ]

    transaction_statuses = [
        "Completed",
        "Pending",
        "Failed"
    ]

    start_date = datetime.now() - timedelta(days=365)

    for i in range(1, NUM_TRANSACTIONS + 1):

        transaction_timestamp = fake.date_time_between(
            start_date=start_date,
            end_date="now"
        )

        transactions.append({
            "transaction_id": i,
            "account_id": random.randint(1, NUM_ACCOUNTS),
            "merchant_id": random.randint(1, NUM_MERCHANTS),
            "transaction_timestamp": transaction_timestamp,
            "transaction_type": random.choice(transaction_types),
            "amount": round(random.uniform(5, 5000), 2),
            "payment_method": random.choice(payment_methods),
            "status": random.choice(transaction_statuses)
        })

    return pd.DataFrame(transactions)


# -----------------------------
# Main Pipeline
# -----------------------------

def main():

    print("Starting BankFlow data generation...")

    print("Generating customers...")
    customers = generate_customers()

    print("Generating accounts...")
    accounts = generate_accounts()

    print("Generating merchants...")
    merchants = generate_merchants()

    print("Generating transactions...")
    transactions = generate_transactions()

    print("Saving datasets...")

    customers.to_csv(
        RAW_DATA_DIR / "customers.csv",
        index=False
    )

    accounts.to_csv(
        RAW_DATA_DIR / "accounts.csv",
        index=False
    )

    merchants.to_csv(
        RAW_DATA_DIR / "merchants.csv",
        index=False
    )

    transactions.to_csv(
        RAW_DATA_DIR / "transactions.csv",
        index=False
    )

    print("\nData generation completed successfully!")

    print(f"Customers: {len(customers):,}")
    print(f"Accounts: {len(accounts):,}")
    print(f"Merchants: {len(merchants):,}")
    print(f"Transactions: {len(transactions):,}")

    print(f"\nFiles saved to: {RAW_DATA_DIR}")


if __name__ == "__main__":
    main()

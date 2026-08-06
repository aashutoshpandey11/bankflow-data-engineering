import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ PostgreSQL connection successful!")
            print(f"Database test result: {result.scalar()}")

    except Exception as error:
        print("❌ PostgreSQL connection failed!")
        print(f"Error: {error}")


if __name__ == "__main__":
    test_connection()
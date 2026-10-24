import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Locate the project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from .env.
load_dotenv(PROJECT_ROOT / ".env")


def test_connection():
    """Test the connection to the PostgreSQL database."""

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not configured in .env.")

    # Explicitly use the psycopg driver.
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    engine = create_engine(database_url, pool_pre_ping=True)

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.scalar_one()

            print("Connection successful!")
            print("PostgreSQL version:", version.split(",")[0])

    finally:
        engine.dispose()


if __name__ == "__main__":
    test_connection()
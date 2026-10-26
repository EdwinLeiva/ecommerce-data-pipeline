
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "products_clean.csv"

load_dotenv(PROJECT_ROOT / ".env")


def load_products():
    """Load cleaned products into PostgreSQL using an upsert."""
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not configured in .env.")

    if database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned CSV not found: {CSV_PATH}. "
            "Run src/transform_products.py first."
        )

    df = pd.read_csv(CSV_PATH)

    if df.empty:
        raise ValueError("The cleaned CSV contains no products.")

    required_columns = {
        "id",
        "title",
        "price",
        "description",
        "category",
        "image",
        "rating_rate",
        "rating_count",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    records = df.astype(object).where(pd.notna(df), None).to_dict(
        orient="records"
    )

    create_table_sql = text("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            price NUMERIC(12, 2) NOT NULL,
            description TEXT,
            category TEXT,
            image TEXT,
            rating_rate NUMERIC(4, 2),
            rating_count INTEGER
        );
    """)

    upsert_sql = text("""
        INSERT INTO products (
            id, title, price, description, category, image,
            rating_rate, rating_count
        )
        VALUES (
            :id, :title, :price, :description, :category, :image,
            :rating_rate, :rating_count
        )
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            price = EXCLUDED.price,
            description = EXCLUDED.description,
            category = EXCLUDED.category,
            image = EXCLUDED.image,
            rating_rate = EXCLUDED.rating_rate,
            rating_count = EXCLUDED.rating_count;
    """)

    engine = create_engine(database_url, pool_pre_ping=True)

    try:
        with engine.begin() as connection:
            connection.execute(create_table_sql)
            connection.execute(upsert_sql, records)

        print("Load completed successfully!")
        print(f"Products processed: {len(records)}")
        print("Destination table: products")
    finally:
        engine.dispose()


if __name__ == "__main__":
    load_products()
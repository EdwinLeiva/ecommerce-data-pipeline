from pathlib import Path

import pandas as pd


# Define the project directories.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "api" / "products.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "products_clean.csv"


def transform_products():
    """Transform and validate product data, then save it as CSV."""

    print("Starting product transformation...")

    # Load the original JSON data.
    df = pd.read_json(INPUT_FILE)

    # Separate the nested rating information into two columns.
    rating = pd.json_normalize(df.pop("rating"))

    rating = rating.rename(
        columns={
            "rate": "rating_rate",
            "count": "rating_count",
        }
    )

    df = pd.concat([df, rating], axis=1)

    # Validate data quality.
    if df.empty:
        raise ValueError("The dataset contains no products.")

    if df["id"].duplicated().any():
        raise ValueError("Duplicate product IDs were found.")

    if df.isnull().any().any():
        raise ValueError("Missing values were found.")

    if (df["price"] < 0).any():
        raise ValueError("Negative prices were found.")

    if (
        (df["rating_rate"] < 0) | (df["rating_rate"] > 5)
    ).any():
        raise ValueError("Ratings outside the 0-5 range were found.")

    if (df["rating_count"] < 0).any():
        raise ValueError("Negative rating counts were found.")

    # Create the output directory if it does not exist.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save the transformed data as CSV.
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"Products processed: {len(df)}")
    print(f"Columns in output: {len(df.columns)}")
    print(f"Processed file saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    transform_products()
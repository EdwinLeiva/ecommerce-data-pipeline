import logging
from pathlib import Path

import pandas as pd


# Define the project directories.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "api" / "products.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "products_clean.csv"

logger = logging.getLogger(__name__)


def transform_products():
    """Transform and validate product data, then save it as CSV."""

    logger.info("Starting product transformation from %s", INPUT_FILE)

    # Load the original JSON data.
    try:
        df = pd.read_json(INPUT_FILE)
    except (ValueError, OSError):
        logger.exception("Failed to read the input product data")
        raise

    # Validate that the dataset contains products before accessing columns.
    if df.empty:
        logger.error("The dataset contains no products")
        raise ValueError("The dataset contains no products.")

    # Separate the nested rating information into two columns.
    try:
        rating = pd.json_normalize(df.pop("rating"))
    except KeyError:
        logger.exception("The input data is missing the rating field")
        raise

    rating = rating.rename(
        columns={
            "rate": "rating_rate",
            "count": "rating_count",
        }
    )

    df = pd.concat([df, rating], axis=1)

    # Validate data quality.
    if df["id"].duplicated().any():
        logger.error("Duplicate product IDs were found")
        raise ValueError("Duplicate product IDs were found.")

    if df.isnull().any().any():
        logger.error("Missing values were found")
        raise ValueError("Missing values were found.")

    if (df["price"] < 0).any():
        logger.error("Negative prices were found")
        raise ValueError("Negative prices were found.")

    if ((df["rating_rate"] < 0) | (df["rating_rate"] > 5)).any():
        logger.error("Ratings outside the 0-5 range were found")
        raise ValueError("Ratings outside the 0-5 range were found.")

    if (df["rating_count"] < 0).any():
        logger.error("Negative rating counts were found")
        raise ValueError("Negative rating counts were found.")

    # Create the output directory if it does not exist.
    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Save the transformed data as CSV.
        df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    except OSError:
        logger.exception("Failed to save transformed product data")
        raise

    logger.info("Products processed: %d", len(df))
    logger.info("Columns in output: %d", len(df.columns))
    logger.info("Processed data saved to %s", OUTPUT_FILE)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    transform_products()
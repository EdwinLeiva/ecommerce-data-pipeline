import json
import logging
from pathlib import Path

import requests


API_URL = "https://fakestoreapi.com/products"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "api" / "products.json"

logger = logging.getLogger(__name__)


def extract_products():
    """Download products from the Fake Store API and save them as JSON."""

    logger.info("Starting product extraction from %s", API_URL)

    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        products = response.json()

    except requests.exceptions.RequestException:
        logger.exception("Failed to retrieve products from the API")
        raise

    except ValueError:
        logger.exception("The API returned invalid JSON")
        raise

    if not isinstance(products, list):
        logger.error("The API response is not a list of products")
        raise ValueError("The API response is not a list of products.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    try:
        with OUTPUT_FILE.open("w", encoding="utf-8") as file:
            json.dump(products, file, indent=2, ensure_ascii=False)

    except OSError:
        logger.exception("Failed to save extracted products to %s", OUTPUT_FILE)
        raise

    logger.info("Products extracted: %d", len(products))
    logger.info("Extracted data saved to %s", OUTPUT_FILE)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    extract_products()
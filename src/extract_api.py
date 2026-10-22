import json
from pathlib import Path

import requests


API_URL = "https://fakestoreapi.com/products"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "api" / "products.json"


def extract_products():
    """Download products from the Fake Store API and save them as JSON."""

    print("Starting product extraction...")

    response = requests.get(API_URL, timeout=30)

    response.raise_for_status()

    products = response.json()

    if not isinstance(products, list):
        raise ValueError("The API response is not a list of products.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(products, file, indent=2, ensure_ascii=False)

    print(f"Products extracted: {len(products)}")
    print(f"File saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    extract_products()
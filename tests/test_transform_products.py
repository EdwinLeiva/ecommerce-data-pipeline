
import json

import pandas as pd
import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import transform_products as transformer


def write_products_json(path, products):
    """Create a temporary JSON file with product data for testing."""
    path.write_text(json.dumps(products), encoding="utf-8")


def valid_product():
    """Return one valid sample product."""
    return {
        "id": 1,
        "title": "Test product",
        "price": 19.99,
        "description": "A product for testing",
        "category": "electronics",
        "image": "https://example.com/product.jpg",
        "rating": {
            "rate": 4.5,
            "count": 10,
        },
    }


def test_transform_products_creates_clean_csv(tmp_path, monkeypatch):
    products = [valid_product(), {**valid_product(), "id": 2}]
    input_file = tmp_path / "products.json"
    output_file = tmp_path / "products_clean.csv"

    write_products_json(input_file, products)

    monkeypatch.setattr(transformer, "INPUT_FILE", input_file)
    monkeypatch.setattr(transformer, "OUTPUT_FILE", output_file)

    transformer.transform_products()

    result = pd.read_csv(output_file)

    assert len(result) == 2
    assert "rating_rate" in result.columns
    assert "rating_count" in result.columns
    assert "rating" not in result.columns


def test_transform_products_rejects_duplicate_ids(tmp_path, monkeypatch):
    product = valid_product()
    input_file = tmp_path / "products.json"
    output_file = tmp_path / "products_clean.csv"

    write_products_json(input_file, [product, product])

    monkeypatch.setattr(transformer, "INPUT_FILE", input_file)
    monkeypatch.setattr(transformer, "OUTPUT_FILE", output_file)

    with pytest.raises(ValueError, match="Duplicate product IDs"):
        transformer.transform_products()


def test_transform_products_rejects_negative_prices(tmp_path, monkeypatch):
    product = valid_product()
    product["price"] = -1
    input_file = tmp_path / "products.json"
    output_file = tmp_path / "products_clean.csv"

    write_products_json(input_file, [product])

    monkeypatch.setattr(transformer, "INPUT_FILE", input_file)
    monkeypatch.setattr(transformer, "OUTPUT_FILE", output_file)

    with pytest.raises(ValueError, match="Negative prices"):
        transformer.transform_products()


def test_transform_products_rejects_empty_dataset(tmp_path, monkeypatch):
    input_file = tmp_path / "products.json"
    output_file = tmp_path / "products_clean.csv"

    write_products_json(input_file, [])

    monkeypatch.setattr(transformer, "INPUT_FILE", input_file)
    monkeypatch.setattr(transformer, "OUTPUT_FILE", output_file)

    with pytest.raises(ValueError, match="dataset contains no products"):
        transformer.transform_products()


def test_transform_products_rejects_out_of_range_rating(tmp_path, monkeypatch):
    product = valid_product()
    product["rating"]["rate"] = 6
    input_file = tmp_path / "products.json"
    output_file = tmp_path / "products_clean.csv"

    write_products_json(input_file, [product])

    monkeypatch.setattr(transformer, "INPUT_FILE", input_file)
    monkeypatch.setattr(transformer, "OUTPUT_FILE", output_file)

    with pytest.raises(ValueError, match="Ratings outside the 0-5 range"):
        transformer.transform_products()


def test_transform_products_rejects_negative_rating_count(tmp_path, monkeypatch):
    product = valid_product()
    product["rating"]["count"] = -1
    input_file = tmp_path / "products.json"
    output_file = tmp_path / "products_clean.csv"

    write_products_json(input_file, [product])

    monkeypatch.setattr(transformer, "INPUT_FILE", input_file)
    monkeypatch.setattr(transformer, "OUTPUT_FILE", output_file)

    with pytest.raises(ValueError, match="Negative rating counts"):
        transformer.transform_products()

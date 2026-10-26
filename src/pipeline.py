from extract_api import extract_products
from transform_products import transform_products
from load_postgres import load_products


def run_pipeline():
    """Execute the complete product ETL pipeline."""

    print("=" * 50)
    print("Starting ecommerce data pipeline")
    print("=" * 50)

    extract_products()
    transform_products()
    load_products()

    print("=" * 50)
    print("Pipeline completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()
import logging

from extract_api import extract_products
from transform_products import transform_products
from load_postgres import load_products


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def run_pipeline():
    """Execute the complete product ETL pipeline."""

    logger.info("Starting ecommerce data pipeline")

    try:
        logger.info("Starting extraction stage")
        extract_products()
        logger.info("Extraction stage completed successfully")

        logger.info("Starting transformation stage")
        transform_products()
        logger.info("Transformation stage completed successfully")

        logger.info("Starting loading stage")
        load_products()
        logger.info("Loading stage completed successfully")

        logger.info("Pipeline completed successfully")

    except Exception:
        logger.exception("Pipeline failed")
        raise


if __name__ == "__main__":
    run_pipeline()
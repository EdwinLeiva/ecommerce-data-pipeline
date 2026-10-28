# Ecommerce Data Pipeline

An end-to-end data engineering portfolio project that extracts e-commerce product data from a public API, transforms and validates it with Python and pandas, and loads it into PostgreSQL.

The project demonstrates ETL development, data quality validation, relational database integration, duplicate-safe loading, structured logging, automated testing, SQL analytics, and continuous integration with GitHub Actions.

## Project Overview

This project implements an ETL pipeline using the Fake Store API as its data source.

The pipeline extracts product records, transforms nested fields, validates data quality, and loads the results into PostgreSQL. It also includes automated transformation tests and SQL queries for basic product analysis.

## Architecture

```text
Fake Store API
      |
      v
 API Extraction
      |
      v
data/raw/api/products.json
      |
      v
 Data Transformation
      |
      v
 Data Quality Validation
      |
      v
data/processed/products_clean.csv
      |
      v
 PostgreSQL Loading
      |
      v
   products table
      |
      v
 SQL Analytics
```

The workflow is orchestrated by `src/pipeline.py`.

## Technology Stack

- **Python 3.13** — ETL implementation
- **Requests** — HTTP requests to the source API
- **Pandas** — data transformation and validation
- **PostgreSQL** — relational data storage
- **SQLAlchemy** — database connectivity and transaction management
- **psycopg** — PostgreSQL driver
- **python-dotenv** — environment variable management
- **pytest** — automated testing
- **SQL** — analytical queries
- **Git and GitHub** — version control and repository hosting
- **GitHub Actions** — continuous integration

## Data Source

The pipeline uses the [Fake Store API](https://fakestoreapi.com/products) to retrieve product data.

The source records include product identifiers, titles, prices, descriptions, categories, image URLs, and ratings.

During the documented successful run, the pipeline extracted and loaded 20 products. The number of records may vary if the source data changes.

## Project Structure

```text
ecommerce-data-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── raw/
│   │   └── api/
│   └── processed/
├── src/
│   ├── extract_api.py
│   ├── transform_products.py
│   ├── load_postgres.py
│   ├── pipeline.py
│   └── test_connection.py
├── sql/
│   └── product_analysis.sql
├── tests/
│   └── test_transform_products.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Generated data files, local environment files, and Python cache files are excluded from version control where appropriate.

## ETL Workflow

### 1. Extract

The extraction stage:

- Sends HTTP requests to the Fake Store API.
- Uses a request timeout and checks for unsuccessful HTTP responses.
- Handles request, JSON parsing, and file-related errors.
- Saves the raw response to `data/raw/api/products.json`.

### 2. Transform and Validate

The transformation stage:

- Loads the raw JSON data with pandas.
- Separates nested rating information into `rating_rate` and `rating_count`.
- Validates the dataset before saving the output.
- Writes the cleaned data to `data/processed/products_clean.csv`.

Current data quality checks include:

- Rejecting empty datasets.
- Rejecting duplicate product IDs.
- Detecting missing required values.
- Rejecting negative prices.
- Ensuring ratings are within the 0–5 range.
- Rejecting negative rating counts.

### 3. Load

The loading stage:

- Reads the cleaned CSV file.
- Validates required columns and rejects empty datasets.
- Connects to PostgreSQL using SQLAlchemy.
- Creates the `products` table if it does not exist.
- Uses PostgreSQL `INSERT ... ON CONFLICT (id) DO UPDATE` to insert new products and update existing records.
- Executes database operations within a transaction.

This approach makes repeated loads safer by preventing duplicate rows for the same product ID.

### 4. Orchestrate and Monitor

The `src/pipeline.py` module runs extraction, transformation, and loading in sequence.

The ETL modules use Python's standard logging framework to report execution progress and failures. Exceptions are logged with context and re-raised instead of being silently ignored.

The loading module also disposes of the SQLAlchemy engine after its database work.

## SQL Analytics

The file `sql/product_analysis.sql` contains five analytical queries:

1. Count the total number of products.
2. Calculate minimum, maximum, average, and total product prices.
3. Summarize products and average prices by category.
4. Identify the five most expensive products.
5. Find products priced above the overall average.

These queries demonstrate basic SQL aggregation, grouping, sorting, and subquery usage.

The analysis operates on the products currently loaded into PostgreSQL.

## Automated Testing

The project uses pytest to validate transformation behavior.

The transformation test suite contains six tests covering:

- Successful CSV generation.
- Duplicate product ID rejection.
- Negative price rejection.
- Empty dataset rejection.
- Out-of-range rating rejection.
- Negative rating count rejection.

A separate database connection test is available in `src/test_connection.py`.

Run the transformation tests:

```powershell
python -m pytest tests/test_transform_products.py -v
```

Run the complete test suite, including the database connection test:

```powershell
python -m pytest -v
```

The complete test suite requires a working database configuration for the connection test.

## Continuous Integration

GitHub Actions is configured in `.github/workflows/ci.yml`.

The workflow runs on pushes to `main` and pull requests targeting `main`. It prepares a Python 3.13 environment, installs dependencies, and executes the six transformation tests.

The workflow does not currently run the database connection test or a full ETL integration test. This keeps CI independent of the project's Neon database credentials.

A successful workflow run confirms that the configured transformation tests passed in the GitHub Actions environment.

## Prerequisites

- Python 3.13 or a compatible Python version
- Git
- A PostgreSQL database, such as Neon
- Internet access to reach the source API

## Setup and Usage

### 1. Clone the repository

```powershell
git clone https://github.com/EdwinLeiva/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and set `DATABASE_URL` to your PostgreSQL connection string.

Keep `.env` private. Never commit database credentials or other secrets to GitHub.

### 5. Test the database connection

```powershell
python src/test_connection.py
```

### 6. Run the complete pipeline

```powershell
python src/pipeline.py
```

The pipeline retrieves product data from the API, transforms and validates the records, and loads them into the PostgreSQL `products` table.

### 7. Run automated tests

```powershell
python -m pytest tests/test_transform_products.py -v
```

To run all tests, including the database connection test:

```powershell
python -m pytest -v
```

### 8. Run SQL analytics

Connect to the PostgreSQL database and execute the queries in:

```text
sql/product_analysis.sql
```

The queries can be used to inspect product counts, price distributions, category summaries, and the most expensive products.

## Security and Configuration

- Database connection settings are provided through environment variables.
- The local `.env` file must not be committed.
- `.env.example` documents the expected configuration without storing real credentials.
- Generated raw and processed data files are excluded from version control.

## Current Project Status

**Implemented and verified:**

- Public API extraction.
- Data transformation and quality validation.
- PostgreSQL connectivity.
- Duplicate-safe upsert loading.
- ETL orchestration.
- Structured logging and error reporting.
- Six automated transformation tests.
- SQL analytics queries.
- GitHub Actions workflow for automated transformation tests.

The pipeline has successfully extracted, transformed, and loaded 20 products in a documented run. The six transformation tests have passed locally, and the GitHub Actions workflow has completed successfully.

## Future Improvements

Potential enhancements include:

- Add integration tests for PostgreSQL loading.
- Add end-to-end tests for the complete ETL pipeline.
- Add pipeline metrics and execution duration tracking.
- Expand validation for malformed and incomplete source data.
- Add data freshness and load monitoring.
- Improve CI coverage while managing database credentials securely.

## License

No license has been specified yet. Unless a license is added, others should not assume that the repository grants permission to reuse or redistribute its code.

## Author

**Edwin Leiva**

Data engineering portfolio project focused on ETL pipelines, data quality, Python, PostgreSQL, SQL analytics, and continuous integration.
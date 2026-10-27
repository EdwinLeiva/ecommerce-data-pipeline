# Ecommerce Data Pipeline

An end-to-end data engineering project that extracts e-commerce product data from a public API, transforms and validates it with Python and pandas, and loads it into PostgreSQL.

The project demonstrates ETL development, data quality validation, database integration, automated testing, structured logging, and version control.

## Project Architecture

```text
Fake Store API
      |
      v
   Extraction
      |
      v
data/raw/api/products.json
      |
      v
 Transformation
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
```

The workflow is orchestrated by `src/pipeline.py`.

## Technology Stack

- **Python** — ETL implementation
- **Requests** — API requests
- **Pandas** — data transformation and validation
- **PostgreSQL** — relational data storage
- **SQLAlchemy** — database connectivity and transactions
- **psycopg** — PostgreSQL driver
- **python-dotenv** — environment variable management
- **pytest** — automated testing
- **Git and GitHub** — version control and project hosting

## Data Source

The current pipeline uses the [Fake Store API](https://fakestoreapi.com/products) to retrieve product data.

The extracted dataset includes product identifiers, titles, prices, descriptions, categories, images, and ratings.

The Olist e-commerce dataset is planned as a separate workflow in a future project stage.

## Project Structure

```text
ecommerce-data-pipeline/
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
├── tests/
│   └── test_transform_products.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Generated data files and local environment files are excluded from version control where appropriate.

## ETL Workflow

### 1. Extract

- Requests product data from the Fake Store API.
- Uses a request timeout and checks for unsuccessful HTTP responses.
- Validates the general structure of the API response.
- Saves the raw response as JSON.

### 2. Transform and Validate

- Loads the raw JSON data with pandas.
- Separates nested rating fields into `rating_rate` and `rating_count`.
- Checks for empty datasets, duplicate product IDs, missing values, negative prices, invalid rating ranges, and negative rating counts.
- Writes the cleaned dataset to CSV.

### 3. Load

- Reads the cleaned CSV file.
- Validates required columns and rejects empty datasets.
- Connects to PostgreSQL using SQLAlchemy.
- Creates the `products` table if it does not exist.
- Uses `INSERT ... ON CONFLICT (id) DO UPDATE` to insert new products and update existing products.
- Executes database operations within a transaction.

### 4. Orchestrate and Monitor

The `pipeline.py` module runs extraction, transformation, and loading in sequence.

The pipeline uses Python's logging framework to report execution progress, stage completion, and failures. Exceptions are logged and re-raised instead of being silently ignored.

## Data Quality Rules

The transformation stage currently validates:

- The dataset is not empty.
- Product IDs are unique.
- Required data does not contain missing values.
- Product prices are not negative.
- Ratings are within the 0–5 range.
- Rating counts are not negative.

Automated tests cover the main transformation rules.

## Prerequisites

- Python 3.13 or a compatible Python version
- Git
- A PostgreSQL database, such as Neon
- Internet access to reach the source API

## Setup

### 1. Clone the repository

```bash
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

### 5. Run the database connection test

```powershell
python src/test_connection.py
```

### 6. Run the complete pipeline

```powershell
python src/pipeline.py
```

The pipeline retrieves the current API data, transforms it, and loads the results into the PostgreSQL `products` table.

### 7. Run automated tests

Run the complete test suite:

```powershell
python -m pytest -v
```

Run only the transformation tests:

```powershell
python -m pytest tests/test_transform_products.py -v
```

The current test suite includes a database connection test and six transformation tests.

## Logging and Error Handling

The ETL modules use Python's standard `logging` library to record progress and errors.

Log messages include timestamps, severity levels, module names, and contextual messages. Failures are logged with exception tracebacks and propagated to the caller.

The project also uses a database transaction and disposes of the SQLAlchemy engine after loading.

## Current Project Status

Implemented:

- Repository and Python environment setup
- Public API extraction
- Data transformation and quality validation
- PostgreSQL connectivity
- Duplicate-safe upsert loading
- ETL orchestration
- Structured logging and improved error reporting
- Automated tests with pytest

Planned:

- SQL analytics and documented analytical queries
- Automated quality checks with GitHub Actions
- A separate ETL workflow for the Olist dataset

## Future Improvements

- Add integration tests for PostgreSQL loading.
- Add more validation tests for malformed or incomplete source data.
- Add pipeline execution metrics and duration tracking.
- Automate test execution with GitHub Actions.
- Develop documented SQL queries for business analysis.
- Build a separate workflow for the Olist dataset.

## License

A license has not yet been specified for this project.

## Author

**Edwin Leiva**

Data Engineering portfolio project focused on ETL pipelines, data quality, Python, and PostgreSQL.

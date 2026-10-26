# E-Commerce Analytics Data Pipeline

## Overview

An end-to-end data engineering project that extracts product data from a public API, transforms and validates it with Python, and loads it into PostgreSQL for analysis.

The project is designed to demonstrate foundational data engineering skills, including ETL development, data quality validation, database integration, idempotent loading, and version control.

## Architecture

The current pipeline follows this workflow:

```text
Fake Store API
      |
      v
Python Extraction
      |
      v
Raw JSON
      |
      v
Transformation and Data Quality Validation
      |
      v
Clean CSV
      |
      v
PostgreSQL (Neon)
      |
      v
SQL Analytics (planned)
```

The pipeline is orchestrated by `src/pipeline.py`, which executes the extraction, transformation, and loading steps in sequence.

## Data Sources

### Current source

- **Fake Store API:** https://fakestoreapi.com/products
- Provides a sample product catalog used to demonstrate the ETL workflow.

### Planned source

- **Brazilian E-Commerce Public Dataset by Olist:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- Intended for a separate analytical workflow using historical Brazilian e-commerce data.

These sources represent different datasets and will be analyzed independently.

## Technology Stack

- **Python** — pipeline implementation.
- **pandas** — data transformation and validation.
- **Requests** — API extraction.
- **PostgreSQL** — relational data storage.
- **Neon** — hosted PostgreSQL database.
- **SQLAlchemy** — database connectivity and SQL execution.
- **python-dotenv** — local environment configuration.
- **Git and GitHub** — version control and project hosting.

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
│   ├── test_connection.py
│   └── pipeline.py
├── sql/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Raw and processed data files are generated locally and excluded from version control.

## Current Implementation

### 1. Extraction

`src/extract_api.py`

- Retrieves product data from Fake Store API.
- Checks HTTP errors.
- Validates that the API response is a list.
- Saves the response as JSON under `data/raw/api/`.

### 2. Transformation and data quality

`src/transform_products.py`

- Loads the raw JSON into pandas.
- Flattens nested rating fields.
- Validates that the dataset is not empty.
- Detects duplicate product IDs and missing values.
- Checks for negative prices, invalid ratings, and negative rating counts.
- Exports the transformed dataset to CSV under `data/processed/`.

### 3. Database loading

`src/load_postgres.py`

- Reads the cleaned CSV.
- Validates the required columns.
- Creates the PostgreSQL `products` table if it does not exist.
- Inserts new products and updates existing products using `ON CONFLICT (id) DO UPDATE`.
- Uses a database transaction for the table creation and data load.

### 4. Pipeline orchestration

`src/pipeline.py`

Runs extraction, transformation, and loading in sequence.

### 5. Database connectivity

`src/test_connection.py`

Checks the PostgreSQL connection and retrieves the server version.

## Validation Results

The current end-to-end pipeline has been executed successfully.

- **Products extracted:** 20
- **Products transformed:** 20
- **Output columns:** 8
- **Database destination:** PostgreSQL table `products`
- **Duplicate handling:** verified by rerunning the load and confirming that existing product IDs are updated instead of duplicated.

These results describe the current sample dataset and may vary if the source API changes.

## Prerequisites

- Python 3.13 or a compatible Python version.
- Git.
- A PostgreSQL database. This project currently uses Neon.
- A local `.env` file containing the database connection string.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/EdwinLeiva/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the database connection

Create a local `.env` file in the project root using `.env.example` as a reference.

Configure:

```dotenv
DATABASE_URL=your_postgresql_connection_string
```

Replace the placeholder with your own connection string. Do not commit the `.env` file or expose database credentials.

### 5. Test the database connection

```powershell
python src/test_connection.py
```

### 6. Run the complete pipeline

From the project root:

```powershell
python src/pipeline.py
```

The pipeline extracts the source data, transforms and validates it, and loads the resulting records into PostgreSQL.

## Security

- Store credentials in a local `.env` file.
- Never commit secrets or database credentials.
- Raw and processed data files are excluded from version control.
- Use `.env.example` to document required environment variables without including real credentials.

## Roadmap

- [x] Set up the repository and Python environment.
- [x] Extract product data from a public API.
- [x] Transform and validate product data.
- [x] Connect to PostgreSQL.
- [x] Load products with duplicate-safe upsert logic.
- [x] Orchestrate the complete ETL workflow.
- [ ] Add structured logging and improved error reporting.
- [ ] Implement automated tests with pytest.
- [ ] Develop SQL analytics and document analytical queries.
- [ ] Automate quality checks with GitHub Actions.
- [ ] Build a separate workflow for the Olist dataset.

## Author

Edwin Leiva
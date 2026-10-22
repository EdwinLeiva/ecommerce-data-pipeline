# E-Commerce Analytics Data Pipeline

## Overview

This project aims to build a data pipeline that collects, processes, and analyzes e-commerce data using Python, PostgreSQL, and SQL.

The project uses two independent data sources:

- **Fake Store API:** a sample product catalog.
- **Brazilian E-Commerce Public Dataset by Olist:** historical e-commerce data from Brazil.

These sources will be analyzed separately because they represent different datasets and do not describe the same store.

## Objectives

- Extract data from an API and public CSV files.
- Validate and transform data using Python.
- Store structured data in PostgreSQL.
- Write SQL queries to analyze orders, products, and sales.
- Document the pipeline and its results.

## Technology Stack

- Python
- SQL
- PostgreSQL
- pandas
- SQLAlchemy
- Git and GitHub

## Project Structure

```text
ecommerce-data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── src/
├── sql/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Project Status

**Phase 1 — Environment and repository setup**

The initial project structure and GitHub repository have been created.

Upcoming phases will cover data extraction, validation, database loading, and SQL analytics.

## Data Sources

- Fake Store API: https://fakestoreapi.com/products
- Olist dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## Security

Credentials and environment-specific configuration must be stored in a local `.env` file and must not be committed to GitHub.

Raw datasets and processed data files are excluded from version control by default.

## Author

Edwin Leiva
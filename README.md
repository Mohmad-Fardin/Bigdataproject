# NYCRestaurantAnalytics

A big data project analyzing NYC restaurant inspection data using MongoDB.

## Overview
This project processes NYC Restaurant Inspection Results data through a big data pipeline using MongoDB. It fetches data via REST API, stores raw data (Bronze Layer), cleans it (Silver Layer), aggregates it (Gold Layer), and generates three Matplotlib visualizations to uncover insights.

## Setup
1. **Install Poetry**: `pip install poetry`
2. **Install Dependencies**: `poetry install --no-root`
3. **start poetry shell**: `poetry self add poetry-plugin-shell@latest` then `poetry shell`
4. **Run Scripts**:
   - Ingest data: `poetry run python src/ingest_data.py`
   - Clean data: `poetry run python src/clean_data.py`
   - Aggregate data: `poetry run python src/aggregate_data.py`
   - Visualize data: `poetry run python src/visualize_data.py`

## Dataset
- **Source**: NYC Open Data (https://data.cityofnewyork.us/resource/43nn-pn8j.json)
- **Format**: JSON
- **Raw Data**: 100,000 rows, 27 columns
- **Clean Data**: 33,244 rows after filtering missing fields, invalid dates, and duplicates
- **Columns**: Includes `camis`, `dba`, `boro`, `cuisine_description`, `inspection_date`, `grade`, `violation_code`, etc.

## Data Processing
- **Bronze Layer**: Ingested 100,000 raw records from the REST API into `raw_inspections`.
- **Silver Layer**: Cleaned data using MongoDB aggregation pipelines, resulting in 33,244 records in `clean_inspections`. Cleaning included:
  - Filtering records with missing critical fields.
  - Converting `inspection_date` to ISODate and removing invalid dates.
  - Standardizing `grade` to uppercase.
  - Removing duplicates based on `camis` and `inspection_date`.
- **Gold Layer**: Created three aggregated collections:
  - `grade_distribution`: 6 documents (counts of grades A, B, C, N, P, Z).
  - `violations_by_cuisine`: 10 documents (top 10 cuisines by violation count).
  - `inspections_by_year`: 11 documents (inspection counts from 2015 to 2025).

## Visualizations
1. **Grade Distribution** (`grade_distribution.png`): Bar chart showing most restaurants (25,504) received an A grade, with few (273) pending (P).
2. **Violations by Cuisine** (`violations_by_cuisine.png`): Horizontal bar chart revealing American cuisine has the highest violations (5,980), followed by Coffee/Tea (2,752).
3. **Inspections by Year** (`inspections_by_year.png`): Line chart indicating a peak in inspections in 2024 (11,060), with a sharp increase from 2021 onward.

## Submission
- **GitHub**: [Insert Public GitHub URL]
- **YouTube**: [Insert Unlisted YouTube URL]

## Experience
At the start of the semester, big data concepts like distributed databases and NoSQL were overwhelming. Working with MongoDB clarified how to handle large-scale data ingestion, cleaning, and analysis. I now feel confident using MongoDB aggregation pipelines and REST APIs, and I'm excited to apply these skills in real-world data engineering projects.
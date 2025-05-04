import requests
from pymongo import MongoClient
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_data(limit: int = 1000, offset: int = 0) -> List[Dict]:
    """Fetch data from NYC Open Data API."""
    url = f"https://data.cityofnewyork.us/resource/43nn-pn8j.json?$limit={limit}&$offset={offset}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        return []

def ingest_to_mongodb(data: List[Dict], collection) -> None:
    """Insert data into MongoDB collection."""
    if data:
        try:
            collection.insert_many(data, ordered=False)
            logger.info(f"Inserted {len(data)} records")
        except Exception as e:
            logger.error(f"Error inserting data: {e}")

def main():
    # MongoDB connection
    client = MongoClient('mongodb://localhost:27017/')
    db = client['nyc_restaurants']
    collection = db['raw_inspections']
    
    # Drop existing collection to avoid duplicates
    collection.drop()
    
    # Fetch and ingest data
    total_records = 0
    limit = 1000
    offset = 0
    target_records = 100000
    
    while total_records < target_records:
        data = fetch_data(limit, offset)
        if not data:
            break
        ingest_to_mongodb(data, collection)
        total_records += len(data)
        offset += limit
        logger.info(f"Total records ingested: {total_records}")
    
    # Verify row and column count
    row_count = collection.count_documents({})
    sample_doc = collection.find_one()
    column_count = len(sample_doc.keys()) if sample_doc else 0
    logger.info(f"Dataset: {row_count} rows, {column_count} columns")

if __name__ == "__main__":
    main()
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_data():
    """Clean raw data using MongoDB aggregation pipeline."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['nyc_restaurants']
    raw_collection = db['raw_inspections']
    clean_collection = db['clean_inspections']
    
    # Drop existing clean collection
    clean_collection.drop()
    
    # Aggregation pipeline for cleaning
    pipeline = [
        # Filter out records with missing critical fields
        {
            "$match": {
                "camis": {"$exists": True, "$ne": None},
                "inspection_date": {"$exists": True, "$ne": None},
                "grade": {"$exists": True, "$ne": None},
                "cuisine_description": {"$exists": True, "$ne": None}
            }
        },
        # Convert inspection_date to ISODate and filter valid dates
        {
            "$addFields": {
                "inspection_date": {
                    "$toDate": "$inspection_date"
                }
            }
        },
        {
            "$match": {
                "inspection_date": {"$type": "date"}
            }
        },
        # Standardize grade to uppercase
        {
            "$addFields": {
                "grade": {"$toUpper": "$grade"}
            }
        },
        # Remove duplicates based on camis and inspection_date
        {
            "$group": {
                "_id": {
                    "camis": "$camis",
                    "inspection_date": "$inspection_date"
                },
                "doc": {"$first": "$$ROOT"}
            }
        },
        # Project cleaned fields
        {
            "$replaceRoot": {"newRoot": "$doc"}
        },
        # Write to clean collection
        {
            "$out": "clean_inspections"
        }
    ]
    
    try:
        raw_collection.aggregate(pipeline)
        row_count = clean_collection.count_documents({})
        sample_doc = clean_collection.find_one()
        column_count = len(sample_doc.keys()) if sample_doc else 0
        logger.info(f"Cleaned dataset: {row_count} rows, {column_count} columns")
    except Exception as e:
        logger.error(f"Error cleaning data: {e}")

if __name__ == "__main__":
    clean_data()
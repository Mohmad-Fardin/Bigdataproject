from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def aggregate_data():
    """Create aggregated datasets using MongoDB aggregation pipelines."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['nyc_restaurants']
    clean_collection = db['clean_inspections']
    
    # Aggregation 1: Grade distribution
    grade_pipeline = [
        {
            "$group": {
                "_id": "$grade",
                "count": {"$sum": 1}
            }
        },
        {"$out": "grade_distribution"}
    ]
    
    # Aggregation 2: Violations by cuisine
    cuisine_pipeline = [
        {
            "$group": {
                "_id": "$cuisine_description",
                "total_violations": {"$sum": {"$cond": [{"$ne": ["$violation_code", None]}, 1, 0]}}
            }
        },
        {"$sort": {"total_violations": -1}},
        {"$limit": 10},
        {"$out": "violations_by_cuisine"}
    ]
    
    # Aggregation 3: Inspections by year
    year_pipeline = [
        {
            "$addFields": {
                "year": {"$year": "$inspection_date"}
            }
        },
        {
            "$group": {
                "_id": "$year",
                "inspection_count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}},
        {"$out": "inspections_by_year"}
    ]
    
    try:
        # Run aggregations
        clean_collection.aggregate(grade_pipeline)
        clean_collection.aggregate(cuisine_pipeline)
        clean_collection.aggregate(year_pipeline)
        
        # Log collection sizes
        for coll_name in ["grade_distribution", "violations_by_cuisine", "inspections_by_year"]:
            count = db[coll_name].count_documents({})
            logger.info(f"Aggregated collection {coll_name}: {count} documents")
    except Exception as e:
        logger.error(f"Error aggregating data: {e}")

if __name__ == "__main__":
    aggregate_data()
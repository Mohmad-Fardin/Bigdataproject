import matplotlib.pyplot as plt
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def plot_grade_distribution():
    """Plot distribution of inspection grades."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['nyc_restaurants']
    data = list(db['grade_distribution'].find())
    
    grades = [doc['_id'] for doc in data]
    counts = [doc['count'] for doc in data]
    
    plt.figure(figsize=(8, 6))
    plt.bar(grades, counts, color='skyblue')
    plt.title('Distribution of Restaurant Inspection Grades')
    plt.xlabel('Grade')
    plt.ylabel('Number of Inspections')
    plt.grid(True, axis='y')
    plt.savefig('grade_distribution.png')
    plt.close()
    logger.info("Generated grade_distribution.png")

def plot_violations_by_cuisine():
    """Plot top 10 cuisines by violations."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['nyc_restaurants']
    data = list(db['violations_by_cuisine'].find())
    
    cuisines = [doc['_id'] for doc in data]
    violations = [doc['total_violations'] for doc in data]
    
    plt.figure(figsize=(10, 6))
    plt.barh(cuisines, violations, color='salmon')
    plt.title('Top 10 Cuisines by Number of Violations')
    plt.xlabel('Number of Violations')
    plt.ylabel('Cuisine')
    plt.gca().invert_yaxis()
    plt.grid(True, axis='x')
    plt.savefig('violations_by_cuisine.png')
    plt.close()
    logger.info("Generated violations_by_cuisine.png")

def plot_inspections_by_year():
    """Plot inspections over time."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['nyc_restaurants']
    data = list(db['inspections_by_year'].find())
    
    years = [doc['_id'] for doc in data]
    counts = [doc['inspection_count'] for doc in data]
    
    plt.figure(figsize=(8, 6))
    plt.plot(years, counts, marker='o', color='green')
    plt.title('Number of Inspections by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Inspections')
    plt.grid(True)
    plt.savefig('inspections_by_year.png')
    plt.close()
    logger.info("Generated inspections_by_year.png")

if __name__ == "__main__":
    plot_grade_distribution()
    plot_violations_by_cuisine()
    plot_inspections_by_year()
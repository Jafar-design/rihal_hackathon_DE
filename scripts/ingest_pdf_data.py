import psycopg2
import csv

# Database connection parameters
DB_PARAMS = {
    "dbname": "analytics",
    "user": "postgres",
    "password": "postgres",
    "host": "postgres",
    "port": "5432",
}

# Drop and create table SQL
DROP_CREATE_TABLE_SQL = """
DROP TABLE IF EXISTS raw_districts CASCADE;
CREATE TABLE raw_districts (
    district_id SERIAL PRIMARY KEY,
    district_name TEXT,
    population INTEGER,
    governor TEXT
);
"""

# Read CSV and insert data
def ingest_csv_to_postgres(csv_file):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        # Drop and recreate table
        cur.execute(DROP_CREATE_TABLE_SQL)
        conn.commit()
        
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            
            for row in reader:
                cur.execute(
                    "INSERT INTO raw_districts (district_id, district_name, population, governor) VALUES (%s, %s, %s, %s)",
                    (row[0], row[1], int(row[2]), row[3])
                )
        
        conn.commit()
        cur.close()
        conn.close()
        print("PDF text Data ingested successfully!")
    except Exception as e:
        print(f"Error: {e} myerrorr?")

# Call function
# csv_ingestion = ingest_csv_to_postgres(csv_path)

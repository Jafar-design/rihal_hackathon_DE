import psycopg2
import json

DB_PARAMS = {
    "dbname": "analytics",
    "user": "postgres",
    "password": "postgres",
    "host": "postgres",
    "port": "5432",
}

TABLE_NAME = "raw_crime_reports"

# Ensure table exists (idempotent, allows NULL values)
CREATE_TABLE_SQL = f"""
DROP TABLE IF EXISTS {TABLE_NAME} CASCADE;
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id SERIAL PRIMARY KEY,
    district_id INT,
    timestamp TIMESTAMP,
    crime_type TEXT,
    nearest_police_patrol TEXT
);
"""

# Corrected INSERT statement (Removed `id`)
INSERT_SQL = f"""
INSERT INTO {TABLE_NAME} (district_id, timestamp, crime_type, nearest_police_patrol)
VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;
"""

def insert_json_data(json_file):
    with open(json_file, "r") as f:
        json_data = json.load(f)

    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    
    try:
        # Ensure table exists
        cur.execute(CREATE_TABLE_SQL)  
        conn.commit()
        
        for record in json_data:
            cur.execute(
                INSERT_SQL,
                (
                    record.get("district_id"),  # Allows NULL
                    record.get("timestamp"),  # Allows NULL
                    record.get("crime_type"),  # Allows NULL
                    record.get("nearest_police_patrol")  # Allows NULL
                )
            )
        
        conn.commit()
        print("JSON ✅ Data inserted successfully!")
    
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
    
    finally:
        cur.close()
        conn.close()



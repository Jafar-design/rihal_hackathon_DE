import psycopg2
import json

DB_PARAMS = {
    "dbname": "analytics",
    "user": "postgres",
    "password": "postgres",
    "host": "postgres",
    "port": "5432",
}

TABLE_NAME = "lms_video_data"

# Ensure table exists (idempotent, allows NULL values)
CREATE_TABLE_SQL = f"""
DROP TABLE IF EXISTS {TABLE_NAME} CASCADE;
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    student_id PRIMARY KEY,
    course_id INT,
    course_code TEXT,
    video_title TEXT,
    role TEXT,
    completion_rate_percent TEXT

);
"""

# Corrected INSERT statement (Removed `id`)
INSERT_SQL = f"""
INSERT INTO {TABLE_NAME} (student_id,course_id,course_code,video_title,role,completion_rate_percent)
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
                    record.get("student_id"),  # Allows NULL
                    record.get("course_id"),  # Allows NULL
                    record.get("course_code"),  # Allows NULL
                    record.get("video_title")  # Allows NULL
                )
            )
        
        conn.commit()
        print("JSON ✅ Data inserted successfully!")
    
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
    
    finally:
        cur.close()
        conn.close()


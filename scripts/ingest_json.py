import psycopg2
import json
import os

DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB", "analytics"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

def insert_json_data(json_file):
    with open(json_file, "r") as f:
        json_data = json.load(f)
    
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO json_data (data) VALUES (%s) ON CONFLICT (data) DO NOTHING;", [json.dumps(json_data)])
        conn.commit()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    insert_json_data("data/sample.json")

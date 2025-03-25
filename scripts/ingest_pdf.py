import psycopg2
import os
from ocr import extract_text

DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB", "analytics"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

def insert_pdf_data(pdf_file):
    with open(pdf_file, "rb") as f:
        text = extract_text(f.read())

    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO pdf_data (file_name, extracted_text) VALUES (%s, %s) ON CONFLICT (file_name) DO NOTHING;", (pdf_file, text))
        conn.commit()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    insert_pdf_data("data/sample.pdf")

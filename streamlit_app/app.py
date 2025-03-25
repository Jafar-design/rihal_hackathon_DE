import streamlit as st
import pandas as pd
import psycopg2
import os

DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB", "analytics"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

st.title("Data Analytics Dashboard")

conn = psycopg2.connect(**DB_PARAMS)
df_json = pd.read_sql("SELECT * FROM json_data", conn)
df_pdf = pd.read_sql("SELECT * FROM pdf_data", conn)
conn.close()

st.subheader("JSON Data")
st.dataframe(df_json)

st.subheader("PDF Extracted Text")
st.dataframe(df_pdf)

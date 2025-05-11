import requests
import pandas as pd
import os

def download_csv_data(url: str) -> None:
    try:
        response = requests.get(url)
        with open("dbt/seeds/lms_video_engagement.csv", "wb") as file:
            file.write(response.content)
    except requests.RequestException as e:
        print(f"Error downloading data: {e}")
    except IOError as e:
        print(f"Error writing file: {e}")


url = "https://storage.cloud.google.com/miva_data/lms_engagement_data.csv"

download_csv_data(url)

def load_csv_to_df():
    return pd.read_csv("dbt/seeds/lms_video_engagement.csv")

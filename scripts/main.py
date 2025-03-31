from ocr import get_text_from_any_pdf
from transform_districts import transform_to_csv
from ingest_pdf_data import ingest_csv_to_postgres
from load_json import insert_json_data

if __name__ == "__main__":

    path_to_pdf = '/app/data/raw/district_info.pdf'
    path_to_json = '/app/data/raw/crime_records.json'

    #Extract text from pdf
    get_pdf_text = get_text_from_any_pdf(path_to_pdf)
    # Transform to csv
    get_csv_path = transform_to_csv(get_pdf_text)
    #load csv data into database
    ingest_csv_to_postgres(get_csv_path)


    #load_json data into database
    insert_json_data(path_to_json)


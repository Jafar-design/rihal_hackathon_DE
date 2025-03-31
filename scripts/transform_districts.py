import pandas as pd
import re
import csv
#from ocr import get_text_from_any_pdf


def transform_to_csv(get_text_from_any_pdf): 

    lines = get_text_from_any_pdf.strip().split("\n")

    # Skip the first line
    lines = lines[1:]

    cleaned_data = []
    merged_line = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        line = line.replace("|", "")  # Remove '|'

        # If the line starts with a digit, it's a new entry
        if re.match(r"^\d+", line):
            if merged_line:
                cleaned_data.append(merged_line)  # Store previous entry
            merged_line = line  # Start a new entry
        else:
            merged_line += " " + line  # Append to the current entry

    # Append last merged entry
    if merged_line:
        cleaned_data.append(merged_line)

    # Process cleaned data into CSV format
    final_data = []
    for entry in cleaned_data:
        parts = entry.split()

        district_id = parts[0]  # First element is the ID

        # Find where "Al" starts (this marks the governor’s name)
        governor_index = next((i for i, word in enumerate(parts) if word.startswith("Al")), len(parts))

        # Population (salary) is right before the governor’s name
        salary = parts[governor_index - 1].replace(",", "") if governor_index > 1 else "0"

        # Governor's name starts from the first "Al"
        governor = " ".join(parts[governor_index:]) if governor_index < len(parts) else ""

        # Everything between ID and salary is the district name
        district_name = " ".join(parts[1:governor_index - 1])

        # Ensure "District" is added only once to column 2
        final_data.append([district_id, district_name + " District", salary, governor])

    # Writing to CSV
    csv_file_path = "/app/data/transformed/districts.csv"
    with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["district_id", "district_name", "Population", "governor"])  # Single correct header
        writer.writerows(final_data)

    print(f"CSV file '{csv_file_path}' has been created successfully.")


    district_csv_file = "/app/data/transformed/districts.csv"

    return district_csv_file



# Example usage
# pdf_text = get_text_from_any_pdf()
# csv_path = process_pdf_to_csv(pdf_text)

# Use official Python image
FROM python:3.9-slim

# Install system dependencies for OCR & PDF processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \ 
    poppler-utils \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Ensure the Tesseract language data exists
RUN mkdir -p /usr/share/tesseract-ocr/4.00/tessdata && \
    wget -P /usr/share/tesseract-ocr/4.00/tessdata/ \
    https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire scripts directory
COPY scripts/ /app/scripts/

# Set the Tesseract language data environment variable
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

# Set the command to run the script
CMD ["python", "/app/scripts/ocr.py"]

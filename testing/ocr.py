# import pytesseract
# from pdf2image import convert_from_bytes
# from PyPDF2 import PdfReader
# import io

# def extract_text_from_pdf(pdf_path):
#     """
#     Reads a PDF file, extracts text using OCR (for scanned PDFs) 
#     and PyPDF2 (for text-based PDFs).
    
#     :param pdf_path: Path to the PDF file
#     :return: Extracted text as a string
#     """

#     try:
#         # Open the PDF in binary mode
#         with open(pdf_path, "rb") as f:
#             pdf_bytes = f.read()

#         # Try extracting text using PyPDF2 (for searchable PDFs)
#         pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
#         text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])

#         # If PyPDF2 doesn't extract anything, use OCR as a fallback
#         if not text.strip():
#             print("Using OCR since PyPDF2 returned empty text...")
#             images = convert_from_bytes(pdf_bytes)
#             text = "\n".join([pytesseract.image_to_string(img) for img in images])

#         return text.strip()

#     except Exception as e:
#         print(f"❌ Error extracting text: {e}")
#         return ""

# # 🔹 Example Usage
# if __name__ == "__main__":
#     pdf_path = "/Users/jafarakinfenwa/Documents/code_qasr/rihal_hackathon/data/district_info.pdf"  # Change to your PDF file path
#     extracted_text = extract_text_from_pdf(pdf_path)
    

#     print("\n📜 Extracted Text:\n")
#     print(extracted_text)



from pdf2image import convert_from_path
from pytesseract import image_to_string

def convert_pdf_to_img(pdf_file):
    """
    @desc: this function converts a PDF into Image
    
    @params:
        - pdf_file: the file to be converted
    
    @returns:
        - an interable containing image format of all the pages of the PDF
    """
    return convert_from_path(pdf_file)


def convert_image_to_text(file):
    """
    @desc: this function extracts text from image
    
    @params:
        - file: the image file to extract the content
    
    @returns:
        - the textual content of single image
    """
    
    text = image_to_string(file)
    return text


def get_text_from_any_pdf(pdf_file):
    """
    @desc: this function is our final system combining the previous functions
    
    @params:
        - file: the original PDF File
    
    @returns:
        - the textual content of ALL the pages
    """
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        
        final_text += convert_image_to_text(img)
        #print("Page n°{}".format(pg))
        #print(convert_image_to_text(img))
    
    return final_text


path_to_pdf = '../data/district_info.pdf'

print(get_text_from_any_pdf(path_to_pdf))
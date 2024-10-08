import PyPDF2

def extract_text_from_pdf(pdf_file_path):
  """Extracts text from a PDF file."""

  with open(pdf_file_path, 'rb') as pdf_file:
      pdf_reader = PyPDF2.PdfReader(pdf_file)
      num_pages = len(pdf_reader.pages)
      text = ""
      for page_num in range(num_pages):
          page = pdf_reader.pages[page_num]
          text += page.extract_text()
  return text

# Replace 'your_dtc_error_codes.pdf' with your actual PDF file path
pdf_text = extract_text_from_pdf('data/DTC_Codes-m.pdf')

# print the extracted text
# print(pdf_text)
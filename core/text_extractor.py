import os
import fitz
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from colorama import Fore, Style, init

init(autoreset=True)

# Base dir of project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to portable tesseract binary
tesseract_bin = os.path.join(BASE_DIR, "core", "tesseract", "tesseract")  # on Linux: "tesseract"
tessdata_dir = os.path.join(BASE_DIR, "core", "tesseract", "tessdata")

# If portable version exists, configure pytesseract
if os.path.exists(tesseract_bin):
    pytesseract.pytesseract.tesseract_cmd = tesseract_bin
    os.environ["TESSDATA_PREFIX"] = tessdata_dir
    print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} Using portable Tesseract at {tesseract_bin}")

def extract_pdf_native(pdf_path):
    """Extract native text from a PDF using PyMuPDF."""
    text = []
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text.append(page.get_text("text"))
        doc.close()
    except Exception as e:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Native PDF reading failed {pdf_path}: {e}")
    return "\n".join(text)

def extract_pdf_ocr(pdf_path):
    """OCR on a PDF by converting pages to images."""
    text = []
    try:
        pages = convert_from_path(pdf_path)
        for p in pages:
            text.append(pytesseract.image_to_string(p))
    except Exception as e:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} OCR on PDF failed {pdf_path}: {e}")
    return "\n".join(text)

def extract_image(img_path):
    """OCR on image files."""
    try:
        img = Image.open(img_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} OCR on image failed {img_path}: {e}")
        return ""

def extract_text(file_path):
    """Decide the extraction method based on file extension."""
    if file_path.lower().endswith(".pdf"):
        text = extract_pdf_native(file_path)
        if not text.strip():  # fallback to OCR if native text is empty
            text = extract_pdf_ocr(file_path)
        return text
    else:
        return extract_image(file_path)

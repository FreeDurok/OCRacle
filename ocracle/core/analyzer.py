import os
import fitz
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from ocracle.utils import logger


class FileAnalyzer:
    """Responsible for text extraction from PDF and images, using native and OCR."""

    def __init__(self):
        # Setup tesseract portable configuration
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tesseract_bin = os.path.join(BASE_DIR, "core", "tesseract", "tesseract")
        tessdata_dir = os.path.join(BASE_DIR, "core", "tesseract", "tessdata")
        tesseract_lib_dir = os.path.join(BASE_DIR, "core", "tesseract", "lib")

        if os.path.exists(tesseract_bin):
            pytesseract.pytesseract.tesseract_cmd = tesseract_bin
            os.environ["TESSDATA_PREFIX"] = tessdata_dir
            if os.path.exists(tesseract_lib_dir):
                current_ld = os.environ.get("LD_LIBRARY_PATH", "")
                os.environ["LD_LIBRARY_PATH"] = f"{tesseract_lib_dir}:{current_ld}"
            logger.success_block(f"Using portable Tesseract at {tesseract_bin}")

    def extract_pdf_native(self, pdf_path: str) -> str:
        """Extract native text from a PDF using PyMuPDF."""
        text = []
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                text.append(page.get_text("text"))
            doc.close()
        except Exception as e:
            logger.error(f"Native PDF reading failed {pdf_path}: {e}")
        return "\n".join(text)

    def extract_pdf_ocr(self, pdf_path: str) -> str:
        """OCR on a PDF by converting pages to images."""
        text = []
        try:
            pages = convert_from_path(pdf_path)
            for p in pages:
                text.append(pytesseract.image_to_string(p))
        except Exception as e:
            logger.error(f"OCR on PDF failed {pdf_path}: {e}")
        return "\n".join(text)

    def extract_image(self, img_path: str) -> str:
        """OCR on image files."""
        try:
            img = Image.open(img_path)
            return pytesseract.image_to_string(img)
        except Exception as e:
            logger.error(f"OCR on image failed {img_path}: {e}")
            return ""

    def extract_text(self, file_path: str, file_type: str) -> str:
        """
        Extract text based on the file type (detected via magic bytes).
        :param file_path: Path to file
        :param file_type: Detected type, e.g., 'pdf', 'png', 'jpg', 'tiff'
        """
        if file_type == "pdf":
            text = self.extract_pdf_native(file_path)
            if not text.strip():
                text = self.extract_pdf_ocr(file_path)
            return text
        else:
            # All image formats are handled the same way
            return self.extract_image(file_path)

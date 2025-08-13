import fitz
import pytesseract

from PIL import Image

from src.settings.settings import PDFExtractorSettings

class PDFExtractor:
    
    def __init__(self):
        pass
    
    def extract_from_path(self, pdf_path: str):
        extracted_texts = self.__pdf_to_text_direct(pdf_path)
        if extracted_texts:
            return (extracted_texts, False)
        
        return (self.__pdf_to_text_deeply(pdf_path), True)
    
    def __pdf_to_text_direct(self, pdf_path):
        doc = fitz.open(pdf_path)
        extracted_texts = ""
        for page in doc:
            extracted_texts += page.get_text("text")
        return extracted_texts
    
    def __pdf_to_text_deeply(self, pdf_path, zoom=PDFExtractorSettings.ZOOM_CONST):
        doc = fitz.open(pdf_path)
        extracted_texts = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            matrix = fitz.Matrix(zoom, zoom)  # Apply zoom
            pix = page.get_pixmap(matrix=matrix)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)
            extracted_texts += f"\n{text}"
        
        return extracted_texts

import pymupdf
import pytesseract
from PIL import Image
import io
import sys

# Configure tesseract path if needed, usually on PATH in scoop
# pytesseract.pytesseract.tesseract_cmd = r'tesseract'

pdf_path = "1283-tu-dien-tu-vi-dau-so-va-than-so-hoc-thuviensach.vn.pdf"
output_path = "1283-tu-dien-tu-vi-dau-so-va-than-so-hoc-thuviensach.vn_ocr.txt"

try:
    doc = pymupdf.open(pdf_path)
except Exception as e:
    print(f"Error opening PDF: {e}")
    sys.exit(1)

total_pages = len(doc)
print(f"Total pages: {total_pages}")

with open(output_path, "w", encoding="utf-8") as out_f:
    for page_num in range(total_pages):
        page = doc.load_page(page_num)
        
        # Render page to image at 200 DPI
        pix = page.get_pixmap(dpi=200)
        
        # Convert pixmap to PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # OCR with Tesseract
        try:
            text = pytesseract.image_to_string(img, lang="vie")
        except Exception as e:
            print(f"Error OCRing page {page_num + 1}: {e}")
            text = "[OCR ERROR]"
        
        out_f.write(f"--- Trang {page_num + 1} ---\n")
        out_f.write(text)
        out_f.write("\n\n")
        
        if (page_num + 1) % 10 == 0 or (page_num + 1) == total_pages:
            print(f"Processed page {page_num + 1}/{total_pages}")

print(f"OCR process completed. Output saved to {output_path}")

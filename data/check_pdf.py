import sys
sys.stdout.reconfigure(encoding='utf-8')

def check_pdf(file_path):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF (fitz) is not installed. Please run: pip install PyMuPDF")
        return

    print(f"--- Checking: {file_path} ---")
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return

    print(f"Pages: {doc.page_count}")
    
    # Check for text layer by analyzing the first few pages
    has_text = False
    for i in range(min(5, doc.page_count)):
        page = doc[i]
        text = page.get_text()
        if text.strip():
            has_text = True
            break
            
    print(f"Has Text Layer (like pdffonts/pdftotext): {has_text}")
    
    if has_text:
        print("Extracting sample text from page 5 (if exists) or middle page:")
        mid_idx = min(5, doc.page_count - 1)
        if mid_idx >= 0:
            sample_page = doc[mid_idx]
            print(sample_page.get_text("text")[:1000])  # Print first 1000 chars of text
    else:
        print("No text layer detected. This might be a scanned PDF (requires pdftoppm/rasterization).")
    
    doc.close()
    print("\n")

if __name__ == "__main__":
    check_pdf(r"D:\All Code\New folder\Numerology_Project\data\(boitoan)-Tử Vi Đầu Số Tân Biên - Vân Đằng Thái Thứ Lang-dantocking.com.pdf")
    check_pdf(r"D:\All Code\New folder\Numerology_Project\data\Tử Vi Đẩu Số Toàn Thư.pdf")

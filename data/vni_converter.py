import sys
import pymupdf

sys.stdout.reconfigure(encoding='utf-8')

def check_fonts(file_path):
    print(f"--- Fonts in: {file_path} ---")
    doc = pymupdf.open(file_path)
    # Get fonts from first 5 pages
    fonts = set()
    for i in range(min(5, doc.page_count)):
        page_fonts = doc[i].get_fonts()
        for font in page_fonts:
            fonts.add(font[3]) # Font name
    
    for f in fonts:
        print(f)
    doc.close()

if __name__ == "__main__":
    check_fonts(r"D:\All Code\New folder\Numerology_Project\data\Tử Vi Đẩu Số Toàn Thư.pdf")

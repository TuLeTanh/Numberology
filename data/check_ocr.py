import re

with open('1283-tu-dien-tu-vi-dau-so-va-than-so-hoc-thuviensach.vn_ocr.txt', 'r', encoding='utf-8') as f:
    content = f.read()

pages = re.split(r'--- Trang (\d+) ---', content)
if not pages[0].strip():
    pages = pages[1:]

suspicious_pages = []

for i in range(0, len(pages), 2):
    page_num = pages[i]
    text = pages[i+1].strip()
    
    if not text:
        suspicious_pages.append((page_num, "Trang trống"))
        continue
    
    # Calculate ratio of special characters
    special_chars = len(re.findall(r'[^a-zA-ZÀ-ỹ0-9\s.,?!;:()\[\]"\'-]', text))
    total_chars = len(text)
    
    # Calculate number of very short or weird words
    words = text.split()
    if len(words) == 0:
        continue
        
    weird_words = len([w for w in words if re.search(r'[^a-zA-ZÀ-ỹ0-9\.,?!]', w)])
    
    if special_chars > total_chars * 0.05 and total_chars > 50:
        suspicious_pages.append((page_num, f"Nhiều ký tự lạ (Tỷ lệ: {special_chars/total_chars:.1%})"))
    elif len(words) > 10 and weird_words > len(words) * 0.15:
        suspicious_pages.append((page_num, f"Nhiều từ bị lỗi (Tỷ lệ: {weird_words/len(words):.1%})"))

print(f"Total pages: {len(pages)//2}")
if suspicious_pages:
    print("Pages with potential OCR errors:")
    for p, reason in suspicious_pages:
        print(f"- Page {p}: {reason}")
else:
    print("No pages with obvious OCR errors found.")

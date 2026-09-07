import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def get_paragraphs(file_path, keywords):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    pages = text.split('--- Page ')
    results = {kw: [] for kw in keywords}
    
    for p in pages[1:]:
        page_num = p.split('\n')[0].strip()
        paragraphs = p.split('\n\n')
        for para in paragraphs:
            para = para.replace('\n', ' ')
            para_lower = para.lower()
            for kw in keywords:
                if re.search(r'\b' + kw.lower() + r'\b', para_lower):
                    if len(para) > 30 and para not in [x[1] for x in results[kw]]:
                        results[kw].append((page_num, para))
    return results

kws = [
    'cục', 'tử vi', 'thiên phủ',
    'liêm trinh', 'lộc tồn', 'tả phù', 'thái âm', 'thái dương',
    'hữu bật', 'văn xương', 'văn khúc', 'thiên khôi', 'thiên việt',
    'kình dương', 'đà la', 'hoả tinh', 'linh tinh',
    'địa không', 'địa kiếp', 'hoá lộc', 'hoá quyền',
    'hoá khoa', 'hoá kỵ', 'tứ hoá', 'hóa lộc', 'hóa quyền', 'hóa khoa', 'hóa kỵ', 'tứ hóa'
]

tb = get_paragraphs('tan_bien.txt', kws)
tt = get_paragraphs('toan_thu_unicode.txt', kws)

with open('formulas_dump.txt', 'w', encoding='utf-8') as f:
    for kw in kws:
        f.write(f"\n\n{'='*50}\nKEYWORD: {kw.upper()}\n{'='*50}\n")
        f.write("\n--- TÂN BIÊN ---\n")
        for page, para in tb[kw][:8]: # Limit to first 8 matches to avoid too much noise
            f.write(f"[Page {page}] {para}\n")
        f.write("\n--- TOÀN THƯ ---\n")
        for page, para in tt[kw][:8]:
            f.write(f"[Page {page}] {para}\n")

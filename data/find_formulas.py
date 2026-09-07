import sys

sys.stdout.reconfigure(encoding='utf-8')

def find_keywords(file_path, keywords):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    matches = {kw: [] for kw in keywords}
    
    pages = text.split('--- Page ')
    for p in pages[1:]:
        lines = p.split('\n')
        page_num = lines[0].strip()
        page_text = '\n'.join(lines[1:])
        
        for kw in keywords:
            if kw.lower() in page_text.lower():
                matches[kw].append(page_num)
                
    return matches

kws = [
    "An tinh pháp", "Cách an", "An sao", "Lập thành", 
    "Cục số", "Khởi vòng Tử Vi", "Khởi vòng Thiên Phủ",
    "Tả Phù", "Hữu Bật", "Lộc Tồn", "Kình Dương", "Đà La",
    "Hỏa Tinh", "Linh Tinh", "Địa Không", "Địa Kiếp",
    "Văn Xương", "Văn Khúc", "Thiên Khôi", "Thiên Việt",
    "Hóa Lộc", "Hóa Quyền", "Hóa Khoa", "Hóa Kỵ", "Tứ Hóa"
]

print("=== TÂN BIÊN ===")
tb = find_keywords('tan_bien.txt', kws)
for k, v in tb.items():
    print(f"{k}: {', '.join(v)}")
    
print("\n=== TOÀN THƯ ===")
tt = find_keywords('toan_thu_unicode.txt', kws)
for k, v in tt.items():
    print(f"{k}: {', '.join(v)}")

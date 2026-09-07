import sys, re

def find_context(file_path, keywords):
    with open(file_path, 'r', encoding='utf-8') as f: text = f.read()
    results = []
    pages = text.split('--- Page ')
    for p in pages[1:]:
        pnum = p.split('\n')[0].strip()
        for para in p.split('\n\n'):
            para = para.replace('\n', ' ')
            if all(kw.lower() in para.lower() for kw in keywords):
                results.append(f'[Page {pnum}] {para[:300]}')
    return results

out = []
out.append("=== TỨ HÓA CANH ===")
out.extend(find_context('tan_bien.txt', ['Hóa', 'Canh']))
out.extend(find_context('toan_thu_unicode.txt', ['Hoá', 'Canh']))
out.extend(find_context('toan_thu_unicode.txt', ['Hoá', 'Nhật', 'Vũ']))

out.append("=== HỎA LINH ===")
out.extend(find_context('tan_bien.txt', ['Hỏa', 'Dần', 'Tuất']))
out.extend(find_context('toan_thu_unicode.txt', ['Hoả', 'Dần', 'Tuất']))

out.append("=== KHÔI VIỆT ===")
out.extend(find_context('tan_bien.txt', ['Khôi', 'Ngưu']))
out.extend(find_context('toan_thu_unicode.txt', ['Khôi', 'Ngưu']))

out.append("=== KÌNH ĐÀ ===")
out.extend(find_context('tan_bien.txt', ['Kình Dương', 'Lộc Tồn']))
out.extend(find_context('toan_thu_unicode.txt', ['Kình Dương', 'Lộc Tồn']))

out.append("=== TỬ VI ===")
out.extend(find_context('toan_thu_unicode.txt', ['Tử Vi', 'Cục']))

out.append("=== ĐỊA KHÔNG KIẾP ===")
out.extend(find_context('tan_bien.txt', ['Địa Không', 'Hợi']))
out.extend(find_context('toan_thu_unicode.txt', ['Không', 'Kiếp', 'Hợi']))

with open('differences.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

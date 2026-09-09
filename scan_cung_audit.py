import sys
import os
import json
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

counts = Counter()
cung_to_samples = {}
sao_dir = 'sao_json'
file_count = 0

for fname in os.listdir(sao_dir):
    if fname.endswith('.json'):
        file_count += 1
        fpath = os.path.join(sao_dir, fname)
        try:
            with open(fpath, encoding='utf-8') as f:
                d = json.load(f)
                sao_name = d.get('sao', fname)
                for entry in d.get('y_nghia_theo_cung', []):
                    cung_val = entry.get('cung')
                    counts[cung_val] += 1
                    if cung_val not in cung_to_samples:
                        cung_to_samples[cung_val] = (sao_name, entry.get('dien_giai', ''))
        except Exception as e:
            print(f"Lỗi đọc {fname}: {e}")

print(f"Tổng số file JSON quét được: {file_count}")
print(f"Tổng số entry diễn giải theo cung: {sum(counts.values())}")
print(f"Số giá trị unique của trường 'cung': {len(counts)}\n")

print("Danh sách chi tiết từng giá trị 'cung' và số lượng entry:")
for c, cnt in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  - \"{c}\": {cnt} entries")

print("\n--- Chi tiết TOÀN BỘ 8 entry có cung='Giải' ---")
for fname in os.listdir(sao_dir):
    if fname.endswith('.json'):
        fpath = os.path.join(sao_dir, fname)
        with open(fpath, encoding='utf-8') as f:
            d = json.load(f)
            sao_name = d.get('sao', fname)
            for entry in d.get('y_nghia_theo_cung', []):
                if entry.get('cung') == 'Giải':
                    print(f"- Sao '{sao_name}' (file {fname}):")
                    print(f"  \"{entry.get('dien_giai')}\"")


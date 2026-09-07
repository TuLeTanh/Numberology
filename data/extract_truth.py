import json
import os
import re

def extract_project_truth():
    stars = [
        "tử_vi", "thiên_phủ", "liêm_trinh", "lộc_tồn", "tả_phù", "thái_âm", "thái_dương",
        "hữu_bật", "văn_xương", "văn_khúc", "thiên_khôi", "thiên_việt", "kình_dương_hay_dương_nhân", "đà_la",
        "hỏa_tinh", "linh_tinh", "địa_không", "địa_kiếp", "hóa_lộc", "hóa_quyền", "hóa_khoa", "hóa_kỵ",
        "đào_hoa", "hồng_loan", "thiên_hỷ"
    ]
    
    print("=== PROJECT GROUND TRUTH ===")
    out = []
    for s in stars:
        path = os.path.join(r"D:\All Code\New folder\Numerology_Project\sao_json", s + ".json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                rule = data.get('cach_an', data.get('logic', ''))
                out.append(f"{s}: {rule}")
        else:
            out.append(f"Not found: {path}")
    
    with open('truth_out.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))

if __name__ == '__main__':
    extract_project_truth()

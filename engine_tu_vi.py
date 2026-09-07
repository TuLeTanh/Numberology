import json
import os

CHI_MAP = {
    0: "Tý", 1: "Sửu", 2: "Dần", 3: "Mão", 4: "Thìn", 5: "Tỵ",
    6: "Ngọ", 7: "Mùi", 8: "Thân", 9: "Dậu", 10: "Tuất", 11: "Hợi"
}
NAME_TO_CHI = {v: k for k, v in CHI_MAP.items()}

# Tải bang_tu_vi.json vào bộ nhớ (in-memory)
_tu_vi_map = None

def get_tu_vi_map():
    global _tu_vi_map
    if _tu_vi_map is None:
        file_path = os.path.join(os.path.dirname(__file__), 'bang_tu_vi.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            _tu_vi_map = json.load(f)
    return _tu_vi_map

def an_14_chinh_tinh(cuc: str, ngay_sinh_am: int) -> dict:
    tu_vi_map = get_tu_vi_map()
    
    if cuc not in tu_vi_map:
        raise ValueError(f"Cục '{cuc}' không hợp lệ. Phải là một trong các cục chuẩn.")
    
    # BƯỚC 1 - Tra cung Tử Vi
    cung_tu_vi_name = None
    for cung_name, days in tu_vi_map[cuc].items():
        if ngay_sinh_am in days:
            cung_tu_vi_name = cung_name
            break
            
    if cung_tu_vi_name is None:
        raise ValueError(f"Ngày sinh {ngay_sinh_am} không hợp lệ hoặc không có trong {cuc}.")
        
    tv = NAME_TO_CHI[cung_tu_vi_name]
    
    sao_dict = {}
    
    # BƯỚC 2 - Tính 5 sao nhóm Tử Vi
    sao_dict['Tử Vi'] = tv
    sao_dict['Liêm Trinh'] = (tv + 4) % 12
    sao_dict['Thiên Đồng'] = (tv + 7) % 12
    sao_dict['Vũ Khúc'] = (tv + 8) % 12
    sao_dict['Thái Dương'] = (tv + 9) % 12
    sao_dict['Thiên Cơ'] = (tv + 11) % 12
    
    # BƯỚC 3 - Tính Thiên Phủ + 7 sao nhóm Thiên Phủ
    tp = (16 - tv) % 12
    
    sao_dict['Thiên Phủ'] = tp
    sao_dict['Thái Âm'] = (tp + 1) % 12
    sao_dict['Tham Lang'] = (tp + 2) % 12
    sao_dict['Cự Môn'] = (tp + 3) % 12
    sao_dict['Thiên Tướng'] = (tp + 4) % 12
    sao_dict['Thiên Lương'] = (tp + 5) % 12
    sao_dict['Thất Sát'] = (tp + 6) % 12
    sao_dict['Phá Quân'] = (tp + 10) % 12
    
    return sao_dict

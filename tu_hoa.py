import json
import os
from engine_tu_vi import CAN_MAP

# Tải tu_hoa_bang_chuan.json vào bộ nhớ (in-memory)
_tu_hoa_map = None

def get_tu_hoa_map():
    global _tu_hoa_map
    if _tu_hoa_map is None:
        file_path = os.path.join(os.path.dirname(__file__), 'sao_json', 'tu_hoa_bang_chuan.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            _tu_hoa_map = json.load(f)
    return _tu_hoa_map

def get_tu_hoa(can_nam_index: int) -> dict:
    """
    Trả về Tứ Hóa cho Can Năm tương ứng.
    Input: can_nam_index (0-9) tương ứng Giáp-Quý.
    Output: {"Hóa Lộc": "<sao>", "Hóa Quyền": "<sao>", "Hóa Khoa": "<sao>", "Hóa Kỵ": "<sao>"}
    """
    if not (0 <= can_nam_index <= 9):
        raise ValueError(f"can_nam_index = {can_nam_index} không hợp lệ. Phải từ 0 đến 9.")
        
    can_name = CAN_MAP[can_nam_index]
    
    tu_hoa_map = get_tu_hoa_map()
    if can_name not in tu_hoa_map:
        raise ValueError(f"Không tìm thấy cấu hình Tứ Hóa cho Can '{can_name}'.")
        
    th_data = tu_hoa_map[can_name]
    
    return {
        "Hóa Lộc": th_data["HoaLoc"],
        "Hóa Quyền": th_data["HoaQuyen"],
        "Hóa Khoa": th_data["HoaKhoa"],
        "Hóa Kỵ": th_data["HoaKy"]
    }

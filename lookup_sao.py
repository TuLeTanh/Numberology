"""
lookup_sao.py — Phase 2: Lớp tra cứu diễn giải sao

load_sao_data() : Đọc toàn bộ sao_json/, trả dict {ten_sao: {...}}
get_dien_giai_sao() : Tra cứu diễn giải (sao, cung), O(1)
"""
import json
import os

_SAO_DIR = os.path.join(os.path.dirname(__file__), "sao_json")

def load_sao_data(sao_dir: str = _SAO_DIR) -> dict:
    """
    Đọc toàn bộ file JSON trong sao_dir, gộp thành dict:
        {TEN_SAO_UPPER: {toàn bộ nội dung file}}
    Key được chuẩn hoá UPPER để tránh sai lệch hoa/thường giữa các file.
    Caller dùng get_dien_giai_sao() — hàm đó tự upper key khi tra.
    """
    sao_data = {}
    for fname in os.listdir(sao_dir):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(sao_dir, fname)
        try:
            with open(fpath, encoding="utf-8") as f:
                data = json.load(f)
            ten_sao = data.get("sao")
            if ten_sao:
                sao_data[ten_sao.upper()] = data
        except Exception as e:
            print(f"[load_sao_data] Bỏ qua {fname}: {e}")
    return sao_data


CUNG_ALIASES = {
    "Quan Lộc": ["Quan Lộc", "Quan"],
    "Tài Bạch": ["Tài Bạch", "Tài"],
    "Điền Trạch": ["Điền Trạch", "Điền"],
    "Phúc Đức": ["Phúc Đức", "Phúc"],
    "Phu Thê": ["Phu Thê", "Thê", "Phu"],
    "Tử Tức": ["Tử Tức", "Tử"],
    "Nô Bộc": ["Nô Bộc", "Nô"],
    "Huynh Đệ": ["Huynh Đệ", "Bào", "Huynh"],
    "Tật Ách": ["Tật Ách", "Giải", "Ách"],
    "Phụ Mẫu": ["Phụ Mẫu", "Phụ"],
    "Mệnh": ["Mệnh"],
    "Thiên Di": ["Thiên Di", "Di"],
    "Thân": ["Thân"],
}


_cached_sao_data = None

def get_sao_db() -> dict:
    """Trả về sao_data đã nạp vào bộ nhớ (singleton/cached)."""
    global _cached_sao_data
    if not _cached_sao_data:
        _cached_sao_data = load_sao_data()
    return _cached_sao_data


def get_dien_giai_sao(sao_data: dict | None, ten_sao: str, ten_cung: str):
    """
    Tra cứu diễn giải của một sao tại một cung.
    Key tra cứu được upper() tự động để khớp với DB.
    Hỗ trợ alias tên cung viết tắt trong sách cổ (Quan -> Quan Lộc, Thê -> Phu Thê...).
    Nếu sao_data là None hoặc rỗng, tự động dùng get_sao_db().

    Parameters
    ----------
    sao_data  : dict trả về bởi load_sao_data() hoặc None
    ten_sao   : tên sao (e.g. "Tử Vi", "TỬ VI" — đều OK)
    ten_cung  : tên cung đúng chuẩn (e.g. "Mệnh", "Phu Thê", "Quan Lộc")

    Returns
    -------
    str   nếu tìm thấy đầy đủ
    None  nếu không có dữ liệu diễn giải cho cung đó
    dict  {"error": "..."} nếu sao không tồn tại trong db
    """
    if not sao_data:
        sao_data = get_sao_db()

    key = ten_sao.upper()
    if key not in sao_data:
        return {"error": f"Không có dữ liệu cho sao '{ten_sao}'"}

    valid_names = set(CUNG_ALIASES.get(ten_cung, [ten_cung]))
    valid_names.add(ten_cung)

    y_nghia_list = sao_data[key].get("y_nghia_theo_cung", [])
    for entry in y_nghia_list:
        if entry.get("cung") in valid_names:
            return entry.get("dien_giai")

    return None


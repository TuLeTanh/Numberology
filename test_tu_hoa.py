import pytest
from tu_hoa import get_tu_hoa

@pytest.mark.parametrize("can_index, expected", [
    (0, {"Hóa Lộc": "Liêm Trinh", "Hóa Quyền": "Phá Quân", "Hóa Khoa": "Vũ Khúc", "Hóa Kỵ": "Thái Dương"}), # Giáp
    (1, {"Hóa Lộc": "Thiên Cơ", "Hóa Quyền": "Thiên Lương", "Hóa Khoa": "Tử Vi", "Hóa Kỵ": "Thái Âm"}), # Ất
    (2, {"Hóa Lộc": "Thiên Đồng", "Hóa Quyền": "Thiên Cơ", "Hóa Khoa": "Văn Xương", "Hóa Kỵ": "Liêm Trinh"}), # Bính
    (3, {"Hóa Lộc": "Thái Âm", "Hóa Quyền": "Thiên Đồng", "Hóa Khoa": "Thiên Cơ", "Hóa Kỵ": "Cự Môn"}), # Đinh
    
    # Lệch phái: Mậu (Trung Châu Phái: Thái Dương Hóa Khoa)
    (4, {"Hóa Lộc": "Tham Lang", "Hóa Quyền": "Thái Âm", "Hóa Khoa": "Thái Dương", "Hóa Kỵ": "Thiên Cơ"}), # Mậu
    
    (5, {"Hóa Lộc": "Vũ Khúc", "Hóa Quyền": "Tham Lang", "Hóa Khoa": "Thiên Lương", "Hóa Kỵ": "Văn Khúc"}), # Kỷ
    
    # Lệch phái: Canh (Trung Châu Phái: Thiên Phủ Hóa Khoa)
    (6, {"Hóa Lộc": "Thái Dương", "Hóa Quyền": "Vũ Khúc", "Hóa Khoa": "Thiên Phủ", "Hóa Kỵ": "Thiên Đồng"}), # Canh
    
    (7, {"Hóa Lộc": "Cự Môn", "Hóa Quyền": "Thái Dương", "Hóa Khoa": "Văn Khúc", "Hóa Kỵ": "Văn Xương"}), # Tân
    
    # Lệch phái: Nhâm (Trung Châu Phái: Thiên Phủ Hóa Khoa)
    (8, {"Hóa Lộc": "Thiên Lương", "Hóa Quyền": "Tử Vi", "Hóa Khoa": "Thiên Phủ", "Hóa Kỵ": "Vũ Khúc"}), # Nhâm
    
    (9, {"Hóa Lộc": "Phá Quân", "Hóa Quyền": "Cự Môn", "Hóa Khoa": "Thái Âm", "Hóa Kỵ": "Tham Lang"}), # Quý
])
def test_get_tu_hoa_valid(can_index, expected):
    """
    Kiểm tra chức năng lấy Tứ Hóa cho 10 Can.
    Bao gồm cả 3 Can lệch phái (Mậu, Canh, Nhâm) được map đúng theo chuẩn Trung Châu Phái.
    """
    assert get_tu_hoa(can_index) == expected

def test_get_tu_hoa_invalid():
    """Kiểm tra xử lý lỗi khi can_nam_index ngoài khoảng 0-9"""
    with pytest.raises(ValueError):
        get_tu_hoa(10)
    with pytest.raises(ValueError):
        get_tu_hoa(-1)

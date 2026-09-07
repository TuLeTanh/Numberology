import pytest
from engine_tu_vi import an_14_chinh_tinh

def test_moc_tam_cuc_ngay_15():
    # Case 1: Mộc Tam Cục, Ngày 15
    # Tử Vi = Ngọ (6), Thiên Phủ = Tuất (10)
    res = an_14_chinh_tinh("Mộc Tam Cục", 15)
    
    # Vòng Tử Vi
    assert res["Tử Vi"] == 6      # Ngọ
    assert res["Liêm Trinh"] == 10 # Tuất
    assert res["Thiên Đồng"] == 1  # Sửu
    assert res["Vũ Khúc"] == 2    # Dần
    assert res["Thái Dương"] == 3 # Mão
    assert res["Thiên Cơ"] == 5    # Tỵ
    
    # Vòng Thiên Phủ
    assert res["Thiên Phủ"] == 10  # Tuất
    assert res["Thái Âm"] == 11   # Hợi
    assert res["Tham Lang"] == 0   # Tý
    assert res["Cự Môn"] == 1     # Sửu
    assert res["Thiên Tướng"] == 2 # Dần
    assert res["Thiên Lương"] == 3 # Mão
    assert res["Thất Sát"] == 4    # Thìn
    assert res["Phá Quân"] == 8    # Thân
    
def test_kim_tu_cuc_ngay_24():
    # Case 2: Kim Tứ Cục, Ngày 24 (Ngày bị lỗi OCR, đã sửa)
    # Tử Vi = Mùi (7), Thiên Phủ = Dậu (9)
    res = an_14_chinh_tinh("Kim Tứ Cục", 24)
    
    # Vòng Tử Vi
    assert res["Tử Vi"] == 7
    assert res["Liêm Trinh"] == 11
    assert res["Thiên Đồng"] == 2
    assert res["Vũ Khúc"] == 3
    assert res["Thái Dương"] == 4
    assert res["Thiên Cơ"] == 6
    
    # Vòng Thiên Phủ
    assert res["Thiên Phủ"] == 9
    assert res["Thái Âm"] == 10
    assert res["Tham Lang"] == 11
    assert res["Cự Môn"] == 0
    assert res["Thiên Tướng"] == 1
    assert res["Thiên Lương"] == 2
    assert res["Thất Sát"] == 3
    assert res["Phá Quân"] == 7    # Phá Quân đồng cung Tử Vi tại Mùi (7)

def test_thuy_nhi_cuc_ngay_7():
    # Case 3: Thủy Nhị Cục, Ngày 7
    # Tính tay: (7+1=8)/2=4 (Tỵ). X=1 (Lẻ) -> lùi 1 -> Thìn (4).
    # Tử Vi = Thìn (4), Thiên Phủ = (16-4)%12 = Tý (0)
    res = an_14_chinh_tinh("Thủy Nhị Cục", 7)
    
    assert res["Tử Vi"] == 4
    assert res["Liêm Trinh"] == 8
    assert res["Thiên Đồng"] == 11
    assert res["Vũ Khúc"] == 0
    assert res["Thái Dương"] == 1
    assert res["Thiên Cơ"] == 3
    
    assert res["Thiên Phủ"] == 0
    assert res["Thái Âm"] == 1
    assert res["Tham Lang"] == 2
    assert res["Cự Môn"] == 3
    assert res["Thiên Tướng"] == 4 # Tướng đồng cung Tử Vi tại Thìn
    assert res["Thiên Lương"] == 5
    assert res["Thất Sát"] == 6
    assert res["Phá Quân"] == 10

def test_tho_ngu_cuc_ngay_14():
    # Case 4: Thổ Ngũ Cục, Ngày 14
    # Tính tay: (14+1=15)/5=3 (Thìn). X=1 (Lẻ) -> lùi 1 -> Mão (3).
    # Tử Vi = Mão (3), Thiên Phủ = (16-3)%12 = Sửu (1)
    res = an_14_chinh_tinh("Thổ Ngũ Cục", 14)
    
    assert res["Tử Vi"] == 3
    assert res["Liêm Trinh"] == 7
    assert res["Thiên Đồng"] == 10
    assert res["Vũ Khúc"] == 11
    assert res["Thái Dương"] == 0
    assert res["Thiên Cơ"] == 2
    
    assert res["Thiên Phủ"] == 1
    assert res["Thái Âm"] == 2
    assert res["Tham Lang"] == 3 # Tham Lang đồng cung Tử Vi tại Mão
    assert res["Cự Môn"] == 4
    assert res["Thiên Tướng"] == 5
    assert res["Thiên Lương"] == 6
    assert res["Thất Sát"] == 7
    assert res["Phá Quân"] == 11

def test_hoa_luc_cuc_ngay_11():
    # Case 5: Hỏa Lục Cục, Ngày 11
    # Tính tay: (11+1=12)/6=2 (Mão). X=1 (Lẻ) -> lùi 1 -> Dần (2).
    # Tử Vi = Dần (2), Thiên Phủ = (16-2)%12 = Dần (2)
    res = an_14_chinh_tinh("Hỏa Lục Cục", 11)
    
    assert res["Tử Vi"] == 2
    assert res["Liêm Trinh"] == 6
    assert res["Thiên Đồng"] == 9
    assert res["Vũ Khúc"] == 10
    assert res["Thái Dương"] == 11
    assert res["Thiên Cơ"] == 1
    
    assert res["Thiên Phủ"] == 2 # Phủ đồng cung Tử Vi tại Dần
    assert res["Thái Âm"] == 3
    assert res["Tham Lang"] == 4
    assert res["Cự Môn"] == 5
    assert res["Thiên Tướng"] == 6
    assert res["Thiên Lương"] == 7
    assert res["Thất Sát"] == 8
    assert res["Phá Quân"] == 0

def test_invalid_day():
    # Should raise error for non-existent day
    with pytest.raises(ValueError, match="không hợp lệ"):
        an_14_chinh_tinh("Kim Tứ Cục", 31)

def test_invalid_cuc():
    # Should raise error for non-existent Cục
    with pytest.raises(ValueError, match="không hợp lệ"):
        an_14_chinh_tinh("Vô Cực Cục", 1)

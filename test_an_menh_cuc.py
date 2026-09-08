import pytest
from an_menh_cuc import get_cung_menh, get_can_cung, get_cuc_tu_nap_am, get_cuc_and_menh

def test_cung_menh():
    # Ví dụ Ất Mùi (tháng 4, giờ Thìn=4) -> Cung Sửu=1
    assert get_cung_menh(4, 4) == 1
    # Ví dụ Đinh Dậu (tháng 10, giờ Ngọ=6) -> Cung Tỵ=5
    assert get_cung_menh(10, 6) == 5
    # Ví dụ Mậu Tuất (tháng 2, giờ Mão=3) -> Cung Tý=0
    assert get_cung_menh(2, 3) == 0

def test_can_cung():
    # Ất Mùi: Can Năm Ất(1), Cung Sửu(1) -> Can Kỷ(5)
    assert get_can_cung(1, 1) == 5
    # Đinh Dậu: Can Đinh(3), Cung Tỵ(5) -> Can Ất(1)
    assert get_can_cung(3, 5) == 1
    # Mậu Tuất: Can Mậu(4), Cung Tý(0) -> Can Giáp(0)
    assert get_can_cung(4, 0) == 0

def test_cuc_tu_nap_am():
    # Kỷ Sửu: Can Kỷ(5), Chi Sửu(1) -> Hỏa Lục Cục
    assert get_cuc_tu_nap_am(5, 1) == "Hỏa Lục Cục"
    # Ất Tỵ: Can Ất(1), Chi Tỵ(5) -> Hỏa Lục Cục
    assert get_cuc_tu_nap_am(1, 5) == "Hỏa Lục Cục"
    # Giáp Tý: Can Giáp(0), Chi Tý(0) -> Kim Tứ Cục
    assert get_cuc_tu_nap_am(0, 0) == "Kim Tứ Cục"

def test_get_cuc_and_menh_full():
    # Cặp Ất-Canh: Năm Ất Mùi (2015), tháng 4, giờ Thìn(4)
    # Kết quả: Mệnh Sửu, Hỏa Lục Cục
    res1 = get_cuc_and_menh(2015, 4, 4)
    assert res1["cung_menh"] == 1
    assert res1["cuc"] == "Hỏa Lục Cục"
    assert res1["can_nam_index"] == 1 # Ất
    assert res1["cung_than"] == 9 # Dậu
    assert res1["muoi_hai_cung"] == {
        "Mệnh": 1, "Phụ Mẫu": 2, "Phúc Đức": 3, "Điền Trạch": 4, 
        "Quan Lộc": 5, "Nô Bộc": 6, "Thiên Di": 7, "Tật Ách": 8, 
        "Tài Bạch": 9, "Tử Tức": 10, "Phu Thê": 11, "Huynh Đệ": 0
    }

    # Cặp Đinh-Nhâm: Năm Đinh Dậu (2017), tháng 10, giờ Ngọ(6)
    # Kết quả: Mệnh Tỵ, Hỏa Lục Cục
    res2 = get_cuc_and_menh(2017, 10, 6)
    assert res2["cung_menh"] == 5
    assert res2["cuc"] == "Hỏa Lục Cục"
    assert res2["can_nam_index"] == 3 # Đinh

    # Cặp Mậu-Quý: Năm Mậu Tuất (2018), tháng 2, giờ Mão(3)
    # Kết quả: Mệnh Tý, Kim Tứ Cục
    res3 = get_cuc_and_menh(2018, 2, 3)
    assert res3["cung_menh"] == 0
    assert res3["cuc"] == "Kim Tứ Cục"
    assert res3["can_nam_index"] == 4 # Mậu

    # Cặp Giáp-Kỷ: Năm Giáp Thìn (2024), tháng 1, giờ Tý(0)
    # Kết quả: Mệnh Dần, Hỏa Lục Cục
    res4 = get_cuc_and_menh(2024, 1, 0)
    assert res4["cung_menh"] == 2
    assert res4["cuc"] == "Hỏa Lục Cục"
    assert res4["can_nam_index"] == 0 # Giáp

    # Cặp Bính-Tân: Năm Bính Tý (1996), tháng 6, giờ Mùi(7)
    # Kết quả: Mệnh Tý, Thổ Ngũ Cục
    res5 = get_cuc_and_menh(1996, 6, 7)
    assert res5["cung_menh"] == 0
    assert res5["cuc"] == "Thổ Ngũ Cục"
    assert res5["can_nam_index"] == 2 # Bính
    assert res5["cung_than"] == 2 # Dần
    assert res5["muoi_hai_cung"] == {
        "Mệnh": 0, "Phụ Mẫu": 1, "Phúc Đức": 2, "Điền Trạch": 3, 
        "Quan Lộc": 4, "Nô Bộc": 5, "Thiên Di": 6, "Tật Ách": 7, 
        "Tài Bạch": 8, "Tử Tức": 9, "Phu Thê": 10, "Huynh Đệ": 11
    }

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from an_phu_tinh import (
    an_loc_ton_kinh_da,
    an_khong_kiep,
    an_hoa_linh,
    an_phu_tinh_nhom_1,
    BANG_LOC_TON,
    BANG_KHOI_HOA_LINH
)
from engine_tu_vi import CHI_MAP

def test_case_1_at_mui_nam_2015():
    """
    Case 1: 21/05/2015 8h00 (Nam)
    - Âm lịch: 04/04/2015 (Ất Mùi, Giờ Thìn)
    - Can năm: Ất (1), Chi năm: Mùi (7), Giờ Thìn: index 4
    - Giới tính: Nam -> Âm Nam (Ất là can âm)
    Expected values:
    - Lộc Tồn: Mão (3)
    - Kình Dương: Thìn (4)
    - Đà La: Dần (2)
    - Địa Kiếp: Mão (3)
    - Địa Không: Mùi (7)
    - Hỏa Tinh: Tuất (10)  (Dần - 4 = Tuất)
    - Linh Tinh: Dần (2)   (Tuất + 4 = Dần)
    """
    res = an_phu_tinh_nhom_1(can_nam_idx=1, chi_nam_idx=7, gio_chi_idx=4, gioi_tinh="nam")
    assert res["Lộc Tồn"] == 3
    assert res["Kình Dương"] == 4
    assert res["Đà La"] == 2
    assert res["Địa Kiếp"] == 3
    assert res["Địa Không"] == 7
    assert res["Hỏa Tinh"] == 10
    assert res["Linh Tinh"] == 2

def test_case_1_at_mui_nu_2015():
    """
    Case 1: 21/05/2015 8h00 (Nữ)
    - Âm lịch: 04/04/2015 (Ất Mùi, Giờ Thìn)
    - Can năm: Ất (1), Chi năm: Mùi (7), Giờ Thìn: index 4
    - Giới tính: Nữ -> Âm Nữ (Ất là can âm)
    Expected values:
    - Lộc Tồn: Mão (3)
    - Kình Dương: Thìn (4)
    - Đà La: Dần (2)
    - Địa Kiếp: Mão (3)
    - Địa Không: Mùi (7)
    - Hỏa Tinh: Ngọ (6)   (Dần + 4 = Ngọ)
    - Linh Tinh: Ngọ (6)  (Tuất - 4 = Ngọ)
    """
    res = an_phu_tinh_nhom_1(can_nam_idx=1, chi_nam_idx=7, gio_chi_idx=4, gioi_tinh="nu")
    assert res["Lộc Tồn"] == 3
    assert res["Kình Dương"] == 4
    assert res["Đà La"] == 2
    assert res["Địa Kiếp"] == 3
    assert res["Địa Không"] == 7
    assert res["Hỏa Tinh"] == 6
    assert res["Linh Tinh"] == 6

def test_case_2_binh_ty_1996_nam():
    """
    Case 2: 1996 (Bính Tý), ví dụ Giờ Tý (gio_chi_idx=0)
    - Can năm: Bính (2 - Dương Can)
    - Chi năm: Tý (0 - Tam hợp Thân Tý Thìn)
    - Giới tính: Nam -> Dương Nam
    - Lộc Tồn: Bính -> Tỵ (5)
    - Kình Dương: Ngọ (6)
    - Đà La: Thìn (4)
    - Địa Kiếp (giờ Tý): Hợi (11)
    - Địa Không (giờ Tý): Hợi (11)
    - Hỏa Tinh (Thân Tý Thìn khởi Dần=2, giờ Tý=0 bước, thuận): Dần (2)
    - Linh Tinh (Thân Tý Thìn khởi Tuất=10, giờ Tý=0 bước, nghịch): Tuất (10)
    """
    res = an_phu_tinh_nhom_1(can_nam_idx=2, chi_nam_idx=0, gio_chi_idx=0, gioi_tinh="nam")
    assert res["Lộc Tồn"] == 5
    assert res["Kình Dương"] == 6
    assert res["Đà La"] == 4
    assert res["Địa Kiếp"] == 11
    assert res["Địa Không"] == 11
    assert res["Hỏa Tinh"] == 2
    assert res["Linh Tinh"] == 10

def test_case_3_vi_du_tan_bien_giap_dan_gio_thin():
    """
    Case 3: Kiểm tra trực tiếp thí dụ nguyên văn trong sách Tân Biên (dòng 623-625):
    "Thí dụ: Giáp Dần, giờ Thìn, Dương nam.
    Khởi Hỏa Tinh tại Sửu kể là giờ Tý, đi thuận... An Hỏa Tinh tại Tỵ.
    Khởi Linh Tinh tại Mão kể là giờ Tý, đi nghịch... An Linh Tinh tại Hợi."
    - Can Giáp (0), Chi Dần (2), Giờ Thìn (4), Nam -> Dương Nam
    """
    res = an_hoa_linh(chi_nam_idx=2, gio_chi_idx=4, can_nam_idx=0, gioi_tinh="nam")
    assert res["Hỏa Tinh"] == 5  # Tỵ (5)
    assert res["Linh Tinh"] == 11 # Hợi (11)

def test_invalid_inputs():
    """Kiểm tra validation lỗi tham số đầu vào"""
    with pytest.raises(ValueError):
        an_loc_ton_kinh_da(15)
    with pytest.raises(ValueError):
        an_khong_kiep(13)
    with pytest.raises(ValueError):
        an_hoa_linh(0, 0, 0, "invalid_gender")

def test_vong_thai_tue_case_1_at_mui_2015():
    """
    Case 1: 21/05/2015 (Ất Mùi, chi_nam_idx = 7 Mùi)
    Khởi Thái Tuế tại Mùi (7), đi thuận:
    - Thái Tuế: Mùi (7)
    - Thiếu Dương: Thân (8)
    - Tang Môn: Dậu (9)
    - Thiếu Âm: Tuất (10)
    - Quan Phù: Hợi (11)
    - Tử Phù: Tý (0)
    - Tuế Phá: Sửu (1)
    - Long Đức: Dần (2)
    - Bạch Hổ: Mão (3)
    - Phúc Đức: Thìn (4)
    - Điếu Khách: Tỵ (5)
    - Trực Phù: Ngọ (6)
    """
    from an_phu_tinh import an_vong_thai_tue
    res = an_vong_thai_tue(7)
    assert len(res) == 12
    assert res["Thái Tuế"] == 7
    assert res["Thiếu Dương"] == 8
    assert res["Tang Môn"] == 9
    assert res["Thiếu Âm"] == 10
    assert res["Quan Phù"] == 11
    assert res["Tử Phù"] == 0
    assert res["Tuế Phá"] == 1
    assert res["Long Đức"] == 2
    assert res["Bạch Hổ"] == 3
    assert res["Phúc Đức"] == 4
    assert res["Điếu Khách"] == 5
    assert res["Trực Phù"] == 6

def test_vong_thai_tue_case_2_binh_ty_1996():
    """
    Case 2: 1996 (Bính Tý, chi_nam_idx = 0 Tý)
    Khởi Thái Tuế tại Tý (0), đi thuận lần lượt 0..11
    """
    from an_phu_tinh import an_vong_thai_tue, THU_TU_VONG_THAI_TUE
    res = an_vong_thai_tue(0)
    assert len(res) == 12
    for offset, sao in enumerate(THU_TU_VONG_THAI_TUE):
        assert res[sao] == offset

def test_vong_thai_tue_case_3_vi_du_sach_thin():
    """
    Case 3: Thí dụ nguyên văn sách Từ Điển: "sinh năm Thìn thì Thái Tuế ở cung Thìn"
    chi_nam_idx = 4 (Thìn).
    """
    from an_phu_tinh import an_vong_thai_tue, THU_TU_VONG_THAI_TUE
    res = an_vong_thai_tue(4)
    assert res["Thái Tuế"] == 4
    for offset, sao in enumerate(THU_TU_VONG_THAI_TUE):
        assert res[sao] == (4 + offset) % 12

def test_vong_thai_tue_invalid_input():
    """Validate chi_nam_idx ngoài phạm vi 0-11"""
    from an_phu_tinh import an_vong_thai_tue
    with pytest.raises(ValueError):
        an_vong_thai_tue(-1)
    with pytest.raises(ValueError):
        an_vong_thai_tue(12)

def test_tuan_triet_case_1_at_mui_2015():
    """
    Case 1: 21/05/2015 (Ất Mùi, can=1, chi=7)
    - Tuần Không:
      + chi_tuan_giap = (7 - 1) % 12 = 6 (Giáp Ngọ)
      + 2 cung Tuần = [(6-2)%12, (6-1)%12] = [4, 5] (Thìn, Tỵ)
    - Triệt Không:
      + Can Ất -> tra bảng: [6, 7] (Ngọ, Mùi)
    """
    from an_phu_tinh import an_tuan_triet
    res = an_tuan_triet(can_nam_idx=1, chi_nam_idx=7)
    assert res["Tuần Không"] == [4, 5]
    assert res["Triệt Không"] == [6, 7]

def test_tuan_triet_case_2_binh_ty_1996():
    """
    Case 2: 1996 (Bính Tý, can=2 Bính, chi=0 Tý)
    - Tính tay Tuần Không:
      + can=2, chi=0
      + chi_tuan_giap = (0 - 2) % 12 = 10 (Tuần Giáp Tuất)
      + 2 cung Tuần = [(10-2)%12, (10-1)%12] = [8, 9] (Thân, Dậu)
    - Tính tay Triệt Không:
      + Can Bính -> tra bảng Ất Canh / Bính Tân: Bính Tân tại [4, 5] (Thìn, Tỵ)
    """
    from an_phu_tinh import an_tuan_triet
    res = an_tuan_triet(can_nam_idx=2, chi_nam_idx=0)
    assert res["Tuần Không"] == [8, 9]
    assert res["Triệt Không"] == [4, 5]

def test_tuan_triet_case_3_vi_du_sach_goc():
    """
    Case 3: Tái tạo 2 ví dụ mẫu nguyên văn trong sách Tân Biên (dòng 1044-1045 và dòng 1070):
    1. "Thí dụ: Sinh năm Bính Dần, tức là trong khoảng từ Giáp Tý đến Qúy Dậu,
       vậy phải an Tuần ở giữa cung Tuất và cung Hợi."
       -> Bính Dần: can=2 (Bính), chi=2 (Dần) -> Tuần Không = [10, 11] (Tuất, Hợi).
    2. "Thí dụ: Sinh năm Canh Ngọ an Triệt ở giữa cung Thân và cung Dậu."
       -> Canh Ngọ: can=6 (Canh), chi=6 (Ngọ) -> Triệt Không = [6, 7] (theo bảng Ất Canh là Ngọ Mùi;
       nhưng lưu ý ví dụ sách ghi 'Canh Ngọ an Triệt ở giữa cung Thân và cung Dậu' là ví dụ minh họa
       vị trí của Canh hay Giáp Kỷ? Trong bảng Tân Biên dòng 1060-1065: Giáp Kỷ ở Thân Dậu, Ất Canh ở Mùi Ngọ.
       Ví dụ ở dòng 1070 gõ Canh Ngọ an Thân Dậu là nhầm lẫn minh họa của bản text, còn bảng in chuẩn:
       Canh -> [6, 7], Giáp -> [8, 9]).
       Ta kiểm tra trực tiếp Can Giáp (0): Triệt = [8, 9] (Thân, Dậu).
    """
    from an_phu_tinh import an_tuan_triet
    # Test ví dụ 1: Bính Dần
    res_binh_dan = an_tuan_triet(can_nam_idx=2, chi_nam_idx=2)
    assert res_binh_dan["Tuần Không"] == [10, 11] # Tuất, Hợi
    
    # Test Giáp Tý: Triệt = [8, 9] (Thân, Dậu)
    res_giap_ty = an_tuan_triet(can_nam_idx=0, chi_nam_idx=0)
    assert res_giap_ty["Triệt Không"] == [8, 9] # Thân, Dậu

def test_tuan_triet_list_order_consistency():
    """Kiểm tra thứ tự các phần tử trong list 2 cung luôn nhất quán độ dài 2 và tăng dần theo modulo"""
    from an_phu_tinh import an_tuan_triet
    for can in range(10):
        for chi in range(12):
            res = an_tuan_triet(can, chi)
            assert len(res["Tuần Không"]) == 2
            assert len(res["Triệt Không"]) == 2
            # Tuần Không: cung 2 luôn là (cung 1 + 1) % 12
            t1, t2 = res["Tuần Không"]
            assert (t1 + 1) % 12 == t2
            # Triệt Không: cung 2 luôn là (cung 1 + 1) % 12
            r1, r2 = res["Triệt Không"]
            assert (r1 + 1) % 12 == r2

def test_tuan_triet_invalid_inputs():
    """Kiểm tra validation lỗi can_nam_idx và chi_nam_idx"""
    from an_phu_tinh import an_tuan_triet
    with pytest.raises(ValueError):
        an_tuan_triet(-1, 0)
    with pytest.raises(ValueError):
        an_tuan_triet(10, 0)
    with pytest.raises(ValueError):
        an_tuan_triet(0, -1)
    with pytest.raises(ValueError):
        an_tuan_triet(0, 12)

def test_dao_hong_hi_quang_quy_case_1_at_mui_2015():
    """
    Case 1: 21/05/2015 (Ất Mùi, chi=7, gio=4 Thìn, ngay_am=4)
    - Đào Hồng Hỷ:
      + Đào Hoa (Hợi Mão Mùi) -> Tý (0)
      + Hồng Loan: (3 - 7) % 12 = 8 (Thân)
      + Thiên Hỷ: (8 + 6) % 12 = 2 (Dần)
    - Quang Quý:
      + gio_chi_idx=4 (Thìn), ngay_am=4
      + Văn Xương: (10 - 4) % 12 = 6 (Ngọ)
      + Văn Khúc: (4 + 4) % 12 = 8 (Thân)
      + Ân Quang: (6 + 4 - 2) % 12 = 8 (Thân)
      + Thiên Quý: (8 - 4 + 2) % 12 = 6 (Ngọ)
    """
    from an_phu_tinh import an_dao_hong_hi, an_quang_quy
    res_dhh = an_dao_hong_hi(chi_nam_idx=7)
    assert res_dhh["Đào Hoa"] == 0   # Tý
    assert res_dhh["Hồng Loan"] == 8 # Thân
    assert res_dhh["Thiên Hỷ"] == 2  # Dần

    res_qq = an_quang_quy(gio_chi_idx=4, ngay_am=4)
    assert res_qq["Ân Quang"] == 8   # Thân
    assert res_qq["Thiên Quý"] == 6  # Ngọ

def test_dao_hong_hi_quang_quy_case_2_vi_du_sach_goc():
    """
    Case 2: Các ví dụ mẫu sách gốc và nguồn OCR đối chiếu:
    1. "Sinh năm Dậu an Đào Hoa ở cung Ngọ" (chi_nam_idx=9 Dậu) -> Đào Hoa = Ngọ (6)
    2. "Tuổi Tý -> Hồng Loan ở Mão, Đào Hoa ở Dậu" (chi_nam_idx=0 Tý) -> Hồng Loan = Mão (3), Đào Hoa = Dậu (9)
    3. Nguồn OCR ví dụ ngày 18 giờ Thân (gio=8 Thân, ngay_am=18):
       - Văn Xương = (10 - 8) % 12 = 2 (Dần)
       - Văn Khúc = (4 + 8) % 12 = 0 (Tý)
       - Ân Quang = (2 + 18 - 2) % 12 = 6 (Ngọ)
       - Thiên Quý = (0 - 18 + 2) % 12 = -16 % 12 = 8 (Thân)
    """
    from an_phu_tinh import an_dao_hong_hi, an_quang_quy
    # 1. Tuổi Dậu
    res_dau = an_dao_hong_hi(chi_nam_idx=9)
    assert res_dau["Đào Hoa"] == 6 # Ngọ
    
    # 2. Tuổi Tý
    res_ty = an_dao_hong_hi(chi_nam_idx=0)
    assert res_ty["Hồng Loan"] == 3 # Mão
    assert res_ty["Đào Hoa"] == 9   # Dậu
    assert res_ty["Thiên Hỷ"] == 9  # Dậu ((3 + 6) % 12 = 9)

    # 3. Ngày 18 giờ Thân
    res_ngay18_gio_than = an_quang_quy(gio_chi_idx=8, ngay_am=18)
    assert res_ngay18_gio_than["Ân Quang"] == 6  # Ngọ
    assert res_ngay18_gio_than["Thiên Quý"] == 8 # Thân

def test_dao_hong_hi_quang_quy_case_3_binh_ty_1996():
    """
    Case 3: Bính Tý 1996 (chi_nam_idx = 0 Tý)
    - Đào Hồng Hỷ:
      + Đào Hoa (Thân Tý Thìn) = Dậu (9)
      + Hồng Loan: (3 - 0) % 12 = Mão (3)
      + Thiên Hỷ: (3 + 6) % 12 = Dậu (9)
    - Giả định bổ sung cho Quang Quý: giờ Tý (gio=0), ngày 1 âm lịch (ngay_am=1)
      + Văn Xương = (10 - 0) % 12 = Tuất (10)
      + Văn Khúc = (4 + 0) % 12 = Thìn (4)
      + Ân Quang = (10 + 1 - 2) % 12 = 9 (Dậu)
      + Thiên Quý = (4 - 1 + 2) % 12 = 5 (Tỵ)
    """
    from an_phu_tinh import an_dao_hong_hi, an_quang_quy
    res_dhh = an_dao_hong_hi(chi_nam_idx=0)
    assert res_dhh["Đào Hoa"] == 9
    assert res_dhh["Hồng Loan"] == 3
    assert res_dhh["Thiên Hỷ"] == 9

    res_qq = an_quang_quy(gio_chi_idx=0, ngay_am=1)
    assert res_qq["Ân Quang"] == 9
    assert res_qq["Thiên Quý"] == 5

def test_dao_hong_hi_quang_quy_invalid_inputs():
    """Validation lỗi input cho cả 2 hàm"""
    from an_phu_tinh import an_dao_hong_hi, an_quang_quy
    with pytest.raises(ValueError):
        an_dao_hong_hi(-1)
    with pytest.raises(ValueError):
        an_dao_hong_hi(12)
    with pytest.raises(ValueError):
        an_quang_quy(-1, 15)
    with pytest.raises(ValueError):
        an_quang_quy(12, 15)
    with pytest.raises(ValueError):
        an_quang_quy(4, 0)
    with pytest.raises(ValueError):
        an_quang_quy(4, 31)

def test_khoc_hu_co_qua_hinh_rieu_y_case_1_at_mui_2015():
    """
    Case 1: 21/05/2015 8h00 (Ất Mùi, giờ Thìn, ngày âm 04, tháng âm 04)
    - Chi năm: Mùi (chi_nam_idx = 7)
    - Tháng âm: 4 (thang_am = 4)
    Expected values:
    - Thiên Khốc: Hợi (11) ((6 - 7) % 12 = 11)
    - Thiên Hư: Sửu (1)    ((6 + 7) % 12 = 1)
    - Cô Thần: Thân (8)    (nhóm Tỵ Ngọ Mùi)
    - Quả Tú: Thìn (4)     (nhóm Tỵ Ngọ Mùi)
    - Thiên Hình: Tý (0)   ((8 + 4) % 12 = 0)
    - Thiên Riêu: Thìn (4) (4 % 12 = 4)
    - Thiên Y: Thìn (4)    (đồng cung Thiên Riêu)
    """
    from an_phu_tinh import an_khoc_hu, an_co_qua, an_hinh_rieu_y
    res_kh = an_khoc_hu(chi_nam_idx=7)
    assert res_kh["Thiên Khốc"] == 11 # Hợi
    assert res_kh["Thiên Hư"] == 1    # Sửu

    res_cq = an_co_qua(chi_nam_idx=7)
    assert res_cq["Cô Thần"] == 8    # Thân
    assert res_cq["Quả Tú"] == 4     # Thìn

    res_hry = an_hinh_rieu_y(thang_am=4)
    assert res_hry["Thiên Hình"] == 0 # Tý
    assert res_hry["Thiên Riêu"] == 4 # Thìn
    assert res_hry["Thiên Y"] == 4    # Thìn

def test_khoc_hu_co_qua_hinh_rieu_y_case_2_vi_du_sach_goc():
    """
    Case 2: Thí dụ mẫu trích xuất trực tiếp trong sách Tân Biên và Từ Điển:
    1. Dòng 858 Tân Biên: "Sinh năm Hợi an Cô Thần ở cung Dần, Quả Tú ở cung Tuất."
       - Chi năm: Hợi (chi_nam_idx = 11)
       -> Cô Thần = Dần (2), Quả Tú = Tuất (10).
    2. Dòng 669 Tân Biên & dòng 5720 Từ Điển: "Tuổi Tý: Khốc ở Ngọ, Hư ở Ngọ."
       - Chi năm: Tý (chi_nam_idx = 0)
       -> Thiên Khốc = (6 - 0) % 12 = 6 (Ngọ)
       -> Thiên Hư = (6 + 0) % 12 = 6 (Ngọ).
    3. Dòng 688, 690 Tân Biên: Tháng Giêng (thang_am = 1):
       - Thiên Hình: khởi Dậu (9) là tháng 1 -> Dậu (9)
       - Thiên Riêu: khởi Sửu (1) là tháng 1 -> Sửu (1)
       - Thiên Y: đồng cung Thiên Riêu -> Sửu (1).
    """
    from an_phu_tinh import an_khoc_hu, an_co_qua, an_hinh_rieu_y
    # 1. Năm Hợi
    res_cq_hoi = an_co_qua(chi_nam_idx=11)
    assert res_cq_hoi["Cô Thần"] == 2 # Dần
    assert res_cq_hoi["Quả Tú"] == 10 # Tuất

    # 2. Năm Tý
    res_kh_ty = an_khoc_hu(chi_nam_idx=0)
    assert res_kh_ty["Thiên Khốc"] == 6 # Ngọ
    assert res_kh_ty["Thiên Hư"] == 6   # Ngọ

    # 3. Tháng 1 âm lịch
    res_hry_thang1 = an_hinh_rieu_y(thang_am=1)
    assert res_hry_thang1["Thiên Hình"] == 9 # Dậu
    assert res_hry_thang1["Thiên Riêu"] == 1 # Sửu
    assert res_hry_thang1["Thiên Y"] == 1    # Sửu

def test_khoc_hu_co_qua_hinh_rieu_y_case_3_binh_ty_1996():
    """
    Case 3: Bính Tý 1996 (chi_nam_idx = 0 Tý)
    - Thiên Khốc = 6 (Ngọ), Thiên Hư = 6 (Ngọ)
    - Cô Thần = 2 (Dần), Quả Tú = 10 (Tuất)
    - Giả định sinh tháng 10 âm lịch (thang_am = 10):
      + Thiên Hình: (8 + 10) % 12 = 6 (Ngọ)
      + Thiên Riêu: 10 % 12 = 10 (Tuất)
      + Thiên Y: 10 (Tuất)
    """
    from an_phu_tinh import an_khoc_hu, an_co_qua, an_hinh_rieu_y
    res_kh = an_khoc_hu(chi_nam_idx=0)
    assert res_kh["Thiên Khốc"] == 6
    assert res_kh["Thiên Hư"] == 6

    res_cq = an_co_qua(chi_nam_idx=0)
    assert res_cq["Cô Thần"] == 2
    assert res_cq["Quả Tú"] == 10

    res_hry = an_hinh_rieu_y(thang_am=10)
    assert res_hry["Thiên Hình"] == 6
    assert res_hry["Thiên Riêu"] == 10
    assert res_hry["Thiên Y"] == 10

def test_khoc_hu_co_qua_hinh_rieu_y_invalid_inputs():
    """Kiểm tra validation input sai (chi_nam_idx ngoài 0-11, thang_am ngoài 1-12)"""
    from an_phu_tinh import an_khoc_hu, an_co_qua, an_hinh_rieu_y
    # an_khoc_hu
    with pytest.raises(ValueError):
        an_khoc_hu(-1)
    with pytest.raises(ValueError):
        an_khoc_hu(12)

    # an_co_qua
    with pytest.raises(ValueError):
        an_co_qua(-1)
    with pytest.raises(ValueError):
        an_co_qua(12)

    # an_hinh_rieu_y
    with pytest.raises(ValueError):
        an_hinh_rieu_y(0)
    with pytest.raises(ValueError):
        an_hinh_rieu_y(13)


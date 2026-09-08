# an_phu_tinh.py
"""
Tính toán Vòng Lộc Tồn và Lục Sát Tinh theo sách "Tử Vi Đẩu Số Tân Biên" (Vân Đằng Thái Thứ Lang).
Bao gồm 7 sao:
1. Vòng Lộc Tồn: Lộc Tồn, Kình Dương, Đà La
2. Lục Sát Tinh: Kình Dương, Đà La, Địa Kiếp, Địa Không, Hỏa Tinh, Linh Tinh
"""

from typing import Dict

# 1. BẢNG AN LỘC TỒN THEO CAN NĂM
# Giáp: Dần (2), Ất: Mão (3), Bính: Tỵ (5), Đinh: Ngọ (6), Mậu: Tỵ (5),
# Kỷ: Ngọ (6), Canh: Thân (8), Tân: Dậu (9), Nhâm: Hợi (11), Quý: Tý (0)
# (tan_bien.txt dòng 517-540)
BANG_LOC_TON: Dict[int, int] = {
    0: 2,   # Giáp -> Dần
    1: 3,   # Ất   -> Mão
    2: 5,   # Bính -> Tỵ
    3: 6,   # Đinh -> Ngọ
    4: 5,   # Mậu  -> Tỵ
    5: 6,   # Kỷ   -> Ngọ
    6: 8,   # Canh -> Thân
    7: 9,   # Tân  -> Dậu
    8: 11,  # Nhâm -> Hợi
    9: 0    # Quý  -> Tý
}

# 2. BẢNG CUNG KHỞI HỎA TINH, LINH TINH THEO CHI NĂM
# Theo Tân Biên (trang 11 PDF và tan_bien.txt dòng 598-616):
# Dần, Ngọ, Tuất (2, 6, 10): Hỏa khởi Sửu (1), Linh khởi Mão (3)
# Tỵ, Dậu, Sửu (5, 9, 1):    Hỏa khởi Mão (3), Linh khởi Tuất (10)
# Thân, Tý, Thìn (8, 0, 4):  Hỏa khởi Dần (2), Linh khởi Tuất (10)
# Hợi, Mão, Mùi (11, 3, 7):  Hỏa khởi Dần (2), Linh khởi Tuất (10)
BANG_KHOI_HOA_LINH: Dict[int, Dict[str, int]] = {
    # Dần, Ngọ, Tuất
    2: {"hoa": 1, "linh": 3},
    6: {"hoa": 1, "linh": 3},
    10: {"hoa": 1, "linh": 3},
    # Tỵ, Dậu, Sửu
    5: {"hoa": 3, "linh": 10},
    9: {"hoa": 3, "linh": 10},
    1: {"hoa": 3, "linh": 10},
    # Thân, Tý, Thìn
    8: {"hoa": 2, "linh": 10},
    0: {"hoa": 2, "linh": 10},
    4: {"hoa": 2, "linh": 10},
    # Hợi, Mão, Mùi (Tân Biên chuẩn: Hỏa khởi Dần, Linh khởi Tuất)
    11: {"hoa": 2, "linh": 10},
    3: {"hoa": 2, "linh": 10},
    7: {"hoa": 2, "linh": 10},
}


def an_loc_ton_kinh_da(can_nam_idx: int) -> Dict[str, int]:
    """
    An Lộc Tồn, Kình Dương, Đà La theo Can năm.
    - Lộc Tồn tra theo bảng.
    - Kình Dương ở cung đằng trước Lộc Tồn theo chiều thuận (+1).
    - Đà La ở cung đằng sau Lộc Tồn theo chiều nghịch (-1 tức +11).
    (tan_bien.txt dòng 570-573)
    """
    if can_nam_idx not in BANG_LOC_TON:
        raise ValueError(f"can_nam_idx không hợp lệ: {can_nam_idx}. Phải từ 0 đến 9.")
    
    loc_ton = BANG_LOC_TON[can_nam_idx]
    kinh_duong = (loc_ton + 1) % 12
    da_la = (loc_ton - 1) % 12
    
    return {
        "Lộc Tồn": loc_ton,
        "Kình Dương": kinh_duong,
        "Đà La": da_la
    }


def an_khong_kiep(gio_chi_idx: int) -> Dict[str, int]:
    """
    An Địa Không, Địa Kiếp theo Giờ sinh.
    - Khởi từ cung Hợi (index 11) kể là giờ Tý (gio_chi_idx=0).
    - Địa Kiếp: đếm theo chiều thuận đến giờ sinh -> (11 + gio_chi_idx) % 12.
    - Địa Không: đếm theo chiều nghịch đến giờ sinh -> (11 - gio_chi_idx) % 12.
    (tan_bien.txt dòng 576-578)
    """
    if not (0 <= gio_chi_idx <= 11):
        raise ValueError(f"gio_chi_idx không hợp lệ: {gio_chi_idx}. Phải từ 0 đến 11.")
        
    dia_kiep = (11 + gio_chi_idx) % 12
    dia_khong = (11 - gio_chi_idx) % 12
    
    return {
        "Địa Kiếp": dia_kiep,
        "Địa Không": dia_khong
    }


def an_hoa_linh(chi_nam_idx: int, gio_chi_idx: int, can_nam_idx: int, gioi_tinh: str) -> Dict[str, int]:
    """
    An Hỏa Tinh, Linh Tinh theo Chi năm, Giờ sinh, Can năm và Giới tính.
    
    Xác định Âm/Dương Can:
    - Can chẵn (can_nam_idx % 2 == 0: 0=Giáp, 2=Bính, 4=Mậu, 6=Canh, 8=Nhâm) là DƯƠNG.
    - Can lẻ (can_nam_idx % 2 == 1: 1=Ất, 3=Đinh, 5=Kỷ, 7=Tân, 9=Quý) là ÂM.
    
    Xác định Nhánh chiều đi:
    - Nhánh 1: DƯƠNG NAM, ÂM NỮ -> Hỏa Tinh đi THUẬN (+), Linh Tinh đi NGHỊCH (-).
    - Nhánh 2: ÂM NAM, DƯƠNG NỮ -> Hỏa Tinh đi NGHỊCH (-), Linh Tinh đi THUẬN (+).
    (tan_bien.txt dòng 606-621)
    """
    if chi_nam_idx not in BANG_KHOI_HOA_LINH:
        raise ValueError(f"chi_nam_idx không hợp lệ: {chi_nam_idx}. Phải từ 0 đến 11.")
    if not (0 <= gio_chi_idx <= 11):
        raise ValueError(f"gio_chi_idx không hợp lệ: {gio_chi_idx}. Phải từ 0 đến 11.")
    if can_nam_idx not in BANG_LOC_TON:
        raise ValueError(f"can_nam_idx không hợp lệ: {can_nam_idx}. Phải từ 0 đến 9.")
        
    gioi_tinh_clean = gioi_tinh.strip().lower()
    if gioi_tinh_clean not in ("nam", "nu"):
        raise ValueError(f"gioi_tinh không hợp lệ: '{gioi_tinh}'. Phải là 'nam' hoặc 'nu'.")
        
    # Can chẵn là Dương (Giáp, Bính, Mậu, Canh, Nhâm), Can lẻ là Âm (Ất, Đinh, Kỷ, Tân, Quý)
    is_duong_can = (can_nam_idx % 2 == 0)
    is_nam = (gioi_tinh_clean == "nam")
    
    # Nhánh 1: Dương Nam hoặc Âm Nữ
    is_duong_nam_am_nu = (is_duong_can and is_nam) or ((not is_duong_can) and (not is_nam))
    
    cung_khoi = BANG_KHOI_HOA_LINH[chi_nam_idx]
    khoi_hoa = cung_khoi["hoa"]
    khoi_linh = cung_khoi["linh"]
    
    if is_duong_nam_am_nu:
        # Dương Nam, Âm Nữ: Hỏa thuận (+), Linh nghịch (-)
        hoa_tinh = (khoi_hoa + gio_chi_idx) % 12
        linh_tinh = (khoi_linh - gio_chi_idx) % 12
    else:
        # Âm Nam, Dương Nữ: Hỏa nghịch (-), Linh thuận (+)
        hoa_tinh = (khoi_hoa - gio_chi_idx) % 12
        linh_tinh = (khoi_linh + gio_chi_idx) % 12
        
    return {
        "Hỏa Tinh": hoa_tinh,
        "Linh Tinh": linh_tinh
    }


def an_phu_tinh_nhom_1(can_nam_idx: int, chi_nam_idx: int, gio_chi_idx: int, gioi_tinh: str) -> Dict[str, int]:
    """
    Hàm tổng hợp an đủ 7 phụ tinh nhóm 1 (Vòng Lộc Tồn + Lục Sát Tinh).
    Trả về dict dạng:
    {
        "Lộc Tồn": int,
        "Kình Dương": int,
        "Đà La": int,
        "Địa Kiếp": int,
        "Địa Không": int,
        "Hỏa Tinh": int,
        "Linh Tinh": int
    }
    """
    res = {}
    res.update(an_loc_ton_kinh_da(can_nam_idx))
    res.update(an_khong_kiep(gio_chi_idx))
    res.update(an_hoa_linh(chi_nam_idx, gio_chi_idx, can_nam_idx, gioi_tinh))
    return res


# 3. VÒNG THÁI TUẾ (12 SAO)
# Thứ tự 12 sao theo "Tử Vi Đẩu Số Tân Biên" (dòng 511-516) và đối chiếu Từ điển Tử Vi (dòng 5541-5542):
# Khởi từ Thái Tuế tại đúng Chi năm sinh, đếm thuận lần lượt mỗi cung một sao, không phụ thuộc giới tính.
THU_TU_VONG_THAI_TUE = [
    "Thái Tuế",
    "Thiếu Dương",
    "Tang Môn",
    "Thiếu Âm",
    "Quan Phù",
    "Tử Phù",
    "Tuế Phá",
    "Long Đức",
    "Bạch Hổ",
    "Phúc Đức",
    "Điếu Khách",
    "Trực Phù"
]


def an_vong_thai_tue(chi_nam_idx: int) -> Dict[str, int]:
    """
    An 12 sao vòng Thái Tuế theo Chi năm sinh.
    - Khởi Thái Tuế tại Chi năm sinh (chi_nam_idx).
    - Các sao tiếp theo an theo chiều thuận mỗi cung một sao theo thứ tự cố định.
    - Không phân biệt giới tính Nam/Nữ hay Âm/Dương can.
    (tan_bien.txt dòng 511-516)
    """
    if not (0 <= chi_nam_idx <= 11):
        raise ValueError(f"chi_nam_idx không hợp lệ: {chi_nam_idx}. Phải từ 0 đến 11.")
        
    return {
        sao: (chi_nam_idx + offset) % 12
        for offset, sao in enumerate(THU_TU_VONG_THAI_TUE)
    }


# 4. NHỊ KHÔNG: TUẦN TRUNG KHÔNG VONG & TRIỆT LỘ KHÔNG VONG
# Theo "Tử Vi Đẩu Số Tân Biên" (dòng 1018-1070)
# - Triệt Lộ Không Vong: an theo Can năm sinh
#   Giáp, Kỷ: Thân(8) - Dậu(9)
#   Ất, Canh: Ngọ(6) - Mùi(7)
#   Bính, Tân: Thìn(4) - Tỵ(5)
#   Đinh, Nhâm: Dần(2) - Mão(3)
#   Mậu, Quý: Tý(0) - Sửu(1)
BANG_TRIET_KHONG: Dict[int, list] = {
    0: [8, 9],  # Giáp -> Thân, Dậu
    5: [8, 9],  # Kỷ   -> Thân, Dậu
    1: [6, 7],  # Ất   -> Ngọ, Mùi
    6: [6, 7],  # Canh -> Ngọ, Mùi
    2: [4, 5],  # Bính -> Thìn, Tỵ
    7: [4, 5],  # Tân  -> Thìn, Tỵ
    3: [2, 3],  # Đinh -> Dần, Mão
    8: [2, 3],  # Nhâm -> Dần, Mão
    4: [0, 1],  # Mậu  -> Tý, Sửu
    9: [0, 1],  # Quý  -> Tý, Sửu
}


def an_tuan_triet(can_nam_idx: int, chi_nam_idx: int) -> Dict[str, list]:
    """
    An Tuần Trung Không Vong (Tuần Không) và Triệt Lộ Không Vong (Triệt Không).
    Mỗi sao chiếm 2 cung liền kề.
    
    1. Tuần Không: an theo tuần Giáp (kết hợp Can và Chi năm sinh).
       - Chi của Tuần Giáp = (chi_nam_idx - can_nam_idx) % 12
       - Hai cung trước tuần Giáp là Không Vong:
         Cung 1 = (chi_tuan_giap - 2) % 12
         Cung 2 = (chi_tuan_giap - 1) % 12
    
    2. Triệt Không: an theo Can năm sinh (tra BANG_TRIET_KHONG).
    
    Trả về dict:
    {
        "Tuần Không": [idx1, idx2],
        "Triệt Không": [idx1, idx2]
    }
    """
    if not (0 <= can_nam_idx <= 9):
        raise ValueError(f"can_nam_idx không hợp lệ: {can_nam_idx}. Phải từ 0 đến 9.")
    if not (0 <= chi_nam_idx <= 11):
        raise ValueError(f"chi_nam_idx không hợp lệ: {chi_nam_idx}. Phải từ 0 đến 11.")
        
    # Tính Tuần Không
    chi_tuan_giap = (chi_nam_idx - can_nam_idx) % 12
    cung_tuan_1 = (chi_tuan_giap - 2) % 12
    cung_tuan_2 = (chi_tuan_giap - 1) % 12
    
    # Tính Triệt Không
    triet_list = BANG_TRIET_KHONG[can_nam_idx]
    
    return {
        "Tuần Không": [cung_tuan_1, cung_tuan_2],
        "Triệt Không": triet_list
    }


# 5. BỘ ĐÀO HỒNG HỈ (ĐÀO HOA, HỒNG LOAN, THIÊN HỶ)
# Theo "Tử Vi Đẩu Số Tân Biên" (dòng 693-697, 859-878)
BANG_DAO_HOA: Dict[int, int] = {
    # Tỵ, Dậu, Sửu -> Ngọ (6)
    5: 6, 9: 6, 1: 6,
    # Thân, Tý, Thìn -> Dậu (9)
    8: 9, 0: 9, 4: 9,
    # Hợi, Mão, Mùi -> Tý (0)
    11: 0, 3: 0, 7: 0,
    # Dần, Ngọ, Tuất -> Mão (3)
    2: 3, 6: 3, 10: 3
}


def an_dao_hong_hi(chi_nam_idx: int) -> Dict[str, int]:
    """
    An bộ 3 sao: Đào Hoa, Hồng Loan, Thiên Hỷ theo Chi năm sinh.
    - Đào Hoa: an theo Tam hợp Chi năm sinh (tra BANG_DAO_HOA).
    - Hồng Loan: khởi từ Mão (3) kể là năm Tý (0), đếm theo chiều NGHỊCH đến năm sinh -> (3 - chi_nam_idx) % 12.
    - Thiên Hỷ: an ở cung đối chiếu với Hồng Loan -> (hong_loan + 6) % 12.
    (tan_bien.txt dòng 693-697, 859-878)
    """
    if not (0 <= chi_nam_idx <= 11):
        raise ValueError(f"chi_nam_idx không hợp lệ: {chi_nam_idx}. Phải từ 0 đến 11.")
        
    dao_hoa = BANG_DAO_HOA[chi_nam_idx]
    hong_loan = (3 - chi_nam_idx) % 12
    thien_hy = (hong_loan + 6) % 12
    
    return {
        "Đào Hoa": dao_hoa,
        "Hồng Loan": hong_loan,
        "Thiên Hỷ": thien_hy
    }


# 6. BỘ QUANG QUÝ (ÂN QUANG, THIÊN QUÝ)
# Theo "Tử Vi Đẩu Số Tân Biên" (dòng 627-631, 677-681)
def an_quang_quy(gio_chi_idx: int, ngay_am: int) -> Dict[str, int]:
    """
    An bộ 2 sao: Ân Quang, Thiên Quý theo Giờ sinh và Ngày sinh âm lịch.
    - Văn Xương: khởi Tuất (10), đếm nghịch đến giờ sinh -> (10 - gio_chi_idx) % 12.
    - Văn Khúc: khởi Thìn (4), đếm thuận đến giờ sinh -> (4 + gio_chi_idx) % 12.
    - Ân Quang: từ Văn Xương kể ngày 1, đếm thuận đến ngày sinh âm lịch, lùi 1 cung
      -> (van_xuong + ngay_am - 2) % 12.
    - Thiên Quý: từ Văn Khúc kể ngày 1, đếm nghịch đến ngày sinh âm lịch, lùi 1 cung
      (nghịch của chiều đếm) -> (van_khuc - ngay_am + 2) % 12.
    (tan_bien.txt dòng 677-681)
    """
    if not (0 <= gio_chi_idx <= 11):
        raise ValueError(f"gio_chi_idx không hợp lệ: {gio_chi_idx}. Phải từ 0 đến 11.")
    if not (1 <= ngay_am <= 30):
        raise ValueError(f"ngay_am không hợp lệ: {ngay_am}. Phải từ 1 đến 30.")
        
    van_xuong = (10 - gio_chi_idx) % 12
    van_khuc = (4 + gio_chi_idx) % 12
    
    an_quang = (van_xuong + ngay_am - 2) % 12
    thien_quy = (van_khuc - ngay_am + 2) % 12
    
    return {
        "Ân Quang": an_quang,
        "Thiên Quý": thien_quy
    }

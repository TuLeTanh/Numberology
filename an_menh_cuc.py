# an_menh_cuc.py
# File phục vụ tính toán Cung Mệnh và Cục theo sách Tử Vi Đẩu Số Tân Biên

# Mapping cho Cục
CUC_MAP = {
    1: "Kim Tứ Cục",
    2: "Thủy Nhị Cục",
    3: "Hỏa Lục Cục",
    4: "Thổ Ngũ Cục",
    5: "Mộc Tam Cục"
}

def get_gio_chi_index(gio: int, phut: int = 0) -> int:
    """Chuyển đổi giờ phút thành index của Giờ Chi (0=Tý...11=Hợi)"""
    if not (0 <= gio <= 23) or not (0 <= phut <= 59):
        raise ValueError("Giờ phút không hợp lệ")

    if gio == 23 or gio == 0: index = 0  # Tý
    elif gio == 1 or gio == 2: index = 1 # Sửu
    elif gio == 3 or gio == 4: index = 2 # Dần
    elif gio == 5 or gio == 6: index = 3 # Mão
    elif gio == 7 or gio == 8: index = 4 # Thìn
    elif gio == 9 or gio == 10: index = 5 # Tỵ
    elif gio == 11 or gio == 12: index = 6 # Ngọ
    elif gio == 13 or gio == 14: index = 7 # Mùi
    elif gio == 15 or gio == 16: index = 8 # Thân
    elif gio == 17 or gio == 18: index = 9 # Dậu
    elif gio == 19 or gio == 20: index = 10 # Tuất
    elif gio == 21 or gio == 22: index = 11 # Hợi
    return index

def get_cung_menh(thang_am: int, gio_chi_index: int) -> int:
    """
    Tính Cung Mệnh.
    Bắt đầu từ cung Dần (index=2) là tháng 1.
    Đếm thuận đến tháng sinh (1 bước = 1 tháng).
    Đếm nghịch đến giờ sinh (1 bước = 1 giờ, khởi từ Tý=0).
    """
    thang_index = (2 + thang_am - 1) % 12
    cung_menh_index = (thang_index - gio_chi_index) % 12
    return cung_menh_index

def get_cung_than(thang_am: int, gio_chi_index: int) -> int:
    """
    Tính Cung Thân.
    Bắt đầu từ cung Dần (index=2) là tháng 1.
    Đếm thuận đến tháng sinh (1 bước = 1 tháng).
    Đếm thuận đến giờ sinh (1 bước = 1 giờ, khởi từ Tý=0).
    """
    thang_index = (2 + thang_am - 1) % 12
    cung_than_index = (thang_index + gio_chi_index) % 12
    return cung_than_index

TEN_12_CUNG = [
    "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc", 
    "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ"
]

def get_12_cung(cung_menh_index: int) -> dict:
    """
    An 12 cung, khởi từ Mệnh rồi theo chiều thuận (offset 0..11).
    Trả về dict: {"Mệnh": index, "Phụ Mẫu": index, ...}
    """
    result = {}
    for offset, ten_cung in enumerate(TEN_12_CUNG):
        result[ten_cung] = (cung_menh_index + offset) % 12
    return result

def get_can_cung(can_nam_index: int, cung_index: int) -> int:
    """
    Tính Can của một cung bất kỳ dựa trên Ngũ Hổ Độn.
    Giáp=0, Ất=1, Bính=2, Đinh=3, Mậu=4, Kỷ=5, Canh=6, Tân=7, Nhâm=8, Quý=9.
    Khởi tháng Giêng tại cung Dần (index 2).
    """
    # Tính Can của tháng Dần dựa trên quy tắc Ngũ Hổ Độn:
    # Giáp Kỷ -> Bính Dần (Bính=2)
    # Ất Canh -> Mậu Dần (Mậu=4)
    # Bính Tân -> Canh Dần (Canh=6)
    # Đinh Nhâm -> Nhâm Dần (Nhâm=8)
    # Mậu Quý -> Giáp Dần (Giáp=0)
    can_dan_index = ((can_nam_index % 5) * 2 + 2) % 10
    
    # Tính can của cung_index dựa vào khoảng cách từ cung Dần (phải tính tiến theo chiều thuận)
    distance = (cung_index - 2) % 12
    can_cung_index = (can_dan_index + distance) % 10
    return can_cung_index

def get_cuc_tu_nap_am(can_index: int, chi_index: int) -> str:
    """
    Tính Cục (Ngũ Hành Nạp Âm) từ Can và Chi của cung Mệnh.
    Quy tắc giá trị Nạp Âm:
    Can: Giáp/Ất=1, Bính/Đinh=2, Mậu/Kỷ=3, Canh/Tân=4, Nhâm/Quý=5
    Chi: Tý/Sửu=0, Ngọ/Mùi=0; Dần/Mão=1, Thân/Dậu=1; Thìn/Tỵ=2, Tuất/Hợi=2
    Nạp Âm = Can + Chi (nếu > 5 thì trừ 5).
    1=Kim, 2=Thủy, 3=Hỏa, 4=Thổ, 5=Mộc.
    """
    can_val = (can_index // 2) + 1
    chi_val = (chi_index % 6) // 2
    
    nap_am_val = can_val + chi_val
    if nap_am_val > 5:
        nap_am_val -= 5
        
    return CUC_MAP[nap_am_val]

def get_cuc_and_menh(nam_am: int, thang_am: int, gio_chi_index: int) -> dict:
    """
    Tổng hợp: trả về dict {"cung_menh": int, "cuc": str}
    """
    # Tính Can index của năm (Giáp=0... Quý=9)
    can_nam_index = (nam_am - 4) % 10
    
    # Bước 1: Tính Cung Mệnh
    cung_menh_index = get_cung_menh(thang_am, gio_chi_index)
    
    # Bước 2: Tính Can của Cung Mệnh
    can_menh_index = get_can_cung(can_nam_index, cung_menh_index)
    
    # Bước 3: Tính Cục từ Nạp Âm của Cung Mệnh
    cuc = get_cuc_tu_nap_am(can_menh_index, cung_menh_index)
    
    cung_than_index = get_cung_than(thang_am, gio_chi_index)
    muoi_hai_cung = get_12_cung(cung_menh_index)
    
    return {
        "cung_menh": cung_menh_index,
        "cuc": cuc,
        "can_nam_index": can_nam_index,
        "cung_than": cung_than_index,
        "muoi_hai_cung": muoi_hai_cung
    }

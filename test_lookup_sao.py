import pytest
from lookup_sao import load_sao_data, get_dien_giai_sao

# Load một lần cho tất cả test
@pytest.fixture(scope="module")
def sao_db():
    return load_sao_data()

def test_load_sao_data_count(sao_db):
    # Phải load được ít nhất 90 sao (có 102 file, trừ tu_hoa_bang_chuan.json
    # và một số file không có field "sao")
    assert len(sao_db) >= 90, f"Chỉ load được {len(sao_db)} sao"

def test_lookup_tu_vi_tai_menh(sao_db):
    """Tử Vi tại cung Mệnh — file tử_vi.json có entry này"""
    result = get_dien_giai_sao(sao_db, "Tử Vi", "Mệnh")
    assert result is not None, "Không tìm thấy diễn giải Tử Vi tại Mệnh"
    assert isinstance(result, str), "Diễn giải phải là string"
    assert "Tử Vi" in result or len(result) > 50, "Diễn giải quá ngắn, nghi bị sai"

def test_lookup_tham_lang_tai_phu_the(sao_db):
    """Tham Lang tại Phu Thê — file tham_lang.json có entry này"""
    result = get_dien_giai_sao(sao_db, "Tham Lang", "Phu Thê")
    assert result is not None, "Không tìm thấy diễn giải Tham Lang tại Phu Thê"
    assert isinstance(result, str)

def test_lookup_thien_co_tai_quan_loc(sao_db):
    """Thiên Cơ tại Quan Lộc — file thiên_cơ.json phải có entry này"""
    result = get_dien_giai_sao(sao_db, "Thiên Cơ", "Quan Lộc")
    assert result is not None, "Không tìm thấy diễn giải Thiên Cơ tại Quan Lộc"
    assert isinstance(result, str)

def test_lookup_sao_khong_ton_tai(sao_db):
    """Sao giả lập — phải trả error dict, không raise exception"""
    result = get_dien_giai_sao(sao_db, "Sao Giả Lập Không Tồn Tại", "Mệnh")
    assert isinstance(result, dict)
    assert "error" in result

def test_lookup_cung_khong_co_trong_sao(sao_db):
    """Sao tồn tại nhưng không có entry cho cung đó — phải trả None"""
    # "Hạn" không phải 1 trong 12 cung chính nên đây là cung lạ với Tử Vi
    result = get_dien_giai_sao(sao_db, "Tử Vi", "Cung Giả Không Tồn Tại")
    assert result is None


# ── Tests kiểm chứng cơ chế CUNG_ALIASES ─────────────────────────────────────

def test_lookup_alias_thien_luong_quan_loc(sao_db):
    """File thiên_lương.json ghi cung 'Quan' -> tra cứu bằng 'Quan Lộc' phải tìm thấy."""
    result = get_dien_giai_sao(sao_db, "Thiên Lương", "Quan Lộc")
    assert result is not None, "Alias 'Quan' -> 'Quan Lộc' thất bại cho Thiên Lương"
    assert "Cơ, Lương, Quang, Quí" in result


def test_lookup_alias_liem_trinh_phu_the(sao_db):
    """File liêm_trinh.json ghi cung 'Thê' -> tra cứu bằng 'Phu Thê' phải tìm thấy."""
    result = get_dien_giai_sao(sao_db, "Liêm Trinh", "Phu Thê")
    assert result is not None, "Alias 'Thê' -> 'Phu Thê' thất bại cho Liêm Trinh"
    assert isinstance(result, str)


def test_lookup_alias_loc_ton_tat_ach(sao_db):
    """File lộc_tồn.json ghi cung 'Giải' -> tra cứu bằng 'Tật Ách' phải tìm thấy."""
    result = get_dien_giai_sao(sao_db, "Lộc Tồn", "Tật Ách")
    assert result is not None, "Alias 'Giải' -> 'Tật Ách' thất bại cho Lộc Tồn"
    assert "ốm gặp thuốc" in result


def test_lookup_alias_thien_phu_huynh_de(sao_db):
    """File thiên_phủ.json ghi cung 'Bào' -> tra cứu bằng 'Huynh Đệ' phải tìm thấy."""
    result = get_dien_giai_sao(sao_db, "Thiên Phủ", "Huynh Đệ")
    assert result is not None, "Alias 'Bào' -> 'Huynh Đệ' thất bại cho Thiên Phủ"
    assert isinstance(result, str)


def test_lookup_3_sao_chuan_hoa(sao_db):
    """Kiểm tra 3 sao chuẩn hóa alias: Kình Dương, Thiên Riêu, Thiên Quý"""
    # 1. Kình Dương (12/12 cung, test Mệnh và Điền Trạch)
    res_kd_menh = get_dien_giai_sao(sao_db, "Kình Dương", "Mệnh")
    assert res_kd_menh is not None and isinstance(res_kd_menh, str)
    res_kd_dien = get_dien_giai_sao(sao_db, "Kình Dương", "Điền Trạch")
    assert "vô điền sản" in res_kd_dien

    # 2. Thiên Riêu (test Mệnh)
    res_rieu_menh = get_dien_giai_sao(sao_db, "Thiên Riêu", "Mệnh")
    assert res_rieu_menh is not None and isinstance(res_rieu_menh, str)

    # 3. Thiên Quý (test Mệnh và Điền Trạch)
    res_quy_menh = get_dien_giai_sao(sao_db, "Thiên Quý", "Mệnh")
    assert res_quy_menh is not None and isinstance(res_quy_menh, str)
    res_quy_dien = get_dien_giai_sao(sao_db, "Thiên Quý", "Điền Trạch")
    assert res_quy_dien is not None and isinstance(res_quy_dien, str)


def test_lookup_4_sao_moi_va_bo_sung(sao_db):
    """Kiểm tra 4 sao mới: Bạch Hổ, Trực Phù, Ân Quang, Long Đức và các cung mới bổ sung"""
    # 1. Bạch Hổ
    res_bh_menh = get_dien_giai_sao(sao_db, "Bạch Hổ", "Mệnh")
    assert res_bh_menh is not None and "Bạch Hổ" in res_bh_menh
    res_bh_phuc = get_dien_giai_sao(sao_db, "Bạch Hổ", "Phúc Đức")
    assert res_bh_phuc is not None and "đá trắng" in res_bh_phuc

    # 2. Ân Quang
    res_aq_menh = get_dien_giai_sao(sao_db, "Ân Quang", "Mệnh")
    assert res_aq_menh is not None and "Thông minh" in res_aq_menh
    res_aq_tat = get_dien_giai_sao(sao_db, "Ân Quang", "Tật Ách")
    assert res_aq_tat is not None and "thầy giỏi thuốc hay" in res_aq_tat

    # 3. Trực Phù
    res_tp_menh = get_dien_giai_sao(sao_db, "Trực Phù", "Mệnh")
    assert res_tp_menh is not None and "gian tà" in res_tp_menh

    # 4. Long Đức
    res_ld_menh = get_dien_giai_sao(sao_db, "Long Đức", "Mệnh")
    assert res_ld_menh is not None and "Tứ Đức" in res_ld_menh

    # 5. Các cung bổ sung của Chính tinh từ tan_bien.txt
    res_lt_phu = get_dien_giai_sao(sao_db, "Liêm Trinh", "Phụ Mẫu")
    assert res_lt_phu is not None and "bất hòa" in res_lt_phu
    res_vk_the = get_dien_giai_sao(sao_db, "Vũ Khúc", "Phu Thê")
    assert res_vk_the is not None and "muộn đường hôn phối" in res_vk_the
    res_loc_tai = get_dien_giai_sao(sao_db, "Lộc Tồn", "Tài Bạch")
    assert res_loc_tai is not None and "sung túc" in res_loc_tai




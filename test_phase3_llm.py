"""
test_phase3_llm.py — Kiểm thử Phase 3: Cohere Client, /dien-giai-cung-llm, và /hoi
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

import cohere_client
from main import app, KEYWORD_TO_CUNG, KEYWORD_TO_CHI_SO

client = TestClient(app)

# Dữ liệu lá số thật ngày 21/05/2015 8h00 (Ất Mùi, Hỏa Lục Cục, Mệnh tại Sửu)
SAMPLE_MUOI_HAI_CUNG = {
    "Mệnh": "Sửu",
    "Phụ Mẫu": "Dần",
    "Phúc Đức": "Mão",
    "Điền Trạch": "Thìn",
    "Quan Lộc": "Tỵ",
    "Nô Bộc": "Ngọ",
    "Thiên Di": "Mùi",
    "Tật Ách": "Thân",
    "Tài Bạch": "Dậu",
    "Tử Tức": "Tuất",
    "Phu Thê": "Hợi",
    "Huynh Đệ": "Tý"
}

SAMPLE_CHINH_TINH = {
    "Tử Vi": "Thìn",
    "Liêm Trinh": "Thân",
    "Thiên Đồng": "Hợi",
    "Vũ Khúc": "Tý",
    "Thái Dương": "Sửu",
    "Thiên Cơ": "Mão",
    "Thiên Phủ": "Tý",
    "Thái Âm": "Sửu",
    "Tham Lang": "Dần",
    "Cự Môn": "Mão",
    "Thiên Tướng": "Thìn",
    "Thiên Lương": "Tỵ",
    "Thất Sát": "Ngọ",
    "Phá Quân": "Tuất"
}

SAMPLE_TU_HOA = {
    "Hóa Lộc": "Thiên Cơ",
    "Hóa Quyền": "Thiên Lương",
    "Hóa Khoa": "Tử Vi",
    "Hóa Kỵ": "Thái Âm"
}

SAMPLE_THAN_SO_HOC = {
    "duong_doi": {"gia_tri": 7, "dien_giai": "Người tìm kiếm tri thức, chiêm nghiệm sâu sắc."},
    "su_menh": {"gia_tri": 7, "dien_giai": "Sứ mệnh khai sáng, chia sẻ hiểu biết và trải nghiệm."},
    "linh_hon": {"gia_tri": 1, "dien_giai": "Khao khát tự chủ, dẫn dắt và độc lập."},
    "nhan_cach": {"gia_tri": 33, "dien_giai": "Bác ái, tận tụy phục vụ và truyền cảm hứng."}
}


# ── Test cohere_client ────────────────────────────────────────────────────────

def test_cohere_missing_key():
    """Khi không có API key, hàm trả về thông báo lỗi rõ ràng chứ không crash."""
    res = cohere_client.goi_cohere("prompt", "hello", api_key="")
    assert "[LỖI] COHERE_API_KEY chưa được cấu hình" in res


@patch("cohere.ClientV2")
def test_cohere_mock_success(mock_client_cls):
    """Giả lập gọi Cohere thành công và bộ đếm tăng lên."""
    initial_count = cohere_client.get_call_count()
    mock_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.message.content = [MagicMock(text="Diễn giải mẫu từ AI.")]
    mock_instance.chat.return_value = mock_response
    mock_client_cls.return_value = mock_instance

    res = cohere_client.goi_cohere("prompt", "hello", api_key="test-key")
    assert res == "Diễn giải mẫu từ AI."
    assert cohere_client.get_call_count() == initial_count + 1


@patch("cohere.ClientV2")
def test_cohere_error_handling(mock_client_cls):
    """Test xử lý ngoại lệ mạng / lỗi chung."""
    mock_instance = MagicMock()
    mock_instance.chat.side_effect = Exception("Connection timeout")
    mock_client_cls.return_value = mock_instance

    res = cohere_client.goi_cohere("prompt", "hello", api_key="test-key")
    assert "[LỖI]" in res
    assert "Connection timeout" in res


@patch("cohere.ClientV2")
def test_cohere_unauthorized_error(mock_client_cls):
    """Test xử lý lỗi 401 Unauthorized từ Cohere không bị AttributeError."""
    import cohere
    mock_instance = MagicMock()
    mock_instance.chat.side_effect = cohere.UnauthorizedError(body="Invalid API key")
    mock_client_cls.return_value = mock_instance

    res = cohere_client.goi_cohere("prompt", "hello", api_key="test-key")
    assert "[LỖI 401]" in res


@patch("cohere.ClientV2")
def test_cohere_rate_limit_error(mock_client_cls):
    """Test xử lý lỗi 429 TooManyRequests từ Cohere không bị AttributeError."""
    import cohere
    mock_instance = MagicMock()
    mock_instance.chat.side_effect = cohere.TooManyRequestsError(body="Rate limit exceeded")
    mock_client_cls.return_value = mock_instance

    res = cohere_client.goi_cohere("prompt", "hello", api_key="test-key")
    assert "[LỖI 429]" in res


# ── Test POST /dien-giai-cung-llm ─────────────────────────────────────────────

@patch("main.COHERE_API_KEY", "")
def test_dien_giai_cung_llm_without_key():
    """Test gọi /dien-giai-cung-llm khi chưa có key (hoặc key rỗng) -> trả raw + llm thông báo cấu hình."""
    payload = {
        "ten_cung": "Mệnh",
        "muoi_hai_cung": SAMPLE_MUOI_HAI_CUNG,
        "chinh_tinh": SAMPLE_CHINH_TINH,
        "tu_hoa": SAMPLE_TU_HOA
    }
    response = client.post("/dien-giai-cung-llm", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["cung"] == "Mệnh"
    assert data["dia_chi"] == "Sửu"
    assert "raw" in data
    assert "llm" in data
    assert "[LỖI] COHERE_API_KEY chưa được cấu hình" in data["llm"]
    # raw phải chứa danh sách sao tại cung Mệnh (Sửu: Thái Dương, Thái Âm)
    raw_sao = [s["sao"] for s in data["raw"]["sao_va_dien_giai"]]
    assert "Thái Dương" in raw_sao
    assert "Thái Âm" in raw_sao


@patch("cohere_client.goi_cohere")
def test_dien_giai_cung_llm_with_mock(mock_goi):
    """Test /dien-giai-cung-llm khi LLM sinh diễn giải thành công."""
    mock_goi.return_value = "Người có Thái Dương, Thái Âm tại Sửu tính tình cẩn trọng, phúc lộc song toàn."
    payload = {
        "ten_cung": "Mệnh",
        "muoi_hai_cung": SAMPLE_MUOI_HAI_CUNG,
        "chinh_tinh": SAMPLE_CHINH_TINH,
        "tu_hoa": SAMPLE_TU_HOA
    }
    response = client.post("/dien-giai-cung-llm", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["llm"] == "Người có Thái Dương, Thái Âm tại Sửu tính tình cẩn trọng, phúc lộc song toàn."
    assert "cohere_calls_phien_nay" in data


# ── Test POST /hoi ────────────────────────────────────────────────────────────

@patch("cohere_client.goi_cohere")
def test_hoi_dap_quan_loc(mock_goi):
    """1. Câu hỏi rõ ràng map được cung Quan Lộc (sự nghiệp, công việc)."""
    mock_goi.return_value = "Cung Quan Lộc tại Tỵ có Thiên Lương đắc Hóa Quyền mang lại công danh vững chắc."
    payload = {
        "cau_hoi": "Công việc và sự nghiệp của tôi sau này như thế nào?",
        "muoi_hai_cung": SAMPLE_MUOI_HAI_CUNG,
        "chinh_tinh": SAMPLE_CHINH_TINH,
        "tu_hoa": SAMPLE_TU_HOA,
        "than_so_hoc": SAMPLE_THAN_SO_HOC
    }
    response = client.post("/hoi", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["cung_detect"] == "Quan Lộc"
    assert "Quan Lộc" in data["context_dung"]
    assert "Thiên Lương" in data["context_dung"]
    assert "Hóa Quyền" in data["context_dung"]
    assert "Thiên Lương đắc Hóa Quyền" in data["tra_loi"]


@patch("cohere_client.goi_cohere")
def test_hoi_dap_than_so_hoc(mock_goi):
    """2. Câu hỏi về Thần Số Học (con số đường đời)."""
    mock_goi.return_value = "Bạn mang con số đường đời 7, là người ham học hỏi và nghiên cứu sâu sắc."
    payload = {
        "cau_hoi": "Số đường đời của tôi mang ý nghĩa gì?",
        "muoi_hai_cung": SAMPLE_MUOI_HAI_CUNG,
        "chinh_tinh": SAMPLE_CHINH_TINH,
        "tu_hoa": SAMPLE_TU_HOA,
        "than_so_hoc": SAMPLE_THAN_SO_HOC
    }
    response = client.post("/hoi", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["chi_so_detect"] == "duong_doi"
    assert "DUONG_DOI = 7" in data["context_dung"]
    assert "đường đời 7" in data["tra_loi"]


def test_hoi_dap_mo_ho_fallback():
    """3. Câu hỏi mơ hồ không khớp từ khóa -> trả về hướng dẫn hỏi lại mà không tốn gọi LLM."""
    payload = {
        "cau_hoi": "Ngày mai trời có mưa không?",
        "muoi_hai_cung": SAMPLE_MUOI_HAI_CUNG,
        "chinh_tinh": SAMPLE_CHINH_TINH,
        "tu_hoa": SAMPLE_TU_HOA,
        "than_so_hoc": SAMPLE_THAN_SO_HOC
    }
    response = client.post("/hoi", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["cung_detect"] is None
    assert data["chi_so_detect"] is None
    assert "Câu hỏi chưa đủ rõ" in data["tra_loi"]

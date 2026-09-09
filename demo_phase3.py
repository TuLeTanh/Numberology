"""
demo_phase3.py — Chạy thử nghiệm thực tế các bước Phase 3
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from fastapi.testclient import TestClient
from unittest.mock import patch
import cohere_client
from main import app

client = TestClient(app)

SAMPLE_MUOI_HAI_CUNG = {
    "Mệnh": "Thân",
    "Phụ Mẫu": "Dậu",
    "Phúc Đức": "Tuất",
    "Điền Trạch": "Hợi",
    "Quan Lộc": "Tý",
    "Nô Bộc": "Sửu",
    "Thiên Di": "Dần",
    "Tật Ách": "Mão",
    "Tài Bạch": "Thìn",
    "Tử Tức": "Tị",
    "Phu Thê": "Ngọ",
    "Huynh Đệ": "Mùi"
}

SAMPLE_CHINH_TINH = {
    "Tử Vi": "Dần",
    "Thiên Cơ": "Sửu",
    "Thái Dương": "Tý",
    "Vũ Khúc": "Hợi",
    "Thiên Đồng": "Tuất",
    "Liêm Trinh": "Thân",
    "Thiên Phủ": "Thân",
    "Thái Âm": "Dậu",
    "Tham Lang": "Tuất",
    "Cự Môn": "Hợi",
    "Thiên Tướng": "Tý",
    "Thiên Lương": "Sửu",
    "Thất Sát": "Dần",
    "Phá Quân": "Ngọ"
}

SAMPLE_TU_HOA = {
    "Hóa Cơ": "Thiên Cơ",
    "Hóa Lương": "Thiên Lương",
    "Hóa Vi": "Tử Vi",
    "Hóa Nguyệt": "Thái Âm"
}

SAMPLE_THAN_SO_HOC = {
    "duong_doi": {"gia_tri": 7, "dien_giai": "Người tìm kiếm chân lý, tri thức sâu sắc và ham học hỏi."},
    "su_menh": {"gia_tri": 1, "dien_giai": "Người tiên phong, lãnh đạo độc lập và tự chủ."},
    "linh_hon": {"gia_tri": 4, "dien_giai": "Khao khát sự an toàn, thực tế và trật tự."},
    "nhan_cach": {"gia_tri": 6, "dien_giai": "Ấn tượng chu đáo, ấm áp, có tinh thần trách nhiệm gia đình."}
}

print("=== DEMO BƯỚC 4: /dien-giai-cung-llm (Cung Mệnh 21/05/2015) ===")
# Giả lập phản hồi LLM tự nhiên khi test local (nếu chưa có API key thực)
mock_llm_response = (
    "Cung Mệnh của bạn tọa tại Thân, được đồng cung bởi hai đại tinh Liêm Trinh và Thiên Phủ. "
    "Sự kết hợp này mang lại cho bạn phong thái đĩnh đạc, tính cách cương trực nhưng cũng rất đôn hậu, bao dung. "
    "Bạn có năng lực lãnh đạo, giỏi quản lý tài chính và hoạch định công việc. "
    "Cuộc đời thường được hưởng phúc lộc, sự nghiệp vững vàng và uy tín xã hội cao."
)

with patch("cohere_client.goi_cohere", return_value=mock_llm_response):
    res_b4 = client.post("/dien-giai-cung-llm", json={
        "ten_cung": "Mệnh",
        "muoi_hai_cung": SAMPLE_MUOI_HAI_CUNG,
        "chinh_tinh": SAMPLE_CHINH_TINH,
        "tu_hoa": SAMPLE_TU_HOA
    })
    print("STATUS:", res_b4.status_code)
    print(json.dumps(res_b4.json(), ensure_ascii=False, indent=2))

print("\n=== DEMO BƯỚC 5: POST /hoi ===")
# Case 1: Rõ ràng map cung Quan Lộc
mock_res_ql = (
    "Về đường công danh và sự nghiệp, cung Quan Lộc của bạn ngụ tại Tý với hai sao Thái Dương và Thiên Tướng hội tụ. "
    "Đây là cách cục rất sáng, chủ về con đường sự nghiệp quang minh chính đại, có danh tiếng, được cấp trên tin cậy và có cơ hội thăng tiến mạnh mẽ trong tổ chức hoặc cơ quan lớn."
)
with patch("cohere_client.goi_cohere", return_value=mock_res_ql):
    res_c1 = client.post("/hoi", json={
        "cau_hoi": "Công việc và sự nghiệp tương lai của tôi có thuận lợi không?",
        "muoi_hai_cung": SAMPLE_MUOI_HAI_CUNG,
        "chinh_tinh": SAMPLE_CHINH_TINH,
        "tu_hoa": SAMPLE_TU_HOA,
        "than_so_hoc": SAMPLE_THAN_SO_HOC
    })
    print("\n--- Case 1 (Hỏi sự nghiệp -> map Quan Lộc) ---")
    print(json.dumps(res_c1.json(), ensure_ascii=False, indent=2))

# Case 2: Câu hỏi mơ hồ không map được
res_c2 = client.post("/hoi", json={
    "cau_hoi": "Mai tôi có nên đi câu cá ngoài trời không?",
    "muoi_hai_cung": SAMPLE_MUOI_HAI_CUNG,
    "chinh_tinh": SAMPLE_CHINH_TINH,
    "tu_hoa": SAMPLE_TU_HOA,
    "than_so_hoc": SAMPLE_THAN_SO_HOC
})
print("\n--- Case 2 (Mơ hồ / ngoài phạm vi -> Fallback không gọi LLM) ---")
print(json.dumps(res_c2.json(), ensure_ascii=False, indent=2))

# Case 3: Hỏi Thần Số Học
mock_res_tsh = (
    "Con số đường đời của bạn là số 7. Trong Thần Số Học, số 7 đại diện cho tinh thần tìm kiếm chân lý, tri thức sâu rộng và sự chiêm nghiệm nội tâm. Bạn phù hợp với công việc nghiên cứu, chuyên môn kỹ thuật hoặc tư vấn chiến lược."
)
with patch("cohere_client.goi_cohere", return_value=mock_res_tsh):
    res_c3 = client.post("/hoi", json={
        "cau_hoi": "Ý nghĩa con số đường đời của tôi là gì?",
        "muoi_hai_cung": SAMPLE_MUOI_HAI_CUNG,
        "chinh_tinh": SAMPLE_CHINH_TINH,
        "tu_hoa": SAMPLE_TU_HOA,
        "than_so_hoc": SAMPLE_THAN_SO_HOC
    })
    print("\n--- Case 3 (Hỏi Thần Số Học -> duong_doi) ---")
    print(json.dumps(res_c3.json(), ensure_ascii=False, indent=2))

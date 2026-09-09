"""
run_real_phase3.py — Chạy thật 100% Phase 3 với key Cohere thật (không mock)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from dotenv import load_dotenv
load_dotenv()

from fastapi.testclient import TestClient
import cohere_client
from main import app

client = TestClient(app)

print("================================================================================")
print("BƯỚC 2: GỌI THẬT 1 LẦN ĐƠN GIẢN ĐỂ XÁC NHẬN MODEL HOẠT ĐỘNG & KIỂM TRA COUNTER")
print("================================================================================")
count_before = cohere_client.get_call_count()
print(f"Giá trị get_call_count() TRƯỚC: {count_before}")

resp_b2 = cohere_client.goi_cohere(
    system_prompt="Bạn là trợ lý AI.",
    user_message="Xin chào, bạn là ai? Trả lời thật ngắn gọn đúng 1 câu.",
    max_tokens=60
)
count_after = cohere_client.get_call_count()
print(f"Phản hồi từ Cohere: {resp_b2}")
print(f"Giá trị get_call_count() SAU: {count_after}")
assert count_after == count_before + 1, "Counter phải tăng đúng 1!"


print("\n================================================================================")
print("BƯỚC 3: CHẠY LẠI /dien-giai-cung-llm BẰNG DỮ LIỆU THẬT TỪ /lap-la-so (KEY THẬT)")
print("================================================================================")
# Gọi /lap-la-so lấy đúng dữ liệu 21/05/2015 8h00
payload_lap_la_so = {
    "ho_ten": "Nguyễn Văn A",
    "ngay_sinh": 21,
    "thang_sinh": 5,
    "nam_sinh": 2015,
    "gio_sinh": 8,
    "phut_sinh": 0
}
res_lap = client.post("/lap-la-so", json=payload_lap_la_so).json()
tu_vi_data = res_lap["tu_vi"]
than_so_data = res_lap["than_so_hoc"]

payload_dien_giai = {
    "ten_cung": "Mệnh",
    "muoi_hai_cung": tu_vi_data["muoi_hai_cung"],
    "chinh_tinh": tu_vi_data["14_chinh_tinh"],
    "tu_hoa": tu_vi_data["tu_hoa"]
}

res_b3 = client.post("/dien-giai-cung-llm", json=payload_dien_giai)
data_b3 = res_b3.json()
print("STATUS CODE:", res_b3.status_code)
print(json.dumps(data_b3, ensure_ascii=False, indent=2))
print(f"cohere_calls_phien_nay sau Bước 3 = {data_b3['cohere_calls_phien_nay']}")


print("\n================================================================================")
print("BƯỚC 4: CHẠY LẠI 3 CASE Ở ROUTE /hoi BẰNG KEY THẬT (KIỂM TRA TĂNG COUNTER & FALLBACK)")
print("================================================================================")

# Case 1: Hỏi Quan Lộc (công việc / sự nghiệp) -> Gọi Cohere thật
print("\n--- CASE 1: Hỏi về sự nghiệp (map tới cung Quan Lộc) ---")
res_c1 = client.post("/hoi", json={
    "cau_hoi": "Công việc và sự nghiệp tương lai của tôi có thuận lợi không?",
    "muoi_hai_cung": tu_vi_data["muoi_hai_cung"],
    "chinh_tinh": tu_vi_data["14_chinh_tinh"],
    "tu_hoa": tu_vi_data["tu_hoa"],
    "than_so_hoc": than_so_data
})
data_c1 = res_c1.json()
print("STATUS CODE:", res_c1.status_code)
print(json.dumps(data_c1, ensure_ascii=False, indent=2))
print(f"cohere_calls_phien_nay sau Case 1 = {data_c1['cohere_calls_phien_nay']}")

# Case 2: Hỏi mơ hồ / ngoài phạm vi -> Fallback không gọi Cohere, counter KHÔNG tăng
print("\n--- CASE 2: Hỏi mơ hồ / ngoài phạm vi (Fallback, KHÔNG gọi Cohere) ---")
res_c2 = client.post("/hoi", json={
    "cau_hoi": "Mai tôi có nên đi câu cá ngoài trời không?",
    "muoi_hai_cung": tu_vi_data["muoi_hai_cung"],
    "chinh_tinh": tu_vi_data["14_chinh_tinh"],
    "tu_hoa": tu_vi_data["tu_hoa"],
    "than_so_hoc": than_so_data
})
data_c2 = res_c2.json()
print("STATUS CODE:", res_c2.status_code)
print(json.dumps(data_c2, ensure_ascii=False, indent=2))
print(f"cohere_calls_phien_nay sau Case 2 = {data_c2['cohere_calls_phien_nay']}")
assert data_c2['cohere_calls_phien_nay'] == data_c1['cohere_calls_phien_nay'], "Case mơ hồ không được tăng counter!"

# Case 3: Hỏi Thần Số Học -> Gọi Cohere thật
print("\n--- CASE 3: Hỏi Thần Số Học (map tới số đường đời) ---")
res_c3 = client.post("/hoi", json={
    "cau_hoi": "Ý nghĩa con số đường đời của tôi là gì?",
    "muoi_hai_cung": tu_vi_data["muoi_hai_cung"],
    "chinh_tinh": tu_vi_data["14_chinh_tinh"],
    "tu_hoa": tu_vi_data["tu_hoa"],
    "than_so_hoc": than_so_data
})
data_c3 = res_c3.json()
print("STATUS CODE:", res_c3.status_code)
print(json.dumps(data_c3, ensure_ascii=False, indent=2))
print(f"cohere_calls_phien_nay sau Case 3 = {data_c3['cohere_calls_phien_nay']}")


print("\n================================================================================")
print("BƯỚC 5: TỔNG KẾT QUOTA ĐÃ SỬ DỤNG")
print("================================================================================")
total_calls = cohere_client.get_call_count()
print(f"Tổng số lượt gọi Cohere API thật trong phiên chạy này: {total_calls}")
print(f"Hạn mức trial: 1000 lượt gọi / tháng")
print(f"Số lượt gọi ước tính còn lại: {1000 - total_calls} lượt")

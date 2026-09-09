"""
audit_alias_impact.py — Đo lường chính xác mức độ ảnh hưởng của bug alias cung
"""
import sys
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

import lookup_sao

sao_data = lookup_sao.load_sao_data()

CUNG_12_CHUAN = [
    "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch",
    "Quan Lộc", "Nô Bộc", "Thiên Di", "Tật Ách",
    "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ"
]

# 1. Đo lường trên TOÀN BỘ 101 sao trong sao_json (mỗi sao x 12 cung = 101 x 12 = 1212 cặp)
total_pairs = 0
found_before = 0
found_after = 0
recovered_list = []

for sao_name in sao_data:
    for cung in CUNG_12_CHUAN:
        total_pairs += 1
        # Tra cứu cũ: chỉ match exact entry["cung"] == cung
        old_found = False
        y_list = sao_data[sao_name].get("y_nghia_theo_cung", [])
        for e in y_list:
            if e.get("cung") == cung:
                old_found = True
                break
        if old_found:
            found_before += 1

        # Tra cứu mới: qua get_dien_giai_sao (có alias)
        new_res = lookup_sao.get_dien_giai_sao(sao_data, sao_name, cung)
        if new_res and not isinstance(new_res, dict):
            found_after += 1
            if not old_found:
                recovered_list.append((sao_name, cung))

print("================================================================================")
print("BÁO CÁO AUDIT MỨC ĐỘ ẢNH HƯỞNG CỦA BUG ALIAS CUNG TRÊN TOÀN BỘ DATABASE")
print("================================================================================")
print(f"Tổng số cặp (sao, cung chuẩn 12 cung) kiểm tra: {total_pairs}")
print(f"- Số cặp tra cứu thành công TRƯỚC khi có alias: {found_before}")
print(f"- Số cặp tra cứu thành công SAU khi có alias   : {found_after}")
print(f"- Số cặp được phục hồi (trước bị warning thiếu dữ liệu, nay đã có dữ liệu): {len(recovered_list)}")
print(f"- Tỷ lệ dữ liệu được phục hồi / cải thiện: +{len(recovered_list) / (found_before if found_before else 1) * 100:.2f}% (tăng thêm {len(recovered_list)} tổ hợp)")

print("\nDanh sách chi tiết các tổ hợp (sao, cung) được phục hồi nhờ bảng alias:")
for idx, (s, c) in enumerate(recovered_list, 1):
    print(f"  {idx:2d}. Sao '{s}' tại cung '{c}'")

# 2. Đo lường trên LÁ SỐ THẬT 21/05/2015 8h00 (14 chính tinh)
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
res_lap = client.post("/lap-la-so", json={
    "ho_ten": "Nguyễn Văn A", "ngay_sinh": 21, "thang_sinh": 5, "nam_sinh": 2015, "gio_sinh": 8, "phut_sinh": 0
}).json()

chinh_tinh = res_lap["tu_vi"]["14_chinh_tinh"]
muoi_hai_cung = res_lap["tu_vi"]["muoi_hai_cung"]
dia_chi_to_cung = {v: k for k, v in muoi_hai_cung.items()}

print("\n================================================================================")
print("AUDIT TRÊN LÁ SỐ THẬT 21/05/2015 8h00 (14 Chính Tinh)")
print("================================================================================")
before_count_ls = 0
after_count_ls = 0
recovered_ls = []

for sao, dc in chinh_tinh.items():
    cung_ten = dia_chi_to_cung[dc]
    # Check old
    old_ok = False
    for e in sao_data.get(sao.upper(), {}).get("y_nghia_theo_cung", []):
        if e.get("cung") == cung_ten:
            old_ok = True
            break
    if old_ok:
        before_count_ls += 1

    # Check new
    new_dg = lookup_sao.get_dien_giai_sao(sao_data, sao, cung_ten)
    if new_dg and not isinstance(new_dg, dict):
        after_count_ls += 1
        if not old_ok:
            recovered_ls.append((sao, cung_ten, dc))

print(f"Tổng số chính tinh trong lá số: 14")
print(f"- Số sao tra cứu thành công TRƯỚC khi có alias: {before_count_ls}/14")
print(f"- Số sao tra cứu thành công SAU khi có alias  : {after_count_ls}/14")
print(f"- Sao được phục hồi cụ thể: {recovered_ls}")

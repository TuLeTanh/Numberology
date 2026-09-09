import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_phase2_demo():
    # Bước 1: Lập lá số
    print("\n=== BƯỚC 1: LẬP LÁ SỐ (21/05/2015, 8h00) ===")
    la_so_resp = client.post("/lap-la-so", json={
        "ho_ten": "Nguyễn Văn An",
        "ngay_sinh": 21, "thang_sinh": 5, "nam_sinh": 2015,
        "gio_sinh": 8, "phut_sinh": 0, "gioi_tinh": "nam"
    })
    assert la_so_resp.status_code == 200
    la_so = la_so_resp.json()
    tu_vi = la_so["tu_vi"]

    print(f"Cung Mệnh : {tu_vi['cung_menh']}")
    print(f"Cung Thân : {tu_vi['cung_than']}")
    print(f"Cục       : {tu_vi['cuc']}")
    print(f"14 Chính Tinh: {json.dumps(tu_vi['14_chinh_tinh'], ensure_ascii=False)}")

    # Bước 2: Tra diễn giải Cung Mệnh (Sửu)
    print("\n=== BƯỚC 2: DIỄN GIẢI CUNG MỆNH ===")
    dg_resp = client.post("/dien-giai-cung", json={
        "ten_cung": "Mệnh",
        "muoi_hai_cung": tu_vi["muoi_hai_cung"],
        "chinh_tinh": tu_vi["14_chinh_tinh"],
        "tu_hoa": tu_vi["tu_hoa"]
    })
    assert dg_resp.status_code == 200
    dg = dg_resp.json()
    print(f"Cung: {dg['cung']} (tại Địa Chi: {dg['dia_chi']})")
    print(f"Số sao tại cung: {dg['so_sao']}")

    for entry in dg["sao_va_dien_giai"]:
        print(f"\n--- SAO: {entry['sao']} ---")
        if entry.get("tu_hoa"):
            print(f"  Tứ Hóa: {entry['tu_hoa']}")
        if entry.get("warning"):
            print(f"  [THIẾU DỮ LIỆU] {entry['warning']}")
        else:
            dien_giai = entry.get("dien_giai", "")
            print(f"  Diễn giải (250 ký tự đầu): {dien_giai[:250]}...")

    # Assertions
    assert dg["cung"] == "Mệnh"
    assert dg["dia_chi"] == tu_vi["cung_menh"]
    assert dg["so_sao"] >= 0

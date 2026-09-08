from fastapi.testclient import TestClient
from main import app
import json

def test_lap_la_so():
    with TestClient(app) as client:
        # 2015-05-21 (Solar) -> Ất Mùi, Tháng 4, Ngày 4 (Lunar)
        # Giờ Thìn (8h00)
        data = {
            "ho_ten": "Nguyễn Văn An",
            "ngay_sinh": 21,
            "thang_sinh": 5,
            "nam_sinh": 2015,
            "gio_sinh": 8,
            "phut_sinh": 0,
            "gioi_tinh": "nam"
        }
        
        response = client.post("/lap-la-so", json=data)
        print("Status Code:", response.status_code)
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=True))

if __name__ == "__main__":
    test_lap_la_so()

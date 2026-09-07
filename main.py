import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

# Import the existing numerology engine
import engine_than_so_hoc

app = FastAPI(title="Tử Vi & Thần Số Học API")

# Global variable for in-memory DB
numerology_db = {}

# Pydantic input model
class LassoInput(BaseModel):
    ho_ten: str
    ngay_sinh: int
    thang_sinh: int
    nam_sinh: int
    gio_sinh: Optional[int] = None
    phut_sinh: Optional[int] = None
    gioi_tinh: Optional[str] = None # "nam" or "nu"

@app.on_event("startup")
def load_data():
    global numerology_db
    json_path = os.path.join("data", "than_so_hoc_bang_tra_v2.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            numerology_db = json.load(f)
        print("Loaded numerology database successfully.")
    except Exception as e:
        print(f"Error loading numerology database: {e}")

@app.post("/lasso")
def get_lasso(data: LassoInput):
    # 1. Tính toán bằng engine
    life_path = engine_than_so_hoc.calculate_life_path(data.ngay_sinh, data.thang_sinh, data.nam_sinh)
    destiny = engine_than_so_hoc.calculate_destiny(data.ho_ten)
    soul_urge = engine_than_so_hoc.calculate_soul_urge(data.ho_ten)
    personality = engine_than_so_hoc.calculate_personality(data.ho_ten)

    # 2. Lookup dữ liệu diễn giải từ DB in-memory
    def get_info(branch, value):
        val_str = str(value)
        if branch in numerology_db and val_str in numerology_db[branch]:
            return numerology_db[branch][val_str]
        return {"error": "No description found"}

    result = {
        "thong_tin_ca_nhan": {
            "ho_ten": data.ho_ten,
            "ngay_thang_nam_sinh": f"{data.ngay_sinh}/{data.thang_sinh}/{data.nam_sinh}"
        },
        "than_so_hoc": {
            "duong_doi": {
                "gia_tri": life_path,
                "dien_giai": get_info("duong_doi", life_path)
            },
            "su_menh": {
                "gia_tri": destiny,
                "dien_giai": get_info("su_menh", destiny)
            },
            "linh_hon": {
                "gia_tri": soul_urge,
                "dien_giai": get_info("linh_hon", soul_urge)
            },
            "nhan_cach": {
                "gia_tri": personality,
                "dien_giai": get_info("nhan_cach", personality)
            }
        }
    }
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

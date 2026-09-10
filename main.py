import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import os
from dotenv import load_dotenv

# Đọc .env trước mọi thứ khác
load_dotenv()
COHERE_API_KEY = os.environ.get("COHERE_API_KEY", "")

# Import the existing numerology engine
import engine_than_so_hoc
# Import the newly created tu vi engine
import engine_tu_vi
# Import Phase 2 retrieval layer
import lookup_sao
# Import Phase 3 Cohere wrapper
import cohere_client

# Global variables for in-memory DB
numerology_db = {}
sao_data = {}

def load_numerology_db() -> dict:
    global numerology_db
    if not numerology_db:
        json_path = os.path.join(os.path.dirname(__file__), "data", "than_so_hoc_bang_tra_v2.json")
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                numerology_db = json.load(f)
            print("Loaded numerology database successfully.")
        except Exception as e:
            print(f"Error loading numerology database: {e}")
    return numerology_db


def get_numerology_info(branch: str, value: int | str):
    """
    Hàm tra cứu Thần Số Học dùng chung cho toàn bộ app (/lasso, /lap-la-so, /hoi).
    Tự động nạp DB nếu chưa có (lazy load).
    """
    db = load_numerology_db()
    val_str = str(value)
    if branch in db and val_str in db[branch]:
        return db[branch][val_str]
    return {"error": "No description found"}


def format_numerology_text(dg) -> str:
    """Format kết quả tra cứu Thần Số Học thành text tự nhiên cho LLM context."""
    if isinstance(dg, dict):
        if "error" in dg:
            return ""
        parts = []
        if "y_nghia_tong_quat" in dg:
            parts.append(dg["y_nghia_tong_quat"])
        if "diem_manh" in dg:
            parts.append(f"Điểm mạnh: {dg['diem_manh']}")
        if "diem_yeu" in dg:
            parts.append(f"Điểm yếu: {dg['diem_yeu']}")
        if parts:
            return " ".join(parts)
        return str(dg)
    return str(dg) if dg else ""


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global numerology_db, sao_data
    # Kiểm tra Cohere key
    if not COHERE_API_KEY:
        print("[CẢNH BÁO] COHERE_API_KEY chưa được cấu hình. Các route LLM sẽ không hoạt động.")
    else:
        print("[OK] COHERE_API_KEY đã được nạp.")
    # Load Thần Số Học DB
    load_numerology_db()
    # Load Sao data (Phase 2)
    try:
        sao_data = lookup_sao.load_sao_data()
        print(f"Loaded {len(sao_data)} sao entries.")
    except Exception as e:
        print(f"Error loading sao data: {e}")
    yield
    # Any cleanup would go here

app = FastAPI(title="Tử Vi & Thần Số Học API", lifespan=lifespan)

# Cấu hình CORS cho phép toàn bộ origin kết nối (MVP nội bộ, không có auth/dữ liệu nhạy cảm theo PRD mục 7)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic input model for Tử Vi An Sao
class AnSaoInput(BaseModel):
    cuc: str
    ngay_sinh_am: int

class LassoInput(BaseModel):
    ho_ten: str
    ngay_sinh: int
    thang_sinh: int
    nam_sinh: int
    gio_sinh: Optional[int] = None
    phut_sinh: Optional[int] = None
    gioi_tinh: Optional[str] = "nam" # "nam" hoặc "nu", mặc định "nam"

def chuan_hoa_gioi_tinh(gt: Optional[str]) -> str:
    """
    Chuẩn hóa input giới tính về 'nam' hoặc 'nu'.
    Chấp nhận: 'nam', 'nu', 'nữ' (không phân biệt hoa thường).
    Nếu không hợp lệ, raise HTTPException 400 rõ ràng.
    """
    if gt is None:
        return "nam"
    s = str(gt).strip().lower()
    if s in ("nam",):
        return "nam"
    if s in ("nu", "nữ"):
        return "nu"
    raise HTTPException(
        status_code=400,
        detail=f"Giới tính '{gt}' không hợp lệ. Chỉ chấp nhận 'nam', 'nu' hoặc 'nữ'."
    )

@app.post("/an-sao")
def post_an_sao(data: AnSaoInput):
    try:
        result = engine_tu_vi.an_14_chinh_tinh(data.cuc, data.ngay_sinh_am)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def tao_bang_12_cung(
    muoi_hai_cung_idx: Dict[str, int],
    can_nam_index: int,
    chinh_tinh: Dict[str, str],
    tu_hoa: Dict[str, str],
    phu_tinh: Dict[str, str],
    vong_thai_tue: Dict[str, str],
    tuan_triet: Dict[str, list],
    dao_hong_hi: Dict[str, str],
    quang_quy: Dict[str, str],
    khoc_hu_co_qua: Dict[str, str],
    hinh_rieu_y: Dict[str, str],
) -> Dict[str, dict]:
    """
    Gộp toàn bộ chính tinh và phụ tinh theo từng cung chức năng (Mệnh, Phụ Mẫu, ...).
    Mỗi cung bao gồm:
    - dia_chi: Tên Chi (Sửu, Dần, ...)
    - can: Tên Can của cung theo Ngũ Hổ Độn (Kỷ, Canh, ...)
    - chinh_tinh: Danh sách dict [{'sao': 'Thái Dương', 'tu_hoa': None}, {'sao': 'Thái Âm', 'tu_hoa': 'Hóa Kỵ'}]
    - phu_tinh: Danh sách tên các phụ tinh đóng tại cung đó.
    """
    import an_menh_cuc
    sao_to_hoa = {sao: loai_hoa for loai_hoa, sao in (tu_hoa or {}).items()}
    
    bang = {}
    for ten_cung, cung_chi_idx in muoi_hai_cung_idx.items():
        dia_chi = engine_tu_vi.CHI_MAP[cung_chi_idx]
        can_idx = an_menh_cuc.get_can_cung(can_nam_index, cung_chi_idx)
        can = engine_tu_vi.CAN_MAP[can_idx]
        
        # Danh sách chính tinh tại cung
        ds_chinh_tinh = [
            {"sao": sao, "tu_hoa": sao_to_hoa.get(sao)}
            for sao, dc in chinh_tinh.items()
            if dc == dia_chi
        ]
        
        # Danh sách phụ tinh tại cung (gộp từ 7 nhóm)
        ds_phu_tinh = []
        for pt_dict in [phu_tinh, vong_thai_tue, dao_hong_hi, quang_quy, khoc_hu_co_qua, hinh_rieu_y]:
            for sao, dc in pt_dict.items():
                if dc == dia_chi:
                    ds_phu_tinh.append(sao)
                    
        # Xử lý riêng Tuần/Triệt (giá trị là list 2 cung)
        for sao_khong, list_dc in (tuan_triet or {}).items():
            if dia_chi in list_dc:
                ds_phu_tinh.append(sao_khong)
                
        bang[ten_cung] = {
            "dia_chi": dia_chi,
            "can": can,
            "chinh_tinh": ds_chinh_tinh,
            "phu_tinh": ds_phu_tinh
        }
        
    return bang


@app.post("/lasso")
def get_lasso(data: LassoInput):
    """
    Endpoint CHÍNH THỨC theo PRD v2 mục 5.4:
    Nhận thông tin sinh (họ tên, ngày/tháng/năm, giờ/phút, giới tính),
    trả về kết quả an sao Tử Vi + chỉ số Thần Số Học trong 1 lần gọi (stateless).
    """
    import datetime as dt
    from lunar_vn import solar_to_lunar
    import an_menh_cuc
    
    # Chuẩn hóa giới tính
    gioi_tinh_clean = chuan_hoa_gioi_tinh(data.gioi_tinh)

    # 1. Thần Số Học (dùng chung get_numerology_info)
    life_path = engine_than_so_hoc.calculate_life_path(data.ngay_sinh, data.thang_sinh, data.nam_sinh)
    destiny = engine_than_so_hoc.calculate_destiny(data.ho_ten)
    soul_urge = engine_than_so_hoc.calculate_soul_urge(data.ho_ten)
    personality = engine_than_so_hoc.calculate_personality(data.ho_ten)

    # 2. Tử Vi Đẩu Số
    # Đổi ngày Dương sang ngày Âm
    solar_date = dt.date(data.nam_sinh, data.thang_sinh, data.ngay_sinh)
    lunar_date = solar_to_lunar(solar_date)
    nam_am = lunar_date.year
    thang_am = lunar_date.month
    ngay_am = lunar_date.day
    
    tu_vi_result = {}
    if data.gio_sinh is not None and data.phut_sinh is not None:
        try:
            from an_menh_cuc import get_gio_chi_index
            gio_chi_idx = get_gio_chi_index(data.gio_sinh, data.phut_sinh)
            
            # Tính Mệnh & Cục
            menh_cuc = an_menh_cuc.get_cuc_and_menh(nam_am, thang_am, gio_chi_idx)
            cung_menh_idx = menh_cuc["cung_menh"]
            cuc = menh_cuc["cuc"]
            can_nam_index = menh_cuc["can_nam_index"]
            cung_than_idx = menh_cuc["cung_than"]
            muoi_hai_cung_idx = menh_cuc["muoi_hai_cung"]
            
            # An 14 Chính Tinh
            chinh_tinh = engine_tu_vi.an_14_chinh_tinh(cuc, ngay_am)
            
            # Chuyển đổi index -> tên cung Mệnh, Thân
            cung_menh_ten = engine_tu_vi.CHI_MAP[cung_menh_idx]
            cung_than_ten = engine_tu_vi.CHI_MAP[cung_than_idx]
            
            # Chuyển đổi index -> tên 12 cung
            muoi_hai_cung_ten = {
                ten_cung: engine_tu_vi.CHI_MAP[idx]
                for ten_cung, idx in muoi_hai_cung_idx.items()
            }
            
            # Format output cho các sao, đưa từ dạng Chi Index sang tên Chi
            sao_ten = {sao: engine_tu_vi.CHI_MAP[idx] for sao, idx in chinh_tinh.items()}
            
            # Tứ Hóa
            import tu_hoa
            tu_hoa_sao = tu_hoa.get_tu_hoa(can_nam_index)

            # Phụ Tinh (Nhóm 1: Vòng Lộc Tồn + Lục Sát Tinh)
            import an_phu_tinh
            chi_nam_index = (nam_am - 4) % 12
            phu_tinh_idx = an_phu_tinh.an_phu_tinh_nhom_1(
                can_nam_idx=can_nam_index,
                chi_nam_idx=chi_nam_index,
                gio_chi_idx=gio_chi_idx,
                gioi_tinh=gioi_tinh_clean
            )
            phu_tinh_ten = {sao: engine_tu_vi.CHI_MAP[idx] for sao, idx in phu_tinh_idx.items()}

            # Vòng Thái Tuế (12 sao an theo Chi năm sinh)
            vong_thai_tue_idx = an_phu_tinh.an_vong_thai_tue(chi_nam_idx=chi_nam_index)
            vong_thai_tue_ten = {sao: engine_tu_vi.CHI_MAP[idx] for sao, idx in vong_thai_tue_idx.items()}

            # Nhị Không (Tuần Trung Không Vong & Triệt Lộ Không Vong)
            tuan_triet_idx = an_phu_tinh.an_tuan_triet(can_nam_idx=can_nam_index, chi_nam_idx=chi_nam_index)
            tuan_triet_ten = {
                sao: [engine_tu_vi.CHI_MAP[idx] for idx in idx_list]
                for sao, idx_list in tuan_triet_idx.items()
            }

            # Bộ Đào Hồng Hỷ (Đào Hoa, Hồng Loan, Thiên Hỷ)
            dao_hong_hi_idx = an_phu_tinh.an_dao_hong_hi(chi_nam_idx=chi_nam_index)
            dao_hong_hi_ten = {sao: engine_tu_vi.CHI_MAP[idx] for sao, idx in dao_hong_hi_idx.items()}

            # Bộ Quang Quý (Ân Quang, Thiên Quý)
            quang_quy_idx = an_phu_tinh.an_quang_quy(gio_chi_idx=gio_chi_idx, ngay_am=ngay_am)
            quang_quy_ten = {sao: engine_tu_vi.CHI_MAP[idx] for sao, idx in quang_quy_idx.items()}

            # Bộ Khốc Hư & Cô Quả (4 sao an theo Chi năm)
            khoc_hu_idx = an_phu_tinh.an_khoc_hu(chi_nam_idx=chi_nam_index)
            co_qua_idx = an_phu_tinh.an_co_qua(chi_nam_idx=chi_nam_index)
            khoc_hu_co_qua_idx = {**khoc_hu_idx, **co_qua_idx}
            khoc_hu_co_qua_ten = {sao: engine_tu_vi.CHI_MAP[idx] for sao, idx in khoc_hu_co_qua_idx.items()}

            # Bộ Hình Riêu Y (3 sao an theo Tháng sinh)
            hinh_rieu_y_idx = an_phu_tinh.an_hinh_rieu_y(thang_am=thang_am)
            hinh_rieu_y_ten = {sao: engine_tu_vi.CHI_MAP[idx] for sao, idx in hinh_rieu_y_idx.items()}
            
            # Gộp dữ liệu theo từng cung chức năng (bang_12_cung)
            bang_12_cung = tao_bang_12_cung(
                muoi_hai_cung_idx=muoi_hai_cung_idx,
                can_nam_index=can_nam_index,
                chinh_tinh=sao_ten,
                tu_hoa=tu_hoa_sao,
                phu_tinh=phu_tinh_ten,
                vong_thai_tue=vong_thai_tue_ten,
                tuan_triet=tuan_triet_ten,
                dao_hong_hi=dao_hong_hi_ten,
                quang_quy=quang_quy_ten,
                khoc_hu_co_qua=khoc_hu_co_qua_ten,
                hinh_rieu_y=hinh_rieu_y_ten,
            )

            tu_vi_result = {
                "am_lich": {
                    "ngay": ngay_am,
                    "thang": thang_am,
                    "nam": nam_am,
                    "nhuan": lunar_date.leap
                },
                "gio_chi": engine_tu_vi.CHI_MAP[gio_chi_idx],
                "cung_menh": cung_menh_ten,
                "cung_than": cung_than_ten,
                "muoi_hai_cung": muoi_hai_cung_ten,
                "cuc": cuc,
                "tu_hoa": tu_hoa_sao,
                "14_chinh_tinh": sao_ten,
                "phu_tinh": phu_tinh_ten,
                "vong_thai_tue": vong_thai_tue_ten,
                "tuan_triet": tuan_triet_ten,
                "dao_hong_hi": dao_hong_hi_ten,
                "quang_quy": quang_quy_ten,
                "khoc_hu_co_qua": khoc_hu_co_qua_ten,
                "hinh_rieu_y": hinh_rieu_y_ten,
                "bang_12_cung": bang_12_cung
            }
        except ValueError as e:
            tu_vi_result = {"error": str(e)}
    else:
        tu_vi_result = {"message": "Thiếu giờ/phút sinh để lập lá số Tử Vi."}

    result = {
        "thong_tin_ca_nhan": {
            "ho_ten": data.ho_ten,
            "ngay_thang_nam_sinh": f"{data.ngay_sinh}/{data.thang_sinh}/{data.nam_sinh}"
        },
        "than_so_hoc": {
            "duong_doi": {
                "gia_tri": life_path,
                "dien_giai": get_numerology_info("duong_doi", life_path)
            },
            "su_menh": {
                "gia_tri": destiny,
                "dien_giai": get_numerology_info("su_menh", destiny)
            },
            "linh_hon": {
                "gia_tri": soul_urge,
                "dien_giai": get_numerology_info("linh_hon", soul_urge)
            },
            "nhan_cach": {
                "gia_tri": personality,
                "dien_giai": get_numerology_info("nhan_cach", personality)
            }
        },
        "tu_vi": tu_vi_result
    }
    
    return result


@app.post("/lap-la-so")
def lap_la_so(data: LassoInput):
    """
    ALIAS cho /lasso (giữ nguyên để đảm bảo backward compatibility với code/test cũ).
    Dùng chung 100% logic với get_lasso.
    """
    return get_lasso(data)


# ── Phase 2: Retrieval routes ────────────────────────────────────────────────

class DienGiaiCungInput(BaseModel):
    """
    Client gửi lại toàn bộ kết quả đã tính từ /lasso + tên cung muốn tra.
    Dùng POST thay vì GET path param vì payload quá lớn cho URL.
    """
    ten_cung: str                                # e.g. "Mệnh", "Phu Thê"
    muoi_hai_cung: Dict[str, str]                # {"Mệnh": "Sửu", "Phụ Mẫu": "Dần", ...}
    chinh_tinh: Dict[str, str]                   # {"Tử Vi": "Thìn", "Tham Lang": "Dần", ...}
    tu_hoa: Optional[Dict[str, str]] = {}        # {"Hóa Lộc": "Thiên Cơ", ...}
    phu_tinh: Optional[Dict[str, str]] = {}
    vong_thai_tue: Optional[Dict[str, str]] = {}
    tuan_triet: Optional[Dict[str, List[str]]] = {}
    dao_hong_hi: Optional[Dict[str, str]] = {}
    quang_quy: Optional[Dict[str, str]] = {}
    khoc_hu_co_qua: Optional[Dict[str, str]] = {}
    hinh_rieu_y: Optional[Dict[str, str]] = {}


@app.post("/dien-giai-cung")
def dien_giai_cung(data: DienGiaiCungInput):
    """
    Từ ten_cung, tìm Địa Chi của cung đó trong muoi_hai_cung,
    sau đó tìm các sao đang đóng tại Địa Chi đó trong chinh_tinh và các nhóm phụ tinh,
    cuối cùng tra dien_giai thô cho từng sao.
    """
    global sao_data
    # Lazy fallback: nếu lifespan chưa chạy (e.g. TestClient không dùng context manager)
    if not sao_data:
        sao_data = lookup_sao.load_sao_data()

    ten_cung = data.ten_cung

    # Bước 1: Tìm địa chi của cung được hỏi
    if ten_cung not in data.muoi_hai_cung:
        raise HTTPException(
            status_code=400,
            detail=f"Cung '{ten_cung}' không có trong muoi_hai_cung được gửi lên."
        )
    dia_chi_cung = data.muoi_hai_cung[ten_cung]  # e.g. "Sửu"

    # Bước 2: Tìm các sao đang ở địa chi đó (gồm chính tinh và phụ tinh)
    sao_tai_cung = [
        ten_sao
        for ten_sao, dia_chi_sao in data.chinh_tinh.items()
        if dia_chi_sao == dia_chi_cung
    ]
    for pt_dict in [
        data.phu_tinh or {},
        data.vong_thai_tue or {},
        data.dao_hong_hi or {},
        data.quang_quy or {},
        data.khoc_hu_co_qua or {},
        data.hinh_rieu_y or {},
    ]:
        for ten_sao, dia_chi_sao in pt_dict.items():
            if dia_chi_sao == dia_chi_cung and ten_sao not in sao_tai_cung:
                sao_tai_cung.append(ten_sao)
    for ten_sao, list_dc in (data.tuan_triet or {}).items():
        if dia_chi_cung in list_dc and ten_sao not in sao_tai_cung:
            sao_tai_cung.append(ten_sao)

    # Bước 3: Với mỗi sao, xác định sao đang ở cung nào trong 12 cung
    # (vì sao tra cứu theo tên cung, không theo địa chi)
    # Đảo ngược muoi_hai_cung: {dia_chi -> ten_cung}
    dia_chi_to_cung = {v: k for k, v in data.muoi_hai_cung.items()}
    ten_cung_de_tra = dia_chi_to_cung.get(dia_chi_cung, ten_cung)

    # Kiểm tra Tứ Hóa xem sao nào đang được hóa
    hoa_map = {}  # ten_sao -> [loai_hoa]
    for loai_hoa, ten_sao_hoa in (data.tu_hoa or {}).items():
        hoa_map.setdefault(ten_sao_hoa, []).append(loai_hoa)

    # Bước 4: Tra diễn giải
    ket_qua = []
    for ten_sao in sao_tai_cung:
        dg = lookup_sao.get_dien_giai_sao(sao_data, ten_sao, ten_cung_de_tra)
        entry = {
            "sao": ten_sao,
            "tai_cung": ten_cung_de_tra,
            "tai_dia_chi": dia_chi_cung,
            "tu_hoa": hoa_map.get(ten_sao, []),
        }
        if isinstance(dg, dict) and "error" in dg:
            entry["dien_giai"] = None
            entry["warning"] = dg["error"]
        elif dg is None:
            entry["dien_giai"] = None
            entry["warning"] = f"Chưa có dữ liệu diễn giải cho {ten_sao} tại cung {ten_cung_de_tra}"
        else:
            entry["dien_giai"] = dg
        ket_qua.append(entry)

    return {
        "cung": ten_cung,
        "dia_chi": dia_chi_cung,
        "so_sao": len(ket_qua),
        "sao_va_dien_giai": ket_qua
    }


# ── Phase 3: System Prompt & LLM routes ─────────────────────────────────────────

SYSTEM_PROMPT_TU_VI = """\
Bạn là trợ lý tư vấn Tử Vi Đẩu Số chuyên nghiệp. Hãy tuân thủ nghiêm ngặt các quy tắc sau:

1. CHỈ dùng thông tin được cung cấp trong phần [CONTEXT] bên dưới. Không thêm bất kỳ kiến thức Tử Vi, 
   Thần Số Học hay tử vi ngoài vào dù bạn có biết.

2. Nếu context THIẾU thông tin để trả lời câu hỏi, hãy NÓI RÕ là "Dữ liệu chưa đủ để diễn giải 
   điểm này" — tuyệt đối không bịa hoặc đoán mò.

3. Viết bằng tiếng Việt, văn phong tự nhiên, dễ hiểu cho người bình thường. Không dùng nguyên văn 
   cổ văn khó đọc từ tài liệu gốc (viết tắt, chữ hán nôm). Giải thích thuật ngữ nếu cần.

4. Giữ độ dài phù hợp: đủ để người đọc hiểu rõ, không dài dòng.
"""

# ── Bảng từ khóa → cung (dùng cho route /hoi) ──
KEYWORD_TO_CUNG = {
    # Sự nghiệp
    "sự nghiệp": "Quan Lộc",
    "công việc": "Quan Lộc",
    "nghề nghiệp": "Quan Lộc",
    "thăng tiến": "Quan Lộc",
    "sự thành đạt": "Quan Lộc",
    "chức vụ": "Quan Lộc",
    # Tài chính
    "tiền bạc": "Tài Bạch",
    "tài chính": "Tài Bạch",
    "thu nhập": "Tài Bạch",
    "tiền tài": "Tài Bạch",
    "làm giàu": "Tài Bạch",
    # Tình cảm / hôn nhân
    "tình cảm": "Phu Thê",
    "hôn nhân": "Phu Thê",
    "vợ chồng": "Phu Thê",
    "tình yêu": "Phu Thê",
    "người yêu": "Phu Thê",
    "bạn đời": "Phu Thê",
    # Sức khỏe
    "sức khỏe": "Tật Ách",
    "bệnh tật": "Tật Ách",
    "tai nạn": "Tật Ách",
    # Con cái
    "con cái": "Tử Tức",
    "sinh con": "Tử Tức",
    "con cái": "Tử Tức",
    # Cha mẹ
    "cha mẹ": "Phụ Mẫu",
    "bố mẹ": "Phụ Mẫu",
    # Bạn bè / người hầu
    "bạn bè": "Nô Bộc",
    "đồng nghiệp": "Nô Bộc",
    "nhân viên": "Nô Bộc",
    # Anh em
    "anh em": "Huynh Đệ",
    "anh chị em": "Huynh Đệ",
    # Nhà cửa / bất động sản
    "nhà cửa": "Điền Trạch",
    "bất động sản": "Điền Trạch",
    "nhà đất": "Điền Trạch",
    # Du lịch / di chuyển
    "du lịch": "Thiên Di",
    "xuất ngoại": "Thiên Di",
    "định cư": "Thiên Di",
    "di chuyển": "Thiên Di",
    # Phúc đức / tâm linh
    "phúc đức": "Phúc Đức",
    "tâm linh": "Phúc Đức",
    "may mắn": "Phúc Đức",
    # Tổng quát / mệnh
    "số mệnh": "Mệnh",
    "vận mệnh": "Mệnh",
    "bản mệnh": "Mệnh",
    "cuộc đời": "Mệnh",
}

# Từ khóa cho Thần Số Học
KEYWORD_TO_CHI_SO = {
    "đường đời": "duong_doi",
    "số đường đời": "duong_doi",
    "sứ mệnh": "su_menh",
    "sứ mạng": "su_menh",
    "linh hồn": "linh_hon",
    "khao khát": "linh_hon",
    "nhân cách": "nhan_cach",
    "ấn tượng": "nhan_cach",
    "thần số": "all",   # Hỏi chung về thần số → trả cả 4 chỉ số
    "thần số học": "all",
}


@app.post("/dien-giai-cung-llm")
def dien_giai_cung_llm(data: DienGiaiCungInput):
    """
    Bản LLM của /dien-giai-cung:
    1. Tái sử dụng trực tiếp hàm dien_giai_cung(data) từ Phase 2 để lấy diễn giải thô.
    2. Đưa context thô vào Cohere để viết lại tự nhiên.
    3. Trả cả bản thô (raw) lẫn bản LLM (llm) để audit.
    """
    # Bước 1: Tái sử dụng hàm dien_giai_cung của Phase 2
    raw_result = dien_giai_cung(data)
    ten_cung = raw_result["cung"]
    dia_chi_cung = raw_result["dia_chi"]
    sao_entries = raw_result["sao_va_dien_giai"]

    # Bước 2: Dựng context từ kết quả thô
    context_lines = [f"Cung {ten_cung} (Địa Chi: {dia_chi_cung}) có các sao sau:"]
    for e in sao_entries:
        line = f"- {e['sao']}"
        if e.get("tu_hoa"):
            line += f" [{', '.join(e['tu_hoa'])}]"
        if e.get("dien_giai"):
            line += f": {e['dien_giai'][:600]}"
        elif e.get("warning"):
            line += f": [Thiếu dữ liệu: {e['warning']}]"
        context_lines.append(line)
    context_text = "\n".join(context_lines)

    user_msg = (
        f"[CONTEXT]\n{context_text}\n\n"
        f"Hãy diễn giải ý nghĩa của cung {ten_cung} trong lá số Tử Vi này "
        f"một cách tự nhiên, dễ hiểu, dựa trên các sao và diễn giải trong context."
    )

    # Bước 3: Gọi LLM
    llm_text = cohere_client.goi_cohere(
        system_prompt=SYSTEM_PROMPT_TU_VI,
        user_message=user_msg,
        api_key=COHERE_API_KEY,
        max_tokens=400,
    )

    return {
        "cung": ten_cung,
        "dia_chi": dia_chi_cung,
        "so_sao": len(sao_entries),
        "raw": raw_result,
        "llm": llm_text,
        "cohere_calls_phien_nay": cohere_client.get_call_count(),
    }


class HoiInput(BaseModel):
    cau_hoi: str
    # Kết quả lá số từ /lap-la-so (client gửi lại, stateless)
    muoi_hai_cung: Optional[Dict[str, str]] = None
    chinh_tinh: Optional[Dict[str, str]] = None
    tu_hoa: Optional[Dict[str, str]] = None
    than_so_hoc: Optional[Dict] = None  # 4 chỉ số: duong_doi, su_menh, linh_hon, nhan_cach


@app.post("/hoi")
def hoi_dap(data: HoiInput):
    """
    Hỏi đáp tự do:
    1. Detect từ khóa → xác định cung/chỉ số liên quan
    2. Retrieve diễn giải thô cho cung/chỉ số đó
    3. Gọi Cohere để trả lời tự nhiên dựa trên context
    """
    import unicodedata
    cau_hoi_lower = unicodedata.normalize('NFC', data.cau_hoi).lower()

    # ── Detect từ khóa Thần Số Học trước ──
    chi_so_match = None
    for kw, chi_so in KEYWORD_TO_CHI_SO.items():
        # Đảm bảo từ khóa cũng được chuẩn hóa NFC
        kw_nfc = unicodedata.normalize('NFC', kw)
        if kw_nfc in cau_hoi_lower:
            chi_so_match = chi_so
            break

    # ── Detect từ khóa Tử Vi ──
    cung_match = None
    for kw, cung in KEYWORD_TO_CUNG.items():
        kw_nfc = unicodedata.normalize('NFC', kw)
        if kw_nfc in cau_hoi_lower:
            cung_match = cung
            break

    context_parts = []

    # Xử lý Thần Số Học nếu có match từ khóa
    if chi_so_match and data.than_so_hoc:
        if chi_so_match == "all":
            # Hỏi chung về thần số → cung cấp tất cả 4 chỉ số
            for cs_key in ["duong_doi", "su_menh", "linh_hon", "nhan_cach"]:
                val = data.than_so_hoc.get(cs_key, {})
                gia_tri = val.get("gia_tri") if isinstance(val, dict) else val
                if gia_tri is not None:
                    dg = get_numerology_info(cs_key, gia_tri)
                    dg_str = format_numerology_text(dg)
                    if not dg_str and isinstance(val, dict) and val.get("dien_giai"):
                        dg_str = format_numerology_text(val.get("dien_giai"))
                    context_parts.append(f"{cs_key.upper()} = {gia_tri}: {dg_str[:250]}")
        else:
            val = data.than_so_hoc.get(chi_so_match, {})
            gia_tri = val.get("gia_tri") if isinstance(val, dict) else val
            if gia_tri is not None:
                dg = get_numerology_info(chi_so_match, gia_tri)
                dg_str = format_numerology_text(dg)
                if not dg_str and isinstance(val, dict) and val.get("dien_giai"):
                    dg_str = format_numerology_text(val.get("dien_giai"))
                context_parts.append(f"{chi_so_match.upper()} = {gia_tri}: {dg_str[:400]}")

    # Retrieve thông tin cung Tử Vi nếu có match
    if cung_match and data.muoi_hai_cung and data.chinh_tinh:
        dia_chi_cung = data.muoi_hai_cung.get(cung_match)
        if dia_chi_cung:
            sao_tai_cung = [ts for ts, dc in data.chinh_tinh.items() if dc == dia_chi_cung]
            dia_chi_to_cung = {v: k for k, v in data.muoi_hai_cung.items()}
            ten_cung_de_tra = dia_chi_to_cung.get(dia_chi_cung, cung_match)
            hoa_map = {}
            for loai_hoa, ten_sao_hoa in (data.tu_hoa or {}).items():
                hoa_map.setdefault(ten_sao_hoa, []).append(loai_hoa)

            context_parts.append(f"\nCung {cung_match} (Địa Chi: {dia_chi_cung}):")
            for ts in sao_tai_cung:
                dg = lookup_sao.get_dien_giai_sao(sao_data, ts, ten_cung_de_tra)
                line = f"  - {ts}"
                if hoa_map.get(ts):
                    line += f" [{', '.join(hoa_map[ts])}]"
                if isinstance(dg, str):
                    line += f": {dg[:400]}"
                else:
                    line += ": [Thiếu dữ liệu diễn giải]"
                context_parts.append(line)

    # Không match được gì
    if not context_parts:
        fallback_msg = (
            "Câu hỏi chưa đủ rõ để xác định cung/chỉ số cần tra. "
            "Bạn có thể hỏi cụ thể hơn, ví dụ: 'sự nghiệp của tôi thế nào?' hoặc "
            "'đường đời số mấy?' hoặc cung cấp kết quả lá số đầy đủ."
        )
        return {
            "cau_hoi": data.cau_hoi,
            "cung_detect": None,
            "chi_so_detect": None,
            "tra_loi": fallback_msg,
            "cohere_calls_phien_nay": cohere_client.get_call_count(),
        }

    context_text = "\n".join(context_parts)
    user_msg = (
        f"[CONTEXT]\n{context_text}\n\n"
        f"[CÂU HỎI] {data.cau_hoi}"
    )

    tra_loi = cohere_client.goi_cohere(
        system_prompt=SYSTEM_PROMPT_TU_VI,
        user_message=user_msg,
        api_key=COHERE_API_KEY,
        max_tokens=350,
    )

    return {
        "cau_hoi": data.cau_hoi,
        "cung_detect": cung_match,
        "chi_so_detect": chi_so_match,
        "context_dung": context_text[:500] + "..." if len(context_text) > 500 else context_text,
        "tra_loi": tra_loi,
        "cohere_calls_phien_nay": cohere_client.get_call_count(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Tử Vi Đẩu Số & Thần Số Học (RAG + LLM) 🌟

Dự án web app kết hợp lập lá số Tử Vi Đẩu Số (trường phái Trung Châu) và tính toán chỉ số Thần Số Học (hệ Pythagorean), tích hợp trợ lý AI (LLM) để diễn giải và hỏi đáp tự do.

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Tests](https://img.shields.io/badge/tests-73%2F73%20passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

## Mục lục
1. [Giới thiệu](#giới-thiệu)
2. [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
3. [Tính năng](#tính-năng)
4. [Cấu trúc thư mục](#cấu-trúc-thư-mục)
5. [Cài đặt & Chạy thử](#cài-đặt--chạy-thử)
6. [Ví dụ sử dụng](#ví-dụ-sử-dụng)
7. [Nguồn dữ liệu](#nguồn-dữ-liệu)
8. [Trạng thái phát triển](#trạng-thái-phát-triển)

## Giới thiệu
Dự án giải quyết bài toán xem Tử Vi và Thần Số Học cá nhân hoá. Thay vì chỉ hiển thị lá số khô khan hoặc yêu cầu người dùng tự tra cứu sách, ứng dụng tự động an sao chính xác 100% bằng thuật toán, sau đó dùng LLM (Cohere) để tổng hợp diễn giải bằng ngôn ngữ tự nhiên dựa trên cơ sở dữ liệu (RAG) đã được thẩm định.
- **Tử Vi Đẩu Số**: Tuân thủ an sao theo chuẩn Trung Châu / Tam Hợp phái (Vương Đình Chi).
- **Thần Số Học**: Áp dụng hệ Pythagorean chuẩn quốc tế.

## Kiến trúc hệ thống
```text
  [Frontend (HTML/JS)] 
           │
           ▼
  [Backend API (FastAPI)] ───────┐
           │                     │
           ▼                     ▼
 [Engine An Sao Tử Vi]   [Engine Thần Số Học]
  (Thuần tính toán)       (Thuần tính toán)
           │                     │
           └─────────┬───────────┘
                     ▼
          [Retrieval (RAG)] 
      (Lookup dict / Exact-match)
                     │
                     ▼
               [LLM (Cohere)]
     (Tổng hợp câu trả lời tự nhiên)
```

## Tính năng
- 🔮 **Lập lá số 12 cung Tử Vi**: An đúng 14 chính tinh và các phụ tinh theo ngày sinh dương lịch (tự động quy đổi âm lịch).
- 🔢 **Tính toán 4 chỉ số Thần Số Học**: Đường đời, Sứ mệnh, Linh hồn, Nhân cách.
- 📜 **Tra cứu diễn giải chi tiết**: Click vào từng cung trên lá số để xem ý nghĩa các sao thông qua Modal.
- 💬 **Hỏi đáp tự do (Chat)**: Trợ lý AI sẵn sàng giải đáp thắc mắc về lá số và chỉ số dựa trên dữ liệu RAG (không ảo giác).

## Cấu trúc thư mục
```text
.
├── data/               # Dữ liệu nguồn tham khảo (sách txt, bảng tra Thần Số Học)
├── sao_json/           # CSDL 101 file JSON ý nghĩa các sao Tử Vi đã thẩm định
├── frontend/           # Giao diện web tĩnh (HTML/CSS/JS)
├── tests/              # Bộ unit tests và integration tests
├── an_menh_cuc.py      # Logic tính toán Cục số và cung Mệnh
├── an_phu_tinh.py      # Logic an các phụ tinh
├── engine_tu_vi.py     # Engine chính an sao 12 cung
├── engine_than_so_hoc.py # Engine tính toán Thần Số Học
├── tu_hoa.py           # Logic tính Tứ Hóa
├── lookup_sao.py       # Logic trích xuất diễn giải sao
├── cohere_client.py    # Client giao tiếp với Cohere LLM
├── main.py             # FastAPI backend (entry point)
└── requirements.txt    # Danh sách thư viện Python
```

## Cài đặt & Chạy thử
**Yêu cầu hệ thống:** Python 3.10 hoặc mới hơn.

**1. Clone dự án**
```bash
git clone https://github.com/TuLeTanh/Numberology.git
cd Numberology
```

**2. Tạo virtual environment (khuyến nghị)**
```bash
python -m venv .venv
# Trên Windows:
.venv\Scripts\activate
# Trên macOS/Linux:
source .venv/bin/activate
```

**3. Cài đặt thư viện**
```bash
pip install -r requirements.txt
```

**4. Khai báo API Key**
- Copy file `.env.example` thành `.env`
- Mở `.env` và điền Cohere API Key của bạn vào:
```env
COHERE_API_KEY=your_cohere_key_here
```

**5. Chạy Backend Server**
```bash
uvicorn main:app --reload --reload-exclude "test_*.py" --reload-exclude "_*.py" --reload-exclude "check_*.py" --reload-exclude "get_*.py"
```
*(Hoặc chạy nhanh bằng file script `start.bat` trên Windows).*
Server sẽ chạy tại `http://localhost:8000`.

**6. Mở Frontend**
- Bạn có thể mở trực tiếp file `frontend/index.html` bằng trình duyệt web.
- Hoặc dùng Live Server (VSCode) để phục vụ thư mục `frontend/`.

**7. Chạy Unit Tests**
```bash
pytest
```

## Ví dụ sử dụng
Thử nhập thông tin sau vào form trên Frontend:
- **Họ và tên**: Nguyễn Văn A
- **Ngày sinh**: 21/05/2015
- **Giờ sinh**: 08:00
- **Giới tính**: Nam
Hệ thống sẽ tính ra lá số Tử Vi (Cục: Hỏa Lục Cục) và Thần Số Học tương ứng.

## Nguồn dữ liệu
- **Tử Vi Đẩu Số Tân Biên** (Vân Đằng Thái Thứ Lang)
- **Tự Điển Tử Vi Đẩu Số và Thần Số Học** (Lê Quang Tiềm) - Nguồn tham khảo ý nghĩa 101 sao.
- **Dữ liệu Thần Số Học**: Tổng hợp chuẩn hoá từ các nguồn Pythagorean quốc tế (Dr. David A. Phillips, Hans Decoz).
> **Lưu ý**: Các file `.txt` nguyên bản (như `tan_bien.txt`, `toan_thu_unicode.txt`) là tư liệu tham khảo học thuật nội bộ, vui lòng không phân phối lại để đảm bảo bản quyền.

## Trạng thái phát triển
- ✅ **Phase 1-3**: Xây dựng 2 Engine tính toán, RAG lookup.
- ✅ **Phase 4**: Hoàn thiện Frontend MVP, Modal click-to-detail, API (Đã hoàn tất 5/5 step).
- ⏳ **Phase 5**: (Roadmap) Tối ưu LLM, thêm luận giải Đại Vận/Lưu Niên, caching, rate limiting.

---
*Phát triển bởi [TuLeTanh](https://github.com/TuLeTanh).*

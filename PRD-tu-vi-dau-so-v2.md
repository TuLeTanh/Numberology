# PRD & Lộ Trình Kỹ Thuật — Ứng Dụng Tử Vi Đẩu Số + Thần Số Học (v2)

> Bản cập nhật dựa trên phiên phỏng vấn yêu cầu ngày 04/09/2026. Thay thế bản PRD v1 (giữ v1 làm tài liệu tham khảo lịch sử quyết định). Coi đây là **living doc** — cập nhật khi có quyết định kỹ thuật mới.

---

## 0. Tóm tắt quyết định (đọc nhanh)

| Hạng mục | Quyết định |
|---|---|
| Phạm vi MVP | **Tử Vi + Thần Số Học ngang nhau ngay từ đầu** (không phải Tử Vi trước) |
| Người làm | 1 người, AI agent code chính, chủ dự án review |
| Tốc độ | Side project, không deadline cứng |
| Nền tảng | Web app, responsive (không cần app native) |
| Quy mô user | Vài chục người quen dùng thử |
| Kinh doanh | Miễn phí hoàn toàn, không có ý định thu phí |
| Backend stack | Python / FastAPI (đã chốt theo code thực tế đang triển khai như engine_tu_vi.py, main.py, test_api.py) |
| Giao diện lá số | Bảng 12 cung truyền thống (giữ đúng hình thức lá số giấy) |
| Hỏi đáp tự do | **Có ngay trong MVP**, không đợi phase sau |
| LLM provider | Cohere (trial key, free tier ~1.000 call/tháng) làm lựa chọn chính |
| Tài khoản / lưu lịch sử | **Không** — mỗi lần nhập là tính lại, không lưu, không login |
| Âm-dương lịch | Chưa có sẵn — cần agent khảo sát hướng làm, chủ dự án có thể tự tạo bảng tra sau |
| Đối chiếu công thức an sao | Cần tìm thêm ít nhất 1 nguồn Trung Châu phái khác trước khi code hoá |
| Audit Thần Số Học | Bắt buộc trong Phase 0, cùng mức độ với 101 file Tử Vi |

---

## 1. Tổng quan sản phẩm

### 1.1 Vấn đề cần giải quyết
Người dùng (bạn bè, người thân của chủ dự án) muốn xem lá số Tử Vi Đẩu Số và/hoặc chỉ số Thần Số Học của mình, được luận giải có cấu trúc, cá nhân hoá theo đúng ngày sinh — thay vì tự tra sách hoặc dùng app chỉ hiển thị lá số không giải thích.

### 1.2 Tầm nhìn sản phẩm
Một web app **miễn phí, quy mô nhỏ** (dùng thử nội bộ, không thương mại hoá), gồm 2 module ngang hàng ngay từ MVP:
1. **Tử Vi Đẩu Số** (trường phái Trung Châu) — an sao chính xác 100% (thuần tính toán, không LLM) + diễn giải tự nhiên (RAG + LLM) + hỏi đáp tự do.
2. **Thần Số Học** — tính các chỉ số từ ngày sinh (Đường đời, Sứ mệnh...) + diễn giải, đối chiếu song song với Tử Vi khi có thể.

### 1.3 Nguyên tắc thiết kế xuyên suốt
- **Tách bạch tuyệt đối 2 lớp**: *tính toán* (an sao, tính chỉ số Thần Số Học — phải đúng 100%, không cho LLM tự suy diễn) và *diễn giải* (ngôn ngữ tự nhiên — LLM tổng hợp nhưng chỉ dựa trên dữ liệu retrieve được).
- **Không tin báo cáo, chỉ tin bằng chứng** — áp dụng cho cả QA dữ liệu lẫn test backend/RAG: mọi câu trả lời cần truy được nguồn (sao nào, cung nào, chỉ số nào).
- **Schema là hợp đồng, không đổi giữa chừng** — có validation script chạy trước mỗi lần dùng dữ liệu mới.
- **Không lưu dữ liệu người dùng** — vì không có tài khoản, mỗi phiên là stateless; cân nhắc điều này khi thiết kế API (không cần bảng `users`, không cần cache theo `user_id`, chỉ cần cache theo **kết quả tính toán** nếu muốn tiết kiệm token LLM).
- **Tiết kiệm LLM call là ưu tiên kỹ thuật thật sự** (không chỉ lý thuyết) — vì dùng Cohere trial (~1.000 call/tháng), thiết kế retrieval phải là **exact-match/lookup trước**, LLM chỉ tổng hợp câu trả lời cuối từ context đã lookup sẵn, không dùng LLM để tìm kiếm nếu không cần thiết.

---

## 2. Người dùng & phạm vi

- **Đối tượng**: bạn bè, người thân của chủ dự án (ước tính vài chục người).
- **Không có**: hệ thống tài khoản, đăng nhập, lưu lịch sử lá số. Mỗi lượt truy cập nhập thông tin sinh → xem kết quả → không lưu lại phía server (có thể lưu tạm ở client/localStorage nếu muốn tiện cho người dùng trong phiên, nhưng không bắt buộc và không phải yêu cầu MVP).
- **Không có kế hoạch thu phí** — không cần thiết kế phân quyền free/premium.
- **Hệ quả kỹ thuật**: bỏ hẳn các mục trong PRD v1 liên quan tới DB lưu user, auth, cache theo user_id. Giảm đáng kể độ phức tạp backend so với bản v1.

---

## 3. Tài sản dữ liệu hiện có

| Tài sản | Nội dung | Trạng thái |
|---|---|---|
| Bảng công thức an sao (gõ tay) | Quy tắc xác định vị trí 14 chính tinh + phụ tinh | [x] Resolved: Đối chiếu bang_tu_vi.json với data/tan_bien.txt dòng 393-444 (Tử Vi Đẩu Số Tân Biên, Thái Thứ Lang) + công thức toán Định Cục, phát hiện và sửa 2 lỗi OCR gốc (ngày 18 bị đọc nhầm thành 8 ở Kim Tứ Cục/Thân; ngày 21 bị lặp sai vào Mùi thay vì chỉ thuộc Thìn). |
| `sao_json/*.json` (101 file) | Diễn giải ý nghĩa từng sao theo từng cung | **Sạch, đã nghiệm thu** (không đổi) |
| `than_so_hoc_bang_tra.json` | Bảng tra Thần Số Học | Đã có, **bắt buộc audit đầy đủ trong Phase 0** — cùng quy trình grep-raw-text đã dùng cho 101 sao (yêu cầu mới, nâng mức ưu tiên vì Thần Số Học nay ngang hàng Tử Vi trong MVP) |
| `bang_tu_vi.json` | Bảng định Cục và vị trí sao Tử Vi theo ngày sinh | [x] Resolved: Là input bắt buộc cho thuật toán An Sao (Bước 1), không trùng lặp với `sao_json/`. Đã quét lại định dạng chuẩn UTF-8. |

### 3.1 Schema chuẩn hoá cho 1 file sao (giữ nguyên từ v1, đã kiểm chứng)
```json
{
  "sao": "Tên sao (chuẩn hóa, viết hoa đầu từ)",
  "loai": "Cát tinh / Hung tinh / Tài tinh / Phúc tinh / Quí tinh / Gian tinh / Thọ tinh / Hộ tinh...",
  "cong_thuc_an_sao": "Thường rỗng ở phần Tự Điển — công thức thật ở chương đầu sách",
  "y_nghia_theo_cung": [
    { "cung": "Mệnh", "dien_giai": "..." }
  ],
  "cach_cuc": "Câu luận về cách cục lớn liên quan tới sao này",
  "ghi_chu_thieu_du_lieu": "",
  "ten_khac": "(tùy chọn)"
}
```
**Ràng buộc bắt buộc**: `y_nghia_theo_cung` luôn là **list**. Có script validate chạy mỗi khi thêm/sửa file.

### 3.2 Schema đề xuất cho dữ liệu Thần Số Học (cần chốt trong Phase 0, không được sẵn có như Tử Vi)
Vì `than_so_hoc_bang_tra.json` chưa qua audit và schema thật sự chưa rõ, Phase 0 cần:
- Kiểm tra cấu trúc file hiện tại có nhất quán không (mỗi chỉ số — ví dụ Số Đường Đời, Số Sứ Mệnh... — có đúng field diễn giải theo từng giá trị số (1–9, 11, 22...) không).
- Chuẩn hoá về 1 schema thống nhất tương tự tinh thần schema Tử Vi (`chi_so`, `gia_tri`, `dien_giai`, `nguon_tinh_toan`...) — agent đề xuất cụ thể sau khi đọc raw data.
- Áp dụng đúng quy trình đã dùng cho Tử Vi: grep raw text, đối chiếu, không suy đoán, checklist đầy đủ trước khi tin.

### 3.3 Việc cần làm trong Phase 0 (cập nhật, mở rộng so với v1)
- [x] **Tìm và đối chiếu ≥1 nguồn Trung Châu phái thứ 2** cho bảng công thức an sao trước khi code hoá thành engine (khác v1: v1 để "nếu có thể", nay là yêu cầu bắt buộc theo quyết định mới của chủ dự án). Resolved: Đối chiếu bang_tu_vi.json với data/tan_bien.txt dòng 393-444 (Tử Vi Đẩu Số Tân Biên, Thái Thứ Lang) + công thức toán Định Cục, phát hiện và sửa 2 lỗi OCR gốc (ngày 18 bị đọc nhầm thành 8 ở Kim Tứ Cục/Thân; ngày 21 bị lặp sai vào Mùi thay vì chỉ thuộc Thìn).
- [x] **Xác minh và công nhận `than_so_hoc_bang_tra_v2.json` làm bảng tra Thần Số Học chính thức** (Cập nhật 09/09/2026): Thay thế yêu cầu cũ 'audit than_so_hoc_bang_tra.json theo grep-raw-text' (do file v1 trích từ sách Lê Quang Tiềm bị lỗi font, thiếu Master Number 11/22/33 và gộp sai 4 chỉ số). Đã đối chiếu chéo 10 mục đại diện (bao gồm các Master Number 11, 22, 33) của v2.json qua 2 vòng Web Search + HTTP fetch thật (vòng 1 phát hiện lỗi trích dẫn diễn giải bị trình bày sai thành nguyên văn ở 8/10 mục; vòng 2 đã sửa đúng bằng trích dẫn copy-paste thật 100% từ trang nguồn — có URL, HTTP status, đoạn trích xác nhận). Nguồn đối chiếu: Dr. David A. Phillips, Hans Decoz/World Numerology, centreofexcellence.com, astrologynumerology.org, jobcannon.io và các nguồn Pythagorean quốc tế khác — nội dung khớp đúng tinh thần/ngữ nghĩa, không khớp tuyệt đối từng chữ (khác bản chất với audit grep-raw-text 1 sách gốc duy nhất như Tử Vi, vì Numerology Pythagorean không có 1 văn bản gốc độc quyền). Người review đã tự tay fetch độc lập 3/10 URL để xác nhận trước khi duyệt. (Lịch sử: v1 từng yêu cầu audit grep-raw-text sách Lê Quang Tiềm nhưng kết quả thực tế chỉ đạt 78.95% do hạn chế của sách OCR gốc).
- [x] Xác định vai trò `bang_tu_vi.json`: Đã làm rõ đây là bảng tra tính toán an sao Tử Vi, giữ lại nguyên vẹn cho Phase 1.
- [ ] Khảo sát hướng xử lý chuyển đổi dương lịch → âm lịch cho stack Node.js/TypeScript (thư viện có sẵn hay cần bảng tra tự dựng — xem mục 7.1).

---

## 4. Kiến trúc tổng thể

```
┌──────────────┐      ┌───────────────────────┐      ┌─────────────────────┐
│   Frontend    │─────▶│   Backend API (Python/FastAPI) │─────▶│  An Sao Engine        │
│  (web, nhập   │      │   (orchestration,        │      │  (thuần tính toán)    │
│  ngày sinh,   │◀─────│    stateless — không có  │◀─────│                       │
│  hỏi đáp)     │      │    DB user/session)       │      └─────────────────────┘
└──────────────┘      └────────────┬─────────────┘
                                     │                      ┌─────────────────────┐
                                     ├─────────────────────▶│ Thần Số Học Engine    │
                                     │                      │ (thuần tính toán)     │
                                     │                      └─────────────────────┘
                                     ▼
                          ┌────────────────────┐
                          │   Retrieval          │
                          │  (lookup dict theo    │
                          │  tên sao/chỉ số +      │
                          │  cung, exact-match     │
                          │  trước, vector search  │
                          │  chỉ khi cần cho hỏi   │
                          │  đáp tự do)            │
                          └───────────┬────────────┘
                                     ▼
                          ┌────────────────────┐
                          │   LLM (Cohere)        │
                          │   tổng hợp câu trả lời │
                          │   từ context retrieve  │
                          │   được, không bịa       │
                          └────────────────────┘
```

### 4.1 Nguyên tắc luồng dữ liệu
1. User nhập ngày/giờ/tháng/năm sinh (+ giới tính nếu cần cho Tử Vi) → Backend gọi song song **An Sao Engine** và **Thần Số Học Engine**.
2. Cả 2 engine trả kết quả **deterministic**, không qua LLM.
3. Backend không lưu kết quả (stateless) — chỉ giữ trong response trả về frontend / hoặc state tạm trong phiên làm việc của client.
4. Khi user hỏi (theo cung/chỉ số cụ thể hoặc hỏi tự do) → **Retrieval** lấy đúng đoạn diễn giải liên quan (từ 101 file sao và dữ liệu Thần Số Học đã audit) → LLM (Cohere) tổng hợp câu trả lời tự nhiên, ràng buộc chỉ dùng context được cấp.

### 4.2 Quyết định kỹ thuật đã chốt (cập nhật so với v1)
| Vấn đề | Quyết định |
|---|---|
| Backend stack | **Python (FastAPI hoặc Flask — chờ chốt cụ thể framework nào)** (Cập nhật 07/09/2026: Chốt lại dùng Python để đồng bộ với toàn bộ code extract/engine đã viết) |
| Retrieval strategy | Exact-match/lookup theo (tên sao hoặc chỉ số, cung) làm mặc định; vector search chỉ bật khi câu hỏi tự do không map được rõ ràng vào (sao, cung) hoặc (chỉ số) cụ thể |
| Vector DB (nếu cần) | Local/nhẹ (ví dụ Chroma local) — quy mô vài chục user, không cần dịch vụ trả phí |
| LLM cho diễn giải + hỏi đáp | **Cohere** (trial key, free ~1.000 call/tháng, rate limit ~20 call/phút cho Chat) — vì thiết kế retrieval là lookup trước nên mỗi lượt gọi LLM chỉ cần context nhỏ, phù hợp giới hạn trial. Ghi chú: trial key về nguyên tắc chỉ dành cho testing/dev, không phải production — cần theo dõi nếu traffic thật tăng, có phương án nâng cấp key trả phí ($2.5/$10 mỗi 1M token input/output cho Command R+) nếu vượt giới hạn |
| Lưu trữ | **Không có DB user/session** — stateless hoàn toàn, khác biệt lớn nhất so với v1 |
| API backend | REST, đơn giản, không cần auth |
| Frontend | Web responsive, không cần app native |

---

## 5. Đặc tả các module

### 5.1 Module: An Sao Engine
Giữ nguyên tinh thần v1: input (ngày/giờ/tháng/năm sinh dương lịch, giới tính) → xử lý (đổi âm lịch, xác định Cục số, an 12 cung, an chính tinh/phụ tinh) → output JSON 12 cung.

**Thay đổi so với v1**:
- Cài đặt bằng **Python** — cần khảo sát thư viện âm-dương lịch tương ứng cho hệ sinh thái Python (xem 7.1), hoặc dựng bảng tra riêng nếu không có thư viện đủ tin cậy.
- Trước khi code, **bắt buộc** đối chiếu công thức với ≥1 nguồn Trung Châu phái thứ 2 (yêu cầu mới).
- Vẫn cần bộ test case với lá số mẫu đã biết đáp án (5–10 lá số tối thiểu), chạy tự động mỗi khi sửa engine.

### 5.2 Module: Thần Số Học Engine (nâng cấp từ "mở rộng" ở v1 thành module MVP ngang hàng)
- Cài đặt bằng **Python**, kế thừa trực tiếp từ `engine_than_so_hoc.py` đã hoàn thiện.
- Input: ngày/tháng/năm sinh (dương lịch, không cần đổi âm lịch) + **họ và tên đầy đủ lúc khai sinh** (bắt buộc, vì 3/4 chỉ số cốt lõi là Sứ Mệnh, Linh Hồn, Nhân Cách đều tính từ tên).
- Xử lý: tính các chỉ số chuẩn Thần Số Học (Đường đời, Sứ mệnh, Linh hồn... — cần chốt danh sách chỉ số cụ thể áp dụng, dựa theo nội dung thật của `than_so_hoc_bang_tra.json` sau khi audit).
- Output: JSON các chỉ số + giá trị.
- **Yêu cầu chất lượng**: tương tự An Sao Engine — tính toán thuần, không LLM, cần test case với người đã biết đáp án trước (có thể dùng chính ngày sinh của chủ dự án/người quen).

### 5.3 Module: RAG Diễn Giải (gộp chung luồng cho cả Tử Vi và Thần Số Học)
- Nhận (sao, cung) hoặc (chỉ số, giá trị) hoặc câu hỏi tự do → trả lời có căn cứ từ dữ liệu đã audit.
- Với câu hỏi rõ theo cung/chỉ số → lookup trực tiếp, LLM chỉ viết lại cho mượt.
- Với câu hỏi tự do (**bắt buộc có trong MVP** — khác v1 để phase sau) → cần bước map câu hỏi → (các cung/chỉ số liên quan) trước khi retrieve, có thể dùng LLM nhẹ cho bước map này hoặc rule-based đơn giản trước (ưu tiên rule-based nếu đủ, để tiết kiệm call LLM).
- **Ràng buộc system prompt Cohere**: chỉ dùng context được cấp, không thêm kiến thức ngoài; khi thiếu dữ liệu, trả lời trung thực; trích được nguồn (tên sao/chỉ số, cung) để audit.

### 5.4 Module: Backend API (Python)
Endpoint tối thiểu (đã bỏ mọi thứ liên quan lưu trữ/tài khoản so với v1):
- `POST /lasso` — nhận thông tin sinh (**bao gồm cả họ tên khai sinh** để tính Thần Số Học, và ngày/giờ sinh để an sao), trả kết quả an sao + chỉ số Thần Số Học trong 1 lần gọi (không lưu).
- `GET /lasso/cung/{ten_cung}` hoặc endpoint tương đương — trả diễn giải các sao tại 1 cung, dựa trên kết quả vừa tính (truyền lại từ client, không truy DB).
- `POST /hoi` — nhận câu hỏi tự do (kèm kết quả lá số/chỉ số từ client) → RAG + Cohere → trả lời.

**Phi chức năng**:
- Rate limit `/hoi` để tránh vượt giới hạn 1.000 call/tháng của Cohere trial.
- Logging input/output LLM để debug chất lượng câu trả lời (không cần gắn với user_id vì không có tài khoản).

### 5.5 Module: Frontend (Web)
MVP: form nhập **họ tên khai sinh** (chỉ dùng cho Thần Số Học) và ngày/giờ sinh → hiển thị đồng thời (a) bảng 12 cung truyền thống cho Tử Vi và (b) các chỉ số Thần Số Học → bấm vào từng cung/chỉ số xem diễn giải → 1 ô hỏi đáp tự do dùng chung cho cả 2 module. Không có màn hình đăng nhập/tài khoản.

---

## 6. Lộ trình triển khai (cập nhật)

### Phase 0 — Thẩm định dữ liệu nền (mở rộng đáng kể so với v1 vì Thần Số Học nay ngang hàng)
- Validate schema 101 file Tử Vi, quét rác OCR sót.
- Tìm nguồn Trung Châu phái thứ 2, đối chiếu bảng công thức an sao.
- **Audit đầy đủ `than_so_hoc_bang_tra.json`** theo đúng quy trình grep-raw-text đã dùng cho Tử Vi — coi đây là hạng mục ngang mức ưu tiên với audit Tử Vi, không phải "làm sau".
- [x] Làm rõ vai trò `bang_tu_vi.json`.
- Khảo sát thư viện/giải pháp âm-dương lịch cho Python.
- **Đầu ra**: bộ dữ liệu "khoá" (frozen) cho cả 2 module, có version. (ĐÃ HOÀN TẤT Phase 0 cho cả Tử Vi và Thần Số Học)

### Phase 1 — Hai Engine tính toán song song
- An Sao Engine (Python) — theo công thức đã đối chiếu nguồn thứ 2.
- Thần Số Học Engine (Python) — theo schema đã chốt ở Phase 0.
- Test case tự động cho cả 2 (mỗi engine ≥5 case có đáp án trước), phải pass 100%.
- **Đầu ra**: 2 hàm/service tính toán độc lập, deterministic.

### Phase 2 — Lớp truy xuất dữ liệu diễn giải (chưa cần LLM)
- Load dữ liệu Tử Vi + Thần Số Học vào dạng lookup nhanh (in-memory, vì quy mô nhỏ không cần DB phức tạp).
- API lookup trả text thô cho từng cung/chỉ số.
- **Đầu ra**: xem được kết quả tính toán + diễn giải thô, demo được mà chưa cần tích hợp Cohere.

### Phase 3 — Tích hợp Cohere cho diễn giải tự nhiên + hỏi đáp tự do (đưa lên sớm hơn v1, vì MVP cần có ngay)
- System prompt ràng buộc chặt (chỉ dùng context, không bịa).
- Test nhiều dạng câu hỏi, review thủ công (không có ground-truth tự động cho phần tự do).
- Theo dõi sát số lượng call để không vượt giới hạn trial 1.000 call/tháng.
- **Đầu ra**: hỏi đáp tự nhiên hoạt động cho cả 2 module.

### Phase 4 — Backend + Frontend MVP hoàn chỉnh (đơn giản hơn v1: bỏ hẳn phần DB user/auth)
- [x] Ráp API hoàn chỉnh (stateless).
- [x] Frontend: bảng 12 cung + hiển thị chỉ số Thần Số Học + ô hỏi đáp.
- [x] **Step 5: Modal click-to-detail (/dien-giai-cung)**: Đã hoàn tất, xác minh qua Playwright (2 cung test: Mệnh, Quan Lộc — raw HTML khớp raw JSON), pytest 73/73 pass không regression.
- **Đầu ra**: sản phẩm demo end-to-end, gửi link cho bạn bè/người thân dùng thử. (Ghi nhận chính thức: Phase 4 đã hoàn thành đầy đủ 5/5 step).

### Phase 5 — Mở rộng (nếu có nhu cầu sau khi dùng thử)
- Cân nhắc thêm (không phải yêu cầu hiện tại): lưu lịch sử nếu người dùng thật sự cần, xem theo đại vận/lưu niên, so lá số (hợp hôn nhân), nâng cấp Cohere key nếu vượt free tier.

---

## 7. Yêu cầu kỹ thuật phi chức năng

- **Độ chính xác an sao & chỉ số Thần Số Học**: bắt buộc 100%, có test tự động.
- **Chi phí LLM**: theo dõi sát vì dùng Cohere trial (giới hạn ~1.000 call/tháng, ~20 call/phút cho Chat) — thiết kế retrieval lookup-first để giữ context nhỏ và giảm số call cần thiết; cân nhắc cache câu trả lời cho tổ hợp (sao, cung) hoặc (chỉ số, giá trị) phổ biến ở tầng ứng dụng (không phải theo user, vì không lưu theo user) để tránh gọi lại Cohere cho cùng 1 nội dung tĩnh.
- **Không lưu dữ liệu cá nhân**: vì không có tài khoản/DB user, rủi ro bảo mật dữ liệu ngày sinh giảm đáng kể so với v1 — không cần chính sách lưu trữ/ẩn danh phức tạp ở giai đoạn này.
- **Khả năng audit**: mọi câu trả lời cần truy ngược được nguồn dữ liệu gốc.
- **Ngôn ngữ**: tiếng Việt có dấu xuyên suốt — đảm bảo xử lý Unicode nhất quán (NFC/NFD) trong Python.

### 7.1 Việc cần khảo sát: chuyển đổi âm-dương lịch cho Python
- Chưa có phương án cụ thể tại thời điểm viết PRD này.
- Hướng xử lý: agent khảo sát các thư viện Python hiện có cho chuyển đổi âm-dương lịch Việt Nam (ví dụ `lunardate`, `lunarcalendar`, hoặc bảng tra tự dựng nếu cần). Lưu ý: Trong dự án hiện đang có thư mục `khao-sat-am-lich/` chứa các file `.js` (khảo sát cũ theo hướng Node.js), ta có thể kiểm tra xem logic/bảng tra trong đó có thể dùng lại cho Python được không.

---

## 8. Rủi ro & câu hỏi mở còn lại

| Rủi ro / câu hỏi | Ảnh hưởng | Hướng xử lý |
|---|---|---|
| Chuyển đổi âm-dương lịch chưa có giải pháp cụ thể | Sai toàn bộ lá số nếu làm ẩu | **[x] Resolved**: Đã chốt dùng thư viện `lunar-vn==1.4.0` (chuẩn lịch VN). |
| Bảng công thức an sao chưa đối chiếu nguồn thứ 2 | Sai lá số ở trường hợp hiếm | [x] Resolved: Đối chiếu bang_tu_vi.json với data/tan_bien.txt dòng 393-444 (Tử Vi Đẩu Số Tân Biên, Thái Thứ Lang) + công thức toán Định Cục, phát hiện và sửa 2 lỗi OCR gốc (ngày 18 bị đọc nhầm thành 8 ở Kim Tứ Cục/Thân; ngày 21 bị lặp sai vào Mùi thay vì chỉ thuộc Thìn). |
| Dữ liệu Thần Số Học chưa audit | Lỗi tương tự đã gặp ở Tử Vi (OCR, thiếu sót), nhưng nay ảnh hưởng trực tiếp tới 1 nửa MVP (không còn là "phụ") | **[x] Resolved (09/09/2026)**: Chốt sử dụng `data/than_so_hoc_bang_tra_v2.json` (biên soạn chuẩn hệ Pythagorean gồm 48 nodes độc lập). Đã xác minh qua 2 vòng web search + HTTP fetch thật, đối chiếu tinh thần/ngữ nghĩa với nguồn quốc tế uy tín (Dr. David A. Phillips, Hans Decoz/World Numerology, và các nguồn đã fetch kiểm chứng). Không phải grep-raw-text khớp từng chữ như Tử Vi do bản chất dữ liệu khác nhau (không có 1 sách gốc độc quyền). |
| Vai trò `bang_tu_vi.json` chưa rõ | Có thể trùng lặp/xung đột dữ liệu | [x] Resolved: File chứa bảng tra Cục số và vị trí Tử Vi, không trùng lặp, cần giữ nguyên cho thuật toán An Sao. |
| Giới hạn Cohere trial (1.000 call/tháng) | Có thể hết quota nếu bạn bè dùng thử đồng loạt hoặc test nhiều | Thiết kế lookup-first để giảm call; theo dõi usage; có phương án nâng cấp key trả phí nếu cần |
| Không lưu lịch sử — người dùng phải nhập lại mỗi lần | Trải nghiệm kém hơn nếu dùng lại nhiều lần | Chấp nhận theo đúng yêu cầu hiện tại; có thể cân nhắc lưu tạm ở localStorage phía client (không bắt buộc) |
| Stack Backend phân mảnh | Khó maintain nếu dùng Node/TS trong khi code xử lý là Python | [x] Resolved: chốt lại stack Python thay Node/TS, đã đối chiếu với lịch sử code thực tế toàn dự án. |

---

## 9. Định nghĩa "Hoàn thành" cho MVP

Sản phẩm MVP coi là đạt khi:
1. Nhập ngày/giờ sinh trên web → ra đúng lá số 12 cung **và** đúng các chỉ số Thần Số Học (verify bằng test case tự động cho cả 2 engine).
2. Xem được diễn giải cho từng cung/chỉ số, văn phong tự nhiên, không sai lệch so với dữ liệu gốc.
3. Hỏi đáp tự do hoạt động cho cả 2 module, trả lời đúng trọng tâm, có thể audit nguồn.
4. Không còn lỗi dữ liệu đã biết (OCR rác, schema lệch) trong toàn bộ pipeline — dữ liệu Tử Vi đã đạt 390/564 cặp (0 sao thiếu toàn bộ), dữ liệu Thần Số Học v2.json đã được xác minh đối chiếu tinh thần/ngữ nghĩa qua nguồn Pythagorean quốc tế thật (web search + fetch, không phải grep-raw-text 1 sách gốc như Tử Vi).
5. Chạy ổn định trong giới hạn free tier của Cohere với quy mô vài chục người dùng thử.
6. Không có bug bảo mật/rò rỉ dữ liệu cá nhân dù không lưu trữ (vì dữ liệu vẫn đi qua network — cần HTTPS, không log ngày sinh ra file log thô nếu tránh được).

---

## Nợ kỹ thuật đã hoãn (Deferred Technical Debt)
- [ ] **Bảo mật & Logging** (Ghi nhận 10/09/2026, hoãn xử lý): Hiện tại API chạy HTTP thuần (chưa HTTPS), CORS đang mở (allow_origins=*), và thông tin nhạy cảm (ngày/giờ sinh người dùng) đang bị log ra console chưa qua ẩn danh/lọc. Rate limit cho endpoint /hoi (gọi Cohere) cũng chưa có, rủi ro hết quota nếu bị spam. Quyết định: hoãn xử lý để ưu tiên hoàn thành Phase 4 Step 5 (modal click-to-detail) trước. Cần xử lý trước khi mở rộng cho nhiều người dùng thật.

## Ghi chú quy trình (Process Notes)
- **Lỗi quy trình 'step leak' (ghi nhận 10/09/2026)**: Code của Step 5 (Phase 4: modal click-to-detail /dien-giai-cung) thực chất đã được viết lồng vào Step 2 (backend, commit 89143e51, 08/09/2026) và Step 3/4 (frontend, commit 260eb1bf, 09/09/2026) mà không được báo cáo tách riêng theo đúng từng step. Hậu quả: PRD và transcript audit ghi nhận sai hiện trạng dự án trong một khoảng thời gian (tưởng Step 5 'chưa làm' trong khi thực tế đã hoàn tất). Không ảnh hưởng chất lượng code (đã xác minh qua Playwright + pytest), nhưng là bài học cho các phase sau: mỗi step cần báo cáo đúng lúc, đúng phạm vi, không gộp việc của step sau vào step trước mà không khai báo — kỷ luật ngang với nguyên tắc 'không tin báo cáo, chỉ tin bằng chứng' vốn áp dụng cho nội dung, nay áp dụng thêm cho cả tiến độ.

---

*Tài liệu này thay thế PRD v1 cho các quyết định đã chốt lại ở trên; các phần không nhắc tới ở đây (ví dụ chi tiết schema 101 file sao) vẫn giữ nguyên như v1. Cập nhật tiếp khi có quyết định kỹ thuật mới (ví dụ chọn xong thư viện âm lịch, kết quả audit Thần Số Học).*

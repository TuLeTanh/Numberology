# PRD & Lộ Trình Kỹ Thuật — Ứng Dụng Tử Vi Đẩu Số (kèm Thần Số Học)

> Tài liệu tổng hợp dựa trên toàn bộ tiến độ đã có: bộ công thức an sao (gõ tay), 101 file diễn giải ý nghĩa sao (đã qua QA nhiều vòng), bảng tra Thần Số Học. Mục tiêu: định hình kiến trúc, phạm vi, và lộ trình để đi từ "có dữ liệu sạch" đến "sản phẩm chạy được".

---

## 1. Tổng quan sản phẩm

### 1.1 Vấn đề cần giải quyết
Người dùng muốn có lá số Tử Vi (và/hoặc Thần Số Học) của mình được luận giải một cách có cấu trúc, cá nhân hóa theo đúng dữ liệu ngày sinh — thay vì phải tự tra cứu sách hoặc dùng app lá số thuần hiển thị mà không giải thích.

### 1.2 Tầm nhìn sản phẩm
Một trợ lý luận giải Tử Vi Đẩu Số (trường phái Trung Châu) có khả năng:
1. **An sao chính xác 100%** dựa trên ngày/giờ/tháng/năm sinh — phần này là tính toán thuần túy, không dùng LLM.
2. **Diễn giải tự nhiên, đúng ngữ cảnh** ý nghĩa từng sao tại từng cung, dựa trên kho dữ liệu 101 sao đã trích xuất — dùng RAG + LLM để tổng hợp câu trả lời, không bịa.
3. (Mở rộng) Tích hợp Thần Số Học như một lớp luận giải bổ sung, đối chiếu chéo với Tử Vi.

### 1.3 Nguyên tắc thiết kế xuyên suốt
Rút ra từ quá trình làm dữ liệu (rất quan trọng, giữ nguyên khi code backend):
- **Tách bạch tuyệt đối 2 lớp**: lớp *tính toán* (an sao — phải đúng 100%, không cho LLM tự suy diễn) và lớp *diễn giải* (ngôn ngữ tự nhiên — LLM tổng hợp nhưng chỉ dựa trên dữ liệu retrieve được, không tự bịa thêm).
- **Không tin báo cáo, chỉ tin bằng chứng** — nguyên tắc này áp dụng luôn cho việc test backend/RAG sau này: mọi câu trả lời của hệ thống cần truy được về đúng nguồn (sao nào, cung nào) để audit.
- **Schema là hợp đồng, không đổi giữa chừng** — đã bị vi phạm 1 lần trong quá trình làm data (list → dict), gây tốn công sửa lại. Khi bắt đầu code, schema JSON và schema DB cần chốt trước, có validation tự động.

---

## 2. Tài sản dữ liệu hiện có (Input cho hệ thống)

| Tài sản | Nội dung | Trạng thái |
|---|---|---|
| Bảng công thức an sao (gõ tay, dựa theo Lập Thành Tử Vi) | Quy tắc xác định vị trí 14 chính tinh + phụ tinh theo giờ/ngày/tháng/năm sinh, cục số | Đã có, cần thẩm định lại 1 lượt trước khi code hoá thành engine |
| `sao_json/*.json` (101 file) | Diễn giải ý nghĩa từng sao theo từng cung, đã qua 4+ vòng QA (raw text đối chiếu) | **Sạch, đã nghiệm thu** |
| `than_so_hoc_bang_tra.json` | Bảng tra cứu Thần Số Học | Đã có, chưa qua vòng QA nghiêm ngặt như Tử Vi — **cần audit tương tự trước khi dùng** |
| `bang_tu_vi.json` | Dữ liệu tổng hợp/tra cứu khác | Đã có, cần xác nhận vai trò cụ thể trong pipeline trước khi dùng |

### 2.1 Schema chuẩn hóa cho 1 file sao (đã chốt qua thực tế)
```json
{
  "sao": "Tên sao (chuẩn hóa, viết hoa đầu từ)",
  "loai": "Phân loại: Cát tinh / Hung tinh / Tài tinh / Phúc tinh / Quí tinh / Gian tinh / Thọ tinh / Hộ tinh...",
  "cong_thuc_an_sao": "Thường để rỗng ở phần Tự Điển — công thức thật nằm ở chương đầu sách, xử lý riêng",
  "y_nghia_theo_cung": [
    { "cung": "Mệnh", "dien_giai": "..." },
    { "cung": "Thân", "dien_giai": "..." }
  ],
  "cach_cuc": "Các câu luận về cách cục lớn liên quan tới sao này (không gắn với 1 cung cụ thể)",
  "ghi_chu_thieu_du_lieu": "",
  "ten_khac": "(tùy chọn) tên gọi khác của sao, ví dụ Lộc Tồn / Thiên Lộc"
}
```
**Ràng buộc bắt buộc khi nạp vào hệ thống**: `y_nghia_theo_cung` luôn là **list**, không được là dict/object. Cần có script validate chạy CI mỗi khi có file mới hoặc sửa file cũ.

### 2.2 Việc cần làm trước khi dùng dữ liệu này cho code (Phase 0)
- [ ] Chạy 1 script validate toàn bộ 101 file: đúng schema, không rỗng bất thường, không còn rác OCR còn sót (tỉnh→tinh, Mộệnh→Mệnh, v.v. — quét lại bằng regex trên toàn bộ field text).
- [ ] Thẩm định lại bảng công thức an sao — đối chiếu tay với vài lá số mẫu đã biết trước kết quả (ví dụ lá số của chính người dùng, hoặc ví dụ có sẵn trong sách) để bắt lỗi trước khi code hoá thành engine.
- [ ] Audit `than_so_hoc_bang_tra.json` theo đúng quy trình grep-raw-text đã dùng cho Tử Vi (khả năng cao cũng có lỗi OCR/thiếu sót tương tự).
- [ ] Xác định rõ vai trò của `bang_tu_vi.json` — nếu trùng lặp chức năng với dữ liệu khác thì gộp hoặc loại bỏ để tránh 2 nguồn sự thật (2 sources of truth).

---

## 3. Kiến trúc tổng thể

```
┌─────────────┐      ┌──────────────────────┐      ┌────────────────────┐
│   Frontend   │─────▶│   Backend API         │─────▶│  An Sao Engine      │
│ (nhập ngày   │      │  (orchestration)       │      │  (thuần tính toán,  │
│  sinh, hỏi)  │◀─────│                        │◀─────│   không LLM)        │
└─────────────┘      └───────────┬────────────┘      └────────────────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │   RAG Retrieval      │
                       │ (vector DB / lookup   │
                       │  theo tên sao + cung) │
                       └───────────┬────────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │   LLM (tổng hợp câu   │
                       │   trả lời từ context  │
                       │   retrieve được)       │
                       └────────────────────┘
```

### 3.1 Nguyên tắc luồng dữ liệu
1. User nhập ngày/giờ/tháng/năm sinh (dương lịch) → Backend chuyển đổi âm lịch (nếu cần) → gọi **An Sao Engine**.
2. An Sao Engine trả về: vị trí 12 cung, sao nào nằm ở cung nào, cục số, ngũ hành bản mệnh — **kết quả xác định (deterministic), không qua LLM**.
3. Với mỗi câu hỏi của user (ví dụ "Cung Mệnh của tôi thế nào?"), Backend xác định (sao, cung) liên quan → **Retrieval** lấy đúng đoạn `dien_giai` tương ứng từ 101 file (không cần vector search phức tạp nếu tra cứu là exact-match theo tên sao + cung; vector search chỉ cần thiết nếu cho phép user hỏi tự do bằng ngôn ngữ tự nhiên không rõ cung/sao).
4. LLM nhận **context đã retrieve** (không phải toàn bộ 101 file) + câu hỏi → tổng hợp câu trả lời tự nhiên, được yêu cầu (qua system prompt) chỉ dùng thông tin trong context, không suy diễn thêm.

### 3.2 Quyết định kỹ thuật cần chốt sớm
| Vấn đề | Lựa chọn cần cân nhắc | Khuyến nghị ban đầu |
|---|---|---|
| Retrieval strategy | Exact-match theo (tên sao, tên cung) vs. vector similarity search | Vì mỗi lá số chỉ có tối đa ~14-18 sao chính/phụ tại 12 cung cố định, **exact-match/lookup dict là đủ và rẻ hơn nhiều** so với vector DB cho câu hỏi có cấu trúc rõ (cung nào, sao nào). Vector search chỉ cần cho câu hỏi tự do dạng "tôi hợp nghề gì" — lúc đó có thể embed toàn bộ `dien_giai` để retrieve theo chủ đề. |
| Vector DB (nếu cần) | Chroma / pgvector / Pinecone / Qdrant | Bắt đầu với **pgvector** (nếu đã dùng Postgres) hoặc **Chroma local** để tránh chi phí, dữ liệu chỉ ~101 sao × ~12 cung — quy mô rất nhỏ, không cần dịch vụ trả phí ở giai đoạn đầu. |
| LLM cho tầng diễn giải | Claude API (Haiku/Sonnet tùy độ phức tạp câu hỏi) | Câu hỏi đơn giản (tra 1 cung) → model rẻ. Câu hỏi tổng hợp nhiều cung/nhiều sao (ví dụ "luận về sự nghiệp cả đời") → model mạnh hơn. |
| Lưu trữ kết quả an sao của user | DB (Postgres/SQLite) theo user_id, hoặc tính lại mỗi lần | Nên **lưu lại** sau khi tính 1 lần (an sao là deterministic, không đổi theo thời gian) để tránh tính toán lặp lại và làm nền cho tính năng lịch sử/so sánh sau này. |
| API backend | REST hay GraphQL | REST đơn giản là đủ cho quy mô này. |

---

## 4. Đặc tả các module (PRD chi tiết)

### 4.1 Module: An Sao Engine

**Mục tiêu**: Từ (ngày, giờ, tháng, năm sinh dương lịch, giới tính) → ra được lá số đầy đủ 12 cung với vị trí chính tinh/phụ tinh.

**Input**:
- Ngày/giờ/tháng/năm sinh dương lịch
- Giờ sinh (theo 12 giờ Chi: Tý, Sửu, Dần...) — cần xử lý UI cho người dùng không rành giờ Chi
- Giới tính (ảnh hưởng an Đại Vận âm/dương nam nữ)

**Xử lý**:
1. Đổi dương lịch → âm lịch (cần thư viện/bảng chuyển đổi âm dương lịch đáng tin cậy — đây là điểm rủi ro kỹ thuật cần khảo sát kỹ, sai 1 ngày âm lịch = sai toàn bộ lá số).
2. Xác định Cục số (Thủy nhị cục, Mộc tam cục... dựa theo Nạp Âm của Can Chi năm sinh + cung Mệnh).
3. An 12 cung (Mệnh, Phụ Mẫu, Phúc Đức... theo giờ sinh).
4. An 14 chính tinh (Tử Vi, Thiên Cơ... theo Cục số + ngày sinh âm lịch).
5. An các phụ tinh, sát tinh, đào hoa, v.v. theo từng quy tắc riêng (đã có trong bảng công thức gõ tay).

**Output**: JSON có cấu trúc 12 cung, mỗi cung liệt kê tên các sao đóng tại đó.

**Yêu cầu chất lượng**: Đây là phần **không được sai** — cần bộ test case với lá số mẫu đã biết trước đáp án (tối thiểu 5-10 lá số) để so khớp tự động (unit test), chạy mỗi khi sửa engine.

**Việc cần làm rõ trước khi code** (đưa vào Phase 1):
- Nguồn thư viện chuyển đổi âm-dương lịch dùng cái gì (tự viết bảng tra hay dùng thư viện có sẵn, ví dụ `lunar-python`, `lunardate`...).
- Xác nhận lại toàn bộ quy tắc an phụ tinh/sát tinh trong bảng công thức gõ tay có đủ và đúng 100% không — đối chiếu với ít nhất 1 nguồn tài liệu thứ hai nếu có thể, vì đây là phần không có LLM "cứu" nếu sai.

### 4.2 Module: RAG Diễn Giải

**Mục tiêu**: Nhận (sao, cung) hoặc câu hỏi tự do từ user → trả lời có căn cứ từ 101 file dữ liệu.

**Input**: Kết quả an sao (từ module 4.1) + câu hỏi của user (có thể là click chọn cung, hoặc gõ tự do).

**Xử lý**:
- Nếu câu hỏi rõ ràng theo cung (UI dạng "xem cung Mệnh") → lookup trực tiếp tất cả sao đóng ở cung đó, lấy đúng `dien_giai` tương ứng, không cần LLM retrieval, có thể chỉ cần LLM để *viết lại cho mượt* (hoặc thậm chí hiển thị thẳng không qua LLM ở bản MVP).
- Nếu câu hỏi tự do ("tôi có hợp làm kinh doanh không") → cần xác định các cung/chủ đề liên quan (Tài Bạch, Quan Lộc...) rồi mới retrieve, có thể dùng LLM để map câu hỏi → (các cung liên quan) trước khi retrieve.

**Ràng buộc bắt buộc trong system prompt của LLM tổng hợp**:
- Chỉ dùng thông tin trong context được cung cấp (đến từ 101 file), không tự thêm kiến thức Tử Vi ngoài dữ liệu đã có.
- Khi dữ liệu không đủ để trả lời (ví dụ cung không có sao chính diễn giải rõ), trả lời trung thực là dữ liệu hạn chế, không bịa.
- Trích dẫn được nguồn (tên sao, cung) trong câu trả lời nếu cần audit.

**Rủi ro cần lưu ý**: 101 sao × 12 cung, nhiều entry `dien_giai` có nội dung khá dài và lộn xộn (câu cú theo lối sách cổ, liệt kê tổ hợp sao). Cần thử nghiệm xem LLM tổng hợp có "dịch" được sang câu văn dễ hiểu mà không đánh mất/đổi nghĩa hay không — đây là điểm cần user-test kỹ trước khi ra mắt.

### 4.3 Module: Thần Số Học (mở rộng, không phải MVP)

Tích hợp sau khi 2 module trên đã chạy ổn định. Vai trò: luận giải bổ sung dựa trên ngày sinh (tính các chỉ số: Đường đời, Sứ mệnh...), đối chiếu song song với Tử Vi chứ không thay thế.

### 4.4 Module: Backend API

**Các endpoint tối thiểu (MVP)**:
- `POST /lasso` — nhận thông tin sinh, trả về kết quả an sao (gọi module 4.1, lưu vào DB).
- `GET /lasso/{id}/cung/{ten_cung}` — trả về diễn giải các sao tại 1 cung cụ thể (gọi module 4.2 dạng lookup).
- `POST /lasso/{id}/hoi` — nhận câu hỏi tự do, trả lời qua RAG + LLM.

**Phi chức năng**:
- Cache kết quả an sao theo user (không tính lại).
- Rate limit cho endpoint `/hoi` (tốn LLM call).
- Logging đầy đủ input/output của LLM để debug chất lượng câu trả lời (đặc biệt giai đoạn đầu).

### 4.5 Module: Frontend

MVP tối thiểu: form nhập ngày sinh → hiển thị lá số dạng bảng 12 cung (giao diện Tử Vi truyền thống hoặc dạng đơn giản hóa) → cho phép bấm vào từng cung để xem diễn giải, và 1 ô hỏi đáp tự do.

---

## 5. Lộ trình triển khai (Roadmap theo giai đoạn)

### Phase 0 — Hoàn thiện & thẩm định dữ liệu nền (trước khi code bất cứ gì)
- Validate schema 101 file, quét rác OCR còn sót lần cuối.
- Thẩm định bảng công thức an sao bằng lá số mẫu có đáp án trước.
- Audit dữ liệu Thần Số Học theo quy trình QA đã dùng cho Tử Vi.
- **Đầu ra**: bộ dữ liệu "khóa" (frozen), có version, không sửa tùy tiện sau khi bắt đầu code Phase 1.

### Phase 1 — An Sao Engine (lõi tính toán)
- Chọn giải pháp chuyển đổi âm-dương lịch.
- Code hoá toàn bộ quy tắc an sao từ bảng công thức.
- Viết bộ test case (5-10 lá số mẫu có đáp án) — chạy tự động, phải pass 100% trước khi qua Phase 2.
- **Đầu ra**: 1 hàm/service `tinh_la_so(ngay, gio, thang, nam, gioi_tinh) → JSON 12 cung`.

### Phase 2 — Lớp truy xuất dữ liệu diễn giải (Retrieval, chưa cần LLM)
- Load 101 file vào dạng tra cứu nhanh (in-memory dict hoặc DB đơn giản: `sao → cung → dien_giai`).
- API lookup thẳng theo cung, trả về text thô (chưa qua LLM) — có thể demo được ở bước này mà không cần tích hợp LLM.
- **Đầu ra**: có thể xem lá số + đọc diễn giải thô cho từng cung (chức năng dùng được, dù văn phong còn thô).

### Phase 3 — Tích hợp LLM cho diễn giải tự nhiên + hỏi đáp tự do
- Viết system prompt ràng buộc chặt (chỉ dùng context, không bịa).
- Test với nhiều dạng câu hỏi khác nhau, đánh giá chất lượng bằng tay (không có ground-truth tự động cho phần này, cần review thủ công).
- Cân nhắc vector DB nếu quyết định hỗ trợ câu hỏi tự do phức tạp (xem mục 3.2).
- **Đầu ra**: chức năng hỏi đáp tự nhiên hoạt động.

### Phase 4 — Backend hoàn chỉnh + Frontend MVP
- Ráp API hoàn chỉnh, thêm DB lưu lá số user, auth (nếu cần).
- Frontend hiển thị lá số + luồng hỏi đáp.
- **Đầu ra**: sản phẩm demo được end-to-end.

### Phase 5 — Thần Số Học + tính năng mở rộng
- Tích hợp module Thần Số Học sau khi module chính ổn định.
- Các tính năng khác nếu có nhu cầu: lưu lịch sử, so sánh 2 lá số (hợp hôn nhân), xem theo đại vận/lưu niên...

---

## 6. Yêu cầu kỹ thuật phi chức năng (Non-functional requirements)

- **Độ chính xác an sao**: bắt buộc 100%, có test tự động, không chấp nhận "gần đúng".
- **Chi phí LLM**: theo dõi sát vì mỗi câu hỏi tự do tốn 1 lượt gọi API — cân nhắc cache câu trả lời cho các tổ hợp (sao, cung) phổ biến vì bản chất diễn giải theo cung là cố định, không đổi theo user (chỉ khác ở việc user hỏi gì).
- **Khả năng audit**: mọi câu trả lời cần truy ngược được nguồn dữ liệu gốc (phòng trường hợp cần sửa lỗi dữ liệu sau này, giống các vòng QA đã làm).
- **Ngôn ngữ**: toàn bộ dữ liệu và giao diện tiếng Việt có dấu — cần đảm bảo xử lý Unicode nhất quán (bài học từ lỗi NFC/NFD từng gặp khi so sánh tên file).
- **Bảo mật dữ liệu cá nhân**: ngày sinh, giờ sinh là dữ liệu nhạy cảm ở mức độ nhất định — cân nhắc chính sách lưu trữ/ẩn danh nếu mở rộng ra nhiều người dùng.

---

## 7. Rủi ro & câu hỏi mở (cần quyết định sớm)

| Rủi ro / câu hỏi | Ảnh hưởng | Đề xuất hướng xử lý |
|---|---|---|
| Chuyển đổi âm-dương lịch sai | Sai toàn bộ lá số | Khảo sát kỹ thư viện/bảng tra trước khi code Phase 1, test với ngày biên (đầu/cuối tháng âm) |
| Bảng công thức an sao gõ tay có thể còn thiếu sót (chưa đối chiếu nguồn thứ 2) | Sai lá số ở các trường hợp hiếm | Thêm bước đối chiếu chéo ở Phase 0 nếu có thể tìm nguồn tài liệu Trung Châu phái khác để so sánh |
| Chất lượng câu trả lời LLM khi tổng hợp nhiều sao xung khắc nhau tại 1 cung | Trải nghiệm người dùng, độ tin cậy | Cần review thủ công nhiều case ở Phase 3, có thể cần vài vòng chỉnh system prompt |
| Dữ liệu Thần Số Học chưa qua QA nghiêm ngặt | Lỗi tương tự đã gặp ở Tử Vi (OCR, thiếu sót) | Bắt buộc audit ở Phase 0, không đưa thẳng vào dùng |
| Vai trò thật của `bang_tu_vi.json` chưa rõ | Có thể trùng lặp/xung đột dữ liệu | Làm rõ trước Phase 0 kết thúc |
| Quy mô người dùng dự kiến | Ảnh hưởng lựa chọn hạ tầng (vector DB, chi phí LLM) | Cần ước lượng trước Phase 4 để chọn đúng mức đầu tư hạ tầng |

---

## 8. Định nghĩa "Hoàn thành" cho MVP

Sản phẩm MVP coi là đạt khi:
1. Nhập ngày/giờ sinh → ra đúng lá số 12 cung (verify bằng test case tự động).
2. Xem được diễn giải cho từng cung, văn phong tự nhiên, không sai lệch so với dữ liệu gốc.
3. Hỏi đáp tự do trả lời đúng trọng tâm, có thể audit nguồn.
4. Không còn lỗi dữ liệu đã biết (OCR rác, schema lệch) trong toàn bộ pipeline.

---

*Tài liệu này nên được cập nhật khi có quyết định kỹ thuật cụ thể (ví dụ chọn xong thư viện âm lịch, chọn xong vector DB) — coi đây là bản nháp sống (living doc), không phải bản đóng băng.*

# Template PRD Chuẩn (tái sử dụng cho dự án cá nhân/side project)

> Đúc kết từ quy trình xây PRD dự án Tử Vi Đẩu Số. Dùng bản này làm khung, xoá phần không liên quan, copy phần "Bộ câu hỏi khơi gợi yêu cầu" ra hỏi trước khi viết PRD thật.

---

## Cách dùng template này

1. Đừng viết PRD trước khi hỏi. Dùng **Mục A** để tự phỏng vấn bản thân (hoặc nhờ AI agent phỏng vấn) trước.
2. Trả lời xong Mục A mới điền vào khung PRD ở **Mục B**.
3. Với mỗi dự án có xử lý dữ liệu thô (crawl, OCR, gõ tay...), luôn thêm phần **Mục C — Thẩm định dữ liệu nền** trước khi code, không tin dữ liệu "trông có vẻ ổn".

---

## Mục A — Bộ câu hỏi khơi gợi yêu cầu (hỏi trước khi viết PRD)

### A.1 Phạm vi & nguồn lực
- MVP đầu tiên nên có phạm vi rộng hay hẹp? (1 module hay nhiều module song song?)
- Làm một mình hay có người/agent hỗ trợ? Ai code chính?
- Tốc độ mong muốn: gấp rút có deadline, hay side project tranh thủ?

### A.2 Sản phẩm & người dùng
- Nền tảng: web, mobile app, hay cả hai?
- Quy mô người dùng dự kiến: vài chục người quen, cộng đồng nhỏ, hay thương mại quy mô lớn?
- Mô hình kinh doanh: miễn phí, freemium, hay thu phí ngay từ đầu?
- Có cần tài khoản/đăng nhập/lưu lịch sử không, hay dùng xong là thôi (stateless)?

### A.3 Kỹ thuật
- Ngôn ngữ/stack ưu tiên (nếu có), hay để agent tự đề xuất?
- Có ràng buộc ngân sách cho dịch vụ bên thứ 3 không (LLM API, hosting, DB...)? Ưu tiên free tier hay chấp nhận trả phí?
- Có yêu cầu về giao diện cụ thể không (giữ định dạng gốc/truyền thống, hay tự do thiết kế lại)?
- Có tính năng nào bắt buộc phải có ngay ở MVP (không đợi phase sau) không?

### A.4 Dữ liệu (nếu dự án dựa trên dữ liệu thô/tự tổng hợp)
- Dữ liệu hiện có đã qua kiểm chứng/đối chiếu nguồn thứ 2 chưa?
- Có dữ liệu nào "coi là tạm ổn nhưng chưa thật sự audit kỹ" không? Liệt kê rõ, đừng gộp chung với dữ liệu đã audit.
- Rủi ro lớn nhất về độ chính xác dữ liệu là gì, và có phương án kiểm chứng nào chưa?

### A.5 Việc xuất bản/giao sản phẩm
- Có cần xuất PRD/tài liệu ra file cụ thể không (.md, .docx...)?
- Có cần checklist/template dùng lại cho các dự án sau không?

---

## Mục B — Khung PRD

### B.0 Tóm tắt quyết định (đọc nhanh)
Bảng 1 dòng/1 quyết định — copy thẳng câu trả lời từ Mục A vào đây trước tiên, để bất kỳ ai đọc PRD (kể cả agent code) nắm được ràng buộc trong 30 giây.

### B.1 Tổng quan sản phẩm
- Vấn đề cần giải quyết là gì, cho ai.
- Tầm nhìn ngắn gọn.
- Nguyên tắc thiết kế xuyên suốt (bất biến, agent code phải tuân theo suốt dự án — ví dụ "tách tính toán khỏi diễn giải", "không tin báo cáo chỉ tin bằng chứng", "schema là hợp đồng").

### B.2 Người dùng & phạm vi
- Đối tượng cụ thể, quy mô.
- Có/không: tài khoản, thu phí, lưu trữ dữ liệu người dùng.
- Hệ quả kỹ thuật của các lựa chọn trên (ví dụ: không tài khoản → bỏ hẳn DB user, giảm phức tạp).

### B.3 Tài sản dữ liệu hiện có (nếu có)
- Bảng liệt kê từng nguồn dữ liệu, trạng thái (sạch/chưa audit/không rõ vai trò).
- Schema chuẩn hoá + ràng buộc bắt buộc.
- Checklist việc cần làm trước khi tin dữ liệu.

### B.4 Kiến trúc tổng thể
- Sơ đồ luồng dữ liệu (ASCII đơn giản là đủ).
- Bảng quyết định kỹ thuật đã chốt (stack, retrieval strategy, DB, LLM provider, lưu trữ...) — mỗi dòng có lý do ngắn gọn.

### B.5 Đặc tả module
- Mỗi module: input → xử lý → output, ràng buộc chất lượng, cách test/verify.
- Phân biệt rõ module tính toán thuần (deterministic, phải test tự động) vs module dùng LLM (cần review thủ công, ràng buộc prompt chặt).

### B.6 Lộ trình triển khai (Phase 0, 1, 2...)
- Mỗi phase: việc cần làm, đầu ra cụ thể (không mơ hồ).
- Phase 0 luôn nên là "thẩm định dữ liệu nền" nếu dự án có dữ liệu tự tổng hợp — đừng nhảy thẳng vào code.

### B.7 Yêu cầu phi chức năng
- Độ chính xác, chi phí (đặc biệt nếu dùng free tier — ghi rõ giới hạn), bảo mật, ngôn ngữ/locale.

### B.8 Rủi ro & câu hỏi mở
- Bảng: rủi ro/câu hỏi → ảnh hưởng → hướng xử lý. Cập nhật liên tục, đánh dấu resolved khi xong.

### B.9 Định nghĩa "Hoàn thành" cho MVP
- Danh sách điều kiện cụ thể, đo được, không mơ hồ ("chạy tốt" không phải điều kiện hợp lệ — phải là "test case X pass 100%").

---

## Mục C — Checklist thẩm định dữ liệu nền (bắt buộc nếu dự án có dữ liệu tự tổng hợp/OCR/gõ tay)

- [ ] Validate schema toàn bộ file dữ liệu bằng script tự động, không kiểm tra tay từng file.
- [ ] Quét rác OCR/lỗi định dạng còn sót (regex cho ký tự lạ, khoảng trắng thừa, encoding lỗi).
- [ ] Với mỗi "sự thật" quan trọng (công thức, quy tắc tính toán): tìm ≥1 nguồn thứ 2 độc lập để đối chiếu trước khi code hoá thành logic hệ thống.
- [ ] Với mỗi file/nguồn dữ liệu "không rõ vai trò": xác định rõ chức năng, loại bỏ nếu trùng lặp, không để tồn tại mơ hồ tới lúc code.
- [ ] Có bộ test case với đáp án đã biết trước (ground truth) cho mọi logic tính toán quan trọng, chạy tự động mỗi khi sửa.
- [ ] Ghi version cho bộ dữ liệu đã "khoá" (frozen) trước khi bắt đầu code dựa trên nó.

---

*Copy file này, xoá phần chú thích hướng dẫn, giữ lại khung B + C, điền theo dự án cụ thể.*

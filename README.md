# Dự Án Tử Vi Đẩu Số

Dự án này chuyên về việc số hóa và trích xuất dữ liệu từ các sách Tử Vi Đẩu Số và Thần Số Học, chuyển đổi sang định dạng JSON có cấu trúc để phục vụ cho các ứng dụng tra cứu, an sao, và hệ thống RAG (Retrieval-Augmented Generation).

## Trạng thái hiện tại
- Đã hoàn tất khâu trích xuất dữ liệu 101 sao từ Tự Điển Tử Vi sang thư mục `sao_json/`.
- Dữ liệu đã được chuẩn hóa về định dạng đồng nhất, sửa lỗi OCR.
- Đang ở giai đoạn thiết kế kỹ thuật theo PRD.

## Cấu trúc thư mục chính
- `sao_json/`: Chứa 101 file JSON tương ứng với 101 sao, mỗi file bao gồm định nghĩa, tính chất, ý nghĩa theo từng cung và các cách cục liên quan.
- `an_sao.json`: Bảng công thức lưu trữ quy tắc an sao Tử Vi.
- `than_so_hoc_bang_tra.json`, `bang_tu_vi.json`: Dữ liệu bảng tra cứu Thần Số Học và Tử Vi.
- `data/`: Chứa các file raw, tài liệu gốc và kết quả OCR.
- `_archive_extract.py`: Script trích xuất (được lưu trữ để tham khảo logic).

## PRD - Quản Lý Rủi Ro & Tài Sản (Thần Số Học)

### B3 - Tài sản dữ liệu hiện có
- **Engine Thần Số Học**: `engine_than_so_hoc.py` (Đã thống nhất sử dụng Python, loại bỏ các bản nháp ngôn ngữ khác). Chạy thuật toán chuẩn hệ Pythagorean cho 4 chỉ số cốt lõi (Đường Đời, Sứ Mệnh, Linh Hồn, Nhân Cách).
- **Database Nội Dung**: `data/than_so_hoc_bang_tra_v2.json` (Trạng thái: **2.0-frozen**). Nội dung 48 mục đã qua audit, biên soạn chuẩn hệ Pythagorean.

### B8 - Rủi ro & Câu hỏi mở
- [x] **Rủi ro Encoding**: File JSON cũ bị lỗi font -> *Resolved: Sinh file mới `v2.json` với encoding chuẩn UTF-8.*
- [x] **Rủi ro Gộp sai khái niệm**: Khái niệm Đường Đời và Sứ Mệnh bị gộp chung -> *Resolved: Tách bạch rõ 4 nhánh độc lập trong schema JSON v2.*
- [x] **Rủi ro Thiếu Master Number**: Lấy thiếu số 11, 22, 33 -> *Resolved: Đã bổ sung đẩy đủ Master Numbers cho cả 4 nhánh.*
- [x] **Rủi ro Mix Chaldean/Pythagorean**: Lẫn lộn 2 hệ phái -> *Resolved: Chốt cứng hệ Pythagorean cho cả công thức tính và nội dung diễn giải.*
- [x] **Câu hỏi mở Quy tắc Master Number**: Khi nào rút gọn, khi nào giữ? -> *Resolved: Chốt quy tắc giữ nguyên Master Number 11/22/33 ngay khi xuất hiện ở BẤT KỲ bước cộng nào (VD: Einstein Đường đời = 33).*
- [ ] **Kết nối hiển thị (Phase 1)**: Cần viết `main.py` để kết nối Engine và JSON.

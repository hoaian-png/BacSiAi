# Nhật ký công việc

## 27/11/2026 — Sắp xếp dự án theo nội dung bài

- Dùng ảnh làm ví dụ ban đầu, sau đó điều chỉnh theo yêu cầu mới thành 7 nhóm phù hợp bài tai mũi họng.
- Gộp log chương trình vào `07_nhat_ky/chuong_trinh`; kết quả cuối vào `05_bao_cao/ket_qua_cuoi`, tránh tách nhóm trùng mục đích.
- Chuyển giao diện, backend, train và các script xử lý dữ liệu sang tầng mã nguồn.
- Chuyển nguyên bản các file raw, normalized, prepared, config và sources sang tầng dữ liệu.
- Chuyển báo cáo kiểm tra dữ liệu và thư mục so sánh mô hình sang tầng báo cáo.
- Chuyển tài liệu thiết kế, hướng dẫn và các bản nháp cũ sang tầng tài liệu.
- Giữ README.md, AGENTS.md và cấu hình Git ở gốc để đọc và làm việc với dự án.
- Di chuyển thư viện hỗ trợ vào `01_ma_nguon/.data-tools`, không đặt lẫn trong dữ liệu.
- Cập nhật đường dẫn script, tài liệu và thuộc tính Git bảo toàn byte raw.
- Lưu ánh xạ và checksum để đối chiếu việc di chuyển. Trạng thái kiểm tra cuối được ghi trong `sap_xep_thu_muc.json`.
- Chưa stage, commit hoặc push; không huấn luyện mô hình và không tạo ứng dụng web.

Ghi chú: thư mục mô hình, thử nghiệm và kết quả mới có hướng dẫn/chỗ giữ cấu trúc, chưa có artifact hoặc kết quả huấn luyện.

## 27/11/2026 — Đổi đuôi tài liệu và chuẩn bị đồng bộ GitHub

- Người dùng đặt danh sách mô hình tại `03_mo_hinh/MoHinh.txt` và bản phác công việc tại `ThuTuLamViec.txt` ở gốc; đổi hai file sang `.md`, đối chiếu SHA-256 để giữ nguyên nội dung.
- Người dùng tiếp tục yêu cầu cập nhật lên repository BacSiAi.
- Kiểm tra dữ liệu, đường dẫn và thư viện được bỏ qua trước khi commit; đồng bộ với lịch sử GitHub hiện có, không force push.

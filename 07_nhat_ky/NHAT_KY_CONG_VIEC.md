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

## 28/11/2026 — Hoàn thành duyệt tập Pilot (120 câu) và xuất bản phiên bản xác nhận

- Ghi nhận quyết định của người dùng cho 100 câu còn lại của tập Pilot: người dùng chấp thuận 58 nhãn AI đề xuất, loại 26 câu ngoài phạm vi và giữ 16 câu ở trạng thái thảo luận.
- Kết hợp với 20 câu đợt 1 (12 reviewed, 7 excluded, 1 needs_discussion), toàn bộ 120 câu của tập Pilot đã được xử lý xong (0 câu pending_manual_review).
- Thống kê toàn bộ tập Pilot (120 câu):
  + `reviewed`: 70 câu có nhãn chuẩn (`hong_amidan`: 14, `trieu_chung_tai`: 11, `xoang`: 10, `ho_dom`: 9, `cam_lanh`: 8, `trieu_chung_mui`: 8, `cam_cum`: 7, `sot`: 3).
  + `excluded`: 33 câu loại khỏi bài toán TMH.
  + `needs_discussion`: 17 câu (nhãn chuẩn để trống, không dùng train).
  + `pending_manual_review`: 0 câu.
- Xuất bản bộ dữ liệu duyệt chính thức tại `02_du_lieu/filedata/reviewed/annotations/v4_user_accepted_20261128/` (gồm `questions_reviewed.csv`, `questions_reviewed.jsonl` và `review_manifest.json`).
- Kiểm tra hợp lệ bằng `validate_pilot.py --mode annotated` đạt 100%.
- Lưu ý: Việc người dùng chấp thuận đề xuất AI xác định chủ đề câu hỏi, không phải chuyên gia y tế đã xác minh nội dung y khoa. Quy mô 70 câu có nhãn chưa đủ điều kiện để huấn luyện hoặc so sánh 5 mô hình; chuẩn bị kế hoạch mở rộng gán nhãn từ kho `prepared`.
- Chưa huấn luyện mô hình, chưa triển khai ứng dụng, chưa tạo database SQLite, chưa stage/commit/push lên Git.

## 28/11/2026 — Kiểm kê sau pilot và phương án mở rộng 200 câu

- Đối chiếu file làm việc với CSV xuất: tương đương; validator annotated thành công.
- Làm rõ `annotation_complete = False` vì còn 17 needs_discussion, dù không còn pending.
- Kiểm kê 3.130 prepared: bỏ 120 ID pilot còn 3.010; bỏ nhóm trùng pilot còn 2.346 câu trong 1.643 group_id.
- Phát hiện nhóm cảm lạnh chỉ còn 12 ứng viên thuộc 9 nhóm mới, đều ViMedAQA theo nhãn gợi ý; không khẳng định các nguồn khác không có nội dung cảm lạnh.
- Đề xuất đợt 200 câu (184 ứng viên nhãn đơn, 16 câu chưa nhãn đơn); chưa lấy mẫu, chưa thay đổi dữ liệu.
- Duyệt nhãn chủ đề không tương đương duyệt y khoa; 1.814 mục kiến thức vẫn chưa được phê duyệt.
- Chỉ cập nhật tài liệu; không train, tạo ứng dụng, cài thư viện hoặc đồng bộ Git.

## 28/11/2026 — Thực hiện lấy mẫu đợt mở rộng 200 câu (Batch 02) và tạo phiếu duyệt

- Thực hiện lấy mẫu 200 câu ứng viên đợt mở rộng theo seed=42 bằng script `01_ma_nguon/xu_ly_du_lieu/sample_expansion.py`.
- Lọc triệt để: loại bỏ toàn bộ 120 ID pilot và 111 group_id thuộc pilot; mỗi group_id trong đợt chỉ chọn tối đa 1 câu; kiểm tra không trùng lặp văn bản.
- Kết quả lấy mẫu đạt 100% chỉ tiêu theo nhãn gợi ý:
  + `sot`: 30, `cam_cum`: 30, `ho_dom`: 25, `trieu_chung_mui`: 25, `trieu_chung_tai`: 25, `hong_amidan`: 20, `xoang`: 20, `cam_lanh`: 9 (toàn bộ 9 nhóm cảm lạnh mới khả dụng), `Chưa có nhãn đơn tự động`: 16.
  + Phân bố nguồn: ViMQ: 75, ViHealthQA: 67, ViMedAQA: 58.
  + Không thiếu hụt quota ở bất kỳ nhóm nào (deficit = 0).
- Xuất dữ liệu độc lập tại `02_du_lieu/filedata/reviewed/expansion/batch_02_v1/` gồm `questions_expansion.csv`, `questions_expansion.jsonl` và `sampling_manifest.json` (toàn bộ ở trạng thái `pending_manual_review`, các trường duyệt ban đầu để trống).
- Viết công cụ kiểm định độc lập `01_ma_nguon/xu_ly_du_lieu/validate_expansion.py` kiểm tra toàn vẹn schema, checksum và tính không giao cắt với pilot.
- Khởi tạo phiếu duyệt `06_tai_lieu/PHIEU_DUYET_MO_RONG_DOT_02.md` với đủ 200 câu theo STT 001–200, nguyên văn, nhãn gợi ý và các ô `[Chờ điền]`.
- Bảo toàn nguyên vẹn tập pilot (120 câu), bộ đã duyệt `v4_user_accepted_20261128`, và các tệp gốc raw/normalized/prepared.
- Không tự gán nhãn chuẩn, không train, không tạo ứng dụng, không commit/push.

## 28/11/2026 — Chuẩn bị công bố phần đã kiểm tra lên GitHub

- Người dùng yêu cầu cập nhật phần đã ổn lên GitHub, commit tiếng Việt không dấu.
- Công bố công cụ pilot và lấy mẫu/validator mở rộng đã qua kiểm thử; giữ byte snapshot reviewed bằng .gitattributes để checksum đúng sau checkout.
- Pilot: 70 reviewed, 33 excluded, 17 needs_discussion. Đợt mở rộng: 200 câu nguồn, bản làm việc có 1 reviewed, 5 excluded, 194 pending; 26 câu thảo dược chưa duyệt.
- Phiếu mở rộng công bố chỉ giữ câu gốc và quyết định đã xác nhận. Bản nháp AI 168 câu còn lỗi giữ trên máy. Các đề xuất pilot v1–v4 là lịch sử truy vết; bản được chấp thuận nằm trong annotations/v4_user_accepted_20261128.
- Không công bố scratch. Chưa train, chưa triển khai web hoặc phê duyệt kho kiến thức.

## 28/11/2026 — Chọn Gemini API cho LLM

- Theo yêu cầu người dùng, thay lựa chọn Ollama bằng Google Gemini qua Gemini API trong README, kiến trúc, lộ trình và hướng dẫn tác nhân.
- Giữ Streamlit/SQLite chạy local và năm mô hình phân loại; Gemini chỉ tổng hợp, diễn đạt nội dung truy xuất có nguồn.
- Chưa chốt model ID; chưa tích hợp, gọi API, tạo khóa hoặc cài thư viện. Ghi rõ yêu cầu Internet, cấu hình khóa local và xử lý lỗi dịch vụ.
- Chỉ đồng bộ các tài liệu liên quan lựa chọn Gemini; không đưa bộ đề xuất AI 168 câu còn lỗi lên GitHub.

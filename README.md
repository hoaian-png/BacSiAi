# BacSiAi — Hỏi đáp thông tin tai mũi họng

Tài liệu cập nhật ngày **28/11/2026**. Dự án hướng đến ứng dụng **Streamlit chạy localhost**, kết hợp nhận diện từ khóa, mô hình phân loại câu hỏi và truy xuất kiến thức. LLM chỉ diễn đạt lại nội dung đã tìm được.

## Trạng thái thực tế

Hiện đã có dữ liệu và công cụ chuẩn bị dữ liệu; **chưa có ứng dụng Streamlit, backend, SQLite hoặc mô hình đã huấn luyện trong dự án này**. Các thư mục chức năng đang giữ chỗ bằng `.gitkeep`.

| Hạng mục | Hiện trạng |
|---|---|
| Ba bộ dữ liệu | Đã tải ViMQ, ViHealthQA, ViMedAQA |
| Chuẩn hóa | 63.328 bản ghi, có CSV và JSONL |
| Câu hỏi ứng viên | 3.130 câu hỏi sau lọc và loại trùng |
| Kiến thức ứng viên | 1.814 mục sau lọc và loại trùng |
| Nhãn chủ đề | Mới có gợi ý bằng từ khóa; 0 nhãn chuẩn đã được xác nhận trong báo cáo hiện tại |
| Kiến thức dùng trả lời | Chưa được duyệt để đưa vào RAG |
| Năm mô hình | Đã chốt danh sách; chưa train |
| Giao diện, backend, SQLite, LLM | Chưa triển khai |

Số liệu lấy từ `05_bao_cao/kiem_tra_du_lieu/summary.json`, không phải kết quả huấn luyện. Tập ứng viên có thể còn mẫu ngoài phạm vi, đặc biệt câu chỉ nhắc sốt; cần rà soát trước khi dùng.

## Mục tiêu

- Hỏi đáp tiếng Việt về tai, mũi, họng, ho, đờm, sốt, cảm lạnh và cúm.
- Phân loại **chủ đề câu hỏi**, không kết luận người dùng mắc bệnh.
- Tìm nội dung phù hợp và hiển thị nguồn tham khảo.
- Hỏi bổ sung khi thiếu thông tin hoặc chưa có tài liệu phù hợp.
- So sánh 5 mô hình bằng cùng một bộ đánh giá.

## Công nghệ đã chọn

| Thành phần | Lựa chọn |
|---|---|
| Giao diện | Streamlit; một file chính `01_ma_nguon/giaodien/app.py` |
| Xử lý ứng dụng | Python; một file chính `01_ma_nguon/backend/backend.py` |
| Cơ sở dữ liệu | SQLite, dự kiến `02_du_lieu/database/medical.db` |
| ML truyền thống | TF-IDF + Multinomial Naive Bayes, Logistic Regression, Linear SVM, Random Forest |
| Học sâu | Fine-tune PhoBERT-base-v2 cho phân loại chủ đề |
| Truy xuất ban đầu | TF-IDF và cosine similarity, kết hợp từ khóa/chủ đề |
| LLM | Google Gemini qua Gemini API; model ID sẽ cấu hình khi triển khai, chưa tích hợp |

Giao diện vẫn chạy localhost; bước gọi Gemini API cần kết nối Internet. Đây là lựa chọn thiết kế, chưa có mã tích hợp hoặc lời gọi API thực tế.

LLM không nằm trong 5 mô hình cần train. LLM chỉ sắp xếp và diễn đạt nội dung truy xuất được; lời nhắc không bảo đảm tuyệt đối rằng đầu ra đúng, nên vẫn cần kiểm thử độ bám nguồn và cơ chế quay về nội dung gốc khi cần.

## Bắt đầu từ đâu?

Dự án được sắp xếp theo **7 nhóm phù hợp bài tai mũi họng**: `01_ma_nguon`, `02_du_lieu`, `03_mo_hinh`, `04_thu_nghiem`, `05_bao_cao`, `06_tai_lieu`, `07_nhat_ky`. Kết quả cuối nằm trong báo cáo; log kỹ thuật nằm trong nhật ký, không cần hai nhóm riêng ở gốc.

1. Đọc [kiến trúc](06_tai_lieu/PROJECT.md) và [lộ trình](06_tai_lieu/ROADMAP.md).
2. Xem [hướng dẫn thư mục](06_tai_lieu/HUONG_DAN_THU_MUC.md).
3. Đọc [hướng dẫn dữ liệu](06_tai_lieu/DU_LIEU.md), [từ điển cột](06_tai_lieu/TU_DIEN_DU_LIEU.md) và [quy ước lưu trữ](06_tai_lieu/QUY_UOC_LUU_TRU.md).
4. Duyệt nhãn và kiến thức trước khi train hay ghép LLM.

## Lệnh có thể chạy hiện tại

Từ thư mục gốc dự án, dùng Python 3.11 trở lên:

```powershell
python -X utf8 01_ma_nguon/xu_ly_du_lieu/validate_data.py
```

Lệnh trên kiểm tra các file dữ liệu đã xuất, không train và không khởi chạy web. Nếu cần tạo lại dữ liệu, xem các lệnh cùng yêu cầu PyArrow trong `06_tai_lieu/DU_LIEU.md`; sao lưu bản gán nhãn thủ công trước khi chạy lại pipeline.

## Chạy web sau khi triển khai

Lệnh dự kiến là `python -m streamlit run 01_ma_nguon/giaodien/app.py`. **Hiện chưa chạy được lệnh này vì chưa có file ứng dụng và danh sách thư viện chạy web.** Không coi đây là hướng dẫn cho một ứng dụng đã hoàn thành.

## Tài liệu và Git

- [AGENTS.md](AGENTS.md): hướng dẫn làm việc với mã nguồn và dữ liệu.
- [06_tai_lieu/PROJECT.md](06_tai_lieu/PROJECT.md): mục tiêu, nhiệm vụ ML, luồng hỏi đáp và kiến trúc.
- [06_tai_lieu/ROADMAP.md](06_tai_lieu/ROADMAP.md): thứ tự làm và tiêu chí hoàn thành.
- [06_tai_lieu/HUONG_DAN_THU_MUC.md](06_tai_lieu/HUONG_DAN_THU_MUC.md): nơi đặt từng loại file.
- [06_tai_lieu/QUY_UOC_LUU_TRU.md](06_tai_lieu/QUY_UOC_LUU_TRU.md): schema, phiên bản, nhãn và lưu mô hình.

Repository: https://github.com/hoaian-png/BacSiAi. Ngày 27/11/2026, người dùng yêu cầu đồng bộ cấu trúc 7 nhóm và tài liệu lên GitHub sau khi chuẩn bị trên máy. Hai bản phác đã đổi đuôi thành `03_mo_hinh/MoHinh.md` và `ThuTuLamViec.md`, giữ nguyên nội dung. Các file `.txt` máy đọc của dữ liệu và thư viện vẫn giữ định dạng.

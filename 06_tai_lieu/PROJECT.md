# Kiến trúc và phạm vi dự án BacSiAi

## Mục tiêu

Xây dựng ứng dụng Streamlit chạy local để người dùng hỏi thông tin về tai, mũi, họng, ho, đờm, sốt, cảm lạnh và cúm bằng tiếng Việt. Hệ thống dự đoán chủ đề, tìm nội dung phù hợp rồi dùng LLM diễn đạt lại câu trả lời có nguồn.

Tài liệu này mô tả **thiết kế dự kiến**. Hiện dự án có dữ liệu và công cụ chuẩn hóa; chưa có web, backend, SQLite, mô hình train hoặc tích hợp LLM.

## Ba bộ dữ liệu

| Bộ dữ liệu | Số bản ghi đã chuẩn hóa | Vai trò |
|---|---:|---|
| ViMQ | 9.000 | Câu hỏi có nhãn ý định và thực thể; bổ sung nhãn chủ đề |
| ViHealthQA | 10.015 | Câu hỏi thực tế và câu trả lời tham khảo có URL |
| ViMedAQA | 44.313 | Hỏi đáp có ngữ cảnh và từ khóa nguồn, hỗ trợ truy xuất |

Tổng: **63.328 bản ghi**. Sau lọc sơ bộ có **3.130 câu hỏi không trùng** và **1.814 mục kiến thức**. Đây là tập ứng viên, không phải toàn bộ dữ liệu đã được chấp thuận để 01_ma_nguon/train/trả lời.

Nguồn và phiên bản cụ thể nằm trong `02_du_lieu/filedata/sources.json`. Đặc điểm từng bộ, điều kiện sử dụng và các giới hạn nằm trong [hướng dẫn dữ liệu](DU_LIEU.md).

## Phân biệt chủ đề, ý định và từ khóa

| Thành phần | Ví dụ | Cách dùng |
|---|---|---|
| Chủ đề | `ho_dom`, `xoang`, `trieu_chung_tai` | Nhãn đích của thí nghiệm so sánh 5 mô hình |
| Ý định | Nguyên nhân, mức độ, hướng xử lý | Một trục riêng; tận dụng nhãn ViMQ, chưa mở thêm nhiệm vụ train bắt buộc |
| Từ khóa | Ho có đờm, ù tai, nghẹt mũi | Hỗ trợ tạo đặc trưng, nhận diện cụm từ và truy xuất |

Ví dụ minh họa: “Vì sao tôi bị ù tai?” có chủ đề tai, ý định nguyên nhân, từ khóa “ù tai”. Điều này không xác nhận người dùng mắc một bệnh cụ thể.

Tám chủ đề khởi đầu: `ho_dom`, `trieu_chung_mui`, `xoang`, `hong_amidan`, `trieu_chung_tai`, `cam_lanh`, `cam_cum`, `sot`. Có thể sửa bộ nhãn sau giai đoạn gán nhãn thử, nhưng phải giữ phiên bản và thống nhất trước khi đánh giá.

`topic_label` hiện là gợi ý bằng quy tắc. `gold_topic_label` chỉ điền sau khi người gán nhãn xác nhận. Không tự xem câu không khớp từ điển là ngoài phạm vi.

## Năm mô hình và cách train

| Mô hình | Đầu vào | Huấn luyện |
|---|---|---|
| Multinomial Naive Bayes | TF-IDF và tùy chọn đặc trưng từ khóa không âm | Học có giám sát |
| Logistic Regression | Cùng bộ đặc trưng truyền thống | Học có giám sát; chọn regularization trên validation |
| Linear SVM / LinearSVC | Cùng bộ đặc trưng truyền thống | Học có giám sát; chọn C trên validation |
| Random Forest | Cùng bộ đặc trưng truyền thống | Chọn số cây/độ sâu trên validation |
| PhoBERT-base-v2 | Câu hỏi tiếng Việt có dấu, tách từ và tokenize | Fine-tune mô hình pretrained với lớp phân loại |

Bốn mô hình truyền thống so sánh hai cách biểu diễn: TF-IDF và TF-IDF kết hợp đặc trưng từ khóa. PhoBERT dùng quy trình đầu vào riêng nhưng cùng nhãn và cách chia tập.

Các tham số cụ thể, epoch và batch size sẽ được chốt khi triển khai theo cấu hình máy và validation; chưa có kết quả để khẳng định mô hình tốt nhất. Lưu pipeline truyền thống cùng bộ tạo đặc trưng; lưu PhoBERT cùng tokenizer và ánh xạ nhãn.

## Kiến trúc ứng dụng

```text
01_ma_nguon/giaodien/app.py — Streamlit
          ↓
01_ma_nguon/backend/backend.py
  Chuẩn hóa câu hỏi và trích từ khóa
          ↓
  Mô hình phân loại đang được chọn
          ↓
  Truy xuất nội dung từ SQLite/chỉ mục TF-IDF
          ↓
  Kiểm tra mức phù hợp và thông tin còn thiếu
          ↓
  LLM diễn đạt nội dung tìm được, hoặc hỏi bổ sung
          ↓
Giao diện hiển thị câu trả lời và nguồn
```

Không chạy cả năm mô hình trên mọi câu hỏi. Train cả năm để so sánh; triển khai mô hình được chọn theo kết quả và chi phí chạy.

## Truy xuất và vai trò LLM

- Dùng câu hỏi đầy đủ, từ khóa và chủ đề để tìm tài liệu; không chỉ tra một đáp án cố định theo tên bệnh.
- Chủ đề là tín hiệu ưu tiên, không phải bộ lọc cứng duy nhất. Mô hình phân loại có thể sai hoặc câu hỏi có nhiều triệu chứng.
- Chỉ đưa các mục kiến thức đã được duyệt vào chỉ mục trả lời chính thức.
- LLM được phép nối ý, sắp xếp đoạn và diễn đạt dễ hiểu. Không yêu cầu nó tự quyết định chẩn đoán, lựa chọn thuốc hoặc thêm thông tin ngoài nguồn.
- Giữ điều kiện áp dụng, phủ định và nguồn. Không ghép nội dung của các tình huống mâu thuẫn thành một khuyến nghị chung.
- Nếu không tìm thấy nội dung phù hợp: hỏi thêm hoặc thông báo chưa có thông tin. Nếu Ollama không chạy: có thể hiển thị nội dung nguồn đã duyệt.
- Chọn mô hình Ollama sau khi kiểm tra RAM/GPU; tên mô hình chưa được chốt.

## SQLite dự kiến

| Bảng | Nội dung |
|---|---|
| datasets | Tên nguồn, phiên bản, URL và điều kiện sử dụng |
| questions | Câu hỏi, nhãn gợi ý/đã duyệt, từ khóa, nhóm và split |
| knowledge | Nội dung, ngữ cảnh, URL và trạng thái phê duyệt |
| keyword_rules | Biến thể, cách viết chuẩn và chủ đề gợi ý |
| model_runs | Mô hình, cấu hình, kết quả, phiên bản dữ liệu và đường dẫn artifact |

Không lưu trọng số mô hình trong SQLite. Lịch sử hiển thị dùng session state trước; không mặc định lưu toàn bộ nội dung sức khỏe của người hỏi.

## Hội thoại và giao diện

Ba màn hình/tab: **Hỏi đáp**, **Duyệt dữ liệu**, **So sánh mô hình**. Một file giao diện chính và một file xử lý chính; mã train được tách riêng.

Khi hỏi bổ sung, cần lưu trạng thái thông tin đang thiếu, không chỉ lưu danh sách tin nhắn. Không bắt người dùng lặp lại toàn bộ câu hỏi nếu có thể kết hợp câu trả lời ngắn với ngữ cảnh đang chờ. Có chức năng bắt đầu cuộc hội thoại mới để xóa ngữ cảnh cũ.

## Đánh giá

- Phân loại: Macro-F1, Precision/Recall từng nhãn, Accuracy và ma trận nhầm lẫn.
- Tốc độ: thời gian huấn luyện và suy luận trên cùng môi trường được ghi rõ.
- Truy xuất: tạo tập câu hỏi có tài liệu liên quan được gán nhãn để đo Recall@k.
- Câu trả lời cuối: kiểm tra phù hợp câu hỏi, bám nguồn, không thêm thông tin, giữ điều kiện/phủ định và trích dẫn đúng.
- Hội thoại: câu thiếu thông tin, hỏi tiếp ngắn, nhiều triệu chứng, lỗi chính tả, không dấu và ngoài phạm vi.

Tập test không dùng để chọn mô hình/ngưỡng. Không đưa đáp án chuẩn của test vào kho truy xuất rồi coi kết quả đó là khả năng tổng quát hóa. Chưa có số đo nào của các phần này trong dự án hiện tại.

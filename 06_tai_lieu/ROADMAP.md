# Lộ trình triển khai BacSiAi

Tài liệu cập nhật **27/11/2026**. Dấu `[x]` chỉ việc đã có bằng chứng trong dự án, không đánh dấu hoàn thành theo dự định. Đợt hiện tại chỉ bổ sung tài liệu trên máy, chưa đưa lên Git.

## Giai đoạn 0 — Chuẩn bị dữ liệu và thiết kế

- [x] Chốt Streamlit chạy local, Python và SQLite cho ứng dụng dự kiến.
- [x] Chốt năm mô hình: Naive Bayes, Logistic Regression, Linear SVM, Random Forest, PhoBERT-base-v2.
- [x] Chốt LLM chỉ diễn đạt nội dung truy xuất, không train LLM ở giai đoạn đầu.
- [x] Tải ba bộ dữ liệu và lưu nguồn/phiên bản/checksum.
- [x] Chuẩn hóa 63.328 bản ghi thành CSV và JSONL.
- [x] Tạo 3.130 câu hỏi và 1.814 mục kiến thức ứng viên sau lọc/loại trùng.
- [x] Có báo cáo kiểm tra dữ liệu và script kiểm tra lại.
- [x] Viết bộ tài liệu hướng dẫn, kiến trúc và quy ước tại thư mục máy.
- [x] Sắp xếp file vào 7 nhóm theo nội dung đồ án, cập nhật đường dẫn mã và tài liệu; chưa stage, commit hoặc push thay đổi này.

**Chưa hoàn thành:** nhãn chuẩn, phê duyệt kiến thức, train mô hình và ứng dụng.

## Giai đoạn 1 — Chốt nhãn và duyệt dữ liệu

### Việc cần làm

- [ ] Viết hướng dẫn gán nhãn chủ đề; phân biệt với ý định và thực thể.
- [ ] Gán thử một tập nhỏ phủ các chủ đề và câu mơ hồ, thống nhất cách xử lý bất đồng.
- [ ] Kiểm tra tám nhãn khởi đầu và điều chỉnh trước khi gán toàn bộ.
- [ ] Duyệt câu hỏi, điền gold_topic_label; lưu riêng khỏi file sinh tự động.
- [ ] Xử lý câu nhiều triệu chứng, phủ định, tiền sử, lỗi chính tả, ngoài phạm vi và câu chưa rõ.
- [ ] Kiểm tra mẫu còn chứa thông tin nhận dạng cá nhân.
- [ ] Rà soát kiến thức, nguồn và điều kiện áp dụng; chỉ duyệt nội dung đủ căn cứ.
- [ ] Thống kê số mẫu được duyệt theo nhãn và nguồn.

### Điều kiện hoàn thành

Có tập câu hỏi đã duyệt, hướng dẫn gán nhãn có phiên bản và kho kiến thức được đánh dấu chấp thuận riêng. Không đặt mục tiêu số mẫu bằng cách tự sinh nhãn chuẩn hoặc đánh dấu duyệt hàng loạt mà không đọc.

## Giai đoạn 2 — Chuẩn bị thí nghiệm

- [ ] Rà soát trùng, gần trùng và nhóm cùng tài liệu.
- [ ] Chốt split theo nhóm, hướng đến khoảng 70/15/15; kiểm tra hỗ trợ từng nhãn.
- [ ] Lưu split_manifest dùng chung cho cả năm mô hình.
- [ ] Chụp phiên bản dữ liệu, bộ nhãn và từ khóa.
- [ ] Chốt thí nghiệm A: TF-IDF; thí nghiệm B: TF-IDF + đặc trưng từ khóa cho mô hình truyền thống.
- [ ] Viết bộ đọc dữ liệu và kiểm tra chỉ nhận mẫu đáp ứng điều kiện train.

### Điều kiện hoàn thành

Không có nhóm bị tách giữa train/validation/test; số mẫu từng nhãn được báo cáo rõ. Nếu không đủ dữ liệu để đánh giá một lớp thì bổ sung dữ liệu hoặc sửa thiết kế có ghi lý do, không bỏ qua âm thầm.

## Giai đoạn 3 — Train bốn mô hình truyền thống

- [ ] Xây TF-IDF và đặc trưng từ khóa với quy trình dùng được khi suy luận.
- [ ] Train Multinomial Naive Bayes.
- [ ] Train Logistic Regression.
- [ ] Train Linear SVM.
- [ ] Train Random Forest.
- [ ] Chọn tham số trên validation theo Macro-F1; phân tích thêm Recall từng lớp.
- [ ] Nếu cần ngưỡng tin cậy, thiết kế riêng theo mô hình và chọn trên validation.
- [ ] Lưu pipeline, cấu hình, dự đoán và báo cáo theo run_id.

### Điều kiện hoàn thành

Có kết quả so sánh thực tế trên cùng split và phiên bản dữ liệu; bộ tạo đặc trưng không fit trên validation/test. Chưa kết luận mô hình tốt nhất chỉ từ một chỉ số trên train.

## Giai đoạn 4 — Fine-tune PhoBERT

- [ ] Kiểm tra cấu hình RAM/GPU và môi trường tương thích.
- [ ] Tách từ, tokenize và đo độ dài câu trước khi chọn max_length.
- [ ] Thêm lớp phân loại, dùng cùng nhãn và split với bốn mô hình còn lại.
- [ ] Chọn epoch, batch size, learning rate và checkpoint bằng validation.
- [ ] Lưu tokenizer, trọng số, ánh xạ nhãn và môi trường train.
- [ ] Đánh giá đủ năm mô hình trên test sau khi khóa lựa chọn cấu hình.

### Điều kiện hoàn thành

Có bảng kết quả đủ năm mô hình và mô hình được chọn theo chất lượng, tốc độ và tài nguyên. Nếu phần PhoBERT chưa chạy thì ghi rõ chưa hoàn thành yêu cầu năm mô hình.

## Giai đoạn 5 — SQLite và truy xuất

- [ ] Tạo bảng datasets, questions, knowledge, keyword_rules và model_runs.
- [ ] Nhập dữ liệu theo ID; bảo toàn chỉnh sửa/phê duyệt khi nhập lại.
- [ ] Tạo chỉ mục TF-IDF riêng từ kiến thức đã duyệt.
- [ ] Tìm nội dung theo câu hỏi, từ khóa và ưu tiên chủ đề.
- [ ] Tạo tập đánh giá truy xuất có tài liệu liên quan được gán nhãn.
- [ ] Chọn top-k/ngưỡng phù hợp bằng tập đánh giá, không lấy tùy ý như kết quả đã kiểm chứng.

### Điều kiện hoàn thành

Truy xuất trả về ID, nội dung, nguồn và mức phù hợp; có luồng không tìm thấy kết quả. Không dùng nhãn dự đoán như bộ lọc cứng duy nhất.

## Giai đoạn 6 — Backend hỏi đáp và LLM diễn đạt

- [ ] Nạp một mô hình phân loại đã chọn, không train lại trong mỗi lượt hỏi.
- [ ] Chuẩn hóa câu và từ khóa, giữ ngữ cảnh phủ định/câu hỏi giả định.
- [ ] Lưu trạng thái câu hỏi đang chờ bổ sung trong phiên.
- [ ] Kết nối Ollama với mô hình phù hợp cấu hình máy.
- [ ] Giới hạn đầu vào LLM vào câu hỏi và nội dung được tìm thấy.
- [ ] Kiểm thử đầu ra giữ nguồn, điều kiện áp dụng, không thêm chẩn đoán hoặc thuốc ngoài nội dung nguồn.
- [ ] Có phương án hiển thị nội dung gốc khi LLM không hoạt động hoặc đầu ra không phù hợp.

### Điều kiện hoàn thành

Luồng có nội dung phù hợp, thiếu thông tin, không có nguồn, lỗi mô hình và lỗi LLM đều có hành vi rõ ràng. Không coi lời nhắc LLM là bảo đảm an toàn tuyệt đối.

## Giai đoạn 7 — Giao diện Streamlit

- [ ] Tab Hỏi đáp: hội thoại, nguồn, trạng thái hỏi bổ sung và bắt đầu phiên mới.
- [ ] Tab Duyệt dữ liệu: xem/sửa nhãn và duyệt nội dung, lưu bền vững.
- [ ] Tab So sánh mô hình: hiển thị kết quả thực tế, support và ma trận nhầm lẫn.
- [ ] Phân biệt thông tin tham khảo với chẩn đoán.
- [ ] Không lưu nội dung hội thoại nhạy cảm vào log mặc định.
- [ ] Có thông báo rõ khi thiếu mô hình, dữ liệu đã duyệt hoặc Ollama.

### Điều kiện hoàn thành

Ứng dụng chạy bằng lệnh Streamlit trên localhost và thực hiện được các thao tác chính. Không hiển thị kết quả demo như điểm số đã đo.

## Giai đoạn 8 — Kiểm thử và báo cáo đồ án

- [ ] Kiểm thử cài đặt từ môi trường mới theo danh sách thư viện đã chốt.
- [ ] Kiểm thử câu có dấu/không dấu, bí danh, lỗi chính tả, nhiều triệu chứng, phủ định và ngoài phạm vi.
- [ ] Kiểm thử hỏi tiếp ngắn và xóa ngữ cảnh khi bắt đầu phiên mới.
- [ ] Kiểm thử chỉnh nhãn, khởi động lại và nhập lại dữ liệu không làm mất bản duyệt.
- [ ] Đánh giá riêng phân loại, truy xuất và câu trả lời cuối.
- [ ] Hoàn thiện báo cáo nguồn dữ liệu, cách gán nhãn, thí nghiệm, hạn chế và hướng phát triển.
- [ ] Chuẩn bị demo và hướng dẫn tái lập; chỉ ghi bước đã chạy thành hoàn thành.

## Thứ tự ưu tiên ngay bây giờ

**Chốt hướng dẫn gán nhãn → duyệt dữ liệu → khóa tập đánh giá → train bốn mô hình truyền thống → PhoBERT → truy xuất/SQLite → LLM diễn đạt → hoàn thiện Streamlit.**

Có thể xây màn hình duyệt dữ liệu sớm nếu người dùng yêu cầu để hỗ trợ bước gán nhãn. Không tự bắt đầu lập trình chỉ vì một mục trong lộ trình đang chưa hoàn thành.

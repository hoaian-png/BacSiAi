# Lộ trình triển khai BacSiAi

Tài liệu cập nhật **28/11/2026**. Dấu `[x]` chỉ việc đã có bằng chứng trong dự án, không đánh dấu hoàn thành theo dự định. Đợt hiện tại chỉ bổ sung tài liệu trên máy, chưa đưa lên Git.

## Giai đoạn 0 — Chuẩn bị dữ liệu và thiết kế

- [x] Chốt Streamlit chạy local, Python và SQLite cho ứng dụng dự kiến.
- [x] Chốt năm mô hình: Naive Bayes, Logistic Regression, Linear SVM, Random Forest, PhoBERT-base-v2.
- [x] Chốt Google Gemini qua Gemini API làm LLM diễn đạt nội dung truy xuất; chưa tích hợp và không train LLM ở giai đoạn đầu.
- [x] Tải ba bộ dữ liệu và lưu nguồn/phiên bản/checksum.
- [x] Chuẩn hóa 63.328 bản ghi thành CSV và JSONL.
- [x] Tạo 3.130 câu hỏi và 1.814 mục kiến thức ứng viên sau lọc/loại trùng.
- [x] Có báo cáo kiểm tra dữ liệu và script kiểm tra lại.
- [x] Viết bộ tài liệu hướng dẫn, kiến trúc và quy ước tại thư mục máy.
- [x] Sắp xếp file vào 7 nhóm theo nội dung đồ án, cập nhật đường dẫn mã và tài liệu; chưa stage, commit hoặc push thay đổi này.

**Chưa hoàn thành:** mở rộng nhãn chuẩn ngoài 70 câu pilot đã được chấp thuận, xử lý 17 câu thảo luận, phê duyệt kiến thức, train mô hình và ứng dụng.

## Giai đoạn 1 — Chốt nhãn và duyệt dữ liệu

### Việc cần làm

- [x] Viết hướng dẫn gán nhãn chủ đề; phân biệt với ý định và thực thể (đã có HUONG_DAN_GAN_NHAN.md v1.1).
- [x] Gán thử một tập nhỏ phủ các chủ đề và câu mơ hồ, thống nhất cách xử lý bất đồng (đã ghi quyết định xử lý cho tập Pilot 120 câu tại `02_du_lieu/filedata/reviewed/annotations/v4_user_accepted_20261128/`: 70 reviewed có nhãn, 33 excluded, 17 needs_discussion).
- [x] Kiểm tra tám nhãn khởi đầu và điều chỉnh trước khi gán toàn bộ.
- [x] Xử lý câu nhiều triệu chứng, phủ định, tiền sử, lỗi chính tả, ngoài phạm vi và câu chưa rõ (đã chuẩn hóa quy tắc truy xuất đa chủ đề và hỏi bổ sung).
- [ ] Mở rộng gán nhãn cho tập dữ liệu lớn từ kho `prepared` để đạt đủ cỡ mẫu cho huấn luyện 5 mô hình (hiện 70 câu pilot reviewed chưa đủ để train/so sánh).
- [ ] Kiểm tra mẫu còn chứa thông tin nhận dạng cá nhân trên tập mở rộng.
- [ ] Rà soát kiến thức, nguồn và điều kiện áp dụng; chỉ duyệt nội dung đủ căn cứ.
- [ ] Thống kê số mẫu được duyệt theo nhãn và nguồn trên tập mở rộng.

### Điều kiện hoàn thành

Có tập câu hỏi đã duyệt, hướng dẫn gán nhãn có phiên bản và kho kiến thức được đánh dấu chấp thuận riêng. Tập dữ liệu sau gán nhãn mở rộng phải đủ mẫu trên từng lớp để chia train/validation/test công bằng. Lưu ý: 70 câu pilot đã duyệt là kết quả người dùng chấp thuận đề xuất AI về chủ đề câu hỏi, không phải chuyên gia y tế xác minh nội dung y khoa, và chưa đủ điều kiện bắt đầu train.

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
- [ ] Thiết kế cơ chế truy xuất đa chủ đề và đa bộ dữ liệu (yêu cầu đã chốt):
  + Hỗ trợ tìm kiếm từ tất cả chủ đề cần thiết đối với câu hỏi so sánh hoặc nhiều chủ đề (như phân biệt cúm và cảm lạnh).
  + Cho phép kết hợp kiến thức được duyệt từ hai hoặc cả ba bộ dữ liệu nguồn (ViMQ, ViHealthQA, ViMedAQA); không bắt buộc phải dùng nhiều nguồn nếu một nguồn đã đủ.
  + Không giới hạn việc tìm kiếm vào một chủ đề duy nhất chỉ vì mô hình phân loại dự đoán một nhãn.
  + Tách rời bài toán phân loại train (đơn nhãn) khỏi truy xuất hỏi đáp (kết hợp linh hoạt).
- [ ] Lưu trạng thái câu hỏi đang chờ bổ sung trong phiên.
- [ ] Tích hợp Gemini API từ backend Python; cấu hình model ID riêng và đọc khóa từ `GEMINI_API_KEY` hoặc secrets local, không đưa khóa lên Git.
- [ ] Xử lý lỗi API, timeout, hạn mức, thiếu khóa và mất mạng; giới hạn dữ liệu câu hỏi/ngữ cảnh gửi tới dịch vụ.
- [ ] Giới hạn đầu vào LLM vào câu hỏi và nội dung được tìm thấy; LLM chỉ tổng hợp và diễn đạt lại nội dung có nguồn.
- [ ] Kiểm thử đầu ra giữ nguồn, điều kiện áp dụng, phủ định, điểm khác biệt; không thêm chẩn đoán, nguyên nhân hoặc thuốc ngoài nội dung nguồn; nêu rõ điểm mâu thuẫn giữa các nguồn nếu có.
- [ ] Có phương án hiển thị nội dung gốc khi LLM không hoạt động hoặc đầu ra không phù hợp.

### Điều kiện hoàn thành

Luồng có nội dung phù hợp, thiếu thông tin, không có nguồn, lỗi mô hình và lỗi LLM đều có hành vi rõ ràng. Không coi lời nhắc LLM là bảo đảm an toàn tuyệt đối.

## Giai đoạn 7 — Giao diện Streamlit

- [ ] Tab Hỏi đáp: hội thoại, nguồn, trạng thái hỏi bổ sung và bắt đầu phiên mới.
- [ ] Tab Duyệt dữ liệu: xem/sửa nhãn và duyệt nội dung, lưu bền vững.
- [ ] Tab So sánh mô hình: hiển thị kết quả thực tế, support và ma trận nhầm lẫn.
- [ ] Phân biệt thông tin tham khảo với chẩn đoán.
- [ ] Không lưu nội dung hội thoại nhạy cảm vào log mặc định.
- [ ] Có thông báo rõ khi thiếu mô hình phân loại, dữ liệu đã duyệt, khóa Gemini API hoặc không kết nối được dịch vụ.

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

## Bước kế tiếp sau pilot đã có quyết định

- [x] Kiểm tra bundle `v4_user_accepted_20261128`: 70 reviewed, 33 excluded, 17 needs_discussion, 0 pending; `annotation_complete = False`.
- [x] Kiểm kê ứng viên mới sau loại ID/group_id pilot và lập phương án đợt 200 câu: xem [báo cáo kiểm kê](../05_bao_cao/kiem_tra_du_lieu/TONG_KET_DUYET_THU_DOT_01.md).
- [ ] Chốt quota và lấy mẫu đợt mở rộng; chưa thực hiện.
- [ ] Duyệt nhãn đợt mở rộng và kiểm tra độc lập chất lượng nhãn.
- [ ] Duyệt kiến thức trước khi xây kho trả lời; 1.814 mục hiện chưa được chấp thuận.

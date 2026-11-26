# Hướng dẫn làm việc trong BacSiAi

## Phạm vi

Tài liệu này hướng dẫn người phát triển và trợ lý lập trình làm việc trong repository. Đây không phải bằng chứng rằng các chức năng đã được triển khai. Yêu cầu trực tiếp của người dùng quyết định phạm vi thay đổi.

## Trạng thái và quyết định đã chốt

- Có ba bộ dữ liệu ViMQ, ViHealthQA, ViMedAQA trong `02_du_lieu/filedata`.
- Giao diện sẽ dùng Streamlit chạy local; không tự chuyển sang Flask, Tkinter hoặc frontend JavaScript riêng.
- Giữ một file giao diện chính `01_ma_nguon/giaodien/app.py` và một file xử lý chính `01_ma_nguon/backend/backend.py`; mã train được tách riêng trong `01_ma_nguon/train`.
- SQLite là lựa chọn lưu trữ ứng dụng; chưa tạo database khi công việc chỉ yêu cầu tài liệu.
- Năm mô hình cần train: Multinomial Naive Bayes, Logistic Regression, Linear SVM, Random Forest, PhoBERT-base-v2.
- LLM chỉ diễn đạt nội dung tìm được; không tính LLM là mô hình thứ năm và không tự triển khai fine-tune LLM.

## Làm đúng phạm vi được yêu cầu

- Khi người dùng yêu cầu kế hoạch, kiểm tra hoặc tài liệu, thực hiện đúng loại công việc đó; không tự tạo ứng dụng, cài môi trường hoặc huấn luyện.
- Không tự stage, commit, push hoặc đồng bộ thay đổi khi công việc chỉ yêu cầu sửa tại máy. Người dùng đã yêu cầu cập nhật cấu trúc và tài liệu lên GitHub ngày 27/11/2026; yêu cầu đó cho phép lần đồng bộ tương ứng, không thay cho chỉ dẫn phạm vi của các công việc sau.
- Không sửa repository tham khảo `DoAn2_Khanh` để thay cho dự án BacSiAi. Đây là bản mẫu cơ khí, chỉ dùng tham khảo kiến trúc khi được yêu cầu.
- Không xóa hoặc ghi đè file người dùng đang chỉnh. Đọc trạng thái Git và nội dung liên quan trước khi sửa.

## Bảo toàn dữ liệu

- Cấu trúc được chia thành 7 nhóm theo bài: mã nguồn, dữ liệu, mô hình, thử nghiệm, báo cáo, tài liệu và nhật ký. Xem `06_tai_lieu/HUONG_DAN_THU_MUC.md` trước khi thêm file để chọn đúng nơi lưu.
- Đường dẫn trong sources.json và raw_location tính từ `02_du_lieu/filedata`, không phải gốc repository.

- Giữ nguyên byte các tệp nguồn trong `02_du_lieu/filedata/raw`; đối chiếu checksum từ `sources.json`.
- Không sửa trực tiếp câu trả lời nguồn để làm cho nó khớp kỳ vọng của mô hình.
- Các đầu ra `normalized` và `prepared` là file sinh tự động. Dữ liệu gán nhãn thủ công phải lưu riêng và có thể xuất lại.
- Giữ nhãn nguồn, nhãn gợi ý và nhãn đã duyệt thành các trường riêng.
- Không dùng `topic_label` tự động như nhãn chuẩn rồi báo cáo đó là chất lượng trên dữ liệu được người gán nhãn.
- Không tự gán ngoài phạm vi chỉ vì câu hỏi không khớp từ điển.
- Không chia bản dịch, câu trùng hoặc câu diễn đạt lại cùng nội dung sang nhiều tập đánh giá.

## Huấn luyện và đánh giá

- Tác vụ chính là phân loại chủ đề. Nhãn ý định là một trục dữ liệu khác, không trộn chung với nhãn chủ đề.
- Giữ dấu tiếng Việt trong dữ liệu chuẩn; quy trình PhoBERT cần tách từ/tokenize riêng.
- TF-IDF và các biến đổi học từ dữ liệu chỉ được fit trên train.
- Chọn cấu hình và ngưỡng trên validation; giữ test độc lập đến lúc đánh giá cuối.
- Lưu mô hình thực sự được đánh giá cùng cấu hình, bộ nhãn và ID chia tập.
- LinearSVC không có sẵn `predict_proba`; không áp dụng máy móc giao diện xác suất của Logistic Regression cho tất cả mô hình.
- Không tạo điểm số giả hoặc kết luận mô hình tốt nhất khi chưa chạy thí nghiệm.

## Hỏi đáp và LLM

- Nhãn chủ đề nói câu hỏi nhắc đến nội dung gì, không phải chẩn đoán.
- Không yêu cầu người dùng phải biết tên bệnh mới được đặt câu hỏi.
- Không tự từ chối mọi câu có nhiều triệu chứng; hỗ trợ đọc ngữ cảnh hoặc hỏi lại.
- Chỉ đưa nội dung đã được chấp thuận vào kho trả lời chính thức; dữ liệu chưa duyệt chỉ xem ở phần nghiên cứu/duyệt dữ liệu.
- Giữ nguồn, điều kiện áp dụng và phủ định khi diễn đạt lại. Thiếu nguồn phù hợp thì hỏi bổ sung hoặc thông báo chưa đủ thông tin.
- Tách lịch sử hiển thị khỏi trạng thái hội thoại; không mặc định lưu nội dung sức khỏe vào cơ sở dữ liệu hoặc log.

## Kiểm tra và bàn giao

- Đối với dữ liệu đã xuất: `python -X utf8 01_ma_nguon/xu_ly_du_lieu/validate_data.py`.
- Đối với thay đổi mã: chạy kiểm tra phù hợp với phần thay đổi; không nói đã kiểm thử web nếu mới kiểm tra cú pháp.
- Đối với tài liệu: kiểm tra liên kết nội bộ và phân biệt đường dẫn hiện có với đường dẫn dự kiến.
- Đọc `06_tai_lieu/PROJECT.md`, `06_tai_lieu/ROADMAP.md` và `06_tai_lieu/QUY_UOC_LUU_TRU.md` trước khi thay đổi thiết kế có liên quan.
- Báo cáo rõ phần đã làm, phần chưa làm và giới hạn thực tế; không ghi bước kế hoạch thành bước hoàn thành.

# Quy ước lưu trữ dữ liệu, mô hình và báo cáo

## 1. Định dạng và mã hóa

- Tài liệu: Markdown `.md`, UTF-8.
- Bản chuẩn cho pipeline: JSONL UTF-8, mỗi dòng là một bản ghi JSON.
- Bản để xem/duyệt bằng Excel: CSV UTF-8 có BOM, đọc bằng thư viện CSV để giữ đúng ô có dấu phẩy hoặc xuống dòng.
- Cấu hình và metadata: JSON UTF-8; giữ tên cột thống nhất bằng snake_case.
- Danh sách/đối tượng trong CSV lưu dưới dạng chuỗi JSON; trong JSONL là kiểu list/object thật.
- Chuỗi trống là chưa có thông tin; không điền câu trả lời hoặc nhãn giả để làm đầy ô.
- Không đổi `.csv`, `.jsonl`, `.json`, `.py`, `.parquet` hay các file `.txt` máy đọc sang `.md`.

CSV được pipeline bảo vệ các ô mở đầu bằng ký tự công thức; JSONL giữ giá trị chuẩn. Chi tiết nằm trong [từ điển dữ liệu](TU_DIEN_DU_LIEU.md).

## 2. Phân tầng dữ liệu

| Tầng | Thư mục | Quy tắc |
|---|---|---|
| Raw | `02_du_lieu/filedata/raw` | Giữ nguyên nguồn và byte tệp; không sửa thủ công |
| Normalized | `02_du_lieu/filedata/normalized` | Chuẩn schema, giữ nguồn và nội dung liên quan |
| Prepared | `02_du_lieu/filedata/prepared` | Ứng viên đã lọc và loại trùng, nhãn còn cần duyệt |
| Reviewed | `02_du_lieu/filedata/reviewed` — dự kiến | Lưu gán nhãn và phê duyệt của người duyệt, không ghi đè prepared |

Pipeline hiện có có thể ghi đè đầu ra normalized/prepared khi chạy lại. Bản duyệt thủ công phải đặt riêng. Không sửa raw để làm cho kiểm tra số lượng hoặc checksum vượt qua.

## 3. ID và truy vết

Giữ `id`, `dataset`, `original_id`, `raw_location`, `source_split` trong dữ liệu chuẩn hóa. ViMQ không có ID từng câu trong file phát hành; ID nguồn được xác định theo split và thứ tự bản ghi.

- `source_url`: URL bài viết/câu trả lời, để trống nếu nguồn không cung cấp.
- `source_record_id`: liên kết mục kiến thức với bản ghi chuẩn hóa.
- `provenance_ids`: giữ các nguồn của câu hỏi đã gộp do trùng chính xác.
- `question_group_id`: nhóm câu hỏi giống nhau sau chuẩn hóa.
- `group_id`: nhóm liên thông từ câu trùng và cùng URL tài liệu.

Chỉ số thực thể ViMQ là tọa độ token trong câu nguồn, điểm cuối bao gồm. Chỉ số khớp từ khóa bổ sung là tọa độ ký tự trên câu normalized, điểm cuối không bao gồm. Không dùng hai loại tọa độ thay thế nhau.

## 4. Ba loại nhãn phải tách riêng

| Loại | Trường | Cách sử dụng |
|---|---|---|
| Nhãn gốc | source_intent_label, source_topic, source_entities | Bảo toàn ý nghĩa do nguồn công bố |
| Nhãn gợi ý | topic_candidates, topic_label, topic_label_method | Hỗ trợ người gán nhãn, chưa phải nhãn chuẩn |
| Nhãn đã duyệt | gold_topic_label, review_status | Chỉ dùng làm đích train sau xác nhận |

Nhãn ý định không thay cho nhãn chủ đề. Từ khóa có mặt trong câu không mặc nhiên là triệu chứng đang hiện diện: có thể là phủ định, tiền sử, giả định hoặc câu hỏi chung.

## 5. Bản gán nhãn dự kiến

Tên file đề xuất sau khi bắt đầu duyệt:

```text
02_du_lieu/filedata/reviewed/questions_reviewed.csv
02_du_lieu/filedata/reviewed/knowledge_reviewed.jsonl
02_du_lieu/filedata/reviewed/review_manifest.json
```

Những file này **chưa được tạo**. Bản câu hỏi nên giữ ID gốc, câu hỏi và nhãn gợi ý, bổ sung `gold_topic_label`, `review_status`, `reviewer_id`, `reviewed_at`, `review_note`.

Trạng thái đề xuất: `pending_manual_review`, `reviewed`, `needs_discussion`, `excluded`. Không tự suy ra reviewed từ việc ô nhãn không trống. Câu ngoài phạm vi hoặc không rõ cần được xử lý theo hướng dẫn gán nhãn đã chốt.

*Lưu ý về quan hệ giữa nhãn train và truy xuất hỏi đáp:* Nhãn `gold_topic_label` là nhãn mục tiêu cho bài toán phân loại đơn nhãn của mô hình train. Đối với các câu hỏi đa chủ đề hoặc so sánh (như phân biệt cúm và cảm lạnh), khi chưa chốt nhãn phân loại đơn nhãn thì câu có thể giữ trạng thái `needs_discussion` (nhãn chuẩn để trống và chưa đưa vào tập train); điều này không ngăn cản việc hệ thống hỏi đáp sau này truy xuất kết hợp từ nhiều nhóm chủ đề hoặc nhiều bộ dữ liệu nguồn để trả lời người dùng.

Kiến thức cần giữ bản nguồn và phần nội dung chấp thuận riêng nếu có biên tập; ghi lý do, người duyệt và thời điểm. Chỉ bật `approved_for_rag` khi nội dung và nguồn đã được kiểm tra. Bản đã chỉnh không được giả làm nguyên văn nguồn.

## 6. Phiên bản và cách chia tập

- Raw: truy vết bằng URL phiên bản, revision và SHA-256 trong `sources.json`.
- Config nhãn/từ khóa: chụp bản config sử dụng cho từng thí nghiệm.
- Reviewed: ghi checksum file và số lượng từng nhãn sau khi duyệt.
- Split: lưu danh sách ID, group_id và train/validation/test trong `split_manifest.csv`.
- Bản split manifest chính của mỗi run đặt tại `04_thu_nghiem/phan_chia_du_lieu/<run_id>/`; báo cáo có thể giữ bản chụp để tái lập. Cấu hình chính đặt tại `04_thu_nghiem/cau_hinh/`.
- Giữ các nhóm có liên hệ trong cùng tập. Quy trình hiện có xử lý trùng chính xác và cùng URL; câu gần trùng, diễn đạt lại và URL khác nhau cùng nội dung cần rà soát thêm.
- `source_split` là phân chia của nguồn, `split_suggested` là gợi ý của pipeline. Sau duyệt cần hoàn thiện split dùng cho thí nghiệm; không trộn hai khái niệm.
- Cùng một manifest chia tập được dùng cho cả năm mô hình.

## 7. Lưu mô hình

Cấu trúc dự kiến:

```text
03_mo_hinh/<run_id>/
  naive_bayes.joblib
  logistic_regression.joblib
  linear_svm.joblib
  random_forest.joblib
  phobert/
  metadata.json
03_mo_hinh/active_model.json
```

Pipeline truyền thống gồm TF-IDF, bộ tạo đặc trưng bổ sung nếu có và classifier. PhoBERT lưu trọng số, tokenizer và ánh xạ id2label/label2id. Không tải file joblib/pickle từ nguồn không tin cậy.

Metadata cần có: tên mô hình, thời điểm train, phiên bản Python/thư viện, seed, tham số, checksum dữ liệu đã duyệt, phiên bản nhãn/từ khóa, split manifest và kết quả đánh giá.

`active_model.json` chỉ trỏ đến mô hình được chọn, không thay thế báo cáo đánh giá. Nếu refit mô hình phục vụ triển khai sau thí nghiệm, lưu thành artifact mới và ghi rõ khác với checkpoint đã được đo trên test.

Chỉ mục truy xuất có artifact và metadata riêng vì nó dùng kho kiến thức, không phải bộ vectorizer phân loại. Khi nội dung/ trạng thái duyệt thay đổi phải cập nhật chỉ mục.

## 8. Lưu báo cáo mô hình

Dùng `05_bao_cao/BaoCaoSoSanh/<run_id>/`, ví dụ run_id `20261127_140000_baseline` chỉ là minh họa cách đặt tên, không phải một lần train đã thực hiện.

Các file dự kiến:

- `config.json`: tham số thực tế.
- `data_manifest.json`: phiên bản và checksum dữ liệu.
- `split_manifest.csv`: ID và cách chia tập.
- `metrics.csv`: bảng so sánh mô hình, tách validation và test.
- `classification_report.json`: chỉ số từng nhãn và support.
- `confusion_matrix.png`: ma trận nhầm lẫn có tên nhãn rõ ràng.
- `predictions.csv`: ID, nhãn chuẩn, nhãn dự đoán để phân tích lỗi.
- `07_nhat_ky/chuong_trinh/<run_id>/training.log`: quá trình train, không ghi dữ liệu cá nhân không cần thiết.

Không ghi số liệu ví dụ vào báo cáo thật. File chưa có kết quả phải thể hiện chưa chạy, không ghi 0% như thể đã đo.

## 9. SQLite và dữ liệu nhạy cảm

SQLite tại `02_du_lieu/database/medical.db` là kế hoạch, chưa có file DB trong đợt này. DB phục vụ đọc, duyệt và truy vấn; raw và manifest vẫn là nguồn truy vết độc lập. Thao tác nhập lại phải bảo toàn các nhãn/phê duyệt đã sửa thủ công.

Dữ liệu raw/normalized chưa được ẩn danh đầy đủ. Che mẫu email/số điện thoại ở prepared là bước hỗ trợ, không bảo đảm loại hết tên, địa chỉ hoặc thông tin nhận dạng. Không mặc định xuất lịch sử sức khỏe người dùng vào log, Git hoặc dữ liệu train.

## 10. Git và kiểm tra

- Hiện chỉ tạo sáu tài liệu tại máy; chưa stage, commit hay push.
- Không đưa `.venv`, `01_ma_nguon/.data-tools`, cache, secrets và runtime log vào Git.
- Với trọng số/dữ liệu lớn phát sinh sau này, chọn nơi lưu phù hợp và giữ manifest thay vì tự đẩy mọi file lên repository.
- Nếu thay đổi thuộc tính line ending của Git, bảo toàn raw để không làm sai checksum.
- Kiểm tra file dữ liệu bằng `python -X utf8 01_ma_nguon/xu_ly_du_lieu/validate_data.py` khi có thay đổi liên quan. Không cần chạy lại toàn bộ pipeline dữ liệu chỉ vì sửa Markdown.

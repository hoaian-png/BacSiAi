# Dữ liệu cho đồ án hỏi đáp tai mũi họng

Ngày chuẩn bị: **26/11/2026**, múi giờ Việt Nam.

## Kết quả đã thực hiện

Đã tải đúng 3 bộ dữ liệu công khai từ kho của nhóm công bố; giữ nguyên các tệp gốc và chuẩn hóa **63.328 bản ghi**. Đã tạo thêm tập ứng viên tai mũi họng, ho, sốt, cảm lạnh và cúm để tiếp tục gán nhãn.

| Bộ dữ liệu | Tổng bản ghi | Train gốc | Validation gốc | Test gốc | Bản ghi khớp bộ lọc chủ đề |
|---|---:|---:|---:|---:|---:|
| ViMQ | 9.000 | 7.000 | 1.000 | 1.000 | 907 |
| ViHealthQA | 10.015 | 7.009 | 993 | 2.013 | 1.096 |
| ViMedAQA | 44.313 | 39.881 | 2.215 | 2.217 | 1.533 |
| Tổng | 63.328 | 53.890 | 4.208 | 5.230 | 3.536 |

Sau khi loại câu hỏi trùng chính xác theo văn bản chuẩn hóa: **3.130 câu hỏi ứng viên**. Kho kiến thức ứng viên có **1.814 mục** sau khi loại trùng theo nội dung và URL nguồn. Hai con số này đo hai loại dữ liệu khác nhau, không phải cặp một-một.

**Chưa có nhãn chủ đề do người kiểm duyệt xác nhận.** Nhãn chủ đề và từ khóa bổ sung hiện được tạo bằng quy tắc, phải xem là gợi ý. Không có huấn luyện mô hình, xây web hay gọi LLM trong bước này.

## Mở file nào trước?

1. `02_du_lieu/filedata/prepared/questions_ent.csv`: mở bằng Excel để xem câu hỏi, từ khóa và nhãn chủ đề gợi ý; điền nhãn đã duyệt vào `gold_topic_label`.
2. `02_du_lieu/filedata/prepared/knowledge_ent.csv`: xem câu hỏi, câu trả lời hoặc đoạn tài liệu dùng làm ứng viên cho kho truy xuất.
3. `05_bao_cao/kiem_tra_du_lieu/summary.json`: thống kê thực tế và kết quả kiểm tra.
4. `02_du_lieu/filedata/config/labels.json` và `02_du_lieu/filedata/config/keywords.csv`: danh mục nhãn và từ điển từ khóa đang áp dụng.

CSV dùng UTF-8 có BOM để Excel đọc tiếng Việt. JSONL dùng UTF-8; mỗi dòng là một đối tượng JSON. Các trường danh sách trong CSV được lưu dạng chuỗi JSON, ví dụ `["ho","đờm vàng"]`; trong Python đọc bằng `json.loads()`.

## Cấu trúc sau khi sắp xếp theo tầng

```text
01_ma_nguon/xu_ly_du_lieu/       prepare_data.py, validate_data.py, requirements-data.txt
02_du_lieu/filedata/            raw, normalized, prepared, config, sources.json
05_bao_cao/kiem_tra_du_lieu/     summary.json, validation.json và các bảng thống kê
06_tai_lieu/                    DU_LIEU.md, TU_DIEN_DU_LIEU.md
```

Các đường dẫn trong hướng dẫn chạy lệnh tính từ gốc dự án. Các giá trị `path` trong `sources.json` và `raw_location` trong bản ghi vẫn tính từ `02_du_lieu/filedata`; không thay đổi các bản ghi chỉ vì di chuyển thư mục.

PyArrow là thư viện đọc Parquet. Thư viện cục bộ hiện đặt tại `01_ma_nguon/.data-tools`, được loại khỏi Git; không phải một bộ dữ liệu hay mô hình đã train.

## Nguồn dữ liệu và điều kiện sử dụng

### ViMQ

- Nguồn chính thức: https://github.com/tadeephuy/ViMQ
- Bài báo: https://arxiv.org/abs/2304.14405
- Phiên bản đã tải: `b35341cd506f012a4d868674210c532d5a771063`.
- Giữ cả `train.json`, `dev.json`, `test.json`, `entity_set.txt`, `char2index.json`.
- `dev` được chuẩn tên thành `validation`; không tự chia lại dữ liệu gốc.
- Có nhãn ý định và thực thể, **không có câu trả lời trong các tệp dữ liệu phát hành đã tải**. Không tạo câu trả lời giả để điền chỗ trống.
- Nhãn `method_diagnosis` được ánh xạ tên thành `diagnosis`; nhãn gốc còn trong `source_intent_label`.
- Chưa thấy giấy phép dữ liệu rõ ràng trong kho đã tải. Giữ trích dẫn, kiểm tra quyền sử dụng trước khi tái phân phối; giấy phép của bài báo không mặc nhiên là giấy phép dữ liệu.

### ViHealthQA

- Nguồn chính thức: https://huggingface.co/datasets/tarudesu/ViHealthQA
- Bài báo: https://arxiv.org/abs/2206.09600
- Phiên bản đã tải: `d90a62deedfc822a15de3f35535bb41474e4d3f4`.
- Có `question`, `answer`, `link`; chưa có nhãn chủ đề/từ khóa theo thiết kế đồ án.
- **Số lượng thực tế:** `train.csv` 7.009; `val.csv` 993; `test.csv` 2.013. Mô tả trên trang dữ liệu nêu số validation/test khác; pipeline tuân theo tên và nội dung tệp thực tế, không đảo các tập theo mô tả.
- README gốc yêu cầu chỉ dùng cho nghiên cứu và lọc thông tin cá nhân. Chưa có mã giấy phép chuẩn rõ ràng trong metadata; không tự gán giấy phép mới.

### ViMedAQA

- Nguồn chính thức: https://huggingface.co/datasets/tmnam20/ViMedAQA
- Bài báo: https://aclanthology.org/2024.acl-srw.31/
- Phiên bản đã tải: `1b36d77118a7eb5a64d94be33d3b672dea45b989`.
- Tải đủ cấu hình **all**, gồm train/validation/test. Các cấu hình body-part/disease/drug/medicine là các tập con của all; không tải lại để cộng trùng dữ liệu.
- Có câu hỏi, câu trả lời, ngữ cảnh, từ khóa nguồn, nhóm chủ đề tổng quát và URL bài viết.
- Câu hỏi/câu trả lời được tạo với hỗ trợ LLM rồi người gán nhãn rà soát theo quy trình bài báo; không mô tả tất cả là hội thoại trực tiếp với bác sĩ.
- Bài báo, phụ lục B, nêu điều kiện Creative Commons NonCommercial 4.0 và sử dụng phi thương mại. Kho tải về không kèm file LICENSE riêng; xem bài báo và điều kiện nguồn trước khi phân phối.
- 85 bản ghi không có `context`; giữ trống và dùng `answer` làm nội dung ứng viên nếu bản ghi thuộc phạm vi lọc.

## Các bước chuẩn hóa

1. Lưu nguyên byte tệp gốc trong `raw`; lưu URL phiên bản cụ thể và SHA-256 trong `sources.json`.
2. Chuẩn Unicode NFC, giải mã HTML entities, bỏ thẻ HTML có cấu trúc, gộp khoảng trắng. Giữ dấu tiếng Việt, chữ số và thứ tự từ.
3. Riêng ViMQ: thay dấu gạch dưới phân tách từ bằng khoảng trắng, nối lại dấu câu đã tách token. Tọa độ thực thể gốc vẫn là chỉ số token trên `sentence` gốc; điểm cuối **bao gồm** token cuối.
4. Đưa ba nguồn về cùng schema; trường không có thì để trống, không suy diễn dữ liệu nguồn.
5. Tìm từ khóa theo ranh giới từ, không phân biệt hoa/thường. Giữ cụm dài nhất nếu các khớp cùng chủ đề lồng nhau. Không bỏ dấu toàn bộ văn bản, không tự dịch và không tự sửa mọi lỗi chính tả.
6. Chỉ lấy từ trong câu hỏi làm `keywords` và nhãn chủ đề gợi ý. Dùng thêm `title` hoặc `source_keyword` để lọc ứng viên khi câu hỏi chưa nêu trực tiếp tên chủ đề; lưu rõ `scope_evidence`.
7. Không tìm từ khóa trong câu trả lời để gán nhãn cho câu hỏi, nhằm tránh dùng thông tin đích làm đầu vào.
8. Nhận diện thô các từ phủ định/đã giảm gần từ khóa để đánh dấu cần duyệt; không dùng nó làm kết luận triệu chứng hiện diện hay vắng mặt.
9. Phát hiện câu hỏi trùng bằng cách đưa về chữ thường, chuẩn dấu câu và khoảng trắng, vẫn giữ dấu tiếng Việt. Giữ mọi bản ghi trong normalized; chỉ loại trùng ở prepared và lưu `provenance_ids`.
10. Tạo nhóm theo câu hỏi trùng và URL tài liệu giống nhau để gợi ý chia tập. Tập gốc vẫn được giữ nguyên ở `source_split`.

## Nhãn và từ khóa: cách sử dụng

- `source_intent_label`: nhãn ý định do nguồn ViMQ cung cấp.
- `intent_label`: tên nhãn ý định đã chuẩn hóa; nguồn khác để trống, không tự đoán.
- `source_entities`: thực thể gốc do ViMQ gán nhãn, gồm cả loại thuốc/thủ thuật; không đồng nghĩa tất cả là triệu chứng.
- `source_keyword`: từ khóa gốc của ViMedAQA; không đồng nghĩa có đủ mọi từ khóa của câu hỏi.
- `keywords`: các cụm từ thực sự xuất hiện trong câu hỏi chuẩn hóa, do từ điển của dự án trích ra.
- `topic_candidates`: tất cả chủ đề được gợi ý bởi từ khóa câu hỏi.
- `topic_label`: chỉ điền khi có đúng một chủ đề gợi ý; vẫn là nhãn tự động chưa duyệt.
- `gold_topic_label`: để người gán nhãn điền sau khi đọc và xác nhận. Hiện để trống toàn bộ.

Không tự gán nhãn `ngoai_pham_vi` khi không thấy từ khóa. Một câu hỏi có thể liên quan dù dùng cách diễn đạt chưa có trong từ điển. Các ứng viên chỉ có sốt cũng có thể ngoài phạm vi tai mũi họng cuối cùng, cần loại khi duyệt.

Để bắt đầu gán nhãn, sao chép `02_du_lieu/filedata/prepared/questions_ent.csv` thành một file mới, chẳng hạn `questions_ent_reviewed.csv`, rồi chỉnh `gold_topic_label` và `review_status`. **Không chỉnh file sinh tự động rồi chạy lại pipeline**, vì pipeline sẽ ghi đè kết quả sinh trước đó. Giữ nhãn nguồn riêng và không biến nhãn chủ đề thành chẩn đoán.

## Chia tập và tránh rò rỉ

- `source_split` chỉ ghi phân chia do bộ dữ liệu gốc phát hành.
- `split_suggested` là gợi ý mới bằng hash của nhóm, mục tiêu gần 70/15/15: 2.196 train, 475 validation, 459 test trong tập câu hỏi đã lọc.
- Các câu hỏi trùng chính xác hoặc cùng URL nguồn được liên kết trong cùng một `group_id`; không có nhóm xuất hiện ở hai tập gợi ý khác nhau.
- Đây chưa phải chia tập phân tầng theo nhãn. Câu gần giống, diễn đạt lại, URL khác nhau nhưng cùng bài gốc còn cần rà soát.
- Không đưa `topic_label`, `gold_topic_label`, `intent_label`, câu trả lời hoặc `source_entities` gán tay vào đầu vào của mô hình phân loại câu hỏi tại test. Nếu dùng từ khóa làm đặc trưng, chạy cùng quy trình trích từ câu hỏi cho cả train và test.
- Với thí nghiệm RAG, chỉ mục nên chứa tài liệu nguồn đã được chấp thuận, không đưa câu trả lời chuẩn của bộ test vào như tài liệu để rồi báo cáo đó là khả năng tổng quát hóa.

## Thông tin cá nhân và nội dung y tế

`raw` và `normalized` là dữ liệu nghiên cứu cục bộ, chưa ẩn danh hoàn toàn. Tập prepared che email và chuỗi giống số điện thoại bằng `[EMAIL]` và `[PHONE]`; đây là quy tắc thô, có thể bỏ sót hoặc che nhầm. Tên, địa chỉ và thông tin nhận dạng khác vẫn cần duyệt.

Tọa độ từ khóa/thực thể trong prepared tham chiếu câu hỏi normalized **trước khi che thông tin liên hệ**, được ghi rõ ở `annotation_reference`.

`knowledge_ent` là kho **ứng viên**, tất cả `approved_for_rag=false`. Nội dung chưa được kiểm duyệt y khoa hoặc cập nhật tính hiện hành; không dùng trực tiếp như chỉ dẫn điều trị cho người dùng cuối.

## Chạy lại

Từ thư mục gốc dự án, dùng Python 3.11 trở lên:

```powershell
python -m pip install --target 01_ma_nguon/.data-tools -r 01_ma_nguon/xu_ly_du_lieu/requirements-data.txt
python -X utf8 01_ma_nguon/xu_ly_du_lieu/prepare_data.py --offline
```

Lệnh `--offline` dùng lại raw đã tải. Nếu bỏ `--offline`, script truy vấn phiên bản hiện tại của nguồn và tải lại trước khi chuẩn hóa; manifest sẽ ghi phiên bản mới. Không chạy lại khi chưa sao lưu các chỉnh sửa thủ công.

Kiểm tra lại các file đã xuất mà không cần PyArrow:

```powershell
python -X utf8 01_ma_nguon/xu_ly_du_lieu/validate_data.py
```

Đã kiểm tra: số lượng cả ba nguồn, ID duy nhất, SHA-256 bản gốc, tọa độ ký tự từ khóa, tính nhất quán nhóm chia tập và dữ liệu CSV khớp JSONL. Kết quả chi tiết nằm trong `05_bao_cao/kiem_tra_du_lieu/summary.json` và `05_bao_cao/kiem_tra_du_lieu/validation.json`.

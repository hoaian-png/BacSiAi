# Từ điển dữ liệu

## Quy ước chung

- JSONL là bản chuẩn cho Python; CSV là bản dễ xem và duyệt bằng Excel.
- Chuỗi trống `""` là không có dữ liệu/không gán; danh sách trống `[]` là không có phần tử.
- Danh sách/đối tượng trong CSV được lưu bằng chuỗi JSON. Không tách cột bằng dấu phẩy bên trong dữ liệu bằng tay; dùng `csv.DictReader`.
- CSV thêm dấu nháy đơn trước ô bắt đầu bằng `=`, `+`, `-`, `@` để Excel không thực thi như công thức. JSONL không thay đổi các giá trị này.

## normalized: ba nguồn dùng cùng schema

| Cột | Kiểu JSON | Ý nghĩa |
|---|---|---|
| id | string | Mã duy nhất: dataset:source_split:original_id |
| dataset | string | ViMQ, ViHealthQA hoặc ViMedAQA |
| original_id | string | ID nguồn; riêng ViMQ là số thứ tự bản ghi trong split, bắt đầu 1 |
| source_split | string | train/validation/test theo tệp nguồn; dev/val đổi tên thành validation |
| raw_location | string | File và số thứ tự bản ghi gốc, không phải số dòng vật lý của CSV nhiều dòng |
| question | string | Câu hỏi đã chuẩn Unicode, HTML và khoảng trắng |
| answer | string | Câu trả lời nguồn; ViMQ không có nên để trống |
| context | string | Ngữ cảnh ViMedAQA; nguồn không có thì để trống |
| title | string | Tiêu đề mục nguồn của ViMedAQA |
| source_url | string | URL tài liệu/câu trả lời; ViMQ phát hành không có URL từng câu |
| source_topic | string | Nhãn tổng quát ViMedAQA: body-part/disease/drug/medicine |
| source_intent_label | string | Nhãn nguyên gốc ViMQ: method_diagnosis/treatment/severity/cause |
| intent_label | string | Chuẩn method_diagnosis thành diagnosis; các nhãn khác giữ nguyên |
| source_keyword | string | Từ khóa gốc ViMedAQA; không phải nhãn tự tạo |
| source_entities | array[object] | Thực thể gốc ViMQ: text/type/source_token_start/source_token_end_inclusive |
| author | string | Tác giả tài liệu gốc ViMedAQA |
| author_url | string | Trang tác giả gốc ViMedAQA |
| keywords | array[string] | Cụm từ xuất hiện trong question, được khớp bằng config/keywords.csv |
| keyword_matches | array[object] | Chi tiết khớp: surface/canonical/topic/start/end/negation_or_resolution_hint |
| topic_candidates | array[string] | Các chủ đề được gợi ý từ từ khóa của question |
| topic_label | string | Một nhãn gợi ý nếu topic_candidates có đúng 1 nhãn; ngược lại để trống |
| topic_label_method | string | keyword_rule_suggestion hoặc unassigned; không phải nhãn đã duyệt |
| scope_status | string | ent_candidate khi câu hỏi/tiêu đề/từ khóa nguồn khớp; no_keyword_match nếu chưa khớp |
| scope_evidence | array[string] | question/title/source_keyword: trường thực sự dùng làm bằng chứng lọc |
| negation_review_required | boolean | Có dấu hiệu phủ định/giảm triệu chứng gần từ khóa; cần đọc lại câu |
| gold_topic_label | string | Nhãn chủ đề được người duyệt xác nhận; hiện để trống |
| review_status | string | Hiện pending_manual_review; chỉ đổi sau khi duyệt |
| privacy_status | string | Có chuỗi giống thông tin liên hệ hoặc chưa được ẩn danh đầy đủ |
| question_group_id | string | Hash nhóm câu hỏi giống nhau sau chuẩn hóa, không phải nhóm cùng bệnh |
| group_id | string | Nhóm liên thông từ câu hỏi trùng và URL tài liệu giống nhau |
| split_suggested | string | Gợi ý chia tập từ group_id, không thay source_split |
| duplicate_of | string | ID bản ghi câu hỏi giống nhau đã xuất hiện trước đó; không tự xóa bản ghi |

`keyword_matches.start/end` là chỉ số ký tự của Python trên question normalized; start bao gồm, end không bao gồm. Có thể kiểm tra bằng `question[start:end] == surface`.

`source_entities` dùng chỉ số token của **sentence ViMQ gốc có dấu gạch dưới**, điểm cuối bao gồm. Không dùng trực tiếp những chỉ số này như tọa độ ký tự trên question normalized.

## prepared/questions_ent

Giữ các cột liên quan câu hỏi, nhãn và từ khóa của normalized; không chứa answer/context để tránh vô tình đưa đáp án vào mô hình phân loại. Chỉ giữ một câu hỏi cho mỗi question_group_id.

Cột bổ sung:

| Cột | Ý nghĩa |
|---|---|
| annotation_reference | Tọa độ khớp từ khóa/thực thể tham chiếu câu normalized trước che email/số điện thoại |
| provenance_ids | ID tất cả bản ghi normalized có cùng câu hỏi chuẩn hóa; dùng truy lại các nguồn |

Nhãn gợi ý và từ khóa theo câu đại diện được giữ, không trộn tự động nhãn nguồn khác nhau. Tham khảo provenance_ids khi cần đối chiếu.

## prepared/knowledge_ent

| Cột | Ý nghĩa |
|---|---|
| id | ID mục kiến thức, hash theo URL nguồn và nội dung |
| source_record_id | ID normalized tạo mục này |
| dataset | Bộ dữ liệu nguồn |
| question | Câu hỏi nguồn, đã che mẫu email/số điện thoại |
| answer | Câu trả lời nguồn, đã che mẫu liên hệ |
| context | Ngữ cảnh nguồn nếu có, đã che mẫu liên hệ |
| text | context nếu có, nếu không dùng answer; chưa chia nhỏ thành chunk |
| text_origin | context hoặc answer |
| title | Tiêu đề nguồn nếu có |
| source_url | URL nguồn |
| source_keyword | Từ khóa nguồn nếu có |
| topic_candidates | Chủ đề gợi ý của câu hỏi, không phải nhãn đã duyệt cho toàn bộ tài liệu |
| group_id | Nhóm của bản ghi nguồn |
| split_suggested | Gợi ý chia tập của bản ghi nguồn |
| review_status | pending_medical_and_privacy_review |
| approved_for_rag | Hiện false cho toàn bộ, chỉ bật sau khi kiểm duyệt |

## Cách duyệt một câu hỏi

1. Đọc question và đối chiếu raw_location khi có điểm khó hiểu.
2. Kiểm tra từ khóa có đúng cụm từ đang được hỏi không; xem cả phủ định, tiền sử và câu hỏi giả định.
3. Chọn chủ đề chính theo ý định hỏi. Nếu chưa rõ, giữ trống gold_topic_label và ghi nhận cần thảo luận.
4. Không suy ra người hỏi mắc bệnh chỉ từ việc có nhắc từ khóa.
5. Điền gold_topic_label bằng một mã trong config/labels.json, rồi đổi review_status thành reviewed nếu đã duyệt xong.
6. Với câu ngoài phạm vi, cần thống nhất bổ sung nhãn ngoài phạm vi trong config trước khi sử dụng để huấn luyện; không tự biến mọi câu không khớp từ khóa thành ngoài phạm vi.

Từ điển có 8 nhãn khởi đầu, có thể còn thiếu nhóm hoặc từ khóa. Mở rộng có kiểm soát và giữ phiên bản config khi làm thí nghiệm.

# Báo cáo tổng kết duyệt thử đợt 1 (20 câu pilot)

Phiên bản: **1.0 (Hoàn thành đợt duyệt 20 câu ưu tiên)**  
Ngày cập nhật: **28/11/2026**  
Người thực hiện duyệt: **hoai_an** (ID người duyệt)  
Dự án: **BacSiAi (Tai Mũi Họng)**  
Tài liệu tham chiếu: [HUONG_DAN_GAN_NHAN.md](../../06_tai_lieu/HUONG_DAN_GAN_NHAN.md), [PHIEU_DUYET_THU_20_CAU.md](../../06_tai_lieu/PHIEU_DUYET_THU_20_CAU.md), [review_batch_01.json](../../02_du_lieu/filedata/reviewed/working/review_batch_01.json).

> [!NOTE]
> Báo cáo này ghi nhận kết quả duyệt thực tế của người duyệt (**hoai_an**) cho toàn bộ 20 câu ưu tiên đợt 1 trên tệp làm việc `questions_working.csv`.

---

## 1. Thống kê tiến độ thực hiện

> [!IMPORTANT]
> **Quy ước thống kê:**
> - Bảng A tính trên mẫu số **20 câu** của đợt 1 ([review_batch_01.json](../../02_du_lieu/filedata/reviewed/working/review_batch_01.json)).
> - Bảng B tính trên mẫu số **120 câu** của toàn bộ tập pilot trên tệp `questions_working.csv`.
> - Việc hoàn thành duyệt 20 câu đợt 1 chưa đồng nghĩa với hoàn thành toàn bộ tập pilot 120 câu.

### Bảng A: Kết quả đợt 1 — 20 câu ưu tiên (Mẫu số = 20)

| Trạng thái (`review_status`) | Số lượng câu | Tỷ lệ (%) | Ghi chú |
| :--- | :---: | :---: | :--- |
| `reviewed` (Đã xác định nhãn chuẩn) | **12** | **60.0%** | Đã chốt đúng 1 trong 8 nhãn TMH |
| `needs_discussion` (Cần thảo luận/hội chẩn) | **1** | **5.0%** | Câu 15 (so sánh cúm và cảm lạnh, chưa chốt nhãn train; hỏi đáp dùng 2 nhóm) |
| `excluded` (Loại khỏi tập huấn luyện) | **7** | **35.0%** | Câu 09, 10, 16, 17, 18, 19, 20 (ngoài phạm vi TMH / tiêm chủng / câu hỏi lý thuyết) |
| `pending_manual_review` (Chưa xử lý trong đợt 1) | **0** | **0.0%** | Cả 20 câu đợt 1 đã được xử lý xong |
| **Tổng số câu trong đợt 1** | **20** | **100%** | Đã hoàn tất xử lý 20/20 câu đợt 1 |

### Bảng B: Tiến độ tập pilot tại thời điểm kết thúc đợt 1 *(Số liệu lịch sử đợt 1)*

*(Ghi nhận lịch sử khi mới duyệt xong 20 câu đầu, 100 câu còn lại chưa xử lý)*

| Trạng thái (`review_status`) | Số lượng câu | Tỷ lệ (%) | Ghi chú lịch sử |
| :--- | :---: | :---: | :--- |
| `reviewed` (Đã xác định nhãn chuẩn) | **12** | **10.0%** | 12 câu chốt trong đợt 1 |
| `needs_discussion` (Cần thảo luận/hội chẩn) | **1** | **0.8%** | Câu 15 chờ thống nhất quy tắc đơn nhãn |
| `excluded` (Loại khỏi tập huấn luyện) | **7** | **5.8%** | 7 câu đã loại trong đợt 1 |
| `pending_manual_review` (Chưa xử lý) | **100** | **83.3%** | 100 câu ngoài đợt 1 lúc đó đang chờ duyệt |
| **Tổng số câu toàn bộ pilot** | **120** | **100%** | Quy mô toàn bộ tập pilot |

### Bảng C: Kết quả toàn bộ tập pilot sau khi người dùng duyệt xong 100 câu đợt 2 *(Số liệu hiện tại)*

*(Phiên bản xuất bản: `02_du_lieu/filedata/reviewed/annotations/v4_user_accepted_20261128/`)*

| Trạng thái (`review_status`) | Đợt 1 (20 câu) | Đợt 2 (100 câu) | Toàn bộ Pilot (120 câu) | Tỷ lệ toàn bộ (%) | Ghi chú hiện tại |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `reviewed` (Có nhãn chuẩn) | 12 | 58 | **70** | **58.3%** | Người dùng chấp thuận nhãn AI đề xuất |
| `needs_discussion` (Cần thảo luận) | 1 | 16 | **17** | **14.2%** | Nhãn chuẩn để trống, không dùng train |
| `excluded` (Loại khỏi TMH) | 7 | 26 | **33** | **27.5%** | Câu ngoài phạm vi chuyên khoa TMH |
| `pending_manual_review` (Chưa duyệt) | 0 | 0 | **0** | **0.0%** | Đã hoàn tất 120/120 câu pilot |
| **Tổng cộng** | **20** | **100** | **120** | **100%** | Toàn bộ tập pilot đã có quyết định |

> [!NOTE]
> **Bản chất kết quả duyệt:** Đây là việc người dùng (**hoai_an**) chấp thuận đề xuất của AI về chủ đề câu hỏi trên tập pilot, hoàn toàn **không phải chuyên gia y tế đã xác minh nội dung y khoa**. Đồng thời, 70 câu có nhãn chỉ là bước kiểm nghiệm quy trình pilot, **chưa đủ điều kiện để huấn luyện hoặc so sánh 5 mô hình** mà cần mở rộng gán nhãn ở giai đoạn tiếp theo.

---

## 2. Giải thích trạng thái sẵn sàng huấn luyện và cờ hoàn thành

Theo kết quả kiểm tra tự động (`validate_pilot.py --mode annotated` trên `v4_user_accepted_20261128`):
1. **`annotation_complete = False`:** Không còn câu `pending_manual_review`, nhưng vẫn có 17 câu `needs_discussion` chưa chốt nhãn. Đã ghi quyết định xử lý cho 120 câu không đồng nghĩa hoàn tất gán nhãn.
2. **`usable_for_training_count` là `70`:** Có 70 câu ở trạng thái `reviewed` mang nhãn chuẩn hợp lệ (17 câu `needs_discussion` nhãn để trống không tính vào tập train).
3. **`train_readiness_status`:** `not_evaluated_in_pilot_phase` — Cỡ mẫu 70 câu phân bố trên 8 nhãn còn mỏng (đặc biệt nhãn `sot` chỉ có 3 câu), chưa đủ để chia train/validation/test đại diện cho bài toán 5 mô hình. Dự án cần bước mở rộng gán nhãn trước khi tiến hành huấn luyện.

---

## 3. Phân bố nhãn chuẩn đã duyệt (`gold_topic_label`)

### Phân bố hiện tại trên toàn bộ 70 câu `reviewed` của tập pilot:

| Nhãn chuẩn | Đợt 1 (12 câu) | Đợt 2 (58 câu) | Toàn bộ Pilot (70 câu) | Tỷ lệ (%) |
| :--- | :---: | :---: | :---: | :---: |
| `hong_amidan` | 2 | 12 | **14** | 20.0% |
| `trieu_chung_tai` | 1 | 10 | **11** | 15.7% |
| `xoang` | 3 | 7 | **10** | 14.3% |
| `ho_dom` | 1 | 8 | **9** | 12.9% |
| `cam_lanh` | 1 | 7 | **8** | 11.4% |
| `trieu_chung_mui` | 1 | 7 | **8** | 11.4% |
| `cam_cum` | 1 | 6 | **7** | 10.0% |
| `sot` | 2 | 1 | **3** | 4.3% |
| **Tổng** | **12** | **58** | **70** | **100%** |

---

## 4. Các tình huống phân loại đặc thù đã chốt qua đợt 1

1. **Câu hỏi so sánh song song giữa 2 bệnh cảnh (Câu 15 — `ViMedAQA:train:disease_1587`):**
   - *Biểu hiện:* Người dùng so sánh sự khác nhau giữa cúm và cảm lạnh.
   - *Quyết định:* Ghi nhận trạng thái `needs_discussion`, nhãn chuẩn để trống (chưa dùng train đơn nhãn); ghi nhận yêu cầu hệ thống hỏi đáp phải truy xuất nội dung từ cả hai nhóm `cam_cum` và `cam_lanh` để tổng hợp câu trả lời so sánh.
2. **Câu hỏi đa cơ quan có nghi vấn biến chứng (Câu 11 — `ViMQ:train:4065`):**
   - *Biểu hiện:* Viêm xoang kèm chảy mủ ở tai.
   - *Quyết định:* Người duyệt chọn nhãn `xoang` làm chủ đề chính của câu hỏi.
3. **Cấu trúc phủ định triệu chứng (Câu 13 — `ViMQ:train:2618`):**
   - *Biểu hiện:* Bé không ho hay ngạt mũi nhưng bị sốt.
   - *Quyết định:* Bỏ qua các từ khóa trong mệnh đề phủ định ("không ho hay ngạt mũi"), chọn nhãn `sot`.
4. **Câu hỏi nhiều biểu hiện (Câu 14 — `ViMQ:test:239`):**
   - *Biểu hiện:* Trẻ sốt cao, đau đầu, viêm họng cấp nhưng không than đau họng.
   - *Quyết định:* Người duyệt chọn nhóm họng `hong_amidan` làm chủ đề chính.
5. **Tiền sử bệnh cũ (Câu 12 — `ViMQ:train:5732`):**
   - *Biểu hiện:* Tiền sử viêm xoang hiện tại đau đầu và đau gáy.
   - *Quyết định:* Người duyệt chọn nhãn `xoang`; chỉ xác nhận chủ đề câu hỏi, không coi nhận định nguyên nhân đau đầu gáy là kiến thức y khoa đã xác minh.
6. **Nhóm câu loại trừ (`excluded` - 7 câu):**
   - Gồm câu hỏi về phẫu thuật sọ não / xoang hang (Câu 09), giải phẫu xương sọ (Câu 10), hội chứng chảy dịch mũi sau (Câu 16), hỏi triệu chứng viêm amidan (Câu 17), tiêm chủng vắc-xin Covid-19 (Câu 18), ung thư ống mật (Câu 19), mao mạch tuần hoàn (Câu 20).
   - *Lưu ý:* Quyết định loại trừ áp dụng đúng cho các ID đã xác nhận trong đợt 1, không tự động suy rộng để loại trừ các câu hỏi khác ngoài đợt.

## 5. Kiểm kê ứng viên và đề xuất mở rộng gán nhãn (28/11/2026)

Đây là **phương án chưa lấy mẫu**, không phải dữ liệu đã duyệt và không phải ngưỡng bảo đảm đủ điều kiện train. Nhãn gợi ý `topic_label` chỉ dùng tìm ứng viên.

### Quy mô và cách tránh lặp

- Prepared có **3.130 câu**; bỏ đúng 120 ID pilot còn **3.010 câu**.
- Bỏ tiếp các câu có `group_id` trùng pilot còn **2.346 câu**, thuộc **1.643 group_id**. Như vậy 664 câu ngoài 120 ID vẫn có liên hệ nhóm với pilot và không được đưa vào đợt mới này.
- Số ứng viên còn lại theo dataset: ViMQ **871**, ViHealthQA **629**, ViMedAQA **846**. Đây là số câu, chưa phải số mẫu độc lập hoặc số câu đúng phạm vi.
- Khi lấy mẫu thực tế: mỗi `group_id` tối đa một câu trong đợt; kiểm tra thêm trùng, gần trùng và diễn đạt lại. Không tách các nhóm liên quan qua train/validation/test. `group_id` hiện tại không bảo đảm phát hiện mọi câu gần trùng.

### Nhãn hiện có và ứng viên sau lọc nhóm pilot

| Nhãn gợi ý | Nhãn đã duyệt hiện có | ViMQ | ViHealthQA | ViMedAQA | Tổng câu ứng viên | Nhóm ứng viên khác nhau trong nhãn | Chỉ tiêu đề xuất đợt tới |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `sot` | 3 | 251 | 155 | 184 | 590 | 456 | 30 |
| `cam_cum` | 7 | 27 | 20 | 34 | 81 | 64 | 30 |
| `ho_dom` | 9 | 148 | 78 | 154 | 380 | 308 | 25 |
| `trieu_chung_mui` | 8 | 75 | 105 | 40 | 220 | 177 | 25 |
| `trieu_chung_tai` | 11 | 106 | 70 | 47 | 223 | 189 | 25 |
| `hong_amidan` | 14 | 101 | 69 | 78 | 248 | 196 | 20 |
| `xoang` | 10 | 26 | 51 | 35 | 112 | 81 | 20 |
| `cam_lanh` | 8 | 0 | 0 | 12 | 12 | 9 | 9 |
| Chưa có nhãn đơn tự động | — | 137 | 81 | 262 | 480 | 330 | 16 |

Các số nhóm theo từng nhãn không được cộng thành tổng nhóm toàn kho: cùng một group_id có thể xuất hiện ở nhiều nhãn gợi ý.

### Đề xuất đợt 200 câu

- **184 ứng viên có một nhãn gợi ý**, theo chỉ tiêu ở bảng, cộng **16 câu chưa có nhãn đơn tự động** để kiểm tra phủ định, tiền sử, nhiều chủ đề và phạm vi.
- Ưu tiên nhóm sốt (hiện 3 nhãn đã duyệt) và cúm (7); giảm số câu họng trong đợt mới vì đã có 14.
- Cảm lạnh chỉ còn **12 câu, 9 nhóm**, đều từ ViMedAQA theo nhãn tự động hiện tại. Chỉ tiêu tối đa ban đầu là 9 câu thuộc 9 nhóm mới; không nhân bản, không tự đổi nhãn nhóm khác hoặc bịa câu để đủ số. Có thể rà thủ công ứng viên chưa gán được nhãn và kho nguồn hiện có để tìm thêm, nhưng chưa thực hiện ở lượt này.
- Trộn nguồn khi có ứng viên phù hợp; không áp tỷ lệ ba nguồn cứng cho nhãn chỉ có một nguồn. Kiểm tra tính khả thi sau loại nhóm trùng giữa các nhãn, gần trùng và câu ngoài phạm vi; nếu thiếu phải báo và điều chỉnh chỉ tiêu, không tự lấy câu lặp bù.
- Đợt lấy mẫu mở rộng 200 câu (Batch 02) đã được thực hiện bằng script `01_ma_nguon/xu_ly_du_lieu/sample_expansion.py` (seed = 42). Dữ liệu xuất tại `reviewed/expansion/batch_02_v1/` và phiếu duyệt tại [PHIEU_DUYET_MO_RONG_DOT_02.md](../../06_tai_lieu/PHIEU_DUYET_MO_RONG_DOT_02.md).

### Việc còn thiếu

- 17 câu thảo luận của pilot tiếp tục giữ nguyên, không ép nhãn để tăng số lượng.
- Sau mở rộng phải thống kê số câu **thực sự được duyệt**, số nhóm độc lập từng nhãn và từng nguồn; chỉ quyết định chia tập khi có dữ liệu đại diện. 200 câu mới là một đợt thao tác, không phải cam kết đủ train hay đủ đánh giá PhoBERT.
- Tập đánh giá cần người duyệt đọc độc lập; việc người dùng chấp thuận nhãn AI hàng loạt chưa cung cấp số đo độ đúng nhãn hoặc mức đồng thuận giữa người gán nhãn.
- Kho prepared có **1.814 mục kiến thức**, toàn bộ `pending_medical_and_privacy_review`, `approved_for_rag = False`. Duyệt nhãn câu hỏi không phê duyệt nội dung trả lời; vẫn phải kiểm tra nguồn, tính phù hợp, điều kiện áp dụng và riêng tư trước khi đưa vào kho chính thức.
- Chưa train, chưa chia train/validation/test, chưa tạo SQLite, backend, Streamlit hoặc tích hợp LLM.

### Dấu vết lần kiểm kê

| Đầu vào | SHA-256 |
| --- | --- |
| `prepared/questions_ent.jsonl` | `0548b9a2e4d2d241784d009d5d52e62b84353e677230bcda861ab7f18d6a4fa5` |
| `reviewed/pilot/questions_pilot.jsonl` | `398f113739b8e795a64e1098a4edab59b4f071ab79f3259e0e432dd3e2069d2d` |
| `reviewed/annotations/v4_user_accepted_20261128/questions_reviewed.jsonl` | `1a54170c516a1fdf442798e9722c59835aec8a2036073ced63fe2847d9d80f01` |
| `reviewed/annotations/v4_user_accepted_20261128/review_manifest.json` | `377ca3e4b73400a6a3f0d818d7e93d3a342ac7bfbda4804425bd9785fe2269fe` |

Đường dẫn trong bảng tính từ `02_du_lieu/filedata`. Bộ xuất và file làm việc đã đối chiếu tương đương; validator annotated kiểm tra thành công.

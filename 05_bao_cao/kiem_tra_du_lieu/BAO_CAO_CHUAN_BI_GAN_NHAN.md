# Báo cáo chuẩn bị tập gán nhãn thử (Pilot Annotation)

Thời điểm lập: **28/11/2026** (Cập nhật quy tắc chuẩn hóa)  
Mục đích: Báo cáo kết quả trích chọn tập câu hỏi gán nhãn thử nghiệm (120 mẫu) để đánh giá quy trình gán nhãn chủ đề và kiểm thử mức độ thống nhất trước khi gán nhãn quy mô lớn.  
Tài liệu liên quan:
- Hướng dẫn gán nhãn: [HUONG_DAN_GAN_NHAN.md](../../06_tai_lieu/HUONG_DAN_GAN_NHAN.md)
- Quy ước lưu trữ: [QUY_UOC_LUU_TRU.md](../../06_tai_lieu/QUY_UOC_LUU_TRU.md)
- Script lấy mẫu: [prepare_annotation_pilot.py](../../01_ma_nguon/xu_ly_du_lieu/prepare_annotation_pilot.py)
- Script kiểm tra: [validate_pilot.py](../../01_ma_nguon/xu_ly_du_lieu/validate_pilot.py)
- Manifest lấy mẫu: [sampling_manifest.json](../../02_du_lieu/filedata/reviewed/pilot/sampling_manifest.json)

> [!IMPORTANT]
> **Tuyên bố về phạm vi và tính chất dữ liệu:**
> - Đây **KHÔNG** phải là báo cáo đánh giá chất lượng mô hình phân loại hay hiệu năng của hệ thống hỏi đáp.
> - Tập dữ liệu trong thư mục `reviewed/pilot/` là tập **chuẩn bị để người duyệt đọc và gán nhãn thủ công**, hoàn toàn **chưa được kiểm duyệt y khoa hay gán nhãn chuẩn (`gold_topic_label`)**. Mọi nhãn gợi ý hiện tại đều là kết quả sinh tự động từ luật từ khóa.

---

## 1. Kết quả lấy mẫu thực tế

- **Tổng số câu hỏi được chọn:** **120 câu** (mục tiêu: 120 câu).
- **Phương pháp lấy mẫu:** Lấy mẫu phân tầng ngẫu nhiên có kiểm soát (Stratified Random Sampling) với `seed=42`, đảm bảo tính tái lập 100%.
- **Dữ liệu đầu vào:** `02_du_lieu/filedata/prepared/questions_ent.jsonl` (3.130 câu ứng viên, SHA-256: `0548b9a2e4d2d241784d009d5d52e62b84353e677230bcda861ab7f18d6a4fa5`).
- **Thư mục lưu trữ:** `02_du_lieu/filedata/reviewed/pilot/`
  - [questions_pilot.csv](../../02_du_lieu/filedata/reviewed/pilot/questions_pilot.csv) (UTF-8 có BOM cho Excel).
  - [questions_pilot.jsonl](../../02_du_lieu/filedata/reviewed/pilot/questions_pilot.jsonl) (UTF-8).
  - [sampling_manifest.json](../../02_du_lieu/filedata/reviewed/pilot/sampling_manifest.json) (Metadata truy vết).

---

## 2. Phân bố cơ cấu mẫu

### 2.1. Phân bố theo nhóm chủ đề phân tầng
Mẫu 120 câu được cấu trúc có chủ đích nhằm kiểm thử toàn diện khả năng phân loại của người duyệt và độ bao phủ của bộ nhãn:

| Nhóm phân tầng | Số lượng | Tỷ lệ | Mục đích kiểm tra |
|---|---:|---:|---|
| `ho_dom` | 10 | 8.33% | Nhận diện triệu chứng ho, đờm |
| `trieu_chung_mui` | 10 | 8.33% | Phân biệt kích ứng mũi thông thường với xoang |
| `xoang` | 10 | 8.33% | Nhận diện câu hỏi xoang thật sự và các trường hợp bẫy từ khóa (như xoang hang) |
| `hong_amidan` | 10 | 8.33% | Bao quát vùng họng, amiđan, VA và thanh quản |
| `trieu_chung_tai` | 10 | 8.33% | Triệu chứng tai, mủ tai, ù tai, thính lực |
| `cam_cum` | 10 | 8.33% | Câu hỏi nhắc trực tiếp cảm cúm / cúm |
| `sot` | 10 | 8.33% | Kiểm tra triệu chứng sốt và ranh giới với bệnh toàn thân |
| `cam_lanh` | 8 | 6.67% | Nhóm hiếm (toàn bộ dataset chỉ có 32 câu); kiểm tra phân biệt với cúm |
| **`multiple_topics`** | **28** | **23.33%** | **Câu hỏi có từ 2 chủ đề trở lên (phối hợp triệu chứng)** |
| **`unassigned_no_keywords`** | **14** | **11.67%** | **Câu hỏi chưa có từ khóa khớp trong câu (lọc theo ngữ cảnh nguồn)** |
| **Tổng cộng** | **120** | **100.00%** | |

### 2.2. Phân bố theo nguồn dữ liệu (Datasets)
Cả 3 bộ dữ liệu đều có đại diện cân đối trong tập pilot:

| Bộ dữ liệu | Số lượng câu | Tỷ lệ | Đặc điểm ngữ liệu |
|---|---:|---:|---|
| **ViMQ** | 36 | 30.00% | Câu hỏi ngắn, có nhãn ý định và thực thể gốc |
| **ViHealthQA** | 33 | 27.50% | Câu hỏi người bệnh thực tế trên diễn đàn y khoa |
| **ViMedAQA** | 51 | 42.50% | Câu hỏi gắn liền bài viết tư vấn y khoa chuyên sâu |
| **Tổng cộng** | **120** | **100.00%** | |

### 2.3. Các trường hợp phức tạp cần đọc kỹ ngữ cảnh
- **Số câu có dấu hiệu phủ định / thuyên giảm (`negation_review_required = True`):** **16 câu** (13.33%).  
  Ví dụ: *"Tôi vừa hết sốt xuất huyết..."*, *"Bé ho nhưng không sốt..."*, *"Uống thuốc đã đỡ đau họng nhưng còn khàn tiếng..."*.
- **Số câu đa chủ đề (`multiple_topics`):** **28 câu** (23.33%).  
  Ví dụ: *"Đau họng kèm có đờm có phải viêm amidan không?"* (xuất hiện cả `ho_dom` và `hong_amidan`).
- **Số câu chưa có từ khóa (`unassigned_no_keywords`):** **14 câu** (11.67%).  
  Ví dụ: Các câu hỏi dùng cách nói gián tiếp đòi hỏi người gán nhãn phải đọc hiểu nội dung chứ không thể dựa vào gợi ý tự động.

---

## 3. Những điểm then chốt cần người gán nhãn quyết định

Trong quá trình duyệt 120 câu này, người gán nhãn cần tuân thủ các nguyên tắc phân loại nội dung câu hỏi, không chẩn đoán bệnh:

1. **Phân biệt triệu chứng chính (Chief Complaint) vs Triệu chứng phụ:**
   - Trong 28 câu đa chủ đề, người gán nhãn căn cứ vào trọng tâm người dùng đang hỏi. Nếu các triệu chứng hoàn toàn ngang hàng không thể phân định một cách khách quan -> **chuyển sang `needs_discussion`**, tuyệt đối không cố ép nhãn.
2. **Không tự suy diễn bệnh từ triệu chứng hay hoàn cảnh:**
   - Không suy ra viêm xoang chỉ từ đau trán, đau mặt, nghẹt mũi hoặc tính chất dịch mũi nếu người hỏi không hỏi về xoang.
   - Không suy ra cảm lạnh chỉ từ hoàn cảnh đi mưa, dầm gió nếu câu hỏi chỉ tập trung hỏi về sốt hoặc ho.
   - Không suy ra cảm cúm chỉ từ việc có ho và sốt.
3. **Xử lý từ khóa gây nhiễu y khoa và từ đồng hình:**
   - Ví dụ trong tập pilot có câu: *"Rò rỉ nhẹ động mạch xoang hang có nguy hiểm không?"*. Mặc dù xuất hiện từ *"xoang"*, đây là cấu trúc mạch máu nội sọ chuyên khoa thần kinh/mạch máu, hoàn toàn không phải bệnh lý Tai Mũi Họng. Trường hợp này cần đánh dấu `review_status = "excluded"`, `gold_topic_label = ""` và ghi rõ lý do vào `review_note`.
4. **Phân biệt tiền sử và phủ định:**
   - Nếu từ khóa xuất hiện ở tiền sử (*"trước đây bị viêm xoang, nay đau tai"* -> trọng tâm là `trieu_chung_tai`) hoặc phủ định (*"bác sĩ bảo không phải xoang"* -> gán theo than phiền chính).

---

## 4. Quy ước chuẩn hóa trạng thái duyệt và quy trình 7 bước qua Excel

### 4.1. Thống nhất 3 trạng thái duyệt (`review_status`)
- **`reviewed`:** Người duyệt xác định rõ ràng chủ đề chính. Cột `gold_topic_label` **chứa đúng 1 trong 8 mã nhãn hợp lệ** (`ho_dom`, `trieu_chung_mui`, `xoang`, `hong_amidan`, `trieu_chung_tai`, `cam_lanh`, `cam_cum`, `sot`), có `reviewer_id` và `reviewed_at` (YYYY-MM-DD hợp lệ).
- **`needs_discussion`:** Câu hỏi mập mờ, nhiều triệu chứng ngang hàng không rõ trọng tâm, hoặc có băn khoăn. Cột `gold_topic_label` **bắt buộc để trống (`""`)**, ghi rõ băn khoăn vào `review_note`, có `reviewer_id` và `reviewed_at`. Tuyệt đối không thêm nhãn tự chế vào `gold_topic_label`.
- **`excluded`:** Câu hỏi rác, vô nghĩa, hoặc hoàn toàn ngoài chuyên khoa Tai Mũi Họng. Cột `gold_topic_label` **bắt buộc để trống (`""`)**, ghi rõ lý do loại vào `review_note`, có `reviewer_id` và `reviewed_at`. Không điền nhãn "ngoai_pham_vi" vào `gold_topic_label` khi chưa có quy định toàn dự án.

### 4.2. Quy trình 7 bước thao tác thực tế
1. **Bước 1 — Tạo bản làm việc an toàn (không ghi đè):**
   Chạy lệnh kiểm tra và tạo bản làm việc riêng; nếu file đã có, lệnh sẽ thông báo mở tiếp bản hiện có để bảo vệ dữ liệu đã gán:
   ```powershell
   $workingCsv = "02_du_lieu/filedata/reviewed/working/questions_working.csv"
   if (-not (Test-Path $workingCsv)) {
       New-Item -ItemType Directory -Force -Path (Split-Path $workingCsv) | Out-Null
       Copy-Item "02_du_lieu/filedata/reviewed/pilot/questions_pilot.csv" $workingCsv
       Write-Host "Da tao ban lam viec moi: $workingCsv"
   } else {
       Write-Host "Ban lam viec da ton tai: $workingCsv. Mo tiep file nay de tranh ghi de du lieu da gan nhan!"
   }
   ```
2. **Bước 2 — Mở và gán nhãn trên Excel:**
   Mở file CSV trong thư mục working bằng Excel. Đọc `question`, tham khảo `suggested_topic_label` và `keywords`. Chỉ chỉnh sửa 5 cột: `gold_topic_label`, `review_status`, `reviewer_id`, `reviewed_at` (YYYY-MM-DD hợp lệ), và `review_note`. Không sửa các cột dữ liệu nguồn.
3. **Bước 3 — Lưu file CSV:**
   Lưu file trên Excel ở định dạng CSV UTF-8.
4. **Bước 4 — Chạy kiểm tra tính hợp lệ (`--check-only`):**
   ```powershell
   python -X utf8 01_ma_nguon/xu_ly_du_lieu/export_reviewed_pilot.py --input-csv 02_du_lieu/filedata/reviewed/working/questions_working.csv --check-only
   ```
5. **Bước 5 — Sửa lỗi nếu có:**
   Mở lại Excel và sửa các dòng được script thông báo lỗi (nếu có).
6. **Bước 6 — Xuất phiên bản dữ liệu đã kiểm tra:**
   Xuất sang thư mục phiên bản mới (bắt buộc là thư mục chưa tồn tại):
   ```powershell
   python -X utf8 01_ma_nguon/xu_ly_du_lieu/export_reviewed_pilot.py --input-csv 02_du_lieu/filedata/reviewed/working/questions_working.csv --output-dir 02_du_lieu/filedata/reviewed/annotations/v1
   ```
   Lệnh này tự động sinh bộ 3 file hoàn chỉnh: `questions_reviewed.csv`, `questions_reviewed.jsonl`, và `review_manifest.json`.
7. **Bước 7 — Theo dõi tiến độ:**
   Xem thống kê số lượng câu hoàn tất (`reviewed`), thảo luận (`needs_discussion`), loại (`excluded`), và còn chờ (`pending_manual_review`), cùng số câu có thể dùng cho train (`usable_for_training_count`). Quy trình chuẩn bị train chính thức mới là nơi đánh giá điều kiện sẵn sàng huấn luyện 5 mô hình.

---

## 5. Giới hạn của việc lấy mẫu pilot

- **Kích thước mẫu:** Tập pilot 120 mẫu được thiết kế để rà soát quy trình, phát hiện điểm bất đồng và kiểm thử bộ nhãn, **chưa đại diện cho phân phối xác suất thực tế** của toàn bộ 3.130 câu hỏi ứng viên.
- **Tính đại diện theo nhãn:** Các nhãn hiếm như `cam_lanh` (chỉ có 32 câu trong dữ liệu gốc) được tăng cường tỷ lệ (lấy 8 câu ~ 25% tổng số câu cảm lạnh) để có đủ mẫu quan sát.
- **Chưa dùng để chia train/test:** Mẫu pilot này nằm trong thư mục `reviewed/pilot/`, độc lập hoàn toàn với phân chia `train/validation/test` cuối cùng của đồ án.
- **Chưa có kiểm duyệt y khoa:** Các dữ liệu đầu vào là tập ngữ liệu thu thập từ các nguồn công khai, cần được chuyên gia y tế thẩm định trước khi ứng dụng vào hệ thống thực tế.

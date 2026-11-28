# Ví dụ xử lý câu hỏi nhiều triệu chứng và câu hỏi bổ sung (BacSiAi)

Phiên bản: **1.0 (Tài liệu minh họa phương pháp luận và quy tắc xử lý)**  
Ngày tạo: **28/11/2026**  
Dự án: **BacSiAi (Phân loại câu hỏi y tế Tai Mũi Họng)**  
Tài liệu tham chiếu: [HUONG_DAN_GAN_NHAN.md](HUONG_DAN_GAN_NHAN.md), [QUY_UOC_LUU_TRU.md](QUY_UOC_LUU_TRU.md), [examples_01.jsonl](../02_du_lieu/filedata/reviewed/user_examples/examples_01.jsonl), [examples_01.csv](../02_du_lieu/filedata/reviewed/user_examples/examples_01.csv).

---

## 1. Mục đích và phạm vi lưu trữ

Tài liệu này phân tích 5 câu hỏi ví dụ thực tế do người dùng cung cấp nhằm minh họa quy trình nhận diện từ khóa, xác định chủ đề ứng viên, xử lý câu hỏi đa triệu chứng và cách đặt câu hỏi làm rõ (`clarification_question`) trong hệ thống BacSiAi.

> [!IMPORTANT]
> **Nguyên tắc bảo toàn và tách biệt dữ liệu:**
> - 5 ví dụ này được lưu trữ độc lập tại thư mục:  
>   `02_du_lieu/filedata/reviewed/user_examples/` (`examples_01.csv` và `examples_01.jsonl`).
> - Tuyệt đối **không chèn, bổ sung hay thay thế** vào danh sách 120 ID của tập pilot ban đầu (`02_du_lieu/filedata/reviewed/pilot/`) hay tệp làm việc (`02_du_lieu/filedata/reviewed/working/questions_working.csv`).
> - Đây là các ví dụ minh họa phương pháp luận, **không phải là bộ dữ liệu công khai thứ tư** và **chưa đưa vào tập huấn luyện**.
> - Các nhãn chủ đề ở đây chỉ là đề xuất minh họa theo quy tắc, **chưa được gán nhãn chuẩn (`gold_topic_label`)** và giữ trạng thái `pending_manual_review`.

---

## 2. Bảng tổng hợp xử lý 5 câu ví dụ

| Mã ID | Câu hỏi gốc | Từ khóa nhận diện | Chủ đề ứng viên (`topic_candidates`) | Chủ đề chính gợi ý (`suggested_primary_topic`) | Cần làm rõ (`needs_clarification`) | Câu hỏi làm rõ (`clarification_question`) |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| `USR_EX_001` | *tôi bị đau họng, ho có đờm màu trắng.* | `đau họng`, `ho có đờm màu trắng` | `hong_amidan`, `ho_dom` | *(để trống)* | **true** | *Bạn muốn hỏi chính về triệu chứng đau họng hay ho có đờm?* |
| `USR_EX_002` | *tôi bị đau đầu có sổ mũi và chảy nước mũi màu vàng, ho có đàm vàng, có sốt.* | `đau đầu`, `sổ mũi`, `chảy nước mũi màu vàng`, `ho có đàm vàng`, `sốt` | `trieu_chung_mui`, `ho_dom`, `sot` | *(để trống)* | **true** | *Bạn đang băn khoăn nhiều nhất về triệu chứng nào trong các triệu chứng: đau đầu, sổ mũi/chảy mũi, ho đờm hay sốt?* |
| `USR_EX_003` | *tôi bị nghẹt mũi.* | `nghẹt mũi` | `trieu_chung_mui` | `trieu_chung_mui` | **false** | *(để trống)* |
| `USR_EX_004` | *tôi bị ù tai hơi đau ở tai* | `ù tai`, `hơi đau ở tai` | `trieu_chung_tai` | `trieu_chung_tai` | **false** | *(để trống)* |
| `USR_EX_005` | *tôi bị đau họng kèm vs sổ mũi* | `đau họng`, `sổ mũi` | `hong_amidan`, `trieu_chung_mui` | *(để trống)* | **true** | *Bạn muốn hỏi chính về triệu chứng đau họng hay sổ mũi?* |

---

## 3. Phân tích chi tiết từng trường hợp

### 3.1. Các câu cần làm rõ chủ đề chính (Câu 1, 2, 5)

1. **Câu 1 (`USR_EX_001`): *"tôi bị đau họng, ho có đờm màu trắng."***
   - **Đặc điểm:** Câu hỏi chứa 2 triệu chứng độc lập: *"đau họng"* (thuộc vùng họng / `hong_amidan`) và *"ho có đờm"* (thuộc nhóm chủ đề ho và đờm / `ho_dom`).
   - **Vì sao không tự chọn chủ đề chính:** Không thể lấy thứ tự từ ngữ xuất hiện trước (*"đau họng"*) làm căn cứ quyết định đây là chủ đề chính. Cả hai triệu chứng đều có trọng lượng ngang nhau trong câu mô tả ngắn của người dùng.
   - **Cách xử lý:** Hệ thống ghi nhận đầy đủ cả 2 chủ đề ứng viên, để trống chủ đề chính và kích hoạt cờ `needs_clarification = true` để hỏi người dùng xem họ đang băn khoăn hay khó chịu nhất vì triệu chứng nào.

2. **Câu 2 (`USR_EX_002`): *"tôi bị đau đầu có sổ mũi và chảy nước mũi màu vàng, ho có đàm vàng, có sốt."***
   - **Đặc điểm:** Một câu văn chứa tổ hợp 5 triệu chứng phức tạp: *đau đầu*, *sổ mũi*, *chảy nước mũi màu vàng*, *ho có đàm vàng*, *có sốt*.
   - **Bảo toàn thông tin toàn diện:** Triệu chứng *"đau đầu"* vẫn được ghi nhận nguyên vẹn trong danh sách từ khóa (`keywords`), tuyệt đối không bị bỏ sót dù bộ 8 nhãn TMH hiện tại chưa có nhãn riêng cho đau đầu.
   - **Cảnh báo suy diễn sai lầm:**
     - Người gán nhãn hoặc mô hình không được tự suy ra bệnh `xoang` chỉ vì câu có *đau đầu*, *chảy dịch mũi vàng*.
     - Không được tự suy ra bệnh `cam_cum` chỉ vì câu có tổ hợp *ho*, *sổ mũi* và *sốt*.
   - **Cách xử lý:** Đặt `needs_clarification = true`. Câu hỏi làm rõ liệt kê đầy đủ các lựa chọn (gồm cả đau đầu). Nếu người dùng xác nhận họ lo lắng nhất vì đau đầu (ngoài phạm vi 8 nhãn TMH), hệ thống sẽ ghi nhận cần thảo luận về phạm vi phân loại thay vì cố ép vào nhãn TMH có sẵn.

3. **Câu 5 (`USR_EX_005`): *"tôi bị đau họng kèm vs sổ mũi"***
   - **Đặc điểm:** Người dùng liên kết hai triệu chứng bằng cụm từ *"kèm vs"* (kèm với).
   - **Lý do cần làm rõ:** Cụm từ liên kết này chỉ phản ánh hai triệu chứng cùng xuất hiện đồng thời, không khẳng định triệu chứng nào là bệnh cảnh chính hay nguyên nhân dẫn đến triệu chứng kia.
   - **Cách xử lý:** Để trống `suggested_primary_topic` và đặt câu hỏi gợi mở để người dùng xác định triệu chứng ưu tiên cần tư vấn.

---

### 3.2. Các câu có thể xác định chủ đề ngay (Câu 3, 4)

1. **Câu 3 (`USR_EX_003`): *"tôi bị nghẹt mũi."***
   - **Đặc điểm:** Câu hỏi chỉ có một triệu chứng duy nhất là *"nghẹt mũi"*, khu trú tại đường hô hấp trên vùng mũi.
   - **Xác định chủ đề:** Toàn bộ từ khóa quy tụ trực tiếp và duy nhất về chủ đề `trieu_chung_mui`.
   - **Trạng thái:** `needs_clarification = false` đối với riêng bài toán phân loại chủ đề (không cần hỏi thêm để biết câu hỏi nói về cái gì).

2. **Câu 4 (`USR_EX_004`): *"tôi bị ù tai hơi đau ở tai"***
   - **Đặc điểm:** Câu hỏi mô tả hai biểu hiện: *"ù tai"* và *"hơi đau ở tai"*.
   - **Xác định chủ đề:** Cả hai biểu hiện đều khu trú đồng nhất tại một cơ quan giải phẫu là tai, cùng tương ứng với chủ đề `trieu_chung_tai`.
   - **Trạng thái:** `needs_clarification = false` cho bài toán phân loại chủ đề.

---

## 4. Những nguyên tắc cốt lõi rút ra

### 4.1. Phân biệt nhãn chủ đề với chẩn đoán bệnh học
- **Nhãn chủ đề (`topic_label`):** Chỉ nhằm xác định *trọng tâm nội dung câu hỏi đang hướng tới cơ quan hay nhóm vấn đề nào* (mũi, tai, xoang, họng, ho đờm...) nhằm định tuyến dữ liệu hoặc tìm kiếm tài liệu chuyên khoa phù hợp.
- **Không phải chẩn đoán:**
  - Xác định chủ đề là `trieu_chung_tai` **không đồng nghĩa** chẩn đoán người dùng bị viêm tai giữa hay viêm tai ngoài.
  - Xác định chủ đề là `trieu_chung_mui` **không đồng nghĩa** chẩn đoán người dùng bị viêm mũi dị ứng hay cảm cúm.
- **Chủ đề rõ ràng $\neq$ Đủ thông tin điều trị:** Ở câu 3 và câu 4, dù chủ đề câu hỏi đã đủ rõ ràng để phân loại (`needs_clarification = false`), nhưng câu hỏi hoàn toàn thiếu thông tin bệnh sử, thời gian kéo dài, mức độ sốt... nên **tuyệt đối không đủ dữ kiện y khoa để chẩn đoán hay đưa ra lời khuyên dùng thuốc**.

### 4.2. Quan hệ giữa Từ khóa, Chủ đề ứng viên và Chủ đề chính
1. **Trục thực thể / từ khóa (`keywords`):** Phải phản ánh trung thực mọi triệu chứng hoặc từ ngữ y tế xuất hiện trong câu, không bỏ sót bất kỳ triệu chứng nào (kể cả triệu chứng chưa có trong danh mục nhãn phân loại như *đau đầu*).
2. **Trục chủ đề ứng viên (`topic_candidates`):** Tập hợp tất cả các nhãn trong danh mục mà từ khóa trong câu có thể ánh xạ tới. Một câu có thể có 2 hay nhiều chủ đề ứng viên ngang hàng.
3. **Trục chủ đề chính (`suggested_primary_topic`):**
   - Chỉ được xác định khi câu hỏi có đúng một chủ đề duy nhất hoặc có trọng tâm nổi bật rõ ràng.
   - Khi có nhiều chủ đề ứng viên cạnh tranh mà người dùng chưa nêu rõ trọng tâm, chủ đề chính **bắt buộc phải để trống**, chuyển sang bước hỏi làm rõ (`needs_clarification = true`).
4. **Không suy diễn máy móc:**
   - Màu sắc đờm/dịch mũi (vàng, xanh, trắng) là dấu hiệu lâm sàng cần bác sĩ thăm khám trực tiếp, không phải căn cứ tự động gán nhãn `xoang` hay khẳng định nhiễm khuẩn.
   - Thứ tự xuất hiện của từ ngữ trong câu (từ nào viết trước, từ nào viết sau) không phải là bằng chứng để khẳng định triệu chứng chính.

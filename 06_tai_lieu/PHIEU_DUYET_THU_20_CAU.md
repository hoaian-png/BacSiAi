# Phiếu xác nhận duyệt nhãn đợt 1 (20 câu ưu tiên pilot)

Phiên bản: **2.1 (Bổ sung cột xác nhận, quy trình duyệt từng câu và chuẩn hóa thảo luận câu 12)**  
Ngày cập nhật: **28/11/2026**  
Dự án: **BacSiAi (Phân loại câu hỏi y tế Tai Mũi Họng)**  
Tài liệu tham chiếu: [HUONG_DAN_GAN_NHAN.md](HUONG_DAN_GAN_NHAN.md), [QUY_UOC_LUU_TRU.md](QUY_UOC_LUU_TRU.md), [review_batch_01.json](../02_du_lieu/filedata/reviewed/working/review_batch_01.json), [batch_01_ai_review.jsonl](../02_du_lieu/filedata/reviewed/ai_proposals/batch_01_ai_review.jsonl), [DE_XUAT_DUYET_AI_DOT_01.md](../05_bao_cao/kiem_tra_du_lieu/DE_XUAT_DUYET_AI_DOT_01.md).

> [!IMPORTANT]
> **Nguyên tắc thẩm định và bảo toàn dữ liệu:**
> 1. Toàn bộ cột **Đề xuất AI** trong phiếu này chỉ mang tính chất **tham khảo kỹ thuật sơ bộ**, hoàn toàn **chưa phải là quyết định của con người hay chuyên gia y tế**.
> 2. Các ô thuộc phần **Quyết định của người duyệt** phải do người dùng trực tiếp đưa ra quyết định trên tệp làm việc [questions_working.csv](../02_du_lieu/filedata/reviewed/working/questions_working.csv).
> 3. Không tự động chuyển kết quả AI thành dữ liệu `reviewed` chính thức; không tự ý điền thông tin vào tệp CSV làm việc khi chưa có chỉ định trực tiếp từ người duyệt.
> 4. Ký hiệu **`[Chờ điền]`** trong bảng dưới đây chỉ là ký hiệu trình bày vị trí trên tài liệu markdown. **Tuyệt đối không chép chuỗi ký tự "[Chờ điền]" vào tệp CSV**.

---

## 1. Thông tin tệp làm việc và quy ước ghi nhận

> [!NOTE]
> **Trạng thái thực tế:** Đợt 1 (20 câu ưu tiên) đã hoàn tất 100% quyết định của người duyệt (**12 `reviewed`, 7 `excluded`, 1 `needs_discussion`**). Toàn bộ 120 câu pilot (kết hợp cả đợt 1 và đợt 2) hiện đã hoàn tất và xuất bản tại [v4_user_accepted_20261128](../02_du_lieu/filedata/reviewed/annotations/v4_user_accepted_20261128/).

- **Tệp làm việc chính:** `02_du_lieu/filedata/reviewed/working/questions_working.csv` (120 câu pilot).
- **Năm (05) cột được phép chỉnh sửa khi xác nhận:**
  - `review_status`: `reviewed`, `needs_discussion`, hoặc `excluded`. (Các câu chưa xử lý giữ `pending_manual_review`).
  - `gold_topic_label`: Chỉ điền 1 trong 8 nhãn TMH khi `review_status = reviewed`. **Bắt buộc để trống (`""`)** khi chọn `needs_discussion` hoặc `excluded`.
  - `reviewer_id`: Mã định danh thực tế của người duyệt (ví dụ: `hoai_an`). **Tuyệt đối không dùng `anti_ai` thay cho người duyệt con người**.
  - `reviewed_at`: Ngày duyệt thực tế định dạng chuẩn `YYYY-MM-DD` (ví dụ: `2026-11-28`).
  - `review_note`: Ghi chú lý do (bắt buộc khi `needs_discussion` hoặc `excluded`).

---

## 2. Cách thực hiện lượt duyệt đầu tiên

1. **Nguyên tắc thực hiện:** Người duyệt đọc nguyên văn câu hỏi và đưa ra quyết định độc lập dựa trên [HUONG_DAN_GAN_NHAN.md](HUONG_DAN_GAN_NHAN.md). Các gợi ý tự động ban đầu và đề xuất của AI chỉ đóng vai trò tham khảo kỹ thuật sơ bộ, tuyệt đối không được coi là đã được chấp thuận.
2. **Phân nhóm 20 câu theo dữ liệu thực tế:**
   - **Nhóm `label_proposed` (10 câu - AI đề xuất có nhãn rõ ràng):** Câu 01, 02, 03, 04, 05, 06, 07, 08, 13, 17. Người duyệt đối chiếu xem nhãn đề xuất có thực sự là trọng tâm duy nhất của câu hỏi hay không.
   - **Nhóm `excluded_proposed` (3 câu - AI đề xuất loại trừ):** Câu 09, 19, 20. Người duyệt xác nhận nội dung câu hỏi có thực sự nằm ngoài phạm vi chuyên khoa TMH hay không.
   - **Nhóm `needs_discussion` (7 câu - AI đề xuất cần thảo luận):** Câu 10, 11, 12, 14, 15, 16, 18. Người duyệt xem xét các điểm vướng mắc tại Mục 4 dưới đây để quyết định chọn nhãn, loại trừ hoặc giữ nguyên cần thảo luận.
   *(Lưu ý: Mọi đề xuất quy tắc mới tại mục thảo luận đều ở trạng thái "chưa được chấp thuận" và không tự động áp dụng vào nhãn chuẩn).*
3. **Mẫu trả lời để người duyệt gửi quyết định (theo từng câu hoặc theo nhóm):**

```text
STT hoặc ID: 
Quyết định: reviewed / needs_discussion / excluded
Nhãn: <một nhãn hợp lệ nếu reviewed; để trống nếu trạng thái khác>
Ghi chú: <lý do nếu needs_discussion hoặc excluded; tùy chọn nếu reviewed>
Người duyệt: <mã định danh của bạn>
Ngày duyệt: YYYY-MM-DD
```

---

## 3. Bảng 20 câu ưu tiên kèm đề xuất AI và các ô xác nhận của người duyệt

*(Thống kê đề xuất AI tham khảo: 10 `label_proposed`, 7 `needs_discussion`, 3 `excluded_proposed`)*

| STT | Mã ID | Nội dung câu hỏi đầy đủ (nguyên văn) | Nhãn gợi ý ban đầu | Đề xuất AI (Trạng thái & Nhãn) | Lý do tóm tắt của AI | Quyết định người duyệt (`review_status`) | Nhãn chuẩn chọn (`gold_topic_label`) | Ghi chú người duyệt (`review_note`) | Người duyệt (`reviewer_id`) | Ngày duyệt (`reviewed_at`) |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **01** | `ViHealthQA:test:454` | Ho ra máu là dấu hiệu của bệnh gì? | `ho_dom` | `label_proposed` (`ho_dom`) | Trọng tâm phản xạ ho và tính chất đờm máu. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **02** | `ViMQ:train:1459` | Tại sao thường xuyên chảy máu mũi? | `trieu_chung_mui` | `label_proposed` (`trieu_chung_mui`) | Triệu chứng xuất huyết khu trú tại hốc mũi. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **03** | `ViMedAQA:train:disease_13292` | Điều quan trọng cần làm để phòng ngừa viêm xoang là gì? | `xoang` | `label_proposed` (`xoang`) | Câu hỏi trực tiếp về phòng ngừa bệnh lý viêm xoang. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **04** | `ViHealthQA:train:3338` | Có nên cắt viêm amidan không? | `hong_amidan` | `label_proposed` (`hong_amidan`) | Can thiệp thủ thuật viêm amidan vùng họng. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **05** | `ViMQ:train:1239` | Trẻ 1 tuổi bị viêm tai giữa phải làm sao? | `trieu_chung_tai` | `label_proposed` (`trieu_chung_tai`) | Xử trí bệnh lý viêm tai giữa khu trú ở tai. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **06** | `ViMQ:train:6945` | Làm thế nào để phân biệt cảm lạnh do thời tiết hay mắc các bệnh về đường hô hấp? | `cam_lanh` | `label_proposed` (`cam_lanh`) | Trọng tâm tìm hiểu để nhận diện bệnh cảnh cảm lạnh. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **07** | `ViMQ:test:151` | Bệnh cúm thường kéo dài bao lâu? | `cam_cum` | `label_proposed` (`cam_cum`) | Diễn tiến thời gian của bệnh cúm. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **08** | `ViHealthQA:train:5674` | Thường xuyên bị sốt phải điều trị như thế nào? | `sot` | `label_proposed` (`sot`) | Triệu chứng sốt tái diễn đơn thuần, không kèm triệu chứng cơ quan. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **09** | `ViHealthQA:test:1492` | Rò rỉ nhẹ động mạch xoang hang có nguy hiểm không? | `xoang` | `excluded_proposed` *(để trống)* | Từ đồng âm: xoang hang là cấu trúc mạch máu màng cứng sọ não. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **10** | `ViMedAQA:train:body-part_4327` | Rãnh nào nằm ở giữa rãnh nhị thân và rãnh xoang xích ma? | `xoang` | `needs_discussion` *(để trống)* | Câu hỏi giải phẫu xương sọ ("xoang xích ma"); chưa rõ quy tắc phạm vi. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **11** | `ViMQ:train:4065` | Viêm xoang kèm chảy mủ ở tai báo là dấu hiệu bệnh gì? | `xoang` | `needs_discussion` *(để trống)* | Đa cơ quan (xoang + tai), không có căn cứ coi cơ quan nào là phụ. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **12** | `ViMQ:train:5732` | Người có tiền sử viêm xoang bị đau đầu và đau gáy nên điều trị thế nào? | `xoang` | `needs_discussion` *(để trống)* | Viêm xoang là tiền sử; vấn đề cần trị là đau đầu đau gáy (ngoài TMH). | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **13** | `ViMQ:train:2618` | Bé không ho hay ngạt mũi nhưng bị sốt có sao không? | *(trống)* | `label_proposed` (`sot`) | Phủ định ho ngạt mũi ("không ho hay ngạt mũi"), trọng tâm là sốt. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **14** | `ViMQ:test:239` | Trẻ sốt cao, đau đầu, viêm họng cấp nhưng không đau họng là bị làm sao? | *(trống)* | `needs_discussion` *(để trống)* | Đề cập viêm họng cấp, sốt cao, đau đầu; chưa rõ trọng tâm họng hay sốt. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **15** | `ViMedAQA:train:disease_1587` | Bệnh cúm khác cảm lạnh ở những điểm nào? | *(trống)* | `needs_discussion` *(để trống)* | So sánh bình đẳng giữa 2 chủ đề cúm và cảm lạnh trong bài toán đơn nhãn. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **16** | `ViMedAQA:validation:disease_2616` | Ho kéo dài liên quan chảy dịch mũi sau có thể cải thiện khi sử dụng loại thuốc nào? | *(trống)* | `needs_discussion` *(để trống)* | Giằng co giữa triệu chứng phàn nàn (ho kéo dài) và nguyên nhân (chảy dịch mũi sau). | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **17** | `ViHealthQA:train:1052` | Đau họng kèm có đờm có phải viêm amidan không? | *(trống)* | `label_proposed` (`hong_amidan`) | Người hỏi chủ động hướng nghi vấn vào bệnh cảnh viêm amidan. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **18** | `ViHealthQA:train:1216` | Cách đây 3 hôm, tôi bị cảm lạnh và viêm họng nên đã uống thuốc để điều trị. Tôi hết các triệu chứng đau người nên dừng thuốc. Tuy nhiên, do họng vẫn viêm nên tôi có sử dụng viên ngậm hàng ngày. Theo lịch ngày mai tôi thực hiện tiêm vaccine Covid-19, như vậy tôi có tiêm được không hay phải hoãn. (Hiện tại họng tôi vẫn đang hơi có cảm giác đau rát). | *(trống)* | `needs_discussion` *(để trống)* | Trọng tâm là hoãn/tiêm vaccine Covid-19 khi họng còn rát. Chưa rõ phạm vi tiêm chủng. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **19** | `ViMedAQA:train:disease_12172` | Có phải tất cả các trường hợp bị ung thư ống mật đều gây sốt? | `sot` | `excluded_proposed` *(để trống)* | Bệnh ung thư ống mật thuộc chuyên khoa tiêu hóa - gan mật, ngoài TMH. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |
| **20** | `ViMedAQA:train:body-part_2016` | Đặc điểm cấu tạo của mao mạch không liên tục là gì? | *(trống)* | `excluded_proposed` *(để trống)* | Thuần túy lý thuyết mô học tuần hoàn đại cương, ngoài phạm vi TMH. | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` | `[Chờ điền]` |

---

## 4. Khung hướng dẫn thảo luận cho 7 câu chưa rõ (`needs_discussion`)

Dưới đây là 7 câu hỏi phức tạp cần người duyệt đưa ra quyết định chính sách phân loại hoặc lựa chọn hướng xử lý cụ thể:

### 4.1. Câu 10 (`ViMedAQA:train:body-part_4327`)
- **Nội dung:** *"Rãnh nào nằm ở giữa rãnh nhị thân và rãnh xoang xích ma?"*
- **Điểm chưa rõ về trọng tâm / phạm vi:** Câu hỏi thuần túy lý thuyết giải phẫu học xương sọ. Từ *"xoang"* ở đây là rãnh mạch máu sọ não (xoang xích ma), không phải xoang cạnh mũi TMH. Quy tắc hiện tại chưa quy định rõ việc tiếp nhận hay loại trừ các câu hỏi thuần giải phẫu học sọ não.
- **Các hướng xử lý có căn cứ:**
  - Hướng 1: `excluded` (Loại trừ vì là câu hỏi giải phẫu sọ não lý thuyết, không thuộc bệnh lý/triệu chứng TMH).
  - Hướng 2: `needs_discussion` (Giữ nguyên chờ hội đồng chốt chính sách đối với nhóm câu hỏi giải phẫu nền sọ / xương chũm).
- **Câu hỏi quyết định cho người duyệt:**  
  *“Bạn quyết định loại trừ câu này (`excluded`) do tính chất giải phẫu sọ não ngoài TMH, hay giữ `needs_discussion` để chờ quy định mở rộng phạm vi?”*

### 4.2. Câu 11 (`ViMQ:train:4065`)
- **Nội dung:** *"Viêm xoang kèm chảy mủ ở tai báo là dấu hiệu bệnh gì?"*
- **Điểm chưa rõ về trọng tâm / phạm vi:** Câu hỏi xuất hiện đồng thời hai cơ quan bệnh lý: viêm xoang (`xoang`) và chảy mủ tai (`trieu_chung_tai`). Đây là tình huống đa cơ quan có khả năng liên quan biến chứng, không có căn cứ ngữ pháp để xem cơ quan nào là phụ.
- **Các hướng xử lý có căn cứ:**
  - Hướng 1: `reviewed` với nhãn `xoang` (nếu quy ước ưu tiên bệnh lý căn nguyên gốc).
  - Hướng 2: `reviewed` với nhãn `trieu_chung_tai` (nếu quy ước ưu tiên triệu chứng cấp tính phàn nàn là chảy mủ tai).
  - Hướng 3: `needs_discussion` (chưa chốt nhãn đơn và ghi chú cần đặt câu hỏi bổ sung người dùng).
- **Câu hỏi quyết định cho người duyệt:**  
  *“Bạn quyết định chọn nhãn theo căn nguyên (`xoang`), theo triệu chứng cấp tính (`trieu_chung_tai`), hay giữ `needs_discussion` để hỏi lại trọng tâm?”*

### 4.3. Câu 12 (`ViMQ:train:5732`)
- **Nội dung:** *"Người có tiền sử viêm xoang bị đau đầu và đau gáy nên điều trị thế nào?"*
- **Điểm chưa rõ về trọng tâm / phạm vi:** Câu hỏi có tiền sử viêm xoang và triệu chứng hiện tại là đau đầu, đau gáy. Vấn đề cần thống nhất là cách phân loại khi câu hỏi có tiền sử TMH nhưng triệu chứng phàn nàn hiện tại (đau đầu, đau gáy) chưa có nhãn riêng trong bộ 8 nhãn TMH.
- **Các hướng xử lý có căn cứ:**
  - Hướng 1: `excluded` (Loại trừ vì triệu chứng cần điều trị hiện tại nằm ngoài 8 chủ đề TMH).
  - Hướng 2: `needs_discussion` (Giữ needs_discussion vì chưa rõ trọng tâm hiện tại và phạm vi phân loại; không suy diễn nguyên nhân từ tiền sử viêm xoang).
- **Câu hỏi quyết định cho người duyệt:**  
  *“Bạn quyết định loại trừ câu này (`excluded`) do triệu chứng cần điều trị ngoài 8 nhãn TMH, hay giữ `needs_discussion` vì chưa rõ cách phân loại khi có tiền sử viêm xoang?”*

### 4.4. Câu 14 (`ViMQ:test:239`)
- **Nội dung:** *"Trẻ sốt cao, đau đầu, viêm họng cấp nhưng không đau họng là bị làm sao?"*
- **Điểm chưa rõ về trọng tâm / phạm vi:** Câu hỏi đề cập đồng thời bệnh lý viêm họng cấp (`hong_amidan`), sốt cao (`sot`) và đau đầu. Chỉ phân loại nội dung câu hỏi, không phán xét tính đúng sai của chẩn đoán lâm sàng. Trọng tâm phân loại giằng co giữa bệnh cảnh họng và phản ứng sốt toàn thân.
- **Các hướng xử lý có căn cứ:**
  - Hướng 1: `reviewed` với nhãn `hong_amidan` (người hỏi xoay quanh thắc mắc về bệnh cảnh viêm họng).
  - Hướng 2: `reviewed` với nhãn `sot` (người hỏi tập trung vào triệu chứng thực thể sốt cao của trẻ).
  - Hướng 3: `needs_discussion` (chưa đủ căn cứ xác định ưu tiên giữa họng và sốt).
- **Câu hỏi quyết định cho người duyệt:**  
  *“Bạn quyết định chọn nhãn `hong_amidan`, nhãn `sot`, hay giữ `needs_discussion` để làm rõ thêm?”*

### 4.5. Câu 15 (`ViMedAQA:train:disease_1587`)
- **Nội dung:** *"Bệnh cúm khác cảm lạnh ở những điểm nào?"*
- **Điểm chưa rõ về trọng tâm / phạm vi:** Câu hỏi so sánh trực tiếp, bình đẳng giữa hai chủ đề hợp lệ: `cam_cum` và `cam_lanh`. Cả hai có vai trò ngang hàng trong bài toán phân loại đơn nhãn. Quy tắc hiện tại chưa quy định tiêu chí ưu tiên cho câu hỏi so sánh hai chủ đề trong danh mục.
- **Các hướng xử lý có căn cứ:**
  - Hướng 1: `needs_discussion` (Chờ quy ước nguyên tắc cho nhóm câu hỏi so sánh hai bệnh lý hô hấp trong bài toán đơn nhãn; không tự ý chuyển sang đa nhãn).
  - Hướng 2: `reviewed` với nhãn `cam_cum` (nếu người duyệt quyết định một quy ước riêng).
  - Hướng 3: `reviewed` với nhãn `cam_lanh` (nếu người duyệt quyết định một quy ước riêng).
- **Câu hỏi quyết định cho người duyệt:**  
  *“Bạn quyết định chọn `cam_cum`, chọn `cam_lanh`, hay giữ `needs_discussion` để chờ quy tắc thống nhất cho câu hỏi so sánh?”*

### 4.6. Câu 16 (`ViMedAQA:validation:disease_2616`)
- **Nội dung:** *"Ho kéo dài liên quan chảy dịch mũi sau có thể cải thiện khi sử dụng loại thuốc nào?"*
- **Điểm chưa rõ về trọng tâm / phạm vi:** Giằng co giữa triệu chứng phàn nàn muốn dùng thuốc điều trị ("ho kéo dài" - `ho_dom`) và cơ chế bệnh sinh căn nguyên ("chảy dịch mũi sau" - `trieu_chung_mui`). Quy tắc hiện tại chưa chốt thứ tự ưu tiên giữa triệu chứng biểu hiện và cơ chế gốc.
- **Các hướng xử lý có căn cứ:**
  - Hướng 1: `reviewed` với nhãn `ho_dom` (ưu tiên mục tiêu dùng thuốc cải thiện cơn ho).
  - Hướng 2: `reviewed` với nhãn `trieu_chung_mui` (ưu tiên cơ chế căn nguyên dịch mũi sau).
  - Hướng 3: `needs_discussion` (chờ quy tắc cho hội chứng chảy dịch mũi sau gây ho).
- **Câu hỏi quyết định cho người duyệt:**  
  *“Bạn quyết định chọn nhãn theo triệu chứng cần điều trị (`ho_dom`), theo cơ chế gốc (`trieu_chung_mui`), hay giữ `needs_discussion`?”*

### 4.7. Câu 18 (`ViHealthQA:train:1216`)
- **Nội dung:** *"Cách đây 3 hôm, tôi bị cảm lạnh và viêm họng nên đã uống thuốc để điều trị. Tôi hết các triệu chứng đau người nên dừng thuốc. Tuy nhiên, do họng vẫn viêm nên tôi có sử dụng viên ngậm hàng ngày. Theo lịch ngày mai tôi thực hiện tiêm vaccine Covid-19, như vậy tôi có tiêm được không hay phải hoãn. (Hiện tại họng tôi vẫn đang hơi có cảm giác đau rát)."*
- **Điểm chưa rõ về trọng tâm / phạm vi:** Câu hỏi chính là về chỉ định tiêm phòng hay hoãn vaccine Covid-19 khi họng còn đau rát. Triệu chứng rát họng đóng vai trò là điều kiện sức khỏe lúc tiêm, không phải hỏi cách chữa viêm họng.
- **Các hướng xử lý có căn cứ:**
  - Hướng 1: `excluded` (Loại trừ vì bản chất câu hỏi thuộc quy trình tiêm chủng dịch tễ học, ngoài phạm vi TMH).
  - Hướng 2: `reviewed` với nhãn `hong_amidan` (phân loại theo triệu chứng duy nhất đang còn tồn tại ở họng).
  - Hướng 3: `needs_discussion` (giữ lại để làm rõ phạm vi đối với câu hỏi điều kiện tiêm chủng vắc xin).
- **Câu hỏi quyết định cho người duyệt:**  
  *“Bạn quyết định loại trừ khỏi TMH (`excluded`), chọn nhãn theo triệu chứng họng (`hong_amidan`), hay giữ `needs_discussion`?”*

---

## 5. Hướng dẫn kiểm tra sau khi bạn lưu quyết định

Sau khi bạn đã nhập quyết định của mình vào tệp `02_du_lieu/filedata/reviewed/working/questions_working.csv` bằng Excel (lưu đúng định dạng CSV UTF-8), chạy lệnh kiểm tra tính hợp lệ:

```powershell
python -B -X utf8 01_ma_nguon/xu_ly_du_lieu/export_reviewed_pilot.py --input-csv 02_du_lieu/filedata/reviewed/working/questions_working.csv --check-only
```

> [!TIP]
> - 100 câu còn lại vẫn giữ nguyên trạng thái `pending_manual_review` và `gold_topic_label` để trống.
> - Lệnh `--check-only` sẽ xác thực tính hợp lệ của toàn bộ cú pháp ngày tháng, nhãn và trạng thái mà không làm thay đổi hay ghi đè bất kỳ tệp dữ liệu nào.

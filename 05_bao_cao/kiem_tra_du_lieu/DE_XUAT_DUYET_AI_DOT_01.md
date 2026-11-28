# Báo cáo đề xuất duyệt nhãn bằng AI (Đợt 1 — 20 câu ưu tiên)

Phiên bản: **1.1 (Cập nhật chuẩn hóa theo quy tắc: Câu 10, 14, 15)**  
Ngày cập nhật: **28/11/2026**  
Dự án: **BacSiAi (Phân loại câu hỏi y tế Tai Mũi Họng)**  
Người thực hiện đề xuất: `anti_ai` (`reviewer_type: ai`)  
Tài liệu tham chiếu: [HUONG_DAN_GAN_NHAN.md](../../06_tai_lieu/HUONG_DAN_GAN_NHAN.md), [PHIEU_DUYET_THU_20_CAU.md](../../06_tai_lieu/PHIEU_DUYET_THU_20_CAU.md), [batch_01_ai_manifest.json](../../02_du_lieu/filedata/reviewed/ai_proposals/batch_01_ai_manifest.json).

> [!CAUTION]
> **Tuyên bố giới hạn và nguyên tắc sử dụng:**
> 1. Kết quả trong tài liệu này là **đề xuất sơ bộ do AI tổng hợp theo quy tắc**, **KHÔNG phải là nhãn chuẩn (`gold_topic_label`)** đã được người dùng hoặc chuyên gia y tế thẩm định.
> 2. Tuyệt đối **không đưa kết quả này vào tập dữ liệu huấn luyện**, không dùng để báo cáo điểm số hay đánh giá chất lượng mô hình.
> 3. Không điền kết quả này vào báo cáo tổng kết thủ công như thể người dùng đã hoàn thành việc gán nhãn.

---

## 1. Bảng chi tiết kết quả đề xuất AI cho 20 câu ưu tiên

Quy ước trạng thái đề xuất:
- `label_proposed`: Xác định được một chủ đề chính đơn nhất theo quy tắc.
- `needs_discussion`: Chưa đủ căn cứ chốt một nhãn (câu hỏi giải phẫu chưa rõ quy tắc phạm vi, đa triệu chứng ngang hàng, thiếu ngữ cảnh xác định trọng tâm, hoặc ranh giới phân loại chưa thống nhất).
- `excluded_proposed`: Đề xuất loại khỏi phạm vi chuyên khoa TMH (từ đồng âm giải phẫu mạch máu não, bệnh lý ngoài chuyên khoa gan mật, mô học đại cương).

| STT | Mã ID | Nội dung câu hỏi đầy đủ | Nhãn gợi ý tự động ban đầu | Nhãn AI đề xuất | Trạng thái đề xuất | Lý do tóm tắt & Điểm chưa rõ (`uncertainty_note`) |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **01** | `ViHealthQA:test:454` | Ho ra máu là dấu hiệu của bệnh gì? | `ho_dom` | `ho_dom` | `label_proposed` | Trọng tâm duy nhất là phản xạ ho và tính chất đờm máu. Triệu chứng ho rõ ràng. |
| **02** | `ViMQ:train:1459` | Tại sao thường xuyên chảy máu mũi? | `trieu_chung_mui` | `trieu_chung_mui` | `label_proposed` | Hiện tượng xuất huyết khu trú tại mũi (chảy máu mũi / chảy máu cam) đơn thuần. |
| **03** | `ViMedAQA:train:disease_13292` | Điều quan trọng cần làm để phòng ngừa viêm xoang là gì? | `xoang` | `xoang` | `label_proposed` | Câu hỏi trực tiếp về phòng ngừa bệnh viêm xoang mũi. Nội dung tường minh. |
| **04** | `ViHealthQA:train:3338` | Có nên cắt viêm amidan không? | `hong_amidan` | `hong_amidan` | `label_proposed` | Câu hỏi trực tiếp về can thiệp thủ thuật viêm amidan vùng họng miệng. |
| **05** | `ViMQ:train:1239` | Trẻ 1 tuổi bị viêm tai giữa phải làm sao? | `trieu_chung_tai` | `trieu_chung_tai` | `label_proposed` | Câu hỏi trực tiếp về bệnh lý viêm tai giữa khu trú ở tai. |
| **06** | `ViMQ:train:6945` | Làm thế nào để phân biệt cảm lạnh do thời tiết hay mắc các bệnh về đường hô hấp? | `cam_lanh` | `cam_lanh` | `label_proposed` | Trọng tâm tìm hiểu để nhận diện bệnh cảnh cảm lạnh so với bệnh hô hấp chung. |
| **07** | `ViMQ:test:151` | Bệnh cúm thường kéo dài bao lâu? | `cam_cum` | `cam_cum` | `label_proposed` | Câu hỏi trực tiếp về diễn tiến thời gian của bệnh cúm. |
| **08** | `ViHealthQA:train:5674` | Thường xuyên bị sốt phải điều trị như thế nào? | `sot` | `sot` | `label_proposed` | Triệu chứng sốt tái diễn đơn thuần, không có triệu chứng cơ quan khác đi kèm. |
| **09** | `ViHealthQA:test:1492` | Rò rỉ nhẹ động mạch xoang hang có nguy hiểm không? | `xoang` | *(để trống)* | `excluded_proposed` | **Từ đồng âm ngoài TMH**: "Xoang hang" là cấu trúc mạch máu màng cứng sọ não, không phải xoang cạnh mũi TMH. Đề xuất loại trừ. |
| **10** | `ViMedAQA:train:body-part_4327` | Rãnh nào nằm ở giữa rãnh nhị thân và rãnh xoang xích ma? | `xoang` | *(để trống)* | `needs_discussion` | **Ngữ cảnh giải phẫu sọ não**: Câu hỏi về rãnh xương sọ ("xoang xích ma"). Không gán nhãn xoang chỉ vì trùng từ khóa; chưa đủ quy tắc để khẳng định câu hỏi giải phẫu có thuộc phạm vi hay loại trừ hoàn toàn. |
| **11** | `ViMQ:train:4065` | Viêm xoang kèm chảy mủ ở tai báo là dấu hiệu bệnh gì? | `xoang` | *(để trống)* | `needs_discussion` | **Đa triệu chứng phức tạp (xoang + tai)**: Câu hỏi hỏi mối liên hệ giữa hai bệnh cảnh, không có căn cứ coi cơ quan nào là phụ. Phân vân giữa `xoang` và `trieu_chung_tai`. |
| **12** | `ViMQ:train:5732` | Người có tiền sử viêm xoang bị đau đầu và đau gáy nên điều trị thế nào? | `xoang` | *(để trống)* | `needs_discussion` | **Tiền sử vs Hiện tại**: Viêm xoang chỉ là tiền sử làm nền; vấn đề cần trị là "đau đầu đau gáy" (ngoài TMH). Cần thảo luận phạm vi để quyết định tiếp nhận hay loại trừ. |
| **13** | `ViMQ:train:2618` | Bé không ho hay ngạt mũi nhưng bị sốt có sao không? | *(trống)* | `sot` | `label_proposed` | **Ngữ cảnh phủ định**: Ho và ngạt mũi bị phủ định ("không ho hay ngạt mũi"), triệu chứng khẳng định duy nhất là "bị sốt". Đề xuất nhãn `sot`. |
| **14** | `ViMQ:test:239` | Trẻ sốt cao, đau đầu, viêm họng cấp nhưng không đau họng là bị làm sao? | *(trống)* | *(để trống)* | `needs_discussion` | **Phân loại nội dung câu hỏi**: Câu hỏi đề cập viêm họng cấp, sốt cao và đau đầu. Chưa rõ trọng tâm phân loại giữa `hong_amidan` và `sot`. Không nhận định tính đúng sai của chẩn đoán lâm sàng. |
| **15** | `ViMedAQA:train:disease_1587` | Bệnh cúm khác cảm lạnh ở những điểm nào? | *(trống)* | *(để trống)* | `needs_discussion` | **So sánh cân bằng 2 bệnh**: Câu hỏi so sánh trực tiếp và bình đẳng giữa `cam_cum` và `cam_lanh`. Cần thống nhất quy tắc xử lý câu hỏi so sánh trong bài toán đơn nhãn (không tự chuyển dự án sang đa nhãn). |
| **16** | `ViMedAQA:validation:disease_2616` | Ho kéo dài liên quan chảy dịch mũi sau có thể cải thiện khi sử dụng loại thuốc nào? | *(trống)* | *(để trống)* | `needs_discussion` | **Căn nguyên vs Phàn nàn**: Giằng co giữa triệu chứng cần cải thiện ("ho kéo dài" - `ho_dom`) và cơ chế nguyên nhân ("chảy dịch mũi sau" - `trieu_chung_mui`). |
| **17** | `ViHealthQA:train:1052` | Đau họng kèm có đờm có phải viêm amidan không? | *(trống)* | `hong_amidan` | `label_proposed` | **Nghi vấn trọng tâm**: Người hỏi chủ động hướng nghi vấn vào bệnh cảnh "viêm amidan" khi thấy đau họng và đờm. Quy tụ về `hong_amidan`. |
| **18** | `ViHealthQA:train:1216` | Cách đây 3 hôm, tôi bị cảm lạnh và viêm họng nên đã uống thuốc để điều trị. Tôi hết các triệu chứng đau người nên dừng thuốc. Tuy nhiên, do họng vẫn viêm nên tôi có sử dụng viên ngậm hàng ngày. Theo lịch ngày mai tôi thực hiện tiêm vaccine Covid-19, như vậy tôi có tiêm được không hay phải hoãn. (Hiện tại họng tôi vẫn đang hơi có cảm giác đau rát). | *(trống)* | *(để trống)* | `needs_discussion` | **Phạm vi tiêm chủng**: Câu hỏi chính là về chỉ định tiêm vaccine Covid-19 khi còn đau rát họng. Phân vân giữa `hong_amidan` và `excluded_proposed`. |
| **19** | `ViMedAQA:train:disease_12172` | Có phải tất cả các trường hợp bị ung thư ống mật đều gây sốt? | `sot` | *(để trống)* | `excluded_proposed` | **Ngoài phạm vi TMH**: Bệnh lý ung thư gan mật tiêu hóa, không thuộc phạm vi chuyên khoa TMH. Không ép nhãn chỉ vì xuất hiện từ "sốt". |
| **20** | `ViMedAQA:train:body-part_2016` | Đặc điểm cấu tạo của mao mạch không liên tục là gì? | *(trống)* | *(để trống)* | `excluded_proposed` | **Ngoài phạm vi TMH**: Câu hỏi thuần túy lý thuyết mô học - giải phẫu hệ tuần hoàn chung, hoàn toàn không có triệu chứng TMH. |

---

## 2. Thống kê tổng hợp lượt duyệt đề xuất AI

### 2.1. Phân bố theo trạng thái đề xuất

| Trạng thái đề xuất (`proposed_review_status`) | Số lượng câu | Tỷ lệ (%) | Ý nghĩa |
| :--- | :---: | :---: | :--- |
| `label_proposed` | 10 | 50.0% | Đã xác định được 1 nhãn chính rõ ràng theo quy tắc |
| `needs_discussion` | 7 | 35.0% | Chưa thể chốt 1 nhãn đơn nhất, cần thảo luận hoặc đặt câu hỏi bổ sung |
| `excluded_proposed` | 3 | 15.0% | Rõ ràng ngoài phạm vi chuyên khoa Tai Mũi Họng |
| **Tổng cộng** | **20** | **100%** | |

### 2.2. Phân bố nhãn trong nhóm `label_proposed` (10 câu)

| Nhãn chủ đề | Số câu đề xuất | Danh sách mã ID |
| :--- | :---: | :--- |
| `hong_amidan` | 2 | `ViHealthQA:train:3338`, `ViHealthQA:train:1052` |
| `sot` | 2 | `ViHealthQA:train:5674`, `ViMQ:train:2618` |
| `ho_dom` | 1 | `ViHealthQA:test:454` |
| `trieu_chung_mui` | 1 | `ViMQ:train:1459` |
| `xoang` | 1 | `ViMedAQA:train:disease_13292` |
| `trieu_chung_tai` | 1 | `ViMQ:train:1239` |
| `cam_lanh` | 1 | `ViMQ:train:6945` |
| `cam_cum` | 1 | `ViMQ:test:151` |
| **Tổng cộng** | **10** | **Bao phủ đủ 8/8 nhãn trong danh mục khởi đầu** |

---

## 3. Các câu AI đề xuất khác với nhãn gợi ý tự động ban đầu

Trong 20 câu, có **12 câu** AI đưa ra đánh giá khác biệt hoặc bổ sung so với nhãn gợi ý tự động ban đầu:

1. **Câu 09 (`ViHealthQA:test:1492`):** Gợi ý ban đầu `xoang` $\rightarrow$ AI đề xuất `excluded_proposed`.  
   *Lý do:* Nguồn gợi ý bằng từ khóa nhận diện nhầm từ đồng âm "xoang hang" (mạch máu sọ não).
2. **Câu 10 (`ViMedAQA:train:body-part_4327`):** Gợi ý ban đầu `xoang` $\rightarrow$ AI đề xuất `needs_discussion`.  
   *Lý do:* Ngữ cảnh giải phẫu mạch máu xương sọ; không gán xoang máy móc và chưa đủ quy tắc để loại trừ hoàn toàn.
3. **Câu 11 (`ViMQ:train:4065`):** Gợi ý ban đầu `xoang` $\rightarrow$ AI đề xuất `needs_discussion`.  
   *Lý do:* Câu hỏi liên quan cả viêm xoang và chảy mủ tai, không có căn cứ ưu tiên cơ quan nào.
4. **Câu 12 (`ViMQ:train:5732`):** Gợi ý ban đầu `xoang` $\rightarrow$ AI đề xuất `needs_discussion`.  
   *Lý do:* Viêm xoang chỉ là tiền sử làm nền; triệu chứng hiện tại là đau đầu đau gáy.
5. **Câu 13 (`ViMQ:train:2618`):** Gợi ý ban đầu để trống `""` $\rightarrow$ AI đề xuất `sot`.  
   *Lý do:* Nhận diện cấu trúc phủ định ("không ho ngạt mũi nhưng sốt") để chọn đúng trọng tâm.
6. **Câu 14 (`ViMQ:test:239`):** Gợi ý ban đầu để trống `""` $\rightarrow$ AI đề xuất `needs_discussion`.  
   *Lý do:* Câu hỏi đề cập viêm họng cấp, sốt cao và đau đầu; chưa rõ trọng tâm phân loại giữa hong_amidan và sot. Không phán xét tính đúng sai của chẩn đoán lâm sàng.
7. **Câu 15 (`ViMedAQA:train:disease_1587`):** Gợi ý ban đầu để trống `""` $\rightarrow$ AI đề xuất `needs_discussion`.  
   *Lý do:* So sánh bình đẳng giữa 2 chủ đề cúm và cảm lạnh. Cần thống nhất quy tắc cho câu hỏi so sánh trong bài toán đơn nhãn.
8. **Câu 16 (`ViMedAQA:validation:disease_2616`):** Gợi ý ban đầu để trống `""` $\rightarrow$ AI đề xuất `needs_discussion`.  
   *Lý do:* Giằng co giữa triệu chứng phàn nàn (ho kéo dài) và nguyên nhân (chảy dịch mũi sau).
9. **Câu 17 (`ViHealthQA:train:1052`):** Gợi ý ban đầu để trống `""` $\rightarrow$ AI đề xuất `hong_amidan`.  
   *Lý do:* Nhận diện câu hỏi nghi vấn hướng trực tiếp vào bệnh cảnh viêm amidan.
10. **Câu 18 (`ViHealthQA:train:1216`):** Gợi ý ban đầu để trống `""` $\rightarrow$ AI đề xuất `needs_discussion`.  
    *Lý do:* Câu hỏi dài có tiền sử, vấn đề chính là chỉ định tiêm vaccine Covid-19 khi họng rát.
11. **Câu 19 (`ViMedAQA:train:disease_12172`):** Gợi ý ban đầu `sot` $\rightarrow$ AI đề xuất `excluded_proposed`.  
    *Lý do:* Bệnh ung thư ống mật thuộc chuyên khoa tiêu hóa - gan mật, ngoài phạm vi TMH.
12. **Câu 20 (`ViMedAQA:train:body-part_2016`):** Gợi ý ban đầu để trống `""` $\rightarrow$ AI đề xuất `excluded_proposed`.  
    *Lý do:* Câu hỏi mô học mao mạch tuần hoàn đại cương, ngoài phạm vi TMH.

---

## 4. Các ranh giới quy tắc cần người dùng và chuyên gia thống nhất

1. **Quy tắc cho câu hỏi giải phẫu học cơ thể / sọ não (Câu 10):** Xác định rõ tiêu chí tiếp nhận hay loại trừ đối với các câu hỏi thuần giải phẫu lý thuyết xương sọ / mạch máu khi có từ đồng âm.
2. **Quy tắc cho câu hỏi so sánh hai bệnh lý (Câu 15):** Thống nhất quy tắc xử lý câu hỏi so sánh giữa hai chủ đề hợp lệ trong bài toán phân loại đơn nhãn (không tự ý chuyển dự án sang đa nhãn).
3. **Quy tắc cho câu hỏi đề cập nhiều biểu hiện kết hợp (Câu 14):** Xác định trọng tâm phân loại giữa bệnh lý cơ quan được nhắc đến (`hong_amidan`) và phản ứng toàn thân (`sot`).
4. **Quy tắc cho ca đa cơ quan liên quan biến chứng (Câu 11):** Khi có hai cơ quan cùng xuất hiện (Xoang và Tai), nên ưu tiên cơ quan căn nguyên hay cơ quan đang có triệu chứng cấp tính (chảy mủ)?
5. **Quy tắc tiền sử ngoài TMH (Câu 12):** Khi câu hỏi nêu tiền sử TMH nhưng triệu chứng hiện tại thuộc chuyên khoa khác (đau đầu gáy), nên loại trừ khỏi TMH hay đánh dấu cần tư vấn liên chuyên khoa?
6. **Hội chứng chảy dịch mũi sau gây ho (Câu 16):** Ưu tiên triệu chứng người bệnh muốn dùng thuốc cải thiện (`ho_dom`) hay nguyên nhân sinh bệnh (`trieu_chung_mui`)?
7. **Điều kiện tiêm chủng vaccine (Câu 18):** Các câu hỏi về chống chỉ định tiêm vaccine khi có triệu chứng TMH nhẹ nên gán theo triệu chứng TMH hay loại trừ vì thuộc quy trình tiêm chủng dịch tễ?

---

## 5. Tệp lưu trữ kết quả đề xuất

Dữ liệu chi tiết của lượt duyệt đề xuất này đã được lưu độc lập tại:
- Bảng CSV: [batch_01_ai_review.csv](../../02_du_lieu/filedata/reviewed/ai_proposals/batch_01_ai_review.csv)
- Dữ liệu JSONL: [batch_01_ai_review.jsonl](../../02_du_lieu/filedata/reviewed/ai_proposals/batch_01_ai_review.jsonl)
- Manifest xác thực: [batch_01_ai_manifest.json](../../02_du_lieu/filedata/reviewed/ai_proposals/batch_01_ai_manifest.json)

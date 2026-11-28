# Phiếu duyệt nhãn đợt 2 (100 câu còn lại tập Pilot - Phiên bản V4)

Phiên bản tài liệu: **4.0 (Bộ đề xuất AI chuẩn hóa V4 dành cho người duyệt)**  
Ngày cập nhật: **28/11/2026**  
Dự án: **BacSiAi (Phân loại câu hỏi y tế Tai Mũi Họng)**  
Tài liệu tham chiếu: [HUONG_DAN_GAN_NHAN.md](HUONG_DAN_GAN_NHAN.md), [QUY_UOC_LUU_TRU.md](QUY_UOC_LUU_TRU.md), [remaining_100_ai_manifest_v4.json](../02_du_lieu/filedata/reviewed/ai_proposals/remaining_100_ai_manifest_v4.json), [questions_working.csv](../02_du_lieu/filedata/reviewed/working/questions_working.csv).

> [!IMPORTANT]
> **Nguyên tắc thẩm định và bảo toàn dữ liệu:**
> 1. Toàn bộ nội dung trong cột/mục **Đề xuất AI** ở phiếu này chỉ là **tham khảo kỹ thuật sơ bộ**, hoàn toàn **chưa phải là quyết định chính thức (gold label) của con người hay chuyên gia y tế**.
> 2. Các ô **`[Chờ điền]`** được thiết kế để người duyệt xem xét và trực tiếp đưa ra quyết định xác nhận cuối cùng.
> 3. Ký hiệu **`[Chờ điền]`** chỉ dùng để trình bày vị trí trên tài liệu Markdown này. **Tuyệt đối không chép chuỗi ký tự "[Chờ điền]" vào tệp CSV làm việc**.
> 4. Người duyệt `hoai_an` xác nhận “duyệt hết” đề xuất hiện tại ngày `2026-11-28`. Riêng 100 câu trong phiếu: **58 reviewed, 26 excluded, 16 needs_discussion, 0 pending**. Toàn bộ pilot: **70 reviewed, 33 excluded, 17 needs_discussion, 0 pending**. Dữ liệu đã xuất bản chính thức tại [v4_user_accepted_20261128](../02_du_lieu/filedata/reviewed/annotations/v4_user_accepted_20261128/). Các câu `needs_discussion` (17 câu trên toàn bộ pilot) nhãn chuẩn để trống, chưa có nhãn train. Đây là việc người duyệt chấp thuận đề xuất AI về chủ đề, không phải chuyên gia y tế xác minh nội dung y khoa. Cỡ mẫu 70 câu có nhãn chưa đủ điều kiện để bắt đầu huấn luyện hay so sánh 5 mô hình.

---

## 1. Thông tin người duyệt và ngày duyệt

- **Mã định danh người duyệt (`reviewer_id`):** `[hoai_an]` *(người duyệt điền khi xác nhận)*
- **Ngày duyệt thực tế (`reviewed_at`):** `[2026-11-28]` *(định dạng YYYY-MM-DD)*

---

## 2. Thống kê thực tế bộ đề xuất V4 (100 câu)

- **Tổng số câu:** 100 câu (STT cố định 001 – 100, gồm 58 câu đã chấp thuận nhãn, 26 câu đã loại và 16 câu đã xác nhận giữ thảo luận).
- **Nhóm `label_proposed` (58 câu):** Đề xuất có nhãn đơn rõ ràng theo hướng dẫn gán nhãn:
  - `hong_amidan`: 12 câu
  - `trieu_chung_tai`: 10 câu
  - `ho_dom`: 8 câu
  - `xoang`: 7 câu
  - `cam_lanh`: 7 câu
  - `trieu_chung_mui`: 7 câu
  - `cam_cum`: 6 câu
  - `sot`: 1 câu
- **Nhóm `excluded_proposed` (26 câu):** Đề xuất loại khỏi phạm vi chuyên khoa TMH (bao gồm các câu tiêm chủng Covid-19 có bệnh nền TMH chỉ là tiền sử, dược liệu cổ truyền đại cương, câu hỏi chuyên khoa Thần kinh/Răng Hàm Mặt/Truyền nhiễm).
- **Nhóm `needs_discussion` (16 câu):** Các câu hỏi đa triệu chứng phức tạp hoặc hai vấn đề ngang hàng chưa thể ép nhãn đơn mà cần người duyệt quyết định (bao gồm câu 015, 027, 051 mới chuyển về thảo luận theo góp ý của người duyệt).
- **Số câu cần hỏi bổ sung (`needs_clarification = True`):** 4 câu (STT 009, 011, 012, 015).

---

## 3. Danh mục 8 nhãn hợp lệ và giải thích dễ hiểu

| Mã nhãn | Ý nghĩa chuyên khoa | Giải thích dễ hiểu |
| :--- | :--- | :--- |
| `ho_dom` | Ho và đờm | Các câu hỏi tập trung vào cơn ho (ho khan, ho có đờm, ho lâu ngày, ho ra máu) và tính chất đờm (đờm đặc, đờm xanh, vướng đờm). |
| `trieu_chung_mui` | Triệu chứng mũi, viêm mũi | Các vấn đề tại mũi: nghẹt mũi, sổ mũi (chảy nước mũi), hắt hơi, ngứa mũi, viêm mũi dị ứng, chảy máu cam. |
| `xoang` | Xoang và viêm xoang | Câu hỏi có trực tiếp nhắc đến xoang, bệnh viêm xoang (xoang trán, hàm, sàng, bướm, đa xoang) hoặc phẫu thuật/xông xoang. |
| `hong_amidan` | Họng, amidan, thanh quản | Đau rát họng, viêm họng hạt, sưng amidan, viêm amidan mủ, sỏi amidan, nuốt vướng, nuốt đau, khản tiếng, dị vật họng (hóc xương). |
| `trieu_chung_tai` | Tai và thính lực | Đau tai, viêm tai giữa, viêm tai ngoài, chảy mủ tai, ù tai, giảm thính lực, ngứa tai, ráy tai, chấn thương màng nhĩ. |
| `cam_lanh` | Cảm lạnh, cảm mạo | Câu hỏi trực tiếp về cảm lạnh, cảm mạo do gió, thời tiết, dầm mưa (thường không sốt cao, tự giới hạn sau vài ngày). |
| `cam_cum` | Cúm mùa, vi-rút cúm | Câu hỏi trực tiếp về bệnh cúm (cúm mùa, cúm A, cúm gia cầm), di chứng cúm, thuốc trị cúm, vắc-xin phòng cúm mùa. |
| `sot` | Sốt đơn thuần | Triệu chứng sốt cao, sốt tái diễn, sốt phát ban chưa định khu vào một cơ quan TMH cụ thể. |

---

<!-- pending-review-index:start -->
## Tra nhanh đề xuất trước khi xác nhận (lưu để đối chiếu)

**Lịch sử trước xác nhận duyệt toàn bộ, không phải trạng thái hiện tại.** Ảnh chụp sau yêu cầu loại câu ngoài phạm vi: **74 câu chưa duyệt**, gồm **58 câu có nhãn AI đề xuất** và **16 câu cần quyết định riêng**. Đây chưa phải xác nhận nhãn của người duyệt.

| Nhãn AI đề xuất | STT chưa duyệt |
| --- | --- |
| `cam_cum` | 025, 039, 046, 071, 075, 085 |
| `cam_lanh` | 019, 076, 079, 094, 095, 096, 097 |
| `ho_dom` | 004, 033, 043, 052, 084, 088, 089, 091 |
| `hong_amidan` | 009, 020, 030, 034, 041, 048, 062, 063, 064, 072, 077, 081 |
| `sot` | 016 |
| `trieu_chung_mui` | 031, 038, 040, 044, 065, 066, 083 |
| `trieu_chung_tai` | 002, 024, 032, 037, 059, 060, 061, 070, 078, 100 |
| `xoang` | 011, 049, 055, 056, 067, 068, 069 |

**16 câu cần quyết định riêng:**

| STT | Nguyên văn câu hỏi | Chủ đề liên quan, chỉ để tham khảo |
| --- | --- | --- |
| 005 | Bị ho và cổ họng sưng, có vài vết trắng có phải dấu hiệu bệnh bạch hầu không? | `ho_dom`, `hong_amidan` |
| 012 | Nghẹt mũi, nuốt vướng kèm khó thở kéo dài có nguy cơ mắc bệnh gì? | `trieu_chung_mui`, `hong_amidan` |
| 014 | Sốt nhẹ, ho và khô cổ có phải là dấu hiệu nhiễm covid không? | `sot`, `ho_dom`, `hong_amidan` |
| 015 | Lần trước em có hỏi em bị dị ứng cua có lần đi cấp cứu, bị dị ứng thuốc mắt sưng khó thở. Em được bác sĩ tư vấn là thuộc đối tượng chống chị định tiêm tại QĐ 2995/QĐ-BYT. Bác sĩ cho em hỏi em không được tiêm luôn vaccine Covid-19 hay là đợi khi nào có hướng dẫn mới của Bộ Y tế? Năm 2020 em có tiêm vaccine cúm mùa thì bình thường. Vậy hàng năm em có nên tiếp tục tiêm vaccine cúm mùa được không? | `cam_cum` |
| 021 | Thường xuyên bị xây xẩm mặt mày, cứng hàm, đỏ mặt, ù tai phải làm sao? | `trieu_chung_tai` |
| 027 | Viêm xoang trán kèm viêm mũi dị ứng hay tái phát phải làm sao? | `xoang`, `trieu_chung_mui` |
| 028 | Lao hạch dưới hàm phát triển có gây ra ho khan không? | `ho_dom` |
| 035 | Hạch cổ gây sốt, ngày càng sưng to gây mất ngủ về đêm, khát nước khô họng có sao không ạ? | `sot`, `hong_amidan` |
| 036 | Mắc viêm họng hạt kèm theo hiện tượng chảy máu mũi, ù tai là dấu hiệu bệnh gì? | `hong_amidan`, `trieu_chung_mui`, `trieu_chung_tai` |
| 042 | Mẹ bị sốt, đau họng, ho có thể làm xét nghiệm gì để con không bị lây nhiễm? | `sot`, `hong_amidan`, `ho_dom` |
| 045 | Đau rát họng, ho khan, thở khò khè, hít thở nặng đau lồng ngực là bệnh gì? | `hong_amidan`, `ho_dom` |
| 047 | Đau thái dương hàm kèm theo khó nuốt và nuốt đau là bệnh gì? | `hong_amidan` |
| 050 | Viêm amidan kèm nhức, ù tai, đau cổ họng có liên quan đến ung thư vòm họng không? | `hong_amidan`, `trieu_chung_tai` |
| 051 | Trẻ sốt kèm đi tiểu phải rặn có sao không? | `sot` |
| 054 | Trẻ thường xuyên ho, nghẹt mũi khi thay đổi thời tiết phải điều trị thế nào? | `ho_dom`, `trieu_chung_mui` |
| 086 | Cây Xuyên tâm liên có tác dụng gì trong điều trị cảm sốt và viêm xoang? | `cam_lanh`, `cam_cum`, `sot`, `xoang` |

Có thể xác nhận theo nhóm hoặc theo từng STT. Không bắt buộc chọn một nhãn khi chưa rõ trọng tâm; câu nhiều chủ đề vẫn có thể được hỗ trợ hỏi đáp kết hợp nguồn. Chi tiết và ô quyết định giữ tại mục 4 bên dưới.

<!-- pending-review-index:end -->

## 4. Danh sách chi tiết 100 câu hỏi kèm đề xuất AI và ô xác nhận

> Mỗi câu hỏi dưới đây được trình bày độc lập, đầy đủ nguyên văn và tách riêng với lời diễn đạt đời thường. Đã ghi các quyết định theo xác nhận của người duyệt; 16 câu giữ thảo luận chưa có nhãn train.

### Câu 001 — `ViHealthQA:test:239` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi vừa hết sốt xuất huyết Dengue có thể tiêm vaccine Covid-19 không thưa bác sĩ?
- **Diễn đạt đời thường:** Người hỏi vừa khỏi bệnh sốt xuất huyết Dengue, muốn biết hiện tại có thể tiêm vắc-xin ngừa Covid-19 được không.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi thuộc chuyên khoa truyền nhiễm và quy trình tiêm chủng vắc-xin Covid-19 sau sốt xuất huyết Dengue; hoàn toàn ngoài phạm vi bệnh lý Tai Mũi Họng.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 002 — `ViHealthQA:test:517` (ViHealthQA)
- **Nguyên văn câu hỏi:** Rối loạn tiền đình kèm ù tai phải làm sao?
- **Diễn đạt đời thường:** Người hỏi bị rối loạn tiền đình kèm theo triệu chứng ù tai, muốn biết hướng xử trí.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_tai`
- **Lý do đề xuất:** Triệu chứng ù tai khu trú trực tiếp tại cơ quan tai, liên quan đến hệ thống ốc tai - tiền đình thuộc nhóm triệu chứng tai.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_tai` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 003 — `ViHealthQA:train:114` (ViHealthQA)
- **Nguyên văn câu hỏi:** cách đây 2 năm khi cắt chỉ từ vết mổ khối áp xe ở tay, em bị co giật 3 tiếng, dù trước đó bác sĩ không tiêm kháng sinh, chỉ dùng thuốc tê. Em tỉnh táo nhưng chân tay bên phải giật rung bần bật (áp xe ở tay trái). Ngoài ra e bị một số dị ứng như da thường tự nhiên bị đỏ ngứa từng đám, viêm mũi dị ứng quanh năm. Em cũng bị huyết áp thấp và thỉnh thoảng rối loạn tiền đình. Vậy em xin hỏi có bị hạn chế tiêm vaccine Covid-19 của AstraZeneka không ạ?
- **Diễn đạt đời thường:** Người hỏi có tiền sử co giật sau cắt chỉ vết mổ, viêm mũi dị ứng quanh năm, huyết áp thấp và rối loạn tiền đình; thắc mắc có bị hạn chế tiêm vắc-xin Covid-19 AstraZeneca không.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Trọng tâm hỏi là hạn chế tiêm vắc-xin Covid-19 AstraZeneca trên người nhiều bệnh nền; viêm mũi dị ứng chỉ là bệnh nền/tiền sử.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 004 — `ViHealthQA:train:1345` (ViHealthQA)
- **Nguyên văn câu hỏi:** Người cao tuổi điều trị ho mãn tính lâu năm như thế nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết cách điều trị ho mãn tính lâu năm ở người cao tuổi.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `ho_dom`
- **Lý do đề xuất:** Câu hỏi hỏi trực tiếp về điều trị chứng ho mãn tính kéo dài, thuộc chủ đề ho và đờm.
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `ho_dom` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 005 — `ViHealthQA:train:1681` (ViHealthQA)
- **Nguyên văn câu hỏi:** Bị ho và cổ họng sưng, có vài vết trắng có phải dấu hiệu bệnh bạch hầu không?
- **Diễn đạt đời thường:** Người hỏi bị ho, cổ họng sưng và có vài vết trắng; thắc mắc đây có phải là dấu hiệu của bệnh bạch hầu không.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi kết hợp triệu chứng ho và tổn thương họng sưng có màng trắng nghi bạch hầu; có sự giằng co giữa ho_dom và hong_amidan.
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`, `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Cần thảo luận gán theo tổn thương thực thể vùng họng (hong_amidan) hay phản xạ ho (ho_dom).

### Câu 006 — `ViHealthQA:train:2120` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi bị viêm xoang, dị ứng hải sản, khi ăn vào sẽ bị ngứa mẩn đỏ. Vậy tôi có tiêm vaccine được không ạ?
- **Diễn đạt đời thường:** Người hỏi có bệnh viêm xoang và cơ địa dị ứng hải sản (ăn vào bị ngứa mẩn đỏ); muốn biết có tiêm được vắc-xin ngừa Covid-19 không.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Trọng tâm hỏi là điều kiện tiêm vắc-xin Covid-19 trên người có cơ địa dị ứng; viêm xoang chỉ là bệnh nền.
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 007 — `ViHealthQA:train:2322` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi bị viêm xoang, tiền căn từ viêm mũi dị ứng. 1 năm rưỡi trước tôi có từng bị hạ canxi. Vậy tôi có thể chích ngừa vaccine Covid-19 được không?
- **Diễn đạt đời thường:** Người hỏi bị viêm xoang có tiền căn từ viêm mũi dị ứng và từng bị hạ canxi; thắc mắc có thể chích ngừa vắc-xin Covid-19 không.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Trọng tâm hỏi là chích ngừa vắc-xin Covid-19; viêm xoang và viêm mũi dị ứng là bệnh nền/tiền căn.
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`, `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 008 — `ViHealthQA:train:2593` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi thường bị dị ứng thuốc khi uống thuốc điều trị cảm cúm, triệu chứng gồm nóng, ngứa, sưng phù mắt, khó thở. Mỗi lần bị dị ứng, tôi uống thuốc điều trị dị ứng, khoảng một ngày là trở lại bình thường. Tôi có tiêm được vaccine Covid-19 không?
- **Diễn đạt đời thường:** Người hỏi hay bị dị ứng khi uống thuốc cảm cúm (nóng, ngứa, sưng phù mắt, khó thở); muốn biết có tiêm được vắc-xin Covid-19 không.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Trọng tâm hỏi là tiêm vắc-xin Covid-19; dị ứng thuốc cảm cúm là tiền sử phản ứng thuốc.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_cum`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 009 — `ViHealthQA:train:2976` (ViHealthQA)
- **Nguyên văn câu hỏi:** Viêm amidan mủ mãn tính có cần cắt ngay hay đợi hết viêm rồi cắt?
- **Diễn đạt đời thường:** Người hỏi thắc mắc bệnh viêm amidan mủ mãn tính thì có cần phẫu thuật cắt ngay hay phải đợi hết viêm rồi mới cắt.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Hỏi trực tiếp về thời điểm chỉ định phẫu thuật cắt amidan mủ, thuộc chủ đề hong_amidan.
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`
- **Hỏi bổ sung thông tin:** **Có** — *"Bạn đã được bác sĩ chuyên khoa Tai Mũi Họng khám trực tiếp và đưa ra chỉ định cắt amidan cụ thể nào chưa?"*
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 010 — `ViHealthQA:train:2986` (ViHealthQA)
- **Nguyên văn câu hỏi:** Em bị rối loạn tiền đình, viêm gan b, viêm xoang mãn tính, đang cho con bú vậy em tiêm vaccine Covid-19 được không?
- **Diễn đạt đời thường:** Người hỏi đang cho con bú, có tiền sử rối loạn tiền đình, viêm gan B và viêm xoang mãn tính; thắc mắc có tiêm vắc-xin Covid-19 được không.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Trọng tâm hỏi là tiêm vắc-xin Covid-19 cho phụ nữ cho con bú có bệnh nền toàn thân; viêm xoang chỉ là chi tiết phụ.
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 011 — `ViHealthQA:train:3916` (ViHealthQA)
- **Nguyên văn câu hỏi:** Bệnh nhân tiểu đường type II có phẫu thuật viêm xoang được không?
- **Diễn đạt đời thường:** Người hỏi muốn biết bệnh nhân mắc tiểu đường type 2 thì có thể thực hiện phẫu thuật điều trị viêm xoang được không.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `xoang`
- **Lý do đề xuất:** Hỏi về điều kiện can thiệp phẫu thuật điều trị bệnh lý viêm xoang trên nền bệnh tiểu đường, thuộc chủ đề xoang.
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`
- **Hỏi bổ sung thông tin:** **Có** — *"Bạn đang hỏi thông tin chung hay cho một người cụ thể? Nếu là trường hợp cụ thể, bác sĩ đã khám và đề nghị phẫu thuật chưa?"*
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `xoang` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 012 — `ViHealthQA:train:4208` (ViHealthQA)
- **Nguyên văn câu hỏi:** Nghẹt mũi, nuốt vướng kèm khó thở kéo dài có nguy cơ mắc bệnh gì?
- **Diễn đạt đời thường:** Người hỏi bị nghẹt mũi, cảm giác nuốt vướng và khó thở kéo dài; thắc mắc có nguy cơ mắc bệnh gì.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Xuất hiện đồng thời các triệu chứng ở hốc mũi (nghẹt mũi) và họng (nuốt vướng kèm khó thở kéo dài); có sự chồng lấn giữa trieu_chung_mui và hong_amidan.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`, `hong_amidan`
- **Hỏi bổ sung thông tin:** **Có** — *"Triệu chứng nghẹt mũi hay nuốt vướng gây khó chịu nhiều nhất cho bạn và tình trạng này đã kéo dài bao lâu?"*
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Đa triệu chứng kéo dài báo hiệu bệnh lý phức tạp vùng hầu họng mũi; cần thảo luận gán nhãn hoặc hỏi bổ sung trọng tâm.

### Câu 013 — `ViHealthQA:train:4273` (ViHealthQA)
- **Nguyên văn câu hỏi:** Em bị viêm xoang mãn tính nặng, thường ho ra máu vậy có thể tiêm vacine Covid -19 không ạ?
- **Diễn đạt đời thường:** Người hỏi bị viêm xoang mãn tính mức độ nặng và thường xuyên ho ra máu; thắc mắc có thể tiêm vắc-xin Covid-19 không.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Trọng tâm hỏi là tiêm vắc-xin Covid-19; viêm xoang mạn và ho ra máu là bệnh lý/triệu chứng nền.
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`, `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 014 — `ViHealthQA:train:4523` (ViHealthQA)
- **Nguyên văn câu hỏi:** Sốt nhẹ, ho và khô cổ có phải là dấu hiệu nhiễm covid không?
- **Diễn đạt đời thường:** Người hỏi thấy bị sốt nhẹ, ho và khô rát ở cổ họng; thắc mắc liệu đây có phải là dấu hiệu nhiễm Covid-19 không.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Bộ ba triệu chứng sốt nhẹ, ho, khô cổ xuất hiện ngang hàng trong bệnh cảnh nghi nhiễm Covid-19; chưa thể cô lập một nhãn duy nhất.
- **Chủ đề kết hợp khi hỏi đáp:** `sot`, `ho_dom`, `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Cần thảo luận chọn nhãn chủ đạo hoặc kết hợp nội dung truy xuất cả ba nhóm sốt, ho, họng.

### Câu 015 — `ViHealthQA:train:4743` (ViHealthQA)
- **Nguyên văn câu hỏi:** Lần trước em có hỏi em bị dị ứng cua có lần đi cấp cứu, bị dị ứng thuốc mắt sưng khó thở. Em được bác sĩ tư vấn là thuộc đối tượng chống chị định tiêm tại QĐ 2995/QĐ-BYT. Bác sĩ cho em hỏi em không được tiêm luôn vaccine Covid-19 hay là đợi khi nào có hướng dẫn mới của Bộ Y tế? Năm 2020 em có tiêm vaccine cúm mùa thì bình thường. Vậy hàng năm em có nên tiếp tục tiêm vaccine cúm mùa được không?
- **Diễn đạt đời thường:** Người hỏi có tiền sử dị ứng thuốc và thức ăn nặng; hỏi về hai vấn đề: có được tiêm vắc-xin Covid-19 không và hàng năm có nên tiếp tục tiêm vắc-xin cúm mùa không.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi chứa hai yêu cầu riêng biệt: hỏi về việc tiêm vắc-xin Covid-19 khi có tiền sử dị ứng và hỏi về việc tiếp tục tiêm vắc-xin phòng cúm mùa hàng năm. Chưa rõ trọng tâm đơn nhãn; cần làm rõ nhu cầu của người hỏi.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_cum`
- **Hỏi bổ sung thông tin:** **Có** — *"Bạn muốn tìm hiểu cả việc tiêm vaccine COVID-19 và tiêm cúm mùa, hay ưu tiên một vấn đề?"*
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Câu hỏi gồm hai yêu cầu hỏi riêng biệt (tiêm vắc-xin Covid-19 và tiêm vắc-xin cúm mùa), cần thảo luận chọn nhãn đơn hoặc làm rõ yêu cầu.

### Câu 016 — `ViHealthQA:train:484` (ViHealthQA)
- **Nguyên văn câu hỏi:** Sốt và phát ban là dấu hiệu của bệnh gì?
- **Diễn đạt đời thường:** Người hỏi muốn biết khi bị sốt kèm theo nổi phát ban trên da thì là dấu hiệu cảnh báo bệnh gì.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `sot`
- **Lý do đề xuất:** Triệu chứng toàn thân nổi bật là sốt đi kèm biểu hiện ngoài da (phát ban), thuộc chủ đề sot.
- **Chủ đề kết hợp khi hỏi đáp:** `sot`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `sot` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 017 — `ViHealthQA:train:5283` (ViHealthQA)
- **Nguyên văn câu hỏi:** Em bị viêm dạ dày cách đây 4 năm đã điều trị, lâu lâu có tái phát, đi bác sĩ khám có uống thuốc. Em cũng đang bị thoái hóa cột sống, rối loạn nhịp tim (do dịch bệnh phức tạp nên em chưa đi khám tim để tìm hiểu nguyên nhân rối loạn). Em ăn thịt gà và thịt bò bị ngứa, lâu lâu có nổi mề đay, hay bị nghẹt mũi từ lúc còn học phổ thông, vài tháng trước đi khám bác sĩ nói viêm mũi mãn tính. Vậy em có tiêm vaccine ngừa Covid-19 (AstraZeneca) được không ạ?
- **Diễn đạt đời thường:** Người hỏi có tiền sử viêm dạ dày, thoái hóa cột sống, rối loạn nhịp tim, dị ứng thức ăn và viêm mũi mãn tính; thắc mắc có tiêm được vắc-xin ngừa Covid-19 AstraZeneca không.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Trọng tâm hỏi là tiêm vắc-xin Covid-19 AstraZeneca trên người có nhiều bệnh nền toàn thân; viêm mũi mạn tính chỉ là một bệnh nền.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 018 — `ViHealthQA:train:610` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi đi tiêm vaccine ngừa Covid-19, gặp bác sĩ tư vấn trước khi tiêm, tôi có khai bị dị ứng thuộc viêm xoang và thuốc cảm sốt hai lần (mỗi lần điều trị hơn một tháng mới hết). Tôi có bệnh nền cao huyết áp, tiểu đường. Bác sĩ tư vấn nói tôi không thể tiêm ngừa được do bị dị ứng thuốc và có bệnh nền. Xin hỏi điều này có đúng không bác sĩ? Tôi cần làm gì để phòng bệnh ạ!
- **Diễn đạt đời thường:** Người hỏi đi tiêm vắc-xin Covid-19 bị bác sĩ tư vấn hoãn do tiền sử dị ứng thuốc viêm xoang và cảm sốt kèm bệnh nền cao huyết áp, tiểu đường; muốn hỏi việc tư vấn như vậy có đúng không và cách phòng bệnh.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Trọng tâm hỏi là quy trình tư vấn tiêm chủng vắc-xin Covid-19 khi có tiền sử dị ứng thuốc cảm sốt, viêm xoang.
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`, `sot`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 019 — `ViHealthQA:train:645` (ViHealthQA)
- **Nguyên văn câu hỏi:** Bị cảm lạnh, nóng trong người phải làm sao?
- **Diễn đạt đời thường:** Người hỏi bị cảm lạnh và có cảm giác nóng bức trong người; muốn biết cách xử trí.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_lanh`
- **Lý do đề xuất:** Câu hỏi trực tiếp về xử trí chứng cảm lạnh, thuộc nhóm bệnh cảnh cam_lanh.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_lanh`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_lanh` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 020 — `ViHealthQA:train:6824` (ViHealthQA)
- **Nguyên văn câu hỏi:** Amidan sưng to một bên, cổ họng nổi nhiều nốt có nguy hiểm không?
- **Diễn đạt đời thường:** Người hỏi thấy amidan bị sưng to một bên và cổ họng mọc nhiều nốt; lo lắng không biết có nguy hiểm không.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Tổn thương sưng to khu trú tại amidan và họng miệng, thuộc chủ đề hong_amidan.
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 021 — `ViHealthQA:train:6923` (ViHealthQA)
- **Nguyên văn câu hỏi:** Thường xuyên bị xây xẩm mặt mày, cứng hàm, đỏ mặt, ù tai phải làm sao?
- **Diễn đạt đời thường:** Người hỏi hay bị xây xẩm mặt mày, cứng hàm, đỏ mặt và ù tai; muốn biết hướng xử trí.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Tập hợp nhiều triệu chứng: xây xẩm, cứng hàm, đỏ mặt và ù tai; có yếu tố thần kinh mạch máu kết hợp triệu chứng tai.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Ù tai chỉ là một phần trong bệnh cảnh phức tạp; cần thảo luận gán nhãn trieu_chung_tai hay xếp vào nhóm cần thảo luận.

### Câu 022 — `ViHealthQA:train:6989` (ViHealthQA)
- **Nguyên văn câu hỏi:** Giảm Lym% khi bị sốt xuất huyết có sao không?
- **Diễn đạt đời thường:** Người hỏi thắc mắc chỉ số bạch cầu lympho (Lym%) bị giảm trong xét nghiệm máu khi mắc sốt xuất huyết thì có nguy hiểm không.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi chuyên sâu về xét nghiệm huyết học trong bệnh sốt xuất huyết (chuyên khoa Truyền nhiễm); hoàn toàn ngoài phạm vi TMH.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 023 — `ViHealthQA:train:891` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi bị viêm mũi dị ứng mãn tính (hơn 20 năm) vậy tôi có tiêm vaccine được không? Nếu được thì cần chú ý điều gì?
- **Diễn đạt đời thường:** Người hỏi bị viêm mũi dị ứng mãn tính hơn 20 năm; muốn biết có tiêm được vắc-xin Covid-19 không và cần lưu ý gì.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Trọng tâm hỏi là điều kiện tiêm vắc-xin Covid-19; viêm mũi dị ứng hơn 20 năm là bệnh nền.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 024 — `ViHealthQA:train:910` (ViHealthQA)
- **Nguyên văn câu hỏi:** Cách trị dứt điểm bệnh viêm tai giữa lâu ngày không khỏi?
- **Diễn đạt đời thường:** Người hỏi muốn biết cách chữa trị dứt điểm cho bệnh viêm tai giữa bị kéo dài lâu ngày không khỏi.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_tai`
- **Lý do đề xuất:** Hỏi trực tiếp về phương pháp điều trị dứt điểm bệnh viêm tai giữa dai dẳng, thuộc chủ đề trieu_chung_tai.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_tai` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 025 — `ViHealthQA:validation:547` (ViHealthQA)
- **Nguyên văn câu hỏi:** năm 2018 và năm 2019 tôi đến bệnh viện tiêm ngừa cảm cúm. Năm 2020 vừa rồi, tôi đến để xin tiêm tiếp nhưng lần này bệnh viện báo đã hết thuốc nên hẹn tôi hôm khác nhưng đến nay tôi vẫn chưa quay lại để tiêm ngừa cảm cúm. Ngày 19/6 rồi tôi đã tiêm vaccine Covid-19 mũi 1, như vậy thì sau bao lâu tôi mới tiêm vaccine cảm cúm được.
- **Diễn đạt đời thường:** Người hỏi đã tiêm vắc-xin Covid-19 mũi 1 được một thời gian; thắc mắc sau bao lâu thì có thể tiêm tiếp vắc-xin phòng cảm cúm.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_cum`
- **Lý do đề xuất:** Trọng tâm hỏi về khoảng thời gian cần thiết để được tiêm vắc-xin phòng bệnh cảm cúm.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_cum`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_cum` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 026 — `ViHealthQA:validation:624` (ViHealthQA)
- **Nguyên văn câu hỏi:** Lúc nhỏ, tôi có bị dị ứng thuốc kháng sinh dạng nổi mề đay nhưng tôi đã chích nhiều loại vaccine như viêm gan B, cảm cúm. Khi tôi chích ngừa những vaccine trên, cơ thể vẫn bình thường. Xin hỏi tôi có thể chích vaccine Covid-19 ở các điểm tiêm tập trung hay bệnh viện?
- **Diễn đạt đời thường:** Người hỏi có tiền sử dị ứng kháng sinh nổi mề đay nhưng trước đây từng tiêm vắc-xin viêm gan B và cúm bình thường; hỏi nên tiêm vắc-xin Covid-19 tại điểm tiêm cộng đồng hay tại bệnh viện.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Trọng tâm hỏi là lựa chọn địa điểm tiêm vắc-xin Covid-19 an toàn; tiền sử tiêm cúm chỉ là dữ liệu so sánh.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_cum`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 027 — `ViHealthQA:validation:883` (ViHealthQA)
- **Nguyên văn câu hỏi:** Viêm xoang trán kèm viêm mũi dị ứng hay tái phát phải làm sao?
- **Diễn đạt đời thường:** Người hỏi bị cả viêm xoang trán và viêm mũi dị ứng hay tái phát nhiều lần, muốn biết hướng xử trí.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Cả hai bệnh cảnh viêm xoang trán và viêm mũi dị ứng đều được đề cập ngang hàng trong câu hỏi, chưa có căn cứ rõ để ưu tiên một nhãn đơn trong bài toán phân loại. Khi hỏi đáp, hệ thống sẽ kết hợp nội dung của cả hai chủ đề.
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`, `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Đồng thời xuất hiện cả viêm xoang trán và viêm mũi dị ứng ngang hàng, chưa có căn cứ ưu tiên một nhãn đơn; cần thảo luận quyết định.

### Câu 028 — `ViMQ:test:225` (ViMQ)
- **Nguyên văn câu hỏi:** Lao hạch dưới hàm phát triển có gây ra ho khan không?
- **Diễn đạt đời thường:** Người hỏi muốn biết khi bị lao hạch dưới hàm phát triển thì có gây ra triệu chứng ho khan hay không.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi hỏi về mối liên hệ giữa bệnh lao hạch dưới hàm và triệu chứng ho khan. Cần thảo luận xem nên gán theo triệu chứng ho (ho_dom) hay loại trừ do bệnh lao hạch nằm ngoài chuyên khoa TMH.
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Có triệu chứng ho khan nhưng căn nguyên hỏi là bệnh lao hạch dưới hàm; cần thảo luận phạm vi.

### Câu 029 — `ViMQ:test:536` (ViMQ)
- **Nguyên văn câu hỏi:** Nên làm gì khi bị tắc tia sữa, có cục cứng ở ngực, không đau, không sốt?
- **Diễn đạt đời thường:** Người hỏi bị tắc tia sữa, sờ thấy cục cứng ở ngực nhưng không đau và không bị sốt; muốn biết nên xử trí thế nào.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi thuộc chuyên khoa Sản - Phụ khoa / tuyến vú; từ 'sốt' nằm trong cấu trúc phủ định ('không sốt'), hoàn toàn ngoài TMH.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 030 — `ViMQ:train:1003` (ViMQ)
- **Nguyên văn câu hỏi:** Đau họng kèm đổ mồ hôi về đêm là dấu hiệu của bệnh lý gì?
- **Diễn đạt đời thường:** Người hỏi bị đau ở họng kèm theo hiện tượng đổ mồ hôi trộm về ban đêm; thắc mắc đây là dấu hiệu của bệnh gì.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Triệu chứng chính tại cơ quan hô hấp trên là đau họng, thuộc chủ đề hong_amidan.
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 031 — `ViMQ:train:1955` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ sơ sinh khụt khịt khô, không chảy nước mũi là dấu hiệu bệnh gì?
- **Diễn đạt đời thường:** Người hỏi thấy trẻ sơ sinh thở khụt khịt khô trong mũi nhưng không thấy chảy nước mũi; thắc mắc là dấu hiệu bệnh gì.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_mui`
- **Lý do đề xuất:** Hỏi về tiếng thở khụt khịt tại hốc mũi ở trẻ sơ sinh dù không chảy nước mũi (giữ đúng phủ định), thuộc nhóm triệu chứng mũi.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_mui` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 032 — `ViMQ:train:2729` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ 30 tháng tuổi bị viêm tai giữa có điều trị được không?
- **Diễn đạt đời thường:** Người hỏi muốn biết trẻ nhỏ 30 tháng tuổi bị mắc viêm tai giữa thì có điều trị khỏi được không.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_tai`
- **Lý do đề xuất:** Câu hỏi về khả năng điều trị khỏi bệnh viêm tai giữa ở trẻ nhỏ, thuộc chủ đề trieu_chung_tai.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_tai` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 033 — `ViMQ:train:2755` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ 2 tháng tuổi bị ho có uống thuốc nam được không?
- **Diễn đạt đời thường:** Người hỏi muốn biết em bé 2 tháng tuổi bị ho thì có thể cho uống thuốc nam (thảo dược) được không.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `ho_dom`
- **Lý do đề xuất:** Câu hỏi hỏi về việc dùng thuốc khi trẻ sơ sinh bị ho, thuộc chủ đề ho và đờm.
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `ho_dom` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 034 — `ViMQ:train:2966` (ViMQ)
- **Nguyên văn câu hỏi:** Nuốt vướng ở cổ, có đờm mủ trong họng là dấu hiệu bệnh gì?
- **Diễn đạt đời thường:** Người hỏi thấy cảm giác nuốt vướng ở cổ và khạc thấy có đờm lẫn mủ trong họng; thắc mắc là dấu hiệu bệnh gì.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Cả cảm giác nuốt vướng ở cổ và đờm mủ trong họng đều định khu tại vùng hầu họng miệng.
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`, `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 035 — `ViMQ:train:3293` (ViMQ)
- **Nguyên văn câu hỏi:** Hạch cổ gây sốt, ngày càng sưng to gây mất ngủ về đêm, khát nước khô họng có sao không ạ?
- **Diễn đạt đời thường:** Người hỏi bị nổi hạch ở cổ gây sốt, hạch ngày càng to làm mất ngủ về đêm kèm khát nước khô họng; lo lắng có sao không.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Hạch cổ kèm sốt, mất ngủ và khô họng; xuất hiện đồng thời triệu chứng hạch, sốt và họng.
- **Chủ đề kết hợp khi hỏi đáp:** `sot`, `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Hạch cổ gây sốt có thể là bệnh lý huyết học/nhiễm trùng; chưa rõ ưu tiên sot hay hong_amidan.

### Câu 036 — `ViMQ:train:403` (ViMQ)
- **Nguyên văn câu hỏi:** Mắc viêm họng hạt kèm theo hiện tượng chảy máu mũi, ù tai là dấu hiệu bệnh gì?
- **Diễn đạt đời thường:** Người hỏi bị viêm họng hạt kèm theo hiện tượng chảy máu cam ở mũi và bị ù tai; thắc mắc là dấu hiệu bệnh gì.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Xuất hiện cùng lúc cả 3 cơ quan TMH: họng (viêm họng hạt), mũi (chảy máu mũi), tai (ù tai).
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`, `trieu_chung_mui`, `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Tam chứng kinh điển của bệnh lý vòm họng; không thể ép vào một nhãn duy nhất trong bài toán đơn nhãn mà không qua thảo luận.

### Câu 037 — `ViMQ:train:415` (ViMQ)
- **Nguyên văn câu hỏi:** Viêm tai ngoài ở trẻ tái đi tái lại có chữa khỏi được không?
- **Diễn đạt đời thường:** Người hỏi thắc mắc bệnh viêm tai ngoài ở trẻ nhỏ bị tái đi tái lại nhiều lần thì có chữa khỏi hẳn được không.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_tai`
- **Lý do đề xuất:** Bệnh lý khu trú trực tiếp tại ống tai ngoài của cơ quan tai, thuộc chủ đề trieu_chung_tai.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_tai` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 038 — `ViMQ:train:4221` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ sổ mũi, hắt hơi là dấu hiệu bệnh lý nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết khi trẻ nhỏ bị sổ mũi và hắt hơi liên tục thì là dấu hiệu của bệnh gì.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_mui`
- **Lý do đề xuất:** Bộ đôi triệu chứng sổ mũi và hắt hơi đặc trưng của đường hô hấp trên vùng mũi, thuộc chủ đề trieu_chung_mui.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_mui` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 039 — `ViMQ:train:4276` (ViMQ)
- **Nguyên văn câu hỏi:** Có thể sử dụng thuốc cảm cúm trong thời gian điều trị viêm gan B không?
- **Diễn đạt đời thường:** Người hỏi muốn biết có thể dùng các loại thuốc cảm cúm trong thời gian đang điều trị bệnh viêm gan B được không.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_cum`
- **Lý do đề xuất:** Hỏi về tương tác thuốc và độ an toàn khi dùng thuốc điều trị cảm cúm trên bệnh nhân viêm gan B, thuộc chủ đề cam_cum.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_cum`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_cum` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 040 — `ViMQ:train:4337` (ViMQ)
- **Nguyên văn câu hỏi:** Có nên cho trẻ đi khám khi bị khụt khịt mũi, không ho và sốt?
- **Diễn đạt đời thường:** Người hỏi phân vân có nên cho trẻ đi khám không khi trẻ bị khụt khịt ở mũi, hoàn toàn không bị ho và không sốt.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_mui`
- **Lý do đề xuất:** Triệu chứng duy nhất hiện diện là khụt khịt mũi; các từ ho và sốt nằm trong phủ định rõ ràng ('không ho và sốt').
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_mui` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 041 — `ViMQ:train:4421` (ViMQ)
- **Nguyên văn câu hỏi:** Bị amidan nên điều trị bằng cách nào để hiệu quả?
- **Diễn đạt đời thường:** Người hỏi muốn biết cách điều trị bệnh amidan (viêm amidan) thế nào để mang lại hiệu quả.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Hỏi về phương pháp điều trị bệnh lý amidan vùng họng, thuộc chủ đề hong_amidan.
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 042 — `ViMQ:train:4530` (ViMQ)
- **Nguyên văn câu hỏi:** Mẹ bị sốt, đau họng, ho có thể làm xét nghiệm gì để con không bị lây nhiễm?
- **Diễn đạt đời thường:** Người mẹ đang bị sốt, đau họng và ho; muốn hỏi có thể làm xét nghiệm gì để phòng tránh lây nhiễm cho con.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Xuất hiện đồng thời 3 triệu chứng hô hấp cấp: sốt, đau họng và ho; mục đích là xét nghiệm tìm nguyên nhân lây nhiễm.
- **Chủ đề kết hợp khi hỏi đáp:** `sot`, `hong_amidan`, `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Đa triệu chứng cấp tính (sốt + đau họng + ho); cần hỗ trợ truy xuất đa chủ đề.

### Câu 043 — `ViMQ:train:4709` (ViMQ)
- **Nguyên văn câu hỏi:** Ho khi thay đổi thời tiết và môi trường ô nhiễm phải làm sao?
- **Diễn đạt đời thường:** Người hỏi hay bị ho mỗi khi thời tiết thay đổi hoặc tiếp xúc với môi trường ô nhiễm; muốn biết cách xử trí.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `ho_dom`
- **Lý do đề xuất:** Triệu chứng duy nhất được mô tả là phản xạ ho do kích ứng thời tiết và ô nhiễm, thuộc chủ đề ho_dom.
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `ho_dom` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 044 — `ViMQ:train:4854` (ViMQ)
- **Nguyên văn câu hỏi:** Viêm mũi dị ứng của trẻ có điều trị dứt điểm bằng phương pháp thông thường được không?
- **Diễn đạt đời thường:** Người hỏi muốn biết bệnh viêm mũi dị ứng ở trẻ nhỏ có thể chữa trị dứt điểm bằng các phương pháp thông thường được không.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_mui`
- **Lý do đề xuất:** Câu hỏi trực tiếp về tiên lượng điều trị dứt điểm bệnh viêm mũi dị ứng ở trẻ, thuộc chủ đề trieu_chung_mui.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_mui` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 045 — `ViMQ:train:4944` (ViMQ)
- **Nguyên văn câu hỏi:** Đau rát họng, ho khan, thở khò khè, hít thở nặng đau lồng ngực là bệnh gì?
- **Diễn đạt đời thường:** Người hỏi bị đau rát ở họng, ho khan, thở khò khè và khi hít thở thấy nặng ngực đau lồng ngực; thắc mắc là bệnh gì.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Tập hợp các triệu chứng đường thở trên và dưới: đau rát họng (họng), ho khan (ho_dom) kèm khó thở, đau tức lồng ngực (hô hấp dưới/phổi).
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`, `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Có dấu hiệu cảnh báo đường hô hấp dưới/phổi; cần thảo luận xem xếp vào ho_dom, hong_amidan hay chuyển tuyến.

### Câu 046 — `ViMQ:train:495` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ nôn nhiều có phải là di chứng của cúm A?
- **Diễn đạt đời thường:** Người hỏi thấy trẻ bị nôn nhiều sau khi mắc cúm A; thắc mắc đây có phải là di chứng của bệnh cúm A không.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_cum`
- **Lý do đề xuất:** Hỏi về triệu chứng nôn mửa trong mối liên hệ với bệnh cảnh cúm A (di chứng cúm A), thuộc chủ đề cam_cum.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_cum`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_cum` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 047 — `ViMQ:train:4974` (ViMQ)
- **Nguyên văn câu hỏi:** Đau thái dương hàm kèm theo khó nuốt và nuốt đau là bệnh gì?
- **Diễn đạt đời thường:** Người hỏi bị đau vùng khớp thái dương hàm đi kèm cảm giác khó nuốt và nuốt đau; thắc mắc là bệnh gì.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Kết hợp bệnh lý vùng khớp thái dương hàm (răng hàm mặt) và triệu chứng khó nuốt, nuốt đau (họng).
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Phân vân giữa chuyên khoa Răng Hàm Mặt (khớp thái dương hàm) và Tai Mũi Họng (nuốt đau).

### Câu 048 — `ViMQ:train:5053` (ViMQ)
- **Nguyên văn câu hỏi:** Ngứa cổ họng sau khi uống thuốc hạ sốt paracetamol phải làm sao?
- **Diễn đạt đời thường:** Người hỏi bị ngứa ở cổ họng sau khi uống thuốc hạ sốt paracetamol; muốn biết hướng xử trí.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Triệu chứng phàn nàn chính cần xử trí là ngứa cổ họng; paracetamol hạ sốt chỉ là thuốc uống trước đó.
- **Chủ đề kết hợp khi hỏi đáp:** `sot`, `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 049 — `ViMQ:train:5582` (ViMQ)
- **Nguyên văn câu hỏi:** Mắc viêm xoang, xì mũi có máu nên điều trị thế nào?
- **Diễn đạt đời thường:** Người hỏi bị bệnh viêm xoang và khi xì mũi thấy có lẫn máu; muốn biết nên điều trị thế nào.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `xoang`
- **Lý do đề xuất:** Người hỏi trực tiếp hỏi về cách điều trị khi mắc bệnh viêm xoang có kèm triệu chứng xì mũi ra máu; thuộc chủ đề xoang (kết hợp truy xuất nhóm triệu chứng mũi).
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`, `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `xoang` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 050 — `ViMQ:train:5846` (ViMQ)
- **Nguyên văn câu hỏi:** Viêm amidan kèm nhức, ù tai, đau cổ họng có liên quan đến ung thư vòm họng không?
- **Diễn đạt đời thường:** Người hỏi bị viêm amidan kèm nhức đầu, ù tai và đau cổ họng; lo lắng hỏi có liên quan đến bệnh ung thư vòm họng không.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Nghi vấn ung thư vòm họng khi có viêm amidan kèm ù tai và đau họng; liên quan đồng thời họng và tai.
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`, `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Đa cơ quan (amidan, họng, tai); câu hỏi bày tỏ sự lo lắng về bệnh lý ác tính.

### Câu 051 — `ViMQ:train:6507` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ sốt kèm đi tiểu phải rặn có sao không?
- **Diễn đạt đời thường:** Người hỏi thấy trẻ bị sốt và khi đi tiểu phải rặn mạnh, muốn biết tình trạng này có nguy hiểm không.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi có triệu chứng sốt và khó khăn khi đi tiểu (phải rặn); chưa có quy tắc phân loại đủ rõ để chọn nhãn sot hay loại khỏi tập dữ liệu.
- **Chủ đề kết hợp khi hỏi đáp:** `sot`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Đa triệu chứng toàn thân và bài tiết (sốt + tiểu rặn); cần thảo luận chọn nhãn sot hay loại trừ khỏi phạm vi TMH.

### Câu 052 — `ViMQ:train:897` (ViMQ)
- **Nguyên văn câu hỏi:** Cách nào để giảm ho cho bệnh nhân viêm xoang?
- **Diễn đạt đời thường:** Người hỏi muốn biết cách làm dịu hoặc giảm cơn ho cho người đang có bệnh viêm xoang.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `ho_dom`
- **Lý do đề xuất:** Mục tiêu chính người hỏi muốn giải đáp là phương pháp giảm ho; viêm xoang là bối cảnh liên quan (bỏ khẳng định viêm xoang gây ra ho).
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`, `xoang`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `ho_dom` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 053 — `ViMQ:validation:111` (ViMQ)
- **Nguyên văn câu hỏi:** Bé nổi ban sau sốt kèm sổ mũi, ho ít có phải bị sởi không?
- **Diễn đạt đời thường:** Người hỏi thấy em bé bị nổi ban sau khi hết sốt, kèm sổ mũi và ho ít; thắc mắc có phải bé bị bệnh sởi không.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Người hỏi nêu triệu chứng sốt phát ban kèm sổ mũi, ho ít và chủ động hỏi về bệnh sởi (bệnh truyền nhiễm toàn thân ở trẻ em ngoài phạm vi chuyên khoa TMH).
- **Chủ đề kết hợp khi hỏi đáp:** `sot`, `trieu_chung_mui`, `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 054 — `ViMQ:validation:740` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ thường xuyên ho, nghẹt mũi khi thay đổi thời tiết phải điều trị thế nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết cách chữa trị cho trẻ thường xuyên bị ho và nghẹt mũi mỗi khi thời tiết thay đổi.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Bộ đôi triệu chứng ho và nghẹt mũi xuất hiện ngang hàng khi thay đổi thời tiết; kết hợp giữa ho_dom và trieu_chung_mui.
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`, `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Hai triệu chứng điển hình của đường hô hấp trên; cần thảo luận chọn nhãn đơn hoặc kết hợp truy xuất.

### Câu 055 — `ViMQ:validation:833` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ 5 tuổi bị hắt hơi, nghẹt mũi có phải dấu hiệu của viêm xoang không?
- **Diễn đạt đời thường:** Người hỏi thấy trẻ 5 tuổi bị hắt hơi và nghẹt mũi; thắc mắc đây có phải là dấu hiệu của bệnh viêm xoang không.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `xoang`
- **Lý do đề xuất:** Người hỏi trực tiếp đặt nghi vấn về viêm xoang nên trọng tâm câu hỏi là xoang, theo hướng dẫn gán nhãn hiện có (nhãn chủ đề không xác nhận trẻ mắc viêm xoang).
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`, `xoang`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `xoang` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 056 — `ViMedAQA:test:disease_13320` (ViMedAQA)
- **Nguyên văn câu hỏi:** Nguyên nhân gây ra viêm mũi xoang cấp phổ biến là gì?
- **Diễn đạt đời thường:** Người hỏi muốn biết các nguyên nhân phổ biến nhất gây ra bệnh viêm mũi xoang cấp tính là gì.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `xoang`
- **Lý do đề xuất:** Câu hỏi lý thuyết y khoa về các nguyên nhân phổ biến gây bệnh viêm mũi xoang cấp, thuộc chủ đề xoang (kết hợp truy xuất nhóm mũi).
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`, `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `xoang` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 057 — `ViMedAQA:test:disease_1621` (ViMedAQA)
- **Nguyên văn câu hỏi:** Sự kích hoạt hormone stress mãn tính có tác động gì đến hệ miễn dịch?
- **Diễn đạt đời thường:** Người hỏi muốn biết việc hormone căng thẳng (stress) bị kích hoạt kéo dài liên tục thì gây ảnh hưởng gì đến hệ miễn dịch của cơ thể.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi thuần túy lý thuyết về nội tiết và miễn dịch học đại cương; hoàn toàn ngoài chuyên khoa Tai Mũi Họng.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 058 — `ViMedAQA:test:medicine_478` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cần lưu ý những gì khi sử dụng Dược liệu - Bình vôi?
- **Diễn đạt đời thường:** Người hỏi muốn biết những điều cần chú ý khi sử dụng vị thuốc dược liệu Bình vôi (củ bình vôi).
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Củ bình vôi là dược liệu y học cổ truyền dùng an thần, chữa mất ngủ; không đề cập triệu chứng hay bệnh lý TMH.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 059 — `ViMedAQA:train:body-part_2120` (ViMedAQA)
- **Nguyên văn câu hỏi:** Trong trường hợp bệnh nhân không có màng nhĩ thì cần sự tư vấn và đồng ý của bác sĩ trước khi làm gì?
- **Diễn đạt đời thường:** Người hỏi muốn biết trong trường hợp bệnh nhân không có màng nhĩ thì cần bác sĩ đồng ý và tư vấn trước khi làm việc gì.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_tai`
- **Lý do đề xuất:** Hỏi về các thủ thuật hoặc can thiệp cần thận trọng khi mất màng nhĩ ở tai, thuộc chủ đề trieu_chung_tai.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_tai` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 060 — `ViMedAQA:train:disease_1094` (ViMedAQA)
- **Nguyên văn câu hỏi:** Vi khuẩn hay virus xâm nhập vào tai giữa gây ra tình trạng gì?
- **Diễn đạt đời thường:** Người hỏi muốn biết khi vi khuẩn hoặc vi-rút xâm nhập vào vùng tai giữa thì sẽ gây ra tình trạng bệnh gì.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_tai`
- **Lý do đề xuất:** Hỏi về cơ chế gây bệnh lý tại khoang tai giữa (viêm tai giữa), thuộc chủ đề trieu_chung_tai.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_tai` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 061 — `ViMedAQA:train:disease_1102` (ViMedAQA)
- **Nguyên văn câu hỏi:** Viêm ống tai ngoài ác tính là biến chứng của bệnh gì?
- **Diễn đạt đời thường:** Người hỏi muốn biết bệnh viêm ống tai ngoài ác tính là biến chứng bắt nguồn từ bệnh lý nào.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_tai`
- **Lý do đề xuất:** Hỏi về bệnh học viêm ống tai ngoài ác tính, thuộc nhóm bệnh lý cơ quan tai (trieu_chung_tai).
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_tai` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 062 — `ViMedAQA:train:disease_12274` (ViMedAQA)
- **Nguyên văn câu hỏi:** Biến chứng của viêm amidan cấp - Áp xe vòm họng có thể dẫn đến tử vong không?
- **Diễn đạt đời thường:** Người hỏi muốn biết biến chứng áp-xe thành sau họng do viêm amidan cấp gây ra thì có thể dẫn đến tử vong không.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Câu hỏi hỏi về mức độ nguy hiểm của tình trạng áp-xe vòm họng trong bối cảnh bệnh viêm amidan cấp, thuộc chủ đề hong_amidan.
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 063 — `ViMedAQA:train:disease_12301` (ViMedAQA)
- **Nguyên văn câu hỏi:** Trong những trường hợp nào thì không nên tự lấy sỏi amidan tại nhà?
- **Diễn đạt đời thường:** Người hỏi muốn biết trong những trường hợp nào thì không được tự ý gắp hoặc lấy sỏi amidan tại nhà.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Hỏi về hướng dẫn an toàn khi xử trí sỏi amidan tại vùng họng, thuộc chủ đề hong_amidan.
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 064 — `ViMedAQA:train:disease_12760` (ViMedAQA)
- **Nguyên văn câu hỏi:** Có thể kê thuốc gì để giảm đau và hạ sốt khi bị viêm họng do liên cầu khuẩn?
- **Diễn đạt đời thường:** Người hỏi muốn biết có thể kê những loại thuốc nào để giảm đau và hạ sốt khi bị viêm họng do vi khuẩn liên cầu.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Bệnh lý chính xác định việc kê đơn điều trị là viêm họng do liên cầu khuẩn; giảm đau hạ sốt là mục đích điều trị triệu chứng.
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`, `sot`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 065 — `ViMedAQA:train:disease_13211` (ViMedAQA)
- **Nguyên văn câu hỏi:** Viêm mũi dị ứng nghề nghiệp do nguyên nhân nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết bệnh viêm mũi dị ứng do nghề nghiệp (do môi trường làm việc) bắt nguồn từ những nguyên nhân nào.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_mui`
- **Lý do đề xuất:** Hỏi về nguyên nhân gây bệnh viêm mũi dị ứng nghề nghiệp, thuộc chủ đề trieu_chung_mui.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_mui` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 066 — `ViMedAQA:train:disease_13259` (ViMedAQA)
- **Nguyên văn câu hỏi:** Thực phẩm nào có thể giúp giảm nguy cơ mắc viêm mũi không dị ứng?
- **Diễn đạt đời thường:** Người hỏi muốn biết những loại thức ăn thực phẩm nào có thể giúp giảm bớt nguy cơ bị mắc viêm mũi không do dị ứng.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_mui`
- **Lý do đề xuất:** Hỏi về chế độ ăn uống phòng ngừa bệnh viêm mũi không dị ứng, thuộc chủ đề trieu_chung_mui.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_mui` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 067 — `ViMedAQA:train:disease_13285` (ViMedAQA)
- **Nguyên văn câu hỏi:** Trong số các cách điều trị viêm mũi xoang tại nhà, rửa mũi bằng nước muối mặn có vai trò như thế nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết khi chữa viêm mũi xoang tại nhà thì việc rửa mũi bằng nước muối ưu trương (nước muối mặn) có tác dụng gì.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `xoang`
- **Lý do đề xuất:** Hỏi về tác dụng của dung dịch rửa mũi trong điều trị bệnh lý viêm mũi xoang, thuộc chủ đề xoang (hỗ trợ truy xuất cả triệu chứng mũi).
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`, `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `xoang` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 068 — `ViMedAQA:train:disease_13293` (ViMedAQA)
- **Nguyên văn câu hỏi:** Làm thế nào để tránh viêm xoang khi tiếp xúc với người bệnh?
- **Diễn đạt đời thường:** Người hỏi muốn biết làm cách nào để tránh bị lây hoặc tránh mắc bệnh viêm xoang khi tiếp xúc với người đang bị bệnh.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `xoang`
- **Lý do đề xuất:** Hỏi về các biện pháp dự phòng tránh mắc bệnh viêm xoang, thuộc chủ đề xoang.
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `xoang` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 069 — `ViMedAQA:train:disease_13312` (ViMedAQA)
- **Nguyên văn câu hỏi:** Trong trường hợp nào nên nghĩ đến điều trị ngoại khoa viêm mũi xoang cấp?
- **Diễn đạt đời thường:** Người hỏi muốn biết trong những tình huống nào thì cần tính đến việc phẫu thuật (điều trị ngoại khoa) cho bệnh viêm mũi xoang cấp.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `xoang`
- **Lý do đề xuất:** Câu hỏi hỏi về các trường hợp cần cân nhắc phẫu thuật (điều trị ngoại khoa) đối với bệnh viêm mũi xoang cấp, thuộc chủ đề xoang.
- **Chủ đề kết hợp khi hỏi đáp:** `xoang`, `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `xoang` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 070 — `ViMedAQA:train:disease_13697` (ViMedAQA)
- **Nguyên văn câu hỏi:** Các triệu chứng của viêm tai giữa mạn tính là gì?
- **Diễn đạt đời thường:** Người hỏi muốn biết các triệu chứng và dấu hiệu nhận biết của bệnh viêm tai giữa mạn tính là gì.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_tai`
- **Lý do đề xuất:** Hỏi về triệu chứng lâm sàng của bệnh viêm tai giữa mạn tính, thuộc chủ đề trieu_chung_tai.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_tai` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 071 — `ViMedAQA:train:disease_1417` (ViMedAQA)
- **Nguyên văn câu hỏi:** Khi nào bạn nên đi khám bác sĩ nếu nghi ngờ nhiễm cúm gia cầm?
- **Diễn đạt đời thường:** Người hỏi muốn biết thời điểm nào thì cần đi khám bác sĩ ngay nếu nghi ngờ bản thân bị nhiễm cúm gia cầm.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_cum`
- **Lý do đề xuất:** Hỏi về dấu hiệu cảnh báo cần đi khám khi nghi ngờ mắc cúm gia cầm, thuộc chủ đề cam_cum.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_cum`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_cum` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 072 — `ViMedAQA:train:disease_14929` (ViMedAQA)
- **Nguyên văn câu hỏi:** Có những dấu hiệu nào giúp phát hiện suy giảm miễn dịch khi đau họng?
- **Diễn đạt đời thường:** Người hỏi muốn biết có những dấu hiệu nào giúp phát hiện tình trạng suy giảm miễn dịch khi bị đau họng.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Hỏi về các dấu hiệu nghi ngờ suy giảm miễn dịch biểu hiện qua triệu chứng đau họng kéo dài/bất thường, thuộc chủ đề hong_amidan.
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 073 — `ViMedAQA:train:disease_15101` (ViMedAQA)
- **Nguyên văn câu hỏi:** Các triệu chứng thường gặp của đau đầu thứ phát là gì?
- **Diễn đạt đời thường:** Người hỏi muốn biết các triệu chứng hay gặp nhất của bệnh đau đầu thứ phát (đau đầu do một nguyên nhân bệnh lý khác gây ra) là gì.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Hỏi về phân loại và triệu chứng của hội chứng đau đầu thứ phát thuộc chuyên khoa Thần kinh; hoàn toàn không có triệu chứng TMH.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 074 — `ViMedAQA:train:disease_15118` (ViMedAQA)
- **Nguyên văn câu hỏi:** Đối với những người bị đau đầu thứ phát, thuốc phòng ngừa có tác dụng như thế nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết đối với người bị đau đầu thứ phát thì các loại thuốc uống phòng ngừa có tác dụng như thế nào.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Hỏi về cơ chế thuốc phòng ngừa đau đầu thứ phát thuộc chuyên khoa Thần kinh; hoàn toàn ngoài phạm vi TMH.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 075 — `ViMedAQA:train:disease_1589` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cúm có thể dẫn đến những biến chứng nào khác ngoài đường hô hấp?
- **Diễn đạt đời thường:** Người hỏi muốn biết bệnh cúm có thể gây ra những biến chứng nào khác ở ngoài đường hô hấp.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_cum`
- **Lý do đề xuất:** Hỏi về các biến chứng toàn thân (ngoài hô hấp) do vi-rút cúm gây ra, thuộc chủ đề cam_cum.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_cum`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_cum` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 076 — `ViMedAQA:train:disease_1634` (ViMedAQA)
- **Nguyên văn câu hỏi:** Thời gian trung bình của một đợt cảm lạnh thường là bao lâu?
- **Diễn đạt đời thường:** Người hỏi muốn biết thông thường một đợt bị cảm lạnh sẽ kéo dài trong khoảng thời gian bao lâu.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_lanh`
- **Lý do đề xuất:** Hỏi về thời gian diễn tiến tự nhiên trung bình của bệnh cảm lạnh, thuộc chủ đề cam_lanh.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_lanh`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_lanh` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 077 — `ViMedAQA:train:disease_2757` (ViMedAQA)
- **Nguyên văn câu hỏi:** Vì sao không nên ho khạc nhiều khi hóc xương cá?
- **Diễn đạt đời thường:** Người hỏi muốn biết vì sao khi bị hóc xương cá thì không nên cố gắng ho khạc quá nhiều.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Tình huống tai nạn dị vật họng miệng (hóc xương cá); ho khạc chỉ là phản xạ sai cần tránh.
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`, `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 078 — `ViMedAQA:train:disease_4933` (ViMedAQA)
- **Nguyên văn câu hỏi:** Tại sao không nên tự lấy ráy tai tại nhà?
- **Diễn đạt đời thường:** Người hỏi muốn biết lý do vì sao không nên tự ý dùng dụng cụ lấy ráy tai tại nhà.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_tai`
- **Lý do đề xuất:** Hỏi về việc chăm sóc vệ sinh ống tai ngoài và nguy cơ tổn thương tai khi tự lấy ráy tai, thuộc chủ đề trieu_chung_tai.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_tai` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 079 — `ViMedAQA:train:disease_5220` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cảm lạnh thường kéo dài trong bao lâu?
- **Diễn đạt đời thường:** Người hỏi muốn biết bệnh cảm lạnh thông thường sẽ kéo dài trong bao lâu thì khỏi.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_lanh`
- **Lý do đề xuất:** Hỏi trực tiếp về thời gian kéo dài của bệnh cảm lạnh, thuộc chủ đề cam_lanh.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_lanh`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_lanh` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 080 — `ViMedAQA:train:disease_5463` (ViMedAQA)
- **Nguyên văn câu hỏi:** Dấu hiệu nào cho biết răng bị nhiễm trùng?
- **Diễn đạt đời thường:** Người hỏi muốn biết các dấu hiệu cho thấy một chiếc răng đang bị nhiễm trùng.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi chuyên sâu về bệnh học răng miệng (nhiễm trùng răng/áp-xe răng) thuộc chuyên khoa Răng Hàm Mặt; hoàn toàn ngoài TMH.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 081 — `ViMedAQA:train:disease_7938` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cách nào giúp làm giảm khô họng và ngứa họng?
- **Diễn đạt đời thường:** Người hỏi muốn biết các phương pháp giúp làm dịu cảm giác khô rát họng và ngứa ở cổ họng.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `hong_amidan`
- **Lý do đề xuất:** Hỏi về cách làm giảm triệu chứng khô và ngứa tại vùng họng miệng, thuộc chủ đề hong_amidan.
- **Chủ đề kết hợp khi hỏi đáp:** `hong_amidan`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `hong_amidan` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 082 — `ViMedAQA:train:disease_8258` (ViMedAQA)
- **Nguyên văn câu hỏi:** Mô tả triệu chứng khởi phát của bệnh sốt xuất huyết Lassa?
- **Diễn đạt đời thường:** Người hỏi muốn biết các triệu chứng lúc mới bắt đầu phát bệnh của bệnh sốt xuất huyết Lassa.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi về bệnh sốt xuất huyết Lassa (bệnh truyền nhiễm nhiệt đới do vi-rút Lassa); hoàn toàn ngoài phạm vi TMH.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 083 — `ViMedAQA:train:drug_1970` (ViMedAQA)
- **Nguyên văn câu hỏi:** Thuốc Alzyltex Mebiphar có tác dụng gì đối với tình trạng viêm mũi dị ứng theo mùa?
- **Diễn đạt đời thường:** Người hỏi muốn biết thuốc Alzyltex Mebiphar có tác dụng điều trị như thế nào đối với bệnh viêm mũi dị ứng theo mùa.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_mui`
- **Lý do đề xuất:** Hỏi về tác dụng dược lý của thuốc kháng histamin trong điều trị viêm mũi dị ứng, thuộc chủ đề trieu_chung_mui.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_mui`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_mui` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 084 — `ViMedAQA:train:drug_3926` (ViMedAQA)
- **Nguyên văn câu hỏi:** Khi dùng thuốc ho Atussin cần lưu ý dược chất nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết khi dùng thuốc ho Atussin thì cần lưu ý đến hoạt chất dược chất nào trong thuốc.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `ho_dom`
- **Lý do đề xuất:** Hỏi về thành phần và lưu ý khi sử dụng thuốc giảm ho Atussin, thuộc chủ đề ho_dom.
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `ho_dom` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 085 — `ViMedAQA:train:drug_6484` (ViMedAQA)
- **Nguyên văn câu hỏi:** Brufen có thể được sử dụng kết hợp với các triệu chứng đau nào khi bị cảm cúm?
- **Diễn đạt đời thường:** Người hỏi muốn biết thuốc giảm đau Brufen có thể dùng kết hợp để giảm những triệu chứng đau nhức nào khi bị cảm cúm.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_cum`
- **Lý do đề xuất:** Hỏi về chỉ định dùng thuốc giảm đau kháng viêm Brufen (ibuprofen) trong điều trị triệu chứng bệnh cảm cúm, thuộc chủ đề cam_cum.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_cum`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_cum` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 086 — `ViMedAQA:train:medicine_12865` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cây Xuyên tâm liên có tác dụng gì trong điều trị cảm sốt và viêm xoang?
- **Diễn đạt đời thường:** Người hỏi muốn biết cây thuốc Xuyên tâm liên có tác dụng chữa bệnh như thế nào đối với chứng cảm sốt và bệnh viêm xoang.
- **Đề xuất AI:** `needs_discussion` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Bài thuốc đông y chữa đồng thời cảm sốt và viêm xoang; liên quan đến cả nhóm cảm/sốt và nhóm xoang.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_lanh`, `cam_cum`, `sot`, `xoang`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `needs_discussion` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận giữ thảo luận theo đề xuất AI v4; chưa chốt nhãn train. Đa chủ đề dược liệu (cảm sốt + xoang); cần hỗ trợ truy xuất đa nguồn.

### Câu 087 — `ViMedAQA:train:medicine_13347` (ViMedAQA)
- **Nguyên văn câu hỏi:** Trong bài thuốc có chứa cây Đa lông, thành phần nào là chính?
- **Diễn đạt đời thường:** Người hỏi muốn biết trong bài thuốc dân gian có cây Đa lông thì vị thuốc nào đóng vai trò thành phần chính.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi thuần túy về thành phần bài thuốc cổ truyền cây Đa lông, không đề cập triệu chứng hay bệnh lý TMH.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 088 — `ViMedAQA:train:medicine_13573` (ViMedAQA)
- **Nguyên văn câu hỏi:** Đường phèn kết hợp với nguyên liệu nào để giảm ho khan?
- **Diễn đạt đời thường:** Người hỏi muốn biết đường phèn thường kết hợp cùng nguyên liệu nào để giúp làm giảm triệu chứng ho khan.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `ho_dom`
- **Lý do đề xuất:** Hỏi về mẹo dân gian dùng đường phèn trị chứng ho khan, thuộc chủ đề ho_dom.
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `ho_dom` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 089 — `ViMedAQA:train:medicine_1807` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cà na được sử dụng như thế nào để điều trị ho do cảm lạnh?
- **Diễn đạt đời thường:** Người hỏi muốn biết quả cà na được chế biến và sử dụng như thế nào để chữa chứng ho do bị cảm lạnh.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `ho_dom`
- **Lý do đề xuất:** Trọng tâm câu hỏi là phương pháp dùng cà na để điều trị triệu chứng ho (ho do cảm lạnh).
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`, `cam_lanh`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `ho_dom` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 090 — `ViMedAQA:train:medicine_3925` (ViMedAQA)
- **Nguyên văn câu hỏi:** Liều lượng sử dụng của Vỏ cây Dâu tằm và Vỏ rễ chanh trong bài thuốc là bao nhiêu?
- **Diễn đạt đời thường:** Người hỏi muốn biết liều lượng dùng của vỏ cây dâu tằm và vỏ rễ cây chanh trong bài thuốc đông y là bao nhiêu.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Hỏi về liều lượng thành phần dược liệu chung, không nêu tên bệnh cảnh hay triệu chứng cụ thể.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 091 — `ViMedAQA:train:medicine_3927` (ViMedAQA)
- **Nguyên văn câu hỏi:** Bài thuốc từ cây Dâu tằm để trị ho ra máu được thực hiện như thế nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết cách thực hiện bài thuốc dân gian từ cây dâu tằm để điều trị chứng ho ra máu.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `ho_dom`
- **Lý do đề xuất:** Hỏi về bài thuốc chữa triệu chứng ho ra máu, thuộc nhóm chủ đề ho và đờm (ho_dom).
- **Chủ đề kết hợp khi hỏi đáp:** `ho_dom`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `ho_dom` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 092 — `ViMedAQA:train:medicine_5967` (ViMedAQA)
- **Nguyên văn câu hỏi:** Bài thuốc từ Khoai nưa gồm những thành phần nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết bài thuốc dân gian từ củ khoai nưa gồm có những thành phần nguyên liệu nào.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Hỏi về thành phần bài thuốc khoai nưa, không đề cập bệnh lý hay triệu chứng TMH.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 093 — `ViMedAQA:train:medicine_6053` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cửu vị khương hoạt thang là bài thuốc gồm những thành phần chính nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết bài thuốc cổ phương 'Cửu vị khương hoạt thang' gồm những vị thuốc chính nào.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi thuần túy lý thuyết về thành phần bài thuốc cổ phương Cửu vị khương hoạt thang; không nêu triệu chứng TMH cụ thể.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 094 — `ViMedAQA:train:medicine_6793` (ViMedAQA)
- **Nguyên văn câu hỏi:** Người ta sử dụng lá trầu không chữa cảm mạo bằng cách nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết cách dùng lá trầu không trong dân gian để chữa bệnh cảm mạo (cảm lạnh).
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_lanh`
- **Lý do đề xuất:** Hỏi về cách dùng lá trầu không trị bệnh cảm mạo (cảm lạnh thông thường), thuộc chủ đề cam_lanh.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_lanh`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_lanh` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 095 — `ViMedAQA:train:medicine_6961` (ViMedAQA)
- **Nguyên văn câu hỏi:** Tại sao những người đang cảm lạnh, suy nhược cơ thể, thường xuyên bị lạnh, dễ cảm, ăn uống đầy bụng khó tiêu, đi phân lỏng loãng không nên sử dụng cây Lẻ bạn?
- **Diễn đạt đời thường:** Người hỏi muốn biết vì sao những người đang bị cảm lạnh, người suy nhược, dễ bị lạnh, bụng đầy khó tiêu, đi ngoài phân lỏng thì không nên dùng cây Lẻ bạn.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_lanh`
- **Lý do đề xuất:** Hỏi về chống chỉ định dùng cây Lẻ bạn đối với người có cơ địa cảm lạnh, thuộc chủ đề cam_lanh.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_lanh`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_lanh` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 096 — `ViMedAQA:train:medicine_7122` (ViMedAQA)
- **Nguyên văn câu hỏi:** Tác dụng của bài thuốc chữa cảm lạnh bằng Màng tang là gì?
- **Diễn đạt đời thường:** Người hỏi muốn biết tác dụng chữa bệnh của bài thuốc trị cảm lạnh bằng cây Màng tang là gì.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_lanh`
- **Lý do đề xuất:** Hỏi về tác dụng chữa bệnh của bài thuốc trị cảm lạnh, thuộc chủ đề cam_lanh.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_lanh`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_lanh` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 097 — `ViMedAQA:train:medicine_8025` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cách sử dụng ngân hạnh và lá ngải cứu để chữa bệnh cảm lạnh như thế nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết cách phối hợp hạt ngân hạnh (bạch quả) và lá ngải cứu để chữa bệnh cảm lạnh.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `cam_lanh`
- **Lý do đề xuất:** Hỏi về cách dùng bài thuốc đông y điều trị bệnh cảm lạnh, thuộc chủ đề cam_lanh.
- **Chủ đề kết hợp khi hỏi đáp:** `cam_lanh`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `cam_lanh` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

### Câu 098 — `ViMedAQA:train:medicine_9019` (ViMedAQA)
- **Nguyên văn câu hỏi:** Quy bản là loại dược liệu nào?
- **Diễn đạt đời thường:** Người hỏi muốn biết vị thuốc Quy bản (mai rùa) là loại dược liệu như thế nào.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi thuần định nghĩa vị thuốc đông y Quy bản (mai rùa); hoàn toàn ngoài phạm vi TMH.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 099 — `ViMedAQA:train:medicine_9746` (ViMedAQA)
- **Nguyên văn câu hỏi:** Sa nhân có được dùng nhiều trong y học hay không?
- **Diễn đạt đời thường:** Người hỏi muốn biết vị thuốc Sa nhân có được sử dụng phổ biến trong y học hay không.
- **Đề xuất AI:** `excluded_proposed` | **Nhãn đề xuất:** *(để trống)*
- **Lý do đề xuất:** Câu hỏi đại cương về mức độ phổ biến của vị thuốc Sa nhân; không đề cập triệu chứng hay bệnh lý TMH.
- **Chủ đề kết hợp khi hỏi đáp:** *(không có)*
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu có trọng tâm ngoài phạm vi chủ đề của dự án; giữ nguyên bản ghi nguồn để truy vết.

### Câu 100 — `ViMedAQA:validation:disease_13730` (ViMedAQA)
- **Nguyên văn câu hỏi:** Tại sao không nên dùng que tăm bông để ngoáy tai?
- **Diễn đạt đời thường:** Người hỏi muốn biết lý do vì sao không nên dùng que tăm bông để ngoáy vào trong lỗ tai.
- **Đề xuất AI:** `label_proposed` | **Nhãn đề xuất:** `trieu_chung_tai`
- **Lý do đề xuất:** Hỏi về thói quen vệ sinh tai và nguy cơ tổn thương ống tai/màng nhĩ khi dùng tăm bông, thuộc chủ đề trieu_chung_tai.
- **Chủ đề kết hợp khi hỏi đáp:** `trieu_chung_tai`
- **Hỏi bổ sung thông tin:** Không
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_tai` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chấp thuận nhãn AI đề xuất v4 theo xác nhận duyệt toàn bộ trong cuộc trò chuyện.

---

## 5. Mẫu xác nhận gộp (Dành cho người duyệt gửi quyết định nhanh)

Người duyệt có thể sao chép đoạn dưới đây, chỉnh sửa theo ý mình và gửi trong phản hồi chat:

```text
Người duyệt: hoai_an
Ngày duyệt: 2026-11-28

1. Đồng ý nhãn đề xuất cho các STT: [Điền các STT đồng ý, hoặc ghi "Đồng ý toàn bộ 58 câu nhóm label_proposed trừ các câu nêu bên dưới"]

2. Đổi nhãn các STT:
- STT [...] đổi thành [...] vì [...]

3. Loại các STT:
- [Điền các STT loại, hoặc ghi "Đồng ý toàn bộ 26 câu nhóm excluded_proposed"]

4. Quyết định cho các câu thảo luận (16 câu nhóm needs_discussion):
- Câu 005: [hong_amidan / ho_dom / excluded / needs_discussion]
- Câu 012: [hong_amidan / trieu_chung_mui / excluded / needs_discussion]
- Câu 014: [sot / ho_dom / hong_amidan / excluded / needs_discussion]
- Câu 015: [cam_cum / excluded / needs_discussion]
- Câu 021: [trieu_chung_tai / excluded / needs_discussion]
- Câu 027: [xoang / trieu_chung_mui / excluded / needs_discussion]
- Câu 028: [ho_dom / excluded / needs_discussion]
- Câu 035: [sot / hong_amidan / excluded / needs_discussion]
- Câu 036: [hong_amidan / trieu_chung_mui / trieu_chung_tai / excluded / needs_discussion]
- Câu 042: [hong_amidan / ho_dom / sot / excluded / needs_discussion]
- Câu 045: [hong_amidan / ho_dom / excluded / needs_discussion]
- Câu 047: [hong_amidan / excluded / needs_discussion]
- Câu 050: [hong_amidan / trieu_chung_tai / excluded / needs_discussion]
- Câu 051: [sot / excluded / needs_discussion]
- Câu 054: [ho_dom / trieu_chung_mui / excluded / needs_discussion]
- Câu 086: [xoang / cam_cum / cam_lanh / excluded / needs_discussion]
```

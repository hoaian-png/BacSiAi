# Phiếu duyệt mở rộng đợt 2 (200 câu ứng viên)

Phiên bản: **1.0 (Lấy mẫu mở rộng đợt 2 theo kế hoạch)**  
Ngày tạo: **28/11/2026**  
Dự án: **BacSiAi (Phân loại câu hỏi y tế Tai Mũi Họng)**  
Tệp dữ liệu gốc của đợt: [questions_expansion.csv](../02_du_lieu/filedata/reviewed/expansion/batch_02_v1/questions_expansion.csv) | [sampling_manifest.json](../02_du_lieu/filedata/reviewed/expansion/batch_02_v1/sampling_manifest.json)  
Tài liệu tham chiếu: [HUONG_DAN_GAN_NHAN.md](HUONG_DAN_GAN_NHAN.md), [QUY_UOC_LUU_TRU.md](QUY_UOC_LUU_TRU.md), [TONG_KET_DUYET_THU_DOT_01.md](../05_bao_cao/kiem_tra_du_lieu/TONG_KET_DUYET_THU_DOT_01.md).

> [!IMPORTANT]
> **Nguyên tắc thẩm định và bảo toàn dữ liệu:**
> 1. Toàn bộ nhãn tại mục **Nhãn gợi ý (chưa duyệt)** được sinh tự động bằng quy tắc từ khóa, chỉ dùng để phân bổ lấy mẫu sơ bộ, hoàn toàn **chưa phải là nhãn chuẩn hay quyết định của con người**.
> 2. Người duyệt đọc nguyên văn câu hỏi và đưa ra quyết định độc lập tại các ô **`[Chờ điền]`**.
> 3. Ký hiệu **`[Chờ điền]`** chỉ dùng để trình bày vị trí trên văn bản markdown này. **Tuyệt đối không chép chuỗi ký tự "[Chờ điền]" vào tệp CSV làm việc**.
> 4. **Tách biệt bài toán huấn luyện đơn nhãn và truy xuất hỏi đáp đa nguồn:**
>    - Nhãn huấn luyện (`gold_topic_label`): Mô hình phân loại hiện tại học bài toán đơn nhãn (chọn đúng 1 trong 8 nhãn TMH). Nếu câu hỏi có 1 trọng tâm nổi bật thì chọn nhãn đó. Nếu có nhiều chủ đề ngang hàng hoặc chưa rõ trọng tâm thì đánh dấu `needs_discussion` (nhãn chuẩn để trống).
>    - Truy xuất hỏi đáp: Chatbot sau này không bị bó hẹp trong nhãn đơn của mô hình phân loại; hệ thống sẽ tìm kiếm nội dung phù hợp từ tất cả các chủ đề liên quan và từ cả 3 bộ dữ liệu (ViMQ, ViHealthQA, ViMedAQA).
> 5. Bộ lấy mẫu gốc giữ nguyên 200 câu ban đầu. Quyết định của người duyệt được lưu tại [working/questions_working.csv](../02_du_lieu/filedata/reviewed/expansion/batch_02_v1/working/questions_working.csv): **1 reviewed, 5 excluded, 194 pending**. Trong 194 pending có **26 câu thảo dược/bài thuốc hoặc mẹo dân gian chưa được duyệt**.

---

## 1. Thông tin người duyệt và ngày duyệt

- **Mã định danh người duyệt (`reviewer_id`):** `[hoai_an]` *(người duyệt điền khi duyệt)*
- **Ngày duyệt thực tế (`reviewed_at`):** `[YYYY-MM-DD]` *(ví dụ: 2026-11-28)*

---

## 2. Thống kê số lượng thực tế đợt mở rộng 200 câu

- **Tổng số câu lấy mẫu:** **200 câu** (STT cố định 001 – 200; thuộc 200 nhóm nội dung `group_id` độc lập; hoàn toàn không trùng ID hay nhóm với tập Pilot 120 câu).
- **Phân bố theo nguồn dữ liệu:**
  - `ViMQ`: 75 câu (37.5%)
  - `ViHealthQA`: 67 câu (33.5%)
  - `ViMedAQA`: 58 câu (29.0%)
- **Phân bố theo nhãn gợi ý tự động (`suggested_topic_label`):**
  - `sot`: 30 câu (15.0%) — Ưu tiên bổ sung vì tập pilot hiện mới chỉ có 3 câu nhãn sốt.
  - `cam_cum`: 30 câu (15.0%)
  - `ho_dom`: 25 câu (12.5%)
  - `trieu_chung_mui`: 25 câu (12.5%)
  - `trieu_chung_tai`: 25 câu (12.5%)
  - `hong_amidan`: 20 câu (10.0%)
  - `xoang`: 20 câu (10.0%)
  - `cam_lanh`: 9 câu (4.5%) — Toàn bộ 9 nhóm cảm lạnh mới khả dụng trong kho prepared (do nguồn này rất khan hiếm).
  - `Chưa có nhãn đơn tự động` (nhãn gợi ý trống): 16 câu (8.0%) — Bao gồm các câu đa triệu chứng, câu phủ định, câu tiền sử và cách diễn đạt mở.

---

## 3. Danh mục 8 nhãn hợp lệ và quy ước phân loại

| Mã nhãn | Nhóm bệnh lý / Triệu chứng | Diễn giải ngắn gọn |
| :--- | :--- | :--- |
| `ho_dom` | Ho và đờm | Cơn ho (khan, đờm, ho lâu ngày, ho ra máu) và tính chất đờm (đặc, xanh, vàng, vướng). |
| `trieu_chung_mui` | Triệu chứng mũi, viêm mũi | Vấn đề tại mũi: nghẹt mũi, sổ mũi, hắt hơi, ngứa mũi, viêm mũi dị ứng, chảy máu cam. |
| `xoang` | Xoang và viêm xoang | Câu hỏi có trực tiếp nhắc đến xoang, bệnh viêm xoang hoặc can thiệp mổ/xông xoang. |
| `hong_amidan` | Họng, amidan, thanh quản | Đau họng, viêm amidan, sỏi amidan, nuốt vướng, nuốt đau, khản tiếng, dị vật họng (hóc xương). |
| `trieu_chung_tai` | Tai và thính lực | Đau tai, viêm tai giữa, viêm tai ngoài, chảy mủ tai, ù tai, ngứa tai, ráy tai, thủng màng nhĩ. |
| `cam_lanh` | Cảm lạnh, cảm mạo | Câu hỏi trực tiếp về cảm lạnh, cảm mạo do gió, thời tiết, dầm mưa (tự giới hạn). |
| `cam_cum` | Cúm mùa, cúm A/B/gia cầm | Câu hỏi trực tiếp về bệnh cúm, di chứng cúm, thuốc trị cúm, vắc-xin phòng cúm mùa. |
| `sot` | Sốt đơn thuần | Triệu chứng sốt cao, sốt kéo dài, sốt phát ban chưa định khu vào một cơ quan TMH cụ thể. |

**Quy ước 3 trạng thái duyệt:**
- `reviewed`: Câu hỏi thuộc chuyên khoa TMH và đã xác định được đúng 1 nhãn chuẩn trong 8 nhãn trên (`gold_topic_label` phải điền 1 nhãn hợp lệ).
- `excluded`: Câu hỏi hoàn toàn nằm ngoài chuyên khoa TMH (ví dụ: bệnh lý tiêu hóa, thần kinh, tim mạch, tiêm chủng chung không liên quan TMH). Bắt buộc để `gold_topic_label` trống (`""`) và ghi lý do tại `review_note`.
- `needs_discussion`: Câu hỏi phức tạp có nhiều triệu chứng ngang hàng chưa rõ trọng tâm, câu hỏi so sánh hai bệnh lý hoặc câu hỏi chưa đủ thông tin phân loại. Bắt buộc để `gold_topic_label` trống (`""`) và ghi rõ điểm phân vân tại `review_note`.

---

## 4. Danh sách 200 câu hỏi ứng viên kèm ô xác nhận của người duyệt

### Câu 001 — `ViHealthQA:test:1046` (ViHealthQA)
- **Nguyên văn câu hỏi:** Sưng amidan kéo dài có nguy hiểm không?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["amidan"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 002 — `ViHealthQA:test:1049` (ViHealthQA)
- **Nguyên văn câu hỏi:** Chỉ số xét nghiệm đờm 0-AFB là 15296 và 0 -AFB là 297 có ý nghĩa gì, có phải mắc lao không?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["đờm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 003 — `ViHealthQA:test:1130` (ViHealthQA)
- **Nguyên văn câu hỏi:** Phụ nữ mang thai có được tiêm vắc-xin phòng ngừa cúm không?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 004 — `ViHealthQA:test:1252` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi đã tiêm mũi một vaccine AstraZeneca, tôi bị phản ứng sau tiêm: Đau đầu, đau họng, nhức mỏi toàn thân, ớn lạnh, sốt 2 ngày 38,5 độ và qua ngày thứ 2 sau 38 giờ sau khi tiêm tôi đã bị ngất xỉu. Trường hợp của tôi có tiêm được mũi thứ 2 hay không?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `["đau họng","sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 005 — `ViHealthQA:test:1334` (ViHealthQA)
- **Nguyên văn câu hỏi:** Viêm xoang một bên kéo dài phải làm sao?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["Viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 006 — `ViHealthQA:test:1528` (ViHealthQA)
- **Nguyên văn câu hỏi:** Em năm nay 28 tuổi. Trước khi sinh con, em không bị dị ứng thức ăn gì cả, nhưng sau khi sinh con có lần em ăn tôm thẻ luộc bị nổi mẩn ngứa ở mặt và tiêu chảy, các triệu chứng này qua đêm thì hết. Một thời gian sau em ăn hải sản gồm tôm, sò huyết.... lại lặp lại. Khi ăn tôm với lượng ít thì em hay bị ngứa ở miệng nên sau đó em không ăn tôm nữa.Trước khi sinh em bé, em cũng chích rất nhiều loại vaccine như viêm gan B, ung thư cổ tử cung, cúm, sởi - quai bị - rubela, thủy đậu... và sau khi chích đều không có phản ứng bất thường. Với tình trạng như vậy, em có thể chích ngừa vaccine Covid-19 không vì công ty em cũng đang đăng ký để chích cho nhân viên.
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 007 — `ViHealthQA:test:1673` (ViHealthQA)
- **Nguyên văn câu hỏi:** Cho hỏi con trai tôi 22 tuổi, đã điều trị bịnh lao phổi trong năm 2019. Cháu bị dị ứng với hải sản tôm, cua, ăn vào là ngứa họng và sưng phù mắt, miệng. Vậy cháu có tiêm được vaccine ngừa Covid-19 không?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["ngứa họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 008 — `ViHealthQA:test:1703` (ViHealthQA)
- **Nguyên văn câu hỏi:** Bệnh nhân mắc u phổi bị nôn kèm ho ra máu có nguy hiểm không?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho ra máu"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 009 — `ViHealthQA:test:1716` (ViHealthQA)
- **Nguyên văn câu hỏi:** Mất khứu giác do viêm xoang mãn tính có thể điều trị được không?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 010 — `ViHealthQA:test:1725` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi đi khám bị viêm đa khớp, thường xuyên đau khớp ngón chân và tay, đau nửa đầu. Bác sĩ nói là tôi bị chèn dây thần kinh và thiếu máu lên não gây đau đầu. Tôi bị xoang mũi khoảng trên 10 năm. Tôi xin hỏi với các bệnh như trên có tiêm được vaccine phòng Covid-19 được không?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 011 — `ViHealthQA:test:1783` (ViHealthQA)
- **Nguyên văn câu hỏi:** Bị dị ứng kháng sinh và kháng viêm có chích ngừa được không ạ, thưa bác sĩ? Em đang bị viêm xoang có chích vaccine được không?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 012 — `ViHealthQA:test:1853` (ViHealthQA)
- **Nguyên văn câu hỏi:** Ho, sốt về đêm có phải cúm A không?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `["Ho","sốt","cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 013 — `ViHealthQA:test:305` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi hàng năm có chích ngừa vaccine cúm, nay chích vaccine Covid-19 có ảnh hưởng gì không? Tháng 7 này, tôi đến hẹn chích vaccine cúm.
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 014 — `ViHealthQA:test:907` (ViHealthQA)
- **Nguyên văn câu hỏi:** Viêm xoang và lệch vách ngăn mũi khiến dịch chảy xuống họng có nên mổ không?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["Viêm xoang"]`
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu hỏi về quyết định/phương pháp phẫu thuật trong đợt mở rộng.

### Câu 015 — `ViHealthQA:train:1226` (ViHealthQA)
- **Nguyên văn câu hỏi:** Viêm mũi dị ứng, vẹo vách ngăn có nguy hiểm không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["Viêm mũi dị ứng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 016 — `ViHealthQA:train:130` (ViHealthQA)
- **Nguyên văn câu hỏi:** Ho kéo dài điều trị như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["Ho kéo dài"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 017 — `ViHealthQA:train:1455` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tai phát ra âm thanh có phải ù tai không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["ù tai"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 018 — `ViHealthQA:train:1663` (ViHealthQA)
- **Nguyên văn câu hỏi:** Phụ nữ có thai và đang cho con bú có thể tiêm vaccine Covid-19 được không ạ? Ngoài ra, người có bệnh về hô hấp như viêm mũi dị ứng thì tiêm vaccine này có ảnh hưởng gì không ạ?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["viêm mũi dị ứng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 019 — `ViHealthQA:train:1739` (ViHealthQA)
- **Nguyên văn câu hỏi:** Ngày 25/6, tôi tiêm ngừa cúm Vaxigrip 0,5 ml và uống vaccine tả M.Orcvax tại VNVC. Bây giờ, tôi muốn tiêm vaccine ngừa Covid-19 có được không ? Nếu không, sau bao lâu thì an toàn để tiêm ngừa vaccine Covid-19?Chích ngừa cúm rồi sẽ không bị cảm, đúng không ạ ?Trên vỏ hộp vaccine cúm ghi ngày hết hạn là 6/21 nhưng ngày 25/6 mới chích thì chất lượng có ảnh hưởng không ạ?Sau khi tiêm đủ 2 mũi vaccine Covid-19, hiệu lực vaccine tồn tại bao lâu? Nếu chỉ tiêm một mũi, hiệu lực như thế nào, bao nhiêu %?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 020 — `ViHealthQA:train:1857` (ViHealthQA)
- **Nguyên văn câu hỏi:** Em bị viêm xoang mãn tính hay nhức đầu và gần đây bị rối loạn giấc ngủ đã điều trị nhưng có lúc tái phát. Vậy em tiêm vaccine Covid-19 có được không? Chồng em 62 tuổi mới tiêm vaccine mũi thứ nhất được một tuần thì có uống được thuốc hạ cholesterol, hạ men gan được không?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 021 — `ViHealthQA:train:2070` (ViHealthQA)
- **Nguyên văn câu hỏi:** Trẻ sơ sinh uống quá liều thuốc ho Mucosolvan có sao không?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 022 — `ViHealthQA:train:2099` (ViHealthQA)
- **Nguyên văn câu hỏi:** Em bị viêm mũi dị ứng, lại hay bị ngứa, thường xuyên phải dùng thuốc dị ứng. Năm 2016, em mang thai bé thứ hai thì bị tràn dịch màng phổi. Với những bệnh trên liệu em có được chích ngừa vaccine Covid-19 không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["viêm mũi dị ứng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 023 — `ViHealthQA:train:2388` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi năm nay 31 tuổi, có hai bệnh lý nền là viêm đa xoang và trào ngược dạ dày. Tôi có hai lần phải tiêm huyết thanh kháng uốn ván do tai nạn nghề nghiệp. Lần đầu chỉ tiêm huyết thanh, cơ thể không phản ứng gì. Lần thứ hai tiêm thử huyết thanh, tôi nổi mẩn vùng thử nhưng sau đó tôi vẫn được tiêm cả huyết thanh và mũi uốn ván một, cơ thể không phản ứng gì.Sau một tháng, tôi tiếp tục tiêm mũi uốn ván 2. Sau 2-3 ngày, cơ thể bắt đầu nổi mề đay và ngứa, tôi có đến bệnh viện và bác sĩ kê cho thuốc uống, qua 1-2 ngày hết ngứa và mề đay. Vậy với các bệnh lý nền và tiền sử dị ứng như vậy, tôi có thể tiêm được vaccine Covid-19 không ạ?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 024 — `ViHealthQA:train:240` (ViHealthQA)
- **Nguyên văn câu hỏi:** Nguyên nhân khạc ra đờm lẫn máu sau cắt amidan 6 tháng?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `["đờm","amidan"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 025 — `ViHealthQA:train:2625` (ViHealthQA)
- **Nguyên văn câu hỏi:** Trẻ khò khè mỗi khi viêm họng hay viêm phế quản có phải hen suyễn không?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["viêm họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 026 — `ViHealthQA:train:2640` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi thỉnh thoảng hắt xì hơi, sổ mũi lát sau tự hết, không có bệnh nền thì có thể tiêm vaccine Covid-19 được không thưa bác sĩ?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["hắt xì","sổ mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 027 — `ViHealthQA:train:2644` (ViHealthQA)
- **Nguyên văn câu hỏi:** Người mắc lao kê đang uống thuốc điều trị và sốt 39 độ có sao không?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 028 — `ViHealthQA:train:2832` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi năm nay 38 tuổi, bị tiền đình, viêm đại tràng, nhưng quan trọng là bị tiền sử dị ứng thuốc (không rõ thuốc gì, chỉ rõ uống sau khi bị cảm cúm), vậy tôi có được tiêm vaccine phòng Covid-19 hay không?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 029 — `ViHealthQA:train:2932` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tai chảy dịch vàng có phải viêm tai giữa không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["viêm tai giữa"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 030 — `ViHealthQA:train:3299` (ViHealthQA)
- **Nguyên văn câu hỏi:** Đau một bên đầu, hỉ ra máu sau lấy dịch mũi có gì bất thường?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["dịch mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 031 — `ViHealthQA:train:3320` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi năm nay 43 tuổi đang uống thuốc viêm xoang mũi, mai tôi có thể chích ngừa vaccine Covid-19 được không ạ?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 032 — `ViHealthQA:train:3652` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tình trạng ho đờm kéo dài không khỏi là dấu hiệu bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho đờm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 033 — `ViHealthQA:train:3668` (ViHealthQA)
- **Nguyên văn câu hỏi:** Điều trị đau họng, trào ngược dạ dày như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["đau họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 034 — `ViHealthQA:train:3901` (ViHealthQA)
- **Nguyên văn câu hỏi:** Choáng, hoa mắt,ù tai, nôn rất nhiều uống thuốc không đỡ nên làm gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["ù tai"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 035 — `ViHealthQA:train:3928` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi bị viêm xoang mãn tính, gan nhiễm mỡ bác sĩ bảo đang ở mức độ nhẹ. Tôi có thể tiêm vaccine Covid-19 được không?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 036 — `ViHealthQA:train:3964` (ViHealthQA)
- **Nguyên văn câu hỏi:** Năm 2013 tôi bị huyết khối tĩnh mạch nội sọ đoạn xoang ngang, biến chứng nhồi máu xuất huyết não thuỳ thái dương. Sau khi xét nghiệm máu bác sĩ kết luận tôi bị tăng đông máu do di truyền (hàm lượng Protein S Activity chỉ đạt 37,2). Hiện tại sức khỏe tôi ổn định, không có biểu hiện gì bất thường, không phải dùng thuốc điều trị. Vậy tôi có nên tiêm vaccine ngừa Covid-19 không? Nếu có thể tiêm được thì nên tiêm loại vaccine của hãng nào?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 037 — `ViHealthQA:train:4043` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi bị viêm mũi dị ứng và cơ địa có Bilirubin cao hơn bình thường thì có cần lưu ý gì khi tiêm vaccine Covid-19 không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["viêm mũi dị ứng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 038 — `ViHealthQA:train:4154` (ViHealthQA)
- **Nguyên văn câu hỏi:** Ngứa mũi chảy nước mũi kèm hắt hơi có phải viêm mũi dị ứng không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["Ngứa mũi","chảy nước mũi","hắt hơi","viêm mũi dị ứng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 039 — `ViHealthQA:train:4182` (ViHealthQA)
- **Nguyên văn câu hỏi:** Sốt kèm ho, sổ mũi, đau họng là dấu hiệu của bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `["Sốt","ho","sổ mũi","đau họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 040 — `ViHealthQA:train:4262` (ViHealthQA)
- **Nguyên văn câu hỏi:** Nguyên nhân cảm cúm dẫn đến hôi miệng là do đâu?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 041 — `ViHealthQA:train:4337` (ViHealthQA)
- **Nguyên văn câu hỏi:** Điều trị viêm tai giữa như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["viêm tai giữa"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 042 — `ViHealthQA:train:4339` (ViHealthQA)
- **Nguyên văn câu hỏi:** Đang bị thủy đậu có được uống thuốc hạ sốt không?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 043 — `ViHealthQA:train:4642` (ViHealthQA)
- **Nguyên văn câu hỏi:** Em có tiền sử sốc thuốc khi tiêm mũi đẻ không đau (tiêm dọc sống lưng từ lúc 11h đêm hôm trước đến tầm 5h sáng hôm sau vẫn không sinh được và khi đó có triệu chứng lạnh run phải hỗ trợ các biện pháp khi sinh...) Tuy nhiên, khi đó em không phẫu thuật.Sau đó vài năm có một lần uống thuốc ho và kháng sinh (em không nhớ loại thuốc) bị sưng phồng bàn tay và chân... có đi da liễu TP HCM và xác định dị ứng thuốc... Sau đó, em uống thuốc tầm một tháng thì khỏi tuy nhiên da lòng bàn tay và lòng bàn chân đều lột hết. Đến giờ cũng đã 11 năm mọi thứ ổn...Em có bệnh đau bao tử, thiếu máu, cách đây vài năm có phẫu thuật ruột thừa... và gần đây có tiêm mũi bạch hầu ở VNVC thì ổn... Xin bác sĩ cho biết em có tiêm vaccine Covid-19 được không?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 044 — `ViHealthQA:train:4904` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi bị hiện tượng Arthrus sau khi tiêm vaccine cúm mùa, vậy tôi có tiêm được vaccine Covid-19 không?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 045 — `ViHealthQA:train:5008` (ViHealthQA)
- **Nguyên văn câu hỏi:** Triệu chứng ù tai là do bệnh lý gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["ù tai"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 046 — `ViHealthQA:train:5017` (ViHealthQA)
- **Nguyên văn câu hỏi:** Đột nhiên chóng mặt, mắt tối sầm kèm chảy máu mũi là dấu hiệu bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["chảy máu mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 047 — `ViHealthQA:train:5061` (ViHealthQA)
- **Nguyên văn câu hỏi:** Đau nửa đầu, sáng dậy hay nghẹt mũi, hay quên là dấu hiệu bệnh gì và nên đi khám ở bệnh viện nào?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["nghẹt mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 048 — `ViHealthQA:train:5089` (ViHealthQA)
- **Nguyên văn câu hỏi:** Viêm xoang mãn tính có thể điều trị bằng cách phẫu thuật nội soi mũi không?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["Viêm xoang"]`
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu hỏi về quyết định/phương pháp phẫu thuật trong đợt mở rộng.

### Câu 049 — `ViHealthQA:train:5111` (ViHealthQA)
- **Nguyên văn câu hỏi:** Lúc trẻ, tôi bị dị ứng phấn hoa khi đi du học, khi về nước thì hết. Từ 5 năm nay, hàng năm tôi đều chích ngừa cảm cúm vì khi bị cảm thường kéo dài, đôi lúc giống như suyễn. Từ khi tiêm ngừa cúm, đỡ được 90%. Xin hỏi tôi có được tiêm ngừa Covid-19 không?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm","cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 050 — `ViHealthQA:train:5259` (ViHealthQA)
- **Nguyên văn câu hỏi:** Trẻ thở khò khè, ho và nôn ra máu là dấu hiệu của bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 051 — `ViHealthQA:train:5264` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi bi dị ứng khi uống thuốc giảm đau, hạ sốt Novalgin. Vậy có thể tiêm vaccine Covid-19 được không?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 052 — `ViHealthQA:train:5446` (ViHealthQA)
- **Nguyên văn câu hỏi:** Viêm amidan tái lại nên làm gì? Bệnh trào ngược dạ dày có liên quan viêm họng không?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["Viêm amidan","viêm họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 053 — `ViHealthQA:train:55` (ViHealthQA)
- **Nguyên văn câu hỏi:** Cách đây 3 năm, em bị dị ứng mẩn ngứa tôm, cua, cá... uống thuốc tây mới khỏi. Sau đó, em uống nam thì bớt hẵng. Nhưng hiện tại cơ thể em rất dễ phát nhiệt, lỗ tai hay lùng bùng, da nóng ran do ăn, uống đồ nóng như nước mắm cay, trà gừng hòa tan, vải thiều...Cơ thể em hơi gầy, hay bị đau đầu, choáng mặt và buồn nôn. Em đã từng uống thuốc thiếu máu não, rối loạn tiền đình, viêm xoang... Sắp tới công ty em có đợt chích vaccine Covid-19 tập trung, em có thể chích trong dịp này không?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 054 — `ViHealthQA:train:5538` (ViHealthQA)
- **Nguyên văn câu hỏi:** Sổ mũi có máu trong dịch và ù cả 2 tai là dấu hiệu của bệnh gì và cách điều trị?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["Sổ mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 055 — `ViHealthQA:train:6108` (ViHealthQA)
- **Nguyên văn câu hỏi:** Mang thai 4 tháng bị chảy máu mũi phải làm sao?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["chảy máu mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 056 — `ViHealthQA:train:6144` (ViHealthQA)
- **Nguyên văn câu hỏi:** Năm nay em 25 tuổi, khỏe mạnh bình thường. Khi em bị sốt em dùng thuốc hạ sốt nhưng đều bị nổi mẩn đỏ trên da và ngứa ngáy khó chịu sau khi uống khoảng 15-30 phút. Như vậy có phải em bị dị ứng không và nếu như vậy em có tiêm được vaccine Covid-19 không?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 057 — `ViHealthQA:train:6262` (ViHealthQA)
- **Nguyên văn câu hỏi:** Nữ giới viêm mũi dị ứng điều trị như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["viêm mũi dị ứng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 058 — `ViHealthQA:train:6746` (ViHealthQA)
- **Nguyên văn câu hỏi:** Ho có đờm kèm khó thở trong thời gian dài là bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["Ho có đờm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 059 — `ViHealthQA:train:6865` (ViHealthQA)
- **Nguyên văn câu hỏi:** Nang xoang trán là bệnh gì? Có nguy hiểm và phải mổ không?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["xoang"]`
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu hỏi về quyết định/phương pháp phẫu thuật trong đợt mở rộng.

### Câu 060 — `ViHealthQA:train:6876` (ViHealthQA)
- **Nguyên văn câu hỏi:** Bạn tôi ở Canada từng bị mắc Covid-19 nhưng không biết và vẫn đi chích ngừa vaccine. Chích xong thấy triệu chứng nghi ngờ và được test thử thì kết quả dương tính (do bị Covid mà không biết, tưởng cảm cúm thông thường và đã khoẻ bình thường nhưng lượng virus trong cơ thể vẫn còn). Vậy cho tôi hỏi, trong khi lượng virus trong người còn như thế mà chích vaccine có sao không? Do tôi đọc báo thấy ở Việt Nam khuyến cáo trường hợp nhiễm Covid-19 rồi không nên chích nữa. Bạn tôi vẫn được hẹn chích mũi 2.
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 061 — `ViHealthQA:train:6951` (ViHealthQA)
- **Nguyên văn câu hỏi:** Đau dạ dày uống kháng sinh điều trị viêm họng được không?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["viêm họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 062 — `ViHealthQA:train:726` (ViHealthQA)
- **Nguyên văn câu hỏi:** Vướng cổ họng, khạc đờm kéo dài có phải dấu hiệu của bệnh về phổi không?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["đờm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 063 — `ViHealthQA:validation:279` (ViHealthQA)
- **Nguyên văn câu hỏi:** Màng nhĩ trái lõm một phần trung tâm có phải mổ không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["Màng nhĩ"]`
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt yêu cầu loại câu hỏi về quyết định/phương pháp phẫu thuật trong đợt mở rộng.

### Câu 064 — `ViHealthQA:validation:435` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi bị viêm mũi dị ứng hàng ngày, thường bị hắt hơi, sổ mũi trong, ngứa mắt, tôi phải thường xuyên dùng thuốc để giảm các triệu chứng trên. Xin hỏi tối có thể tiêm vaccine được không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["viêm mũi dị ứng","hắt hơi","sổ mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 065 — `ViHealthQA:validation:591` (ViHealthQA)
- **Nguyên văn câu hỏi:** Tôi từng bị phản ứng sau khi tiêm ngừa uốn ván (dù chỉ mới thử thuốc), tiêm ngừa cúm mùa thì bị nổi mề đay cả người, tay chân, mặt mày sưng húp, tim đập nhanh, thường bị tụt huyết áp, rối loạn tiền đình... Vậy tôi có thể tiêm ngừa vaccine phòng Covid-19 được không?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 066 — `ViHealthQA:validation:693` (ViHealthQA)
- **Nguyên văn câu hỏi:** Thủng màng nhĩ bên tai trái có chữa được không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["màng nhĩ"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 067 — `ViHealthQA:validation:929` (ViHealthQA)
- **Nguyên văn câu hỏi:** Em bị viêm da cơ địa mãn tính không khỏi, bị viêm mũi dị ứng nhưng đã đỡ, thỉnh thoảng mới bị lại, bị dị ứng cua biển khi ăn như đau bụng, nhịp tim hơi nhanh thì có được tiêm vaccine Covid-19 không ạ?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["viêm mũi dị ứng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 068 — `ViMQ:test:52` (ViMQ)
- **Nguyên văn câu hỏi:** Đau ngứa họng nghẹt mũi và nổi hạch ở cổ là dấu hiệu của bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `["ngứa họng","nghẹt mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 069 — `ViMQ:test:608` (ViMQ)
- **Nguyên văn câu hỏi:** Đau thắt ngực, khó thở kèm đau đầu, ù tai có nguy cơ bị bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["ù tai"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 070 — `ViMQ:test:675` (ViMQ)
- **Nguyên văn câu hỏi:** Bé hay nghẹt mũi, ọc sữa khi no phải làm sao?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["nghẹt mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 071 — `ViMQ:test:776` (ViMQ)
- **Nguyên văn câu hỏi:** Đau thắt 2 bên ngực khi hắt hơi triệu chứng bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["hắt hơi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 072 — `ViMQ:test:79` (ViMQ)
- **Nguyên văn câu hỏi:** Phát hiện bị viêm amidan khi đang điều trị bệnh lao thì phải làm sao?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["viêm amidan"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 073 — `ViMQ:test:81` (ViMQ)
- **Nguyên văn câu hỏi:** Hắt hơi sổ mũi, đau nhức hai bên thái dương và trên đỉnh đầu, người mệt mỏi là triệu chứng bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["Hắt hơi","sổ mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 074 — `ViMQ:train:1014` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ đang uống kháng sinh điều trị viêm tai giữa có được tiêm vắc xin phế cầu?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["viêm tai giữa"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 075 — `ViMQ:train:1098` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ 5 tháng ho nhiều, ngạt mũi, hắt hơi có phải biểu hiện của dị ứng thuốc?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `["ho","ngạt mũi","hắt hơi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 076 — `ViMQ:train:1378` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ không sốt nhưng nổi ban đỏ có đáng lo?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 077 — `ViMQ:train:1673` (ViMQ)
- **Nguyên văn câu hỏi:** Mắc virus ho trong thời gian nuôi con bú có uống nghệ được không?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 078 — `ViMQ:train:1856` (ViMQ)
- **Nguyên văn câu hỏi:** Ngứa vòm miệng, sổ mũi lâu ngày liệu có đáng lo ngại?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["sổ mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 079 — `ViMQ:train:1946` (ViMQ)
- **Nguyên văn câu hỏi:** Cảm cúm, viêm thanh quản cấp dẫn đến mất tiếng cần làm gì?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `["Cảm cúm","viêm thanh quản"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 080 — `ViMQ:train:2011` (ViMQ)
- **Nguyên văn câu hỏi:** Mang thai 10 tuần mắc viêm họng cấp có ảnh hưởng đến thai nhi không?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["viêm họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 081 — `ViMQ:train:2111` (ViMQ)
- **Nguyên văn câu hỏi:** Nuốt nước bọt đau bên phải cổ do viêm họng cấp
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["viêm họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 082 — `ViMQ:train:2127` (ViMQ)
- **Nguyên văn câu hỏi:** Bạch cầu tăng nhẹ kèm sốt, quấy khóc ở trẻ phải làm sao?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 083 — `ViMQ:train:2363` (ViMQ)
- **Nguyên văn câu hỏi:** Làm thế nào để dịch viêm tai giữa tự tiêu?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["viêm tai giữa"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 084 — `ViMQ:train:2588` (ViMQ)
- **Nguyên văn câu hỏi:** Có nên chụp CT để tìm nguyên nhân đau đầu, ù tai, căng thẳng không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["ù tai"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 085 — `ViMQ:train:2617` (ViMQ)
- **Nguyên văn câu hỏi:** Bé bị sốt mắt đổ ghèn, chảy nước mắt phải làm thế nào?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 086 — `ViMQ:train:2621` (ViMQ)
- **Nguyên văn câu hỏi:** Uống thuốc điều trị viêm họng 20 ngày nhưng không đỡ, phải làm sao?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["viêm họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 087 — `ViMQ:train:2672` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ sốt 38 độ có nên cho uống thuốc hạ sốt không?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 088 — `ViMQ:train:2731` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ sơ sinh đi ngoài nhiều lần, phân vàng có mùi tanh và sốt nhẹ là dấu hiệu bệnh tiêu chảy?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt nhẹ"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 089 — `ViMQ:train:2758` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ sơ simh 23 ngày tuổi ho nhiều, hay bị sặc sữa là tình trạng gì?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 090 — `ViMQ:train:2925` (ViMQ)
- **Nguyên văn câu hỏi:** Cho trẻ ăn thử lòng đỏ trứng gà trước khi tiêm phòng cúm như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 091 — `ViMQ:train:2935` (ViMQ)
- **Nguyên văn câu hỏi:** Sử dụng thuốc hạ sốt đút hậu môn bao lâu thì hạ sốt?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 092 — `ViMQ:train:30` (ViMQ)
- **Nguyên văn câu hỏi:** Dùng thuốc cảm cúm khi đang điều trị viêm gan B có được không?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 093 — `ViMQ:train:3205` (ViMQ)
- **Nguyên văn câu hỏi:** Cần làm gì khi trẻ sốt cao kèm ho, sổ mũi?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `["sốt cao","ho","sổ mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 094 — `ViMQ:train:3247` (ViMQ)
- **Nguyên văn câu hỏi:** Đau họng, rát họng kéo dài là dấu hiệu bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["Đau họng","rát họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 095 — `ViMQ:train:3306` (ViMQ)
- **Nguyên văn câu hỏi:** Bà bầu dùng thuốc Bromance, Augmentin, Mepoly trị viêm tai ngoài có ảnh hưởng đến thai nhi?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["viêm tai ngoài"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 096 — `ViMQ:train:3429` (ViMQ)
- **Nguyên văn câu hỏi:** Phải làm sao khi bị ốm nghén sau khi cảm cúm?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 097 — `ViMQ:train:3606` (ViMQ)
- **Nguyên văn câu hỏi:** Viêm xoang ở trẻ em có thể chữa khỏi không?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["Viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 098 — `ViMQ:train:3746` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ bị sốt chân tay lạnh kèm đầu nóng nên làm gì?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 099 — `ViMQ:train:380` (ViMQ)
- **Nguyên văn câu hỏi:** Tự ý dùng thuốc kháng sinh điều trị viêm tai giữa cho trẻ được không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["viêm tai giữa"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 100 — `ViMQ:train:3982` (ViMQ)
- **Nguyên văn câu hỏi:** Hỏi đáp: Thường nhức tai, đau đầu kèm sưng chân răng là bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["nhức tai"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 101 — `ViMQ:train:4048` (ViMQ)
- **Nguyên văn câu hỏi:** Da nổi mẩn đỏ, ngứa ngáy do sốt xuất huyết làm gì cho hết?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 102 — `ViMQ:train:4060` (ViMQ)
- **Nguyên văn câu hỏi:** Ợ hơi, nóng ran lồng ngực sau cảm cúm phải làm sao?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 103 — `ViMQ:train:4219` (ViMQ)
- **Nguyên văn câu hỏi:** Viêm mũi dị ứng lâu ngày có chuyển thành phình đại cuốn mũi không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["Viêm mũi dị ứng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 104 — `ViMQ:train:4642` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ 5 tuổi mắc viêm xoang hàm và xoang sàng nên điều trị thế nào?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["viêm xoang","xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 105 — `ViMQ:train:473` (ViMQ)
- **Nguyên văn câu hỏi:** Bé ho vào buổi sáng là do đâu?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 106 — `ViMQ:train:4925` (ViMQ)
- **Nguyên văn câu hỏi:** Sốt, đau đầu uống thuốc tây nổi mẩn ngứa tay, chân là bị sao?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["Sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 107 — `ViMQ:train:5008` (ViMQ)
- **Nguyên văn câu hỏi:** Bị ngạt mũi có dùng thuốc Otrivin lâu dài được không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["ngạt mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 108 — `ViMQ:train:5071` (ViMQ)
- **Nguyên văn câu hỏi:** Bé ho, ọc sữa khi đang ngủ và bị sặc có sao không?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 109 — `ViMQ:train:511` (ViMQ)
- **Nguyên văn câu hỏi:** Sử dụng thuốc Amoxicillin liều 500mg ở trẻ bị viêm tai giữa bằng cách nào?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["viêm tai giữa"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 110 — `ViMQ:train:524` (ViMQ)
- **Nguyên văn câu hỏi:** Người mắc viêm xoang, đau rát 2 bên họng nên điều trị thế nào?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 111 — `ViMQ:train:526` (ViMQ)
- **Nguyên văn câu hỏi:** Biểu hiện thường gặp nhất của bệnh bạch hầu gần giống như viêm họng?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["viêm họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 112 — `ViMQ:train:5323` (ViMQ)
- **Nguyên văn câu hỏi:** Sau tiêm mũi 2 viêm não Nhật Bản trẻ sốt, nôn trớ, đi ngoài nhiều lần thì có nguy hiểm không?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 113 — `ViMQ:train:5345` (ViMQ)
- **Nguyên văn câu hỏi:** Cơ thể lúc nóng lúc lạnh không đáp ứng thuốc hạ sốt có đáng lo?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 114 — `ViMQ:train:559` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ nhiễm virus cúm A nên làm gì?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 115 — `ViMQ:train:5616` (ViMQ)
- **Nguyên văn câu hỏi:** Sốt và đau nhức bả vai có phải do tiêm vắc-xin bạch hầu?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["Sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 116 — `ViMQ:train:5775` (ViMQ)
- **Nguyên văn câu hỏi:** Thủng màng nhĩ có chữa khỏi được không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["màng nhĩ"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 117 — `ViMQ:train:5900` (ViMQ)
- **Nguyên văn câu hỏi:** Tiêm vắc-xin cúm trước khi có thai bao lâu?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 118 — `ViMQ:train:610` (ViMQ)
- **Nguyên văn câu hỏi:** Có phương pháp nào điều trị sỏi amidan không?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["amidan"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 119 — `ViMQ:train:6128` (ViMQ)
- **Nguyên văn câu hỏi:** Viêm mũi dị ứng kéo dài không thuyên giảm phải làm sao?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["Viêm mũi dị ứng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 120 — `ViMQ:train:6134` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ 19 tháng sốt cao co giật, đi không vững là dấu hiệu bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt cao"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 121 — `ViMQ:train:6175` (ViMQ)
- **Nguyên văn câu hỏi:** Thường xuyên nghẹt mũi buổi tối có phải do khối nang vòm mũi không và điều trị thế nào?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["nghẹt mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 122 — `ViMQ:train:6310` (ViMQ)
- **Nguyên văn câu hỏi:** Mẹ mắc cúm A có ảnh hưởng gì tới thai nhi không?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 123 — `ViMQ:train:6334` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ sốt uống thuốc không khỏi, lợi sưng đỏ rộp, miệng lở loét là dấu hiệu của bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 124 — `ViMQ:train:6418` (ViMQ)
- **Nguyên văn câu hỏi:** Mạch ở cổ và tim đập mạnh, mắt mờ, ù tai, cơ thể mỏi nhức là dấu hiệu bệnh lý gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["ù tai"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 125 — `ViMQ:train:6449` (ViMQ)
- **Nguyên văn câu hỏi:** Bé khỏi ốm đã tiêm phòng cúm được chưa?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 126 — `ViMQ:train:6639` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ ho và nôn trớ có nguy hiểm không?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 127 — `ViMQ:train:6721` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ sưng viêm tai tái phát liên tục cần điều trị thế nào?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["viêm tai"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 128 — `ViMQ:train:6726` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ 1 tuổi bị viêm tai giữa nên uống thuốc gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["viêm tai giữa"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 129 — `ViMQ:train:6768` (ViMQ)
- **Nguyên văn câu hỏi:** Bị ù tai có gây điếc đột ngột không?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["ù tai","điếc"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 130 — `ViMQ:train:693` (ViMQ)
- **Nguyên văn câu hỏi:** Khó thở kèm theo ho là tình trạng bệnh lý gì?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 131 — `ViMQ:train:6984` (ViMQ)
- **Nguyên văn câu hỏi:** Ho khạc ra máu, khó thở là dấu hiệu bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["Ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 132 — `ViMQ:train:823` (ViMQ)
- **Nguyên văn câu hỏi:** Viêm ống tai nên dùng thuốc gì để nhanh khỏi?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["Viêm ống tai"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 133 — `ViMQ:train:874` (ViMQ)
- **Nguyên văn câu hỏi:** Tiêm vắc-xin liều phối hợp phòng bệnh bạch hầu, uốn ván, ho gà, bại liệt như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 134 — `ViMQ:train:894` (ViMQ)
- **Nguyên văn câu hỏi:** Bệnh viêm mũi dị ứng là gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["viêm mũi dị ứng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 135 — `ViMQ:train:910` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ cần được tiêm bao nhiêu mũi vắc-xin cúm?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 136 — `ViMQ:validation:116` (ViMQ)
- **Nguyên văn câu hỏi:** Nhức kèm theo giật mí mắt phải do viêm xoang hay do đâu?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 137 — `ViMQ:validation:48` (ViMQ)
- **Nguyên văn câu hỏi:** Trẻ sổ mũi kèm theo sốt nhẹ có cần dùng kháng sinh không?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `["sổ mũi","sốt nhẹ"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 138 — `ViMQ:validation:485` (ViMQ)
- **Nguyên văn câu hỏi:** Xuất hiện triệu chứng ho, buồn nôn và đau đầu sau khi quan hệ tình dục
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 139 — `ViMQ:validation:601` (ViMQ)
- **Nguyên văn câu hỏi:** Cảm cúm trong thai kỳ tháng thứ 6 có ảnh hưởng thai nhi không?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["Cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 140 — `ViMQ:validation:687` (ViMQ)
- **Nguyên văn câu hỏi:** Triệu chứng đau hai bên tai kèm sốt nhẹ cảnh báo bệnh lý gì?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt nhẹ"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 141 — `ViMQ:validation:727` (ViMQ)
- **Nguyên văn câu hỏi:** Bị ù tai một bên cần làm gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["ù tai"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 142 — `ViMQ:validation:862` (ViMQ)
- **Nguyên văn câu hỏi:** Bị viêm tai giữa kèm theo đau nửa đầu phải làm sao?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["viêm tai giữa"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 143 — `ViMedAQA:test:drug_3477` (ViMedAQA)
- **Nguyên văn câu hỏi:** Thuốc Aspirin pH8 có tác dụng gì trong các trường hợp cảm cúm thông thường?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 144 — `ViMedAQA:train:body-part_3049` (ViMedAQA)
- **Nguyên văn câu hỏi:** Vòi nhĩ có công dụng gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["Vòi nhĩ"]`
- **Quyết định của tôi:** `reviewed` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `trieu_chung_tai` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt cho phép chọn một trong hai câu trùng ý 144/145; giữ câu 144 về chức năng vòi nhĩ, chủ đề tai.

### Câu 145 — `ViMedAQA:train:body-part_4872` (ViMedAQA)
- **Nguyên văn câu hỏi:** Vòi nhĩ có chức năng gì?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_tai` | Từ khóa tìm thấy: `["Vòi nhĩ"]`
- **Quyết định của tôi:** `excluded` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** *(để trống)* *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người duyệt chọn giữ câu 144; loại câu 145 vì cùng nội dung hỏi chức năng vòi nhĩ.

### Câu 146 — `ViMedAQA:train:disease_10175` (ViMedAQA)
- **Nguyên văn câu hỏi:** Vì sao thuốc điều trị dị ứng, thuốc điều trị cảm lạnh và thuốc ức chế sự thèm ăn lại gây ra chứng tăng huyết áp?
- **Nhãn gợi ý (chưa duyệt):** `cam_lanh` | Từ khóa tìm thấy: `["cảm lạnh"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 147 — `ViMedAQA:train:disease_11014` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cách chẩn đoán chính của bệnh ung thư amidan là gì?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["amidan"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 148 — `ViMedAQA:train:disease_11393` (ViMedAQA)
- **Nguyên văn câu hỏi:** Nguyên nhân khiến người bị ung thư máu dễ bị sốt là gì?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 149 — `ViMedAQA:train:disease_12230` (ViMedAQA)
- **Nguyên văn câu hỏi:** VA sẽ biến mất khi chúng ta trưởng thành?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `[]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 150 — `ViMedAQA:train:disease_12733` (ViMedAQA)
- **Nguyên văn câu hỏi:** Tại sao trẻ em và thanh thiếu niên đang hồi phục sau bệnh thủy đậu hoặc các triệu chứng giống cúm không nên dùng Aspirin?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 151 — `ViMedAQA:train:disease_12775` (ViMedAQA)
- **Nguyên văn câu hỏi:** Người bị viêm họng do trào ngược cần phải làm gì sau khi ăn?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["viêm họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 152 — `ViMedAQA:train:disease_13634` (ViMedAQA)
- **Nguyên văn câu hỏi:** Triệu chứng sốt xuất hiện khi nào trong quá trình diễn tiến bệnh viêm ruột thừa?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 153 — `ViMedAQA:train:disease_13935` (ViMedAQA)
- **Nguyên văn câu hỏi:** Viêm tuyến tiền liệt cấp tính có triệu chứng sốt không?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 154 — `ViMedAQA:train:disease_14050` (ViMedAQA)
- **Nguyên văn câu hỏi:** Nguyên nhân nào dẫn đến viêm xoang mãn tính?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 155 — `ViMedAQA:train:disease_1452` (ViMedAQA)
- **Nguyên văn câu hỏi:** Biểu hiện của bệnh cúm mùa nặng hơn ở những người nào?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 156 — `ViMedAQA:train:disease_1972` (ViMedAQA)
- **Nguyên văn câu hỏi:** Hen suyễn và sốt cỏ khô có liên quan gì với nhau khi biểu hiện cùng một lúc?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 157 — `ViMedAQA:train:disease_368` (ViMedAQA)
- **Nguyên văn câu hỏi:** Đặc điểm của màng giả trong bệnh bạch hầu vùng họng và amidan như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["amidan"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 158 — `ViMedAQA:train:disease_5095` (ViMedAQA)
- **Nguyên văn câu hỏi:** Viêm mũi gây ngủ ngáy như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["Viêm mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 159 — `ViMedAQA:train:disease_8148` (ViMedAQA)
- **Nguyên văn câu hỏi:** Hội chứng sốt cabin thường bao gồm những cảm giác nào?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 160 — `ViMedAQA:train:disease_8191` (ViMedAQA)
- **Nguyên văn câu hỏi:** Sốt rét có thể gây ra vấn đề gì?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["Sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 161 — `ViMedAQA:train:disease_8205` (ViMedAQA)
- **Nguyên văn câu hỏi:** Nếu không mắc bệnh sốt thung lũng, có cần đề phòng không?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 162 — `ViMedAQA:train:disease_8292` (ViMedAQA)
- **Nguyên văn câu hỏi:** Khi sốt xuất huyết, cần phải làm gì để theo dõi bệnh tại nhà?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 163 — `ViMedAQA:train:disease_8359` (ViMedAQA)
- **Nguyên văn câu hỏi:** Trẻ em bị tay chân miệng có thể cho uống thuốc gì để hạ sốt và giảm đau?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 164 — `ViMedAQA:train:disease_9528` (ViMedAQA)
- **Nguyên văn câu hỏi:** Nghiệm pháp ho có thể được thực hiện để chẩn đoán tình trạng nào?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 165 — `ViMedAQA:train:drug_1289` (ViMedAQA)
- **Nguyên văn câu hỏi:** Aibezym có gây sốt cao không?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["sốt cao"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 166 — `ViMedAQA:train:drug_2784` (ViMedAQA)
- **Nguyên văn câu hỏi:** Anaferon Materia có hiệu quả trong điều trị bệnh cúm không?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 167 — `ViMedAQA:train:drug_534` (ViMedAQA)
- **Nguyên văn câu hỏi:** Khi sử dụng thuốc Aclasta có thể gặp triệu chứng giống cúm nào?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 168 — `ViMedAQA:train:drug_6422` (ViMedAQA)
- **Nguyên văn câu hỏi:** Khi dùng thuốc Broncho-Vaxom, các triệu chứng ho, hen có thể xuất hiện như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 169 — `ViMedAQA:train:drug_6607` (ViMedAQA)
- **Nguyên văn câu hỏi:** Những trường hợp nào nên thận trọng khi dùng thuốc ho Bảo Thanh dạng viên ngậm?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 170 — `ViMedAQA:train:drug_8135` (ViMedAQA)
- **Nguyên văn câu hỏi:** Thuốc Chymodk có tác dụng gì đối với những người bị hen, viêm phế quản, viêm xoang cấp hay các bệnh lý về phổi?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["viêm xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 171 — `ViMedAQA:train:medicine_10011` (ViMedAQA)
- **Nguyên văn câu hỏi:** Bài thuốc chữa viêm họng, viêm phổi, sưng amidan từ Sâm đại hành có tác dụng gì?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["viêm họng","amidan"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 172 — `ViMedAQA:train:medicine_10383` (ViMedAQA)
- **Nguyên văn câu hỏi:** Tang bạch bì có thể dùng để chữa bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `[]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 173 — `ViMedAQA:train:medicine_11347` (ViMedAQA)
- **Nguyên văn câu hỏi:** Tinh dầu húng chanh chứa những hoạt chất quý có tác dụng trị ho, tiêu đờm tốt?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho","đờm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 174 — `ViMedAQA:train:medicine_11492` (ViMedAQA)
- **Nguyên văn câu hỏi:** Làm cách nào tinh dầu nghệ giúp cải thiện chứng cảm lạnh thông thường?
- **Nhãn gợi ý (chưa duyệt):** `cam_lanh` | Từ khóa tìm thấy: `["cảm lạnh"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 175 — `ViMedAQA:train:medicine_1204` (ViMedAQA)
- **Nguyên văn câu hỏi:** Bồ hòn được sử dụng để điều trị tình trạng nào?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `[]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 176 — `ViMedAQA:train:medicine_12349` (ViMedAQA)
- **Nguyên văn câu hỏi:** Người bệnh với cảm mạo do lạnh sẽ sử dụng Tế tân như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `cam_lanh` | Từ khóa tìm thấy: `["cảm mạo"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 177 — `ViMedAQA:train:medicine_13216` (ViMedAQA)
- **Nguyên văn câu hỏi:** Làm thế nào để uống thuốc trị cảm mạo từ trái tắc một cách hiệu quả nhất?
- **Nhãn gợi ý (chưa duyệt):** `cam_lanh` | Từ khóa tìm thấy: `["cảm mạo"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 178 — `ViMedAQA:train:medicine_13448` (ViMedAQA)
- **Nguyên văn câu hỏi:** Theo bài thuốc, người bệnh nên uống nước sắc từ lá cây Đuôi chuột bao nhiêu lần mỗi ngày?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `[]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 179 — `ViMedAQA:train:medicine_13637` (ViMedAQA)
- **Nguyên văn câu hỏi:** Đại hồi có tác dụng gì đối với bệnh cúm?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 180 — `ViMedAQA:train:medicine_2249` (ViMedAQA)
- **Nguyên văn câu hỏi:** Trong bài thuốc chứa cây Giao, người ta dùng cây Giao để làm gì?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `[]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 181 — `ViMedAQA:train:medicine_2985` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cần chuẩn bị những loại nguyên liệu nào để sắc thuốc chữa ho ra máu từ Cúc mốc?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho ra máu"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 182 — `ViMedAQA:train:medicine_3082` (ViMedAQA)
- **Nguyên văn câu hỏi:** Tại sao món cháo cải cúc có thể giúp trị cảm cúm?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 183 — `ViMedAQA:train:medicine_5447` (ViMedAQA)
- **Nguyên văn câu hỏi:** Để chữa cảm mạo do mắc phong hàn, người bệnh nên dùng bao nhiêu gram Hương nhu trắng?
- **Nhãn gợi ý (chưa duyệt):** `cam_lanh` | Từ khóa tìm thấy: `["cảm mạo"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 184 — `ViMedAQA:train:medicine_5762` (ViMedAQA)
- **Nguyên văn câu hỏi:** Ngoài Lá Hồng bì, còn có thể dùng loại thảo dược nào khác để phòng ngừa cảm cúm?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 185 — `ViMedAQA:train:medicine_5892` (ViMedAQA)
- **Nguyên văn câu hỏi:** Kha tử thường được sắc với loại dược liệu nào để chữa ho lâu ngày, mất tiếng?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 186 — `ViMedAQA:train:medicine_6080` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cách dùng hoa khế để trị ho như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `ho_dom` | Từ khóa tìm thấy: `["ho"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 187 — `ViMedAQA:train:medicine_7034` (ViMedAQA)
- **Nguyên văn câu hỏi:** Mật ong Manuka có thể dùng để giảm đau họng khi dùng bằng cách nào?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["đau họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 188 — `ViMedAQA:train:medicine_7334` (ViMedAQA)
- **Nguyên văn câu hỏi:** Các thành phần cần chuẩn bị để chữa cảm mạo, ăn uống không tiêu từ Mùi tàu là gì?
- **Nhãn gợi ý (chưa duyệt):** `cam_lanh` | Từ khóa tìm thấy: `["cảm mạo"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 189 — `ViMedAQA:train:medicine_771` (ViMedAQA)
- **Nguyên văn câu hỏi:** Bạch cương tàm được sử dụng trong bài thuốc chữa bệnh nào?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `[]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 190 — `ViMedAQA:train:medicine_8896` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cây phòng phong có thể dùng để điều trị bệnh gì ngoài các chứng cảm cúm?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 191 — `ViMedAQA:train:medicine_9081` (ViMedAQA)
- **Nguyên văn câu hỏi:** Quế chi có tác dụng gì trong điều trị cảm lạnh?
- **Nhãn gợi ý (chưa duyệt):** `cam_lanh` | Từ khóa tìm thấy: `["cảm lạnh"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 192 — `ViMedAQA:train:medicine_9353` (ViMedAQA)
- **Nguyên văn câu hỏi:** Cách dùng Rau mương để chữa bệnh viêm họng, viêm amidan như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["viêm họng","viêm amidan"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 193 — `ViMedAQA:train:medicine_997` (ViMedAQA)
- **Nguyên văn câu hỏi:** Tác dụng của bạch đàn trong việc điều trị cảm lạnh như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `cam_lanh` | Từ khóa tìm thấy: `["cảm lạnh"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 194 — `ViMedAQA:validation:body-part_2299` (ViMedAQA)
- **Nguyên văn câu hỏi:** Một sự bất thường ở bất kỳ xoang nào sẽ gây ra điều gì?
- **Nhãn gợi ý (chưa duyệt):** `xoang` | Từ khóa tìm thấy: `["xoang"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 195 — `ViMedAQA:validation:disease_1114` (ViMedAQA)
- **Nguyên văn câu hỏi:** Chảy máu mũi thường xuyên là như thế nào?
- **Nhãn gợi ý (chưa duyệt):** `trieu_chung_mui` | Từ khóa tìm thấy: `["Chảy máu mũi"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 196 — `ViMedAQA:validation:disease_4678` (ViMedAQA)
- **Nguyên văn câu hỏi:** Tại sao thuốc cảm lạnh và dị ứng có thể gây khó ngủ?
- **Nhãn gợi ý (chưa duyệt):** `cam_lanh` | Từ khóa tìm thấy: `["cảm lạnh"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 197 — `ViMedAQA:validation:disease_8214` (ViMedAQA)
- **Nguyên văn câu hỏi:** Sốt thấp khớp có thể xảy ra ở lứa tuổi nào?
- **Nhãn gợi ý (chưa duyệt):** `sot` | Từ khóa tìm thấy: `["Sốt"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 198 — `ViMedAQA:validation:drug_8238` (ViMedAQA)
- **Nguyên văn câu hỏi:** Các tác dụng không mong muốn của thực phẩm chức năng Cilzec bao gồm những tác dụng nào khác ngoài tiêu chảy và viêm họng?
- **Nhãn gợi ý (chưa duyệt):** `hong_amidan` | Từ khóa tìm thấy: `["viêm họng"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** `[Chờ điền]`

### Câu 199 — `ViMedAQA:validation:medicine_12495` (ViMedAQA)
- **Nguyên văn câu hỏi:** Tỏi có tác dụng ra sao trong việc điều trị bệnh truyền nhiễm và cảm cúm?
- **Nhãn gợi ý (chưa duyệt):** `cam_cum` | Từ khóa tìm thấy: `["cảm cúm"]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

### Câu 200 — `ViMedAQA:validation:medicine_9426` (ViMedAQA)
- **Nguyên văn câu hỏi:** Trong dân gian, rau răm được dùng để điều trị bệnh gì?
- **Nhãn gợi ý (chưa duyệt):** *(Chưa có nhãn đơn tự động)* | Từ khóa tìm thấy: `[]`
- **Quyết định của tôi:** `[Chờ điền]` *(reviewed / excluded / needs_discussion)*
- **Nhãn tôi chọn:** `[Chờ điền]` *(chọn 1 trong 8 nhãn nếu reviewed; để trống nếu excluded hoặc needs_discussion)*
- **Ghi chú của tôi:** Người dùng chưa duyệt nội dung thảo dược/bài thuốc hoặc mẹo dân gian; giữ pending, chưa dùng train hay kho trả lời.

---

## 5. Mẫu xác nhận gộp (Dành cho người duyệt gửi quyết định nhanh)

Khi duyệt, bạn có thể sao chép đoạn dưới đây để phản hồi nhanh:

```text
Người duyệt: hoai_an
Ngày duyệt: YYYY-MM-DD

1. Đồng ý nhãn gợi ý cho các STT: [...]

2. Đổi nhãn các STT:
- STT [...] đổi thành [...] vì [...]

3. Loại các STT (excluded):
- STT [...] vì [...]

4. Giữ thảo luận (needs_discussion):
- STT [...] vì [...]
```

---

## Trạng thái bản công bố

Bản công bố giữ nguyên 200 câu nguồn và các quyết định đã xác nhận: 1 reviewed, 5 excluded, 194 pending. Trong số pending có 26 câu thảo dược/bài thuốc hoặc mẹo dân gian chưa được duyệt. Bộ đề xuất AI cho 168 câu đang sửa lỗi nên chưa được đưa lên GitHub; không dùng các diễn giải đó như dữ liệu đã duyệt.

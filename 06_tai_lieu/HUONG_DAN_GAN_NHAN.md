# Hướng dẫn gán nhãn chủ đề câu hỏi (BacSiAi)

Phiên bản: **1.1 (Cập nhật quy tắc chuẩn hóa cho tập Pilot)**  
Ngày cập nhật: **28/11/2026**  
Tài liệu tham chiếu: [PROJECT.md](PROJECT.md), [TU_DIEN_DU_LIEU.md](TU_DIEN_DU_LIEU.md), [QUY_UOC_LUU_TRU.md](QUY_UOC_LUU_TRU.md).

---

## 1. Mục đích và nguyên tắc cốt lõi

Tài liệu này hướng dẫn người trực tiếp thực hiện gán nhãn thủ công cho các câu hỏi y tế thuộc phạm vi chuyên khoa Tai Mũi Họng và các chứng hô hấp trên thường gặp (ho, sốt, cảm lạnh, cúm).

### 1.1. Phân biệt chủ đề, ý định hỏi và thực thể y tế
Khi đọc câu hỏi, người gán nhãn cần phân biệt rạch ròi 3 trục thông tin:
- **Chủ đề (`topic_label`) - Mục tiêu gán nhãn chính:** Câu hỏi đang hướng về bộ phận, cơ quan hay vấn đề bệnh lý chính nào? (Ví dụ: mũi, tai, xoang, họng, ho đờm, cảm cúm...).
- **Ý định hỏi (`intent_label`):** Người dùng muốn biết điều gì về chủ đề đó? (Ví dụ: tìm nguyên nhân `cause`, hỏi cách chẩn đoán `diagnosis`, hỏi phương pháp điều trị `treatment`, hỏi mức độ nghiêm trọng `severity`). Đây là trục dữ liệu riêng từ ViMQ, **không gán đè vào nhãn chủ đề**.
- **Thực thể y tế (`entities` / `keywords`):** Các từ ngữ cụ thể xuất hiện trong câu (tên triệu chứng, tên thuốc, bộ phận cơ thể). **Sự xuất hiện của từ khóa không đồng nghĩa với chủ đề chính của câu.**

> [!IMPORTANT]
> **Phân loại nội dung câu hỏi, KHÔNG chẩn đoán bệnh.**
> Nhiệm vụ của người gán nhãn là xác định *trọng tâm nội dung câu hỏi đề cập chủ yếu đến chủ đề gì*, hoàn toàn không phải là bác sĩ kết luận người hỏi đang mắc bệnh gì.
> - Nếu người hỏi viết: *"Tôi bị đau đầu, sốt nhẹ và ngạt mũi, có phải viêm xoang không?"* -> Người hỏi đang chủ động đặt câu hỏi nghi vấn về **xoang**, nên trọng tâm là `xoang`.
> - Nhưng nếu người hỏi chỉ viết: *"Tôi bị đau đầu vùng trán và ngạt mũi 3 ngày nay"* mà không hề nhắc đến xoang -> **Không được tự suy diễn** ra viêm xoang để gán nhãn `xoang`. Trường hợp này câu hỏi mô tả triệu chứng mũi và đau đầu, cần gán theo triệu chứng trọng tâm (ví dụ `trieu_chung_mui`) hoặc đánh dấu `needs_discussion` nếu chưa rõ ràng.

### 1.2. Các quy tắc quan trọng
1. **Chọn chủ đề theo trọng tâm người dùng đang hỏi:** Luôn căn cứ vào vấn đề chính mà người hỏi muốn tìm hiểu, giải đáp hoặc băn khoăn nhiều nhất trong câu văn.
2. **Không tự suy diễn bệnh từ triệu chứng đơn lẻ hoặc hoàn cảnh:**
   - Không suy ra `cam_cum` chỉ vì câu hỏi có nhắc `ho` và `sot`.
   - Không suy ra `xoang` chỉ vì người hỏi kể đau trán, căng tức mặt, nghẹt mũi hay tính chất của dịch mũi.
   - Không suy ra `cam_lanh` chỉ vì câu hỏi nhắc đến việc đi mưa, dầm gió hay thay đổi thời tiết nếu người hỏi chỉ hỏi cách hạ sốt hoặc trị đau họng.
3. **Từ khóa không mặc định là chủ đề chính:**
   - Phân biệt chủ đề hiện tại với **tiền sử** (*"Trước đây từng bị viêm xoang, nay đau tai"* -> trọng tâm hiện tại là tai `trieu_chung_tai`, xoang chỉ là tiền sử).
   - Phân biệt với **phủ định** (*"Bác sĩ khám bảo không phải viêm xoang, tôi chỉ bị ngứa mũi"* -> chủ đề là `trieu_chung_mui`).
   - Phân biệt với **nội dung được nhắc phụ / làm nền** (*"Uống thuốc xoang bị đau dạ dày"* -> câu hỏi hỏi về tác dụng phụ tiêu hóa, không hỏi cách chữa xoang).
   - Cảnh giác với **từ đồng hình ngoài phạm vi y khoa tai mũi họng** (ví dụ: *"xoang hang"* trong rò động mạch xoang hang là cấu trúc mạch máu thần kinh sọ não; *"xoang tim"*).
4. **Không tự gán ngoài phạm vi chỉ vì không khớp từ điển:** Bộ từ điển từ khóa chỉ mang tính gợi ý kỹ thuật. Nếu câu hỏi dùng cách diễn đạt dân gian hoặc đồng nghĩa mà từ điển chưa có nhưng nội dung rõ ràng thuộc phạm vi tai mũi họng, hãy gán đúng chủ đề đó.
5. **Giữ tính khách quan và quy tắc không ép nhãn:** Khi câu hỏi mơ hồ, mâu thuẫn hoặc chưa rõ ràng, đánh dấu `needs_discussion`, tuyệt đối không cố ép vào một nhãn chủ quan.

### 1.3. Quy tắc hỗ trợ hành vi chatbot và truy xuất hỏi đáp (Thiết kế đã chốt)
- **Tiếp nhận cách hỏi đời thường:** Chấp nhận câu kể triệu chứng, cách diễn đạt dân gian, lỗi chính tả, viết tắt và từ đồng nghĩa. Không bắt người dùng phải biết tên bệnh hay tự chọn nhãn trước khi hỏi.
- **Tách biệt nhãn phân loại đơn nhãn và truy xuất hỏi đáp:**
  + Mô hình train hiện tại là bài toán đơn nhãn (chọn 1 trong 8 nhãn TMH).
  + Tầng hỏi đáp sau này có thể kết hợp tìm kiếm nội dung từ nhiều chủ đề (`cam_cum` và `cam_lanh`, `xoang` và `trieu_chung_mui`...) và từ cả 3 bộ dữ liệu (`ViMQ`, `ViHealthQA`, `ViMedAQA`).
  + Câu hỏi đa chủ đề chưa chốt nhãn phân loại đơn nhãn được gán `needs_discussion` (nhãn chuẩn để trống), nhưng vẫn sẽ được hỗ trợ trả lời đa nguồn trong hệ thống hỏi đáp.
- **Hỏi lại khi cần quyết định can thiệp hoặc thiếu ngữ cảnh:**
  + Câu hỏi cá nhân về chỉ định can thiệp ("có cần phẫu thuật/cắt/mổ không") không được kết luận ngay có/không; cần hỏi ngắn gọn thêm thông tin lâm sàng.
  + Không loại câu hỏi khỏi tập dữ liệu chỉ vì có từ phẫu thuật. Nhãn chủ đề và quyết định hỏi lại là hai trường thông tin độc lập.

---

## 2. Danh mục 8 nhãn khởi đầu

Dự án hiện sử dụng 8 nhãn chủ đề khởi đầu (theo `02_du_lieu/filedata/config/labels.json`):

```text
1. ho_dom           (Câu hỏi về ho và đờm)
2. trieu_chung_mui   (Câu hỏi về triệu chứng mũi, viêm mũi)
3. xoang            (Câu hỏi có nhắc xoang hoặc viêm xoang)
4. hong_amidan      (Câu hỏi về họng, amidan và thanh quản)
5. trieu_chung_tai  (Câu hỏi về tai và thính lực)
6. cam_lanh         (Câu hỏi có nhắc cảm lạnh hoặc cảm mạo)
7. cam_cum          (Câu hỏi có nhắc cúm)
8. sot              (Câu hỏi có nhắc sốt)
```

---

## 3. Hướng dẫn chi tiết từng nhãn

### 3.1. `ho_dom` (Ho và đờm)
- **Ý nghĩa:** Câu hỏi tập trung vào triệu chứng ho (ho khan, ho có đờm, ho dai dẳng, ho ra máu, ho về đêm) hoặc tính chất của đờm (đờm xanh, đờm vàng, đờm vướng cổ).
- **Trường hợp chọn:**
  - Trọng tâm câu hỏi là về cơn ho, tần suất ho hoặc các đặc điểm của đờm.
  - Ví dụ: *"Ho kéo dài hơn 2 tuần không khỏi phải làm sao?"*, *"Đờm có màu xanh đặc buổi sáng là dấu hiệu gì?"*.
- **Trường hợp không nên chọn:**
  - Ho chỉ là biểu hiện phụ đi kèm trong câu hỏi tập trung hỏi về bệnh lý họng/amidan hoặc tai.
  - Người hỏi chỉ hỏi về viêm họng hạt gây nuốt vướng -> xem xét `hong_amidan`.
- **Phân biệt:**
  - *Với `hong_amidan`:* Nếu câu hỏi nhấn mạnh cảm giác ngứa rát họng, sưng đau amidan, nuốt đau -> chọn `hong_amidan`. Nếu than phiền trọng tâm là cơn ho, cơn rũ rượi, khạc đờm -> chọn `ho_dom`.

### 3.2. `trieu_chung_mui` (Triệu chứng mũi, viêm mũi)
- **Ý nghĩa:** Câu hỏi về khoang mũi và các triệu chứng tại mũi: nghẹt mũi, tắc mũi, chảy nước mũi (sổ mũi), ngứa mũi, hắt hơi liên tục, polyp mũi, chảy máu cam (chảy máu mũi), viêm mũi dị ứng.
- **Trường hợp chọn:**
  - Vấn đề trọng tâm xảy ra tại mũi hoặc niêm mạc mũi.
  - Ví dụ: *"Sáng ngủ dậy hay bị hắt xì và chảy nước mũi trong suốt"*, *"Bị nghẹt một bên mũi khi nằm nghiêng có sao không?"*, *"Chảy máu cam thường xuyên ở trẻ nhỏ cần khám gì?"*.
- **Trường hợp không nên chọn:**
  - Triệu chứng mũi chỉ xuất hiện như một phần phụ trong câu hỏi mà trọng tâm người hỏi đang hỏi trực tiếp về xoang hoặc phẫu thuật xoang.
- **Phân biệt:**
  - *Với `xoang`:* Chỉ gán `xoang` khi người hỏi trực tiếp nhắc đến hoặc hỏi về xoang/viêm xoang. Nếu người hỏi chỉ kể nghẹt mũi, chảy nước mũi hay đau nhức trán mà không đề cập xoang -> gán `trieu_chung_mui` (nếu mũi là trọng tâm) hoặc `needs_discussion`, tuyệt đối không tự chẩn đoán xoang.

### 3.3. `xoang` (Xoang và viêm xoang)
- **Ý nghĩa:** Câu hỏi mà trọng tâm người hỏi đề cập trực tiếp đến xoang, bệnh lý viêm xoang (xoang trán, xoang hàm, xoang sàng, xoang bướm, viêm đa xoang) hoặc phương pháp điều trị xoang (mổ xoang, xông xoang).
- **Trường hợp chọn:**
  - Câu hỏi trực tiếp hỏi về xoang hoặc viêm xoang.
  - Ví dụ: *"Bị viêm xoang hàm có cần mổ không?"*, *"Thuốc nào trị dứt điểm viêm xoang mạn tính?"*, *"Bác sĩ cho hỏi xông mũi xoang bằng lá cây có tốt không?"*.
- **Trường hợp không nên chọn:**
  - **Không tự suy từ triệu chứng:** Người hỏi chỉ kể nghẹt mũi, chảy dịch vàng, nhức trán, đau mặt nhưng không hỏi về xoang -> KHÔNG được gán `xoang`.
  - **Không ưu tiên xoang chỉ vì có từ khóa:** Nếu từ khóa "xoang" chỉ xuất hiện ở tiền sử (*"từng bị xoang 2 năm trước, nay bị ù tai"* -> chọn `trieu_chung_tai`) hoặc phủ định (*"đi nội soi bác sĩ bảo không phải xoang, vậy tôi nghẹt mũi do đâu?"* -> chọn `trieu_chung_mui`).
  - **Từ đồng hình ngoài phạm vi Tai Mũi Họng:** Ví dụ *"rò rỉ động mạch xoang hang"*, *"viêm tắc xoang tĩnh mạch não"* -> Đây là cấu trúc mạch máu nội sọ, không thuộc bệnh học xoang tai mũi họng -> đánh dấu `excluded` hoặc `needs_discussion`.
- **Phân biệt:**
  - *Với `trieu_chung_mui`:* Chỉ gán `xoang` khi nội dung câu hỏi thực sự xoay quanh vấn đề xoang. Mọi triệu chứng nghẹt, chảy mũi thông thường không nhắc xoang đều thuộc `trieu_chung_mui`.

### 3.4. `hong_amidan` (Họng, amidan, VA, thanh quản)
- **Ý nghĩa:** Vấn đề liên quan đến vùng họng, amiđan, VA và dây thanh quản: đau họng, rát họng, sưng amidan, mủ amidan, viêm họng hạt, khàn tiếng, mất tiếng, nuốt nghẹn, nuốt đau.
- **Trường hợp chọn:**
  - Than phiền và câu hỏi tập trung ở vòm họng, cổ họng, amidan, VA hoặc giọng nói (khàn/mất tiếng).
  - Ví dụ: *"Cổ họng nổi hạt đỏ và nuốt nước bọt đau rát"*, *"Trẻ bị viêm amidan hốc mủ sốt cao có nên cắt không?"*, *"Bị khàn tiếng 3 ngày sau khi nói nhiều"*.
- **Trường hợp không nên chọn:**
  - Đau họng chỉ là cảm giác thoáng qua được liệt kê trong một câu hỏi hỏi chuyên sâu về bệnh lý tai hay sốt kéo dài.

### 3.5. `trieu_chung_tai` (Tai và thính lực)
- **Ý nghĩa:** Triệu chứng và bệnh lý khu trú tại tai: đau nhức tai, ù tai, chảy mủ/chảy dịch tai, ngứa tai, viêm tai giữa, viêm tai ngoài, tắc vòi nhĩ, nghe kém, giảm/mất thính lực.
- **Trường hợp chọn:**
  - Mọi câu hỏi có trọng tâm là tai và chức năng nghe.
  - Ví dụ: *"Tai trái cứ kêu ve ve cả ngày là bệnh gì?"*, *"Bé ngoáy tai xong bị chảy dịch vàng có mùi hôi"*, *"Viêm tai giữa uống kháng sinh gì?"*.
- **Trường hợp không nên chọn:**
  - Ù tai đi kèm chóng mặt quay cuồng nghi ngờ rối loạn tiền đình toàn thân nặng mà không có bất kỳ triệu chứng tai nào khác (cần cân nhắc đánh giá ngữ cảnh hoặc đánh dấu `needs_discussion`).

### 3.6. `cam_lanh` (Cảm lạnh, cảm mạo)
- **Ý nghĩa:** Câu hỏi mà người hỏi trực tiếp đề cập hoặc hỏi về *"cảm lạnh"*, *"cảm mạo"*, hoặc trạng thái cảm nhiễm thời tiết được người hỏi định danh rõ là cảm lạnh.
- **Trường hợp chọn:**
  - Câu hỏi dùng rõ từ *"cảm lạnh"*, *"bị cảm gió"*, *"cảm mạo"*.
  - Ví dụ: *"Đi mưa về bị cảm lạnh thì nên làm gì cho nhanh khỏi?"*, *"Phân biệt cảm lạnh và viêm mũi dị ứng thế nào?"*.
- **Trường hợp không nên chọn:**
  - **Không suy đoán từ thời tiết:** Nếu câu hỏi viết *"Đi mưa về bị sốt cao 39 độ uống thuốc gì"* mà không nhắc chữ cảm lạnh -> Trọng tâm là `sot`, KHÔNG suy thành `cam_lanh`.
  - **Không tự suy từ tổ hợp triệu chứng:** Câu hỏi chỉ liệt kê hắt hơi, sổ mũi, ho mà người hỏi không gọi đó là cảm lạnh -> Gán theo triệu chứng chính hoặc thảo luận, không tự áp đặt nhãn bệnh.
  - Người hỏi nói *"cảm cúm"* hoặc *"bị cúm"* -> chọn `cam_cum`.

### 3.7. `cam_cum` (Cúm, cảm cúm)
- **Ý nghĩa:** Câu hỏi trực tiếp đề cập đến cúm (cúm A, cúm B, cúm mùa, cảm cúm, vaccine phòng cúm).
- **Trường hợp chọn:**
  - Câu hỏi có chứa từ *"cúm"*, *"cảm cúm"*, *"cúm A"*, *"vaccine cúm"*.
  - Ví dụ: *"Trẻ bị cúm A bao lâu thì khỏi?"*, *"Uống thuốc gì khi bị cảm cúm đau nhức người?"*, *"Phụ nữ mang thai tiêm phòng cúm có an toàn không?"*.
- **Trường hợp không nên chọn:**
  - Câu chỉ nhắc sốt và ho mà người hỏi không hề dùng từ cúm/cảm cúm -> Không tự ý chẩn đoán cúm.

### 3.8. `sot` (Sốt)
- **Ý nghĩa:** Câu hỏi xoay quanh triệu chứng sốt (sốt cao, sốt phát ban, sốt co giật, hạ sốt, liều dùng thuốc hạ sốt paracetamol).
- **Trường hợp chọn:**
  - Trọng tâm câu hỏi là việc sốt, cách hạ sốt, liều dùng thuốc hạ nhiệt, theo dõi nhiệt độ cơ thể.
  - Ví dụ: *"Trẻ 1 tuổi sốt 39 độ uống paracetamol liều bao nhiêu?"*, *"Làm sao hạ sốt nhanh tại nhà khi chưa kịp đi viện?"*.
- **Trường hợp không nên chọn:**
  - Sốt chỉ là triệu chứng phụ đi kèm một bệnh cảnh cơ quan rõ ràng (ví dụ: *"Bé đau tai dữ dội kèm sốt 38.5 độ"* -> trọng tâm là `trieu_chung_tai`).
  - Sốt trong bệnh cảnh ngoài chuyên khoa TMH (ví dụ: sốt xuất huyết, sốt rét) -> xem xét đánh dấu `excluded`.

---

## 4. Hướng dẫn xử lý các tình huống phức tạp

### 4.1. Câu hỏi có nhiều triệu chứng (Multiple Symptoms)
Người bệnh rất thường hỏi phối hợp: *"Tôi bị ho, nghẹt mũi và sốt nhẹ..."*. Quy tắc chọn 1 chủ đề chính:
1. **Quy tắc trọng tâm than phiền (Chief Complaint):** Xác định triệu chứng nào làm người hỏi lo lắng nhất, mô tả chi tiết nhất hoặc trực tiếp đặt câu hỏi cần xử lý.
2. **Quy tắc cơ quan đặc thù (Specificity):** Cơ quan khu trú hẹp và rõ ràng thường được ưu tiên hơn triệu chứng toàn thân mơ hồ khi người hỏi than phiền đồng đều.
   - Thường ưu tiên: Bộ phận khu trú (`trieu_chung_tai`, `hong_amidan`, `xoang`) > Đường thở trên chung (`trieu_chung_mui`, `ho_dom`) > Toàn thân (`sot`).
3. **Khi các triệu chứng hoàn toàn ngang hàng:** Nếu người hỏi liệt kê đồng đều không triệu chứng nào trội hơn và không thể xác định trọng tâm một cách khách quan -> **Đánh dấu `needs_discussion`**, ghi rõ các nhãn ứng viên vào `review_note`, tuyệt đối không tự ý ép một nhãn chủ quan.

### 4.2. Xử lý câu phủ định, tiền sử và giả định
- **Phủ định:** Người hỏi nói *"Tôi ho nhiều nhưng không sốt"* -> Chủ đề là `ho_dom`, tuyệt đối không gán `sot`.
- **Tiền sử:** *"Trước đây em bị xoang đã khỏi, dạo này hay bị ù tai"* -> Chủ đề chính của lượt hỏi hiện tại là `trieu_chung_tai`.
- **Giả định / Tư vấn chung:** *"Nếu trẻ bị sốt cao co giật thì sơ cứu thế nào?"* -> Chủ đề vẫn là `sot` (phân loại theo nội dung thông tin được hỏi).
- **Hỏi cho người khác:** *"Bà nội tôi bị nghẹt mũi kinh niên..."* -> Vẫn gán `trieu_chung_mui` bình thường.

### 4.3. Thống nhất quy ước trạng thái duyệt (`review_status`)
Trong file làm việc, cột `review_status` ban đầu là `pending_manual_review`. Người duyệt cập nhật chính xác theo quy ước sau:

1. **`reviewed`:**
   - Dùng khi đã xác định rõ ràng chủ đề chính của câu hỏi.
   - **`gold_topic_label`:** BẮT BUỘC chứa đúng một mã nhãn hợp lệ trong 8 nhãn (`ho_dom`, `trieu_chung_mui`, `xoang`, `hong_amidan`, `trieu_chung_tai`, `cam_lanh`, `cam_cum`, `sot`).
   - `review_note`: Có thể để trống hoặc ghi chú thêm nếu cần.
2. **`needs_discussion`:**
   - Dùng khi câu hỏi mập mờ, nhiều triệu chứng ngang hàng không rõ trọng tâm, có sự mâu thuẫn, hoặc người duyệt chưa chắc chắn.
   - **`gold_topic_label`:** BẮT BUỘC ĐỂ TRỐNG (`""`).
   - **`review_note`:** BẮT BUỘC ghi rõ nội dung băn khoăn hoặc các nhãn đang phân vân.
   - **Cấm:** Không điền mã nhãn tự chế (như "chua_ro", "mixed") vào `gold_topic_label`.
3. **`excluded`:**
   - Dùng khi câu hỏi cần loại khỏi tập dữ liệu huấn luyện phân loại chủ đề tai mũi họng (câu vô nghĩa, chuỗi ký tự rác, câu hỏi hoàn toàn thuộc chuyên khoa khác như sản khoa, xương khớp, thần kinh, cấu trúc giải phẫu ngoài phạm vi như xoang hang sọ não).
   - **`gold_topic_label`:** BẮT BUỘC ĐỂ TRỐNG (`""`).
   - **`review_note`:** BẮT BUỘC ghi rõ lý do loại.
   - **Cấm:** Không thêm mã nhãn ngoài danh mục (như "ngoai_pham_vi") vào `gold_topic_label` khi chưa có quyết định điều chỉnh cấu hình toàn dự án.

---

## 5. Nhận xét và đề xuất về bộ 8 nhãn khởi đầu

Trong quá trình chuẩn bị dữ liệu và rà soát từ khóa, một số hạn chế của bộ 8 nhãn khởi đầu đã được nhận diện. Người gán nhãn cần nắm rõ nhưng **không tự ý sửa file cấu hình `labels.json` hay mã nguồn**, mà sẽ dùng các ghi chú này để tổng kết sau giai đoạn pilot:

1. **Ranh giới nhãn `sot`:** Sốt là triệu chứng toàn thân gặp trong hàng trăm bệnh khác nhau (sốt virus, sốt xuất huyết, nhiễm khuẩn tiết niệu...). Có nhiều câu hỏi trong tập dữ liệu chỉ hỏi về sốt ở trẻ em mà không hề có triệu chứng tai mũi họng. Trong pilot, nếu câu hỏi chỉ tập trung vào việc sốt/hạ sốt, tạm gán `sot`. Sau pilot sẽ xem xét có nên giữ nhãn này trong bài toán chuyên khoa Tai Mũi Họng hay chuyển thành lớp ngoài phạm vi / triệu chứng toàn thân.
2. **Chồng chéo `cam_lanh` vs `cam_cum`:** Trong đời sống và ngôn ngữ bệnh nhân, hai khái niệm này thường bị đánh đồng. Tuy nhiên về mặt nội dung văn bản: bám sát từ ngữ người hỏi dùng (`cảm lạnh` -> `cam_lanh`, `cúm`/`cảm cúm` -> `cam_cum`).
3. **Phạm vi nhãn `hong_amidan` quá rộng:** Đang gom cả vòm họng, amidan, VA và thanh quản (khàn tiếng, mất tiếng). Triệu chứng thanh quản ảnh hưởng đến giọng nói có tính chất khá riêng biệt.
4. **Thiếu nhóm triệu chứng Tai Mũi Họng khác:** Bộ nhãn hiện chưa có nhãn cho triệu chứng chóng mặt/mất thăng bằng (liên quan tiền đình ốc tai), dị vật đường thở/dị vật tai mũi họng, chấn thương tai mũi họng.
5. **Chưa có nhãn chính thức cho `ngoai_pham_vi`:** Hiện tại các câu ngoài phạm vi sẽ đánh dấu `review_status = "excluded"` và `gold_topic_label = ""` cùng ghi chú trong `review_note`. Sau pilot có thể xem xét đề xuất thêm nhãn `ngoai_pham_vi` thành một lớp chính thức nếu muốn mô hình học cách từ chối trả lời.

---

## 6. Hướng dẫn quy trình gán nhãn thực tế qua Excel

Quy trình gán nhãn sử dụng file CSV làm bản làm việc trên Microsoft Excel, bảo toàn tuyệt đối 100% bộ pilot gốc và hỗ trợ xuất phiên bản có kiểm soát.

### Quy trình 7 bước chuẩn:

1. **Bước 1 — Tạo bản làm việc an toàn (không ghi đè bản cũ):**
   Chạy lệnh kiểm tra và tạo bản làm việc trong thư mục riêng; nếu file làm việc đã tồn tại, lệnh sẽ thông báo mở tiếp bản hiện có để bảo vệ dữ liệu đã gán nhãn:
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
   Mở `02_du_lieu/filedata/reviewed/working/questions_working.csv` bằng Microsoft Excel hoặc LibreOffice Calc (chọn UTF-8). Duyệt từng dòng:
   - Đọc nội dung tại cột `question`. Tham khảo `suggested_topic_label` và `keywords` (không sao chép máy móc).
   - **Chỉ chỉnh sửa 5 cột sau:**
     + `gold_topic_label`: Điền 1 trong 8 nhãn hợp lệ (`ho_dom`, `trieu_chung_mui`, `xoang`, `hong_amidan`, `trieu_chung_tai`, `cam_lanh`, `cam_cum`, `sot`) nếu status là `reviewed`; bắt buộc để trống nếu status là `needs_discussion` hoặc `excluded`.
     + `review_status`: Cập nhật thành `reviewed`, `needs_discussion`, hoặc `excluded` (nếu chưa xong câu nào thì giữ `pending_manual_review`).
     + `reviewer_id`: Điền định danh người duyệt (ví dụ: `reviewer_1`).
     + `reviewed_at`: Điền ngày duyệt theo đúng định dạng `YYYY-MM-DD` với lịch thực tế (ví dụ: `2026-11-28`).
     + `review_note`: Bắt buộc ghi rõ lý do nếu chọn `needs_discussion` hoặc `excluded`.
   - **Tuyệt đối không sửa** các cột dữ liệu nguồn (`id`, `dataset`, `question`, `group_id`, `provenance_ids`, `topic_candidates`, `suggested_topic_label`, `keywords`).
3. **Bước 3 — Lưu file CSV:**
   Lưu file trên Excel ở định dạng CSV UTF-8 (Comma delimited).
4. **Bước 4 — Chạy kiểm tra tính hợp lệ (`--check-only`):**
   Từ thư mục gốc dự án, chạy lệnh kiểm tra tự động mà không xuất file:
   ```powershell
   python -X utf8 01_ma_nguon/xu_ly_du_lieu/export_reviewed_pilot.py --input-csv 02_du_lieu/filedata/reviewed/working/questions_working.csv --check-only
   ```
5. **Bước 5 — Sửa lỗi nếu có:**
   Nếu lệnh báo lỗi (ví dụ sai mã nhãn, thiếu ngày, sai định dạng YYYY-MM-DD, thiếu ghi chú khi excluded), mở lại file Excel, sửa theo đúng thông báo và lưu lại.
6. **Bước 6 — Xuất phiên bản dữ liệu đã kiểm tra:**
   Khi lệnh check-only báo thành công, xuất bộ dữ liệu hoàn chỉnh (CSV, JSONL và Manifest) sang thư mục phiên bản mới (phải là thư mục chưa tồn tại):
   ```powershell
   python -X utf8 01_ma_nguon/xu_ly_du_lieu/export_reviewed_pilot.py --input-csv 02_du_lieu/filedata/reviewed/working/questions_working.csv --output-dir 02_du_lieu/filedata/reviewed/annotations/v1
   ```
7. **Bước 7 — Theo dõi tiến độ và báo cáo:**
   Xem bảng tổng kết hiển thị trên màn hình:
   - Số lượng câu theo từng trạng thái: `reviewed`, `needs_discussion`, `excluded`, `pending_manual_review`.
   - Số câu reviewed có nhãn hợp lệ (`usable_for_training_count`).
   - Trạng thái hoàn thành danh sách (`annotation_complete: True` khi pending=0 và discussion=0).
   - Lưu ý: Khả năng sẵn sàng huấn luyện 5 mô hình chưa được đánh giá ở giai đoạn pilot (`train_readiness_status: not_evaluated_in_pilot_phase`), chỉ được chốt sau quy trình chuẩn bị tập train chính thức.

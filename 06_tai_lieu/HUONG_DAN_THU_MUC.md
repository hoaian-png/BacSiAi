# Cấu trúc BacSiAi theo nội dung đồ án

Cập nhật **27/11/2026**. Cấu trúc gồm 7 nhóm phù hợp bài hỏi đáp tai mũi họng, không sao chép cứng 9 nhóm trong ảnh mẫu. Các file hiện có đã được chuyển; thư mục mô hình/thử nghiệm mới là chỗ chuẩn bị, chưa có huấn luyện hoặc web.

## Cây thư mục

```text
DoanCS2_BacSiAi_ban2/
├── README.md                           Điểm bắt đầu đọc dự án
├── AGENTS.md                           Hướng dẫn làm việc toàn dự án
├── ThuTuLamViec.md                     Bản phác thứ tự làm việc do người dùng đặt ở gốc
├── .gitignore / .gitattributes          Cấu hình Git
├── 01_ma_nguon/
│   ├── giaodien/                       Giữ chỗ cho app.py Streamlit
│   ├── backend/                        Giữ chỗ cho backend.py
│   ├── train/                          Giữ chỗ cho mã train 5 mô hình
│   ├── xu_ly_du_lieu/
│   │   ├── prepare_data.py             Tải và chuẩn hóa ba nguồn
│   │   ├── validate_data.py            Kiểm tra các file đã xuất
│   │   └── requirements-data.txt       Phụ thuộc xử lý dữ liệu
│   └── .data-tools/                    Thư viện hỗ trợ local, bỏ qua khi dùng Git
├── 02_du_lieu/
│   └── filedata/
│       ├── raw/                        ViMQ, ViHealthQA, ViMedAQA nguyên bản
│       ├── normalized/                 63.328 bản ghi CSV/JSONL
│       ├── prepared/                   3.130 câu hỏi, 1.814 mục kiến thức ứng viên
│       ├── config/                     labels.json và keywords.csv
│       └── sources.json                Nguồn, phiên bản, SHA-256
├── 03_mo_hinh/
│   ├── MoHinh.md                       Danh sách năm mô hình
│   └── README.md                       Hướng dẫn, hiện chưa có mô hình đã train
├── 04_thu_nghiem/
│   ├── README.md
│   ├── cau_hinh/                       Chỗ lưu tham số thí nghiệm
│   └── phan_chia_du_lieu/               Chỗ lưu split manifest sau khi duyệt nhãn
├── 05_bao_cao/
│   ├── kiem_tra_du_lieu/                Đã có summary, validation và thống kê
│   ├── BaoCaoSoSanh/                   Giữ chỗ cho so sánh năm mô hình
│   └── ket_qua_cuoi/                   Hướng dẫn nơi xuất bản bàn giao cuối
├── 06_tai_lieu/
│   ├── PROJECT.md                      Kiến trúc và phạm vi
│   ├── ROADMAP.md                      Thứ tự làm và trạng thái
│   ├── HUONG_DAN_THU_MUC.md             Tài liệu này
│   ├── QUY_UOC_LUU_TRU.md               Quy ước dữ liệu và artifact
│   ├── DU_LIEU.md                      Hướng dẫn ba bộ dữ liệu
│   ├── TU_DIEN_DU_LIEU.md              Giải thích cột
│   └── ban_nhap/                       Dành cho bản nháp nếu cần
└── 07_nhat_ky/
    ├── README.md
    ├── NHAT_KY_CONG_VIEC.md            Công việc, quyết định và lịch sử thay đổi
    ├── sap_xep_thu_muc.json            Ánh xạ cũ/mới và đối chiếu checksum
    └── chuong_trinh/                   Dành cho log ứng dụng/huấn luyện sau này
```

`.git/` giữ nguyên ở gốc. README và AGENTS là điểm vào làm việc; các tài liệu chuyên đề nằm trong `06_tai_lieu`.

## Vì sao chia như vậy?

| Nhóm | Vai trò trong bài |
|---|---|
| 01_ma_nguon | Mã chạy Streamlit, backend, train và chuẩn hóa |
| 02_du_lieu | Ba bộ dữ liệu, nhãn, từ khóa, kiến thức và SQLite sau này |
| 03_mo_hinh | Pipeline NB/LR/SVM/RF, PhoBERT, tokenizer và chỉ mục truy xuất |
| 04_thu_nghiem | Tham số và cách chia tập dùng chung để so sánh công bằng |
| 05_bao_cao | Kiểm tra dữ liệu, đánh giá mô hình và bản kết quả để nộp |
| 06_tai_lieu | Hướng dẫn, kiến trúc, lộ trình và bản nháp |
| 07_nhat_ky | Nhật ký công việc; thư mục con chuong_trinh cho log kỹ thuật |

Không cần thêm tầng kết quả ở gốc vì đã nằm trong báo cáo. Không cần tách hai tầng nhật ký vì có thể phân loại bằng thư mục con.

## Đường dẫn dự kiến khi làm tiếp

Các file dưới đây **chưa được triển khai**:

- Giao diện: `01_ma_nguon/giaodien/app.py`.
- Backend: `01_ma_nguon/backend/backend.py`.
- Train: `01_ma_nguon/train/`, gồm prepare, features, traditional, phobert, evaluate và điểm chạy train.
- Phụ thuộc ứng dụng: `01_ma_nguon/requirements.txt`, `01_ma_nguon/requirements-phobert.txt`.
- Bản duyệt thủ công: `02_du_lieu/filedata/reviewed/`.
- SQLite: `02_du_lieu/database/medical.db`.
- Artifact: `03_mo_hinh/<run_id>/`, mô hình đang dùng do `03_mo_hinh/active_model.json` xác định.
- Cấu hình thí nghiệm: `04_thu_nghiem/cau_hinh/<run_id>.json`.
- Split manifest: `04_thu_nghiem/phan_chia_du_lieu/<run_id>/split_manifest.csv`.
- Báo cáo mô hình: `05_bao_cao/BaoCaoSoSanh/<run_id>/`.
- Log: `07_nhat_ky/chuong_trinh/<run_id>/training.log`.

## Các file đã di chuyển

- `backend`, `giaodien`, `train` cũ → bên trong `01_ma_nguon`.
- `filedata` cũ → `02_du_lieu/filedata`, giữ nguyên raw/normalized/prepared/config và nguồn.
- Hai script Python và requirements dữ liệu → `01_ma_nguon/xu_ly_du_lieu`.
- `filedata/reports` cũ → `05_bao_cao/kiem_tra_du_lieu`.
- `BaoCaoSoSanh` cũ → `05_bao_cao/BaoCaoSoSanh`.
- PROJECT, ROADMAP, QUY_UOC_LUU_TRU và hướng dẫn thư mục → `06_tai_lieu`.
- README dữ liệu → `06_tai_lieu/DU_LIEU.md`; DATA_DICTIONARY → `06_tai_lieu/TU_DIEN_DU_LIEU.md`.
- Hai bản nháp đã được người dùng sắp lại và đổi đuôi: `03_mo_hinh/MoHinh.md` và `ThuTuLamViec.md` ở gốc. Đổi đuôi giữ nguyên nội dung, không biến bản phác cấu trúc cũ thành trạng thái triển khai hiện tại.

Chi tiết từng file và checksum nằm trong `07_nhat_ky/sap_xep_thu_muc.json` tính từ gốc dự án.

## Kiểm tra dữ liệu

Từ gốc dự án:

```powershell
python -X utf8 01_ma_nguon/xu_ly_du_lieu/validate_data.py
```

Script tự tìm thư mục gốc theo vị trí file. Các giá trị `path` trong sources.json và `raw_location` vẫn tính từ `02_du_lieu/filedata`; không cần sửa hoặc sinh lại dữ liệu chỉ vì đổi thư mục.

## Tài liệu liên quan

[README](../README.md) · [Kiến trúc](PROJECT.md) · [Lộ trình](ROADMAP.md) · [Quy ước](QUY_UOC_LUU_TRU.md) · [Dữ liệu](DU_LIEU.md) · [Từ điển cột](TU_DIEN_DU_LIEU.md).

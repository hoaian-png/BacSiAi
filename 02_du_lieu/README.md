# Dữ liệu

`filedata/` giữ nguyên raw, normalized, prepared, config và sources.json của ba bộ ViMQ, ViHealthQA, ViMedAQA. Nhãn chủ đề và kiến thức hiện vẫn cần duyệt.

Hướng dẫn: [DU_LIEU.md](../06_tai_lieu/DU_LIEU.md). Giải thích cột: [TU_DIEN_DU_LIEU.md](../06_tai_lieu/TU_DIEN_DU_LIEU.md).

Sau này đặt bản duyệt thủ công tại `filedata/reviewed/` và SQLite tại `database/medical.db`; hiện chưa tạo các file đó.

Đường dẫn `path` trong sources.json và `raw_location` trong bản ghi tính từ `filedata/`, không phải gốc repository. Báo cáo kiểm tra nằm trong `05_bao_cao/kiem_tra_du_lieu` tính từ gốc dự án.

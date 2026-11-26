DoanCS2_BacSiAi_ban2/
│
├── giaodien/
│   └── app.py                     Giao diện Streamlit
│
├── backend/
│   └── backend.py                 Xử lý hỏi đáp, truy xuất, gọi LLM và SQLite
│
├── train/
│   ├── train.py                   Điểm chạy huấn luyện các mô hình
│   ├── config.json                Tham số huấn luyện
│   ├── prepare.py                 Đọc nhãn đã duyệt, kiểm tra và chia tập
│   ├── features.py                TF-IDF và đặc trưng từ khóa
│   ├── traditional.py             Train NB, Logistic Regression, SVM, RF
│   ├── phobert.py                 Fine-tune PhoBERT
│   └── evaluate.py                Đánh giá và xuất báo cáo
│
├── filedata/                      Giữ dữ liệu đã chuẩn bị
│   ├── raw/
│   ├── normalized/
│   ├── prepared/
│   ├── config/
│   └── reports/
│
├── database/
│   └── medical.db                 SQLite
│
├── models/                        Kết quả sau huấn luyện
│   ├── naive_bayes.joblib
│   ├── logistic_regression.joblib
│   ├── linear_svm.joblib
│   ├── random_forest.joblib
│   ├── phobert/                   Trọng số, tokenizer và cấu hình
│   ├── retrieval.joblib           Chỉ mục tìm kiếm tài liệu
│   └── active_model.json          Mô hình được chọn để chạy web
│
├── reports/
│   └── <ma_lan_train>/
│       ├── config.json            Cấu hình thực tế của lần train
│       ├── split_manifest.csv     ID câu hỏi và tập tương ứng
│       ├── metrics.csv            So sánh các mô hình
│       ├── classification_report.json
│       ├── confusion_matrix.png
│       └── training.log
│
├── requirements.txt              Thư viện chạy web và ML truyền thống
├── requirements-phobert.txt       Thư viện bổ sung cho PhoBERT
├── README.md                      Hướng dẫn sử dụng
└── mô hình.txt                    Danh sách mô hình đã chọn

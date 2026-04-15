[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23574118&assignment_repo_type=AssignmentRepo)
# Day 10 Lab: Data Pipeline & Data Observability

**Student ID:** 2A202600120
**Student Email:** dat.le@blueboltsoftware.com
**Name:** Luu Luong Vi Nhan

---

## Mô tả

Bài lab này xây dựng một **ETL pipeline tự động** đơn giản bằng Python +
pandas để xử lý dữ liệu sản phẩm từ file JSON, áp dụng validation để loại bỏ
record xấu, transform dữ liệu (tính giá giảm 10%, chuẩn hóa category về
Title Case, thêm cột `processed_at`), rồi lưu kết quả ra CSV. Sau đó, sử
dụng `agent_simulation.py` để so sánh cách một Agent phản ứng với **dữ liệu
sạch** (output của pipeline) và **dữ liệu rác** (file có duplicate IDs, sai
kiểu dữ liệu, outlier và null values), nhằm chứng minh tầm quan trọng của
data quality và observability trong pipeline phục vụ AI Agent.

---

## Cách chạy (How to Run)

### Prerequisites
```bash
python3 -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\activate
pip install pandas pytest
```

### Chạy ETL Pipeline
```bash
python solution.py
```
Sau khi chạy, file `processed_data.csv` sẽ được tạo ra với các cột:
`id, product, price, category, discounted_price, processed_at`.

### Chạy Agent Simulation (Stress Test)
```bash
# 1. Tạo file dữ liệu rác
python generate_garbage.py

# 2. So sánh Agent trên clean vs garbage data
python agent_simulation.py
```

### Chạy bộ test chấm điểm
```bash
pytest tests/ -v
```

---

## Cấu trúc thư mục

```
├── solution.py              # ETL Pipeline script (Extract/Validate/Transform/Load)
├── raw_data.json            # Dữ liệu nguồn
├── processed_data.csv       # Output của pipeline (clean data)
├── generate_garbage.py      # Tạo garbage_data.csv để stress test
├── agent_simulation.py      # Agent RAG đơn giản
├── experiment_report.md     # Báo cáo so sánh Clean vs Garbage
├── tests/                   # Bộ test auto-grader
└── README.md                # File này
```

---

## Kết quả

- **Input:** 5 records từ `raw_data.json`.
- **Validation:** 2 records bị loại (1 record price <= 0, 1 record empty category).
- **Output:** 3 records hợp lệ được lưu ra `processed_data.csv` với cột
  `discounted_price` và `processed_at`.
- **Stress Test:** Agent trả lời chính xác trên clean data (Laptop $1200)
  nhưng trả về outlier vô nghĩa trên garbage data (Nuclear Reactor $999999)
  — khẳng định "**Quality Data > Quality Prompt**". Chi tiết trong
  `experiment_report.md`.

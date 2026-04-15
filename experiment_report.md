# Experiment Report: Data Quality Impact on AI Agent

**Student ID:** 2A202600120
**Name:** Luu Luong Vi Nhan
**Date:** 15/04/2026

---

## 1. Kết quả thí nghiệm

Chạy `agent_simulation.py` với 2 bộ dữ liệu và ghi lại kết quả:

| Scenario | Agent Response | Accuracy (1-10) | Notes |
|----------|----------------|-----------------|-------|
| Clean Data (`processed_data.csv`) | Agent: Based on my data, the best choice is Laptop at $1200. | 9 | Agent chọn đúng sản phẩm electronics hợp lý nhất sau khi pipeline đã loại bỏ các record lỗi (price <= 0, category rỗng). Kết quả đáng tin cậy, phù hợp với kỳ vọng của người dùng. |
| Garbage Data (`garbage_data.csv`) | Agent: Based on my data, the best choice is Nuclear Reactor at $999999. | 2 | Agent trả về outlier cực đoan ($999,999) vì không có lớp validation. Câu trả lời vô nghĩa với người dùng cuối và có thể gây thiệt hại nếu được dùng để ra quyết định kinh doanh. |

---

## 2. Phân tích & nhận xét (Phan tich & nhan xet)

### Tại sao Agent trả lời sai khi dùng Garbage Data? (Tai sao)

Khi dùng file `garbage_data.csv`, Agent chọn "Nuclear Reactor" giá $999,999 làm sản phẩm electronics tốt nhất — một câu trả lời hoàn toàn vô nghĩa với người dùng thực tế. Nguyên nhân gốc rễ không nằm ở prompt hay logic của Agent, mà nằm ở chất lượng dữ liệu đầu vào. Bộ dữ liệu rác chứa nhiều lỗi data quality phổ biến: **Duplicate IDs** (hai record cùng id=1 khiến Agent không thể tin
tưởng vào khóa chính), **Wrong data types** (giá trị "ten dollars" trong cột `price` làm cả cột bị ép về kiểu object/string nên các phép so sánh numeric trở nên không đáng tin), **Extreme outliers** (giá $999,999 của "Nuclear Reactor" làm lệch hàm `idxmax`, khiến Agent luôn chọn item cực đoan thay vì sản phẩm thực tế tốt nhất), và **Null values** (giá trị None trong `id` và `category` có thể gây crash ở các bước lọc tiếp theo). Pipeline sạch của chúng ta (`solution.py`) đã chặn đứng những lỗi này bằng bước validate và transform, trong khi file rác đi thẳng vào Agent nên lỗi được "khuếch đại" ra đến người dùng. Đây chính là lý do vì sao observability và validation ở tầng dữ liệu là bắt buộc trước khi cấp dữ liệu vào bất kỳ LLM hay AI Agent nào.

---

## 3. Kết luận

**Quality Data > Quality Prompt?** Đồng ý.

Thí nghiệm này cho thấy dù prompt có tốt đến đâu ("What is the best electronic
product?" là một câu hỏi rất rõ ràng) thì kết quả cuối cùng vẫn phụ thuộc hoàn
toàn vào chất lượng dữ liệu mà Agent truy vấn. Một Agent thông minh với dữ
liệu rác vẫn trả lời sai; một Agent đơn giản với dữ liệu sạch vẫn trả lời
đúng. Vì vậy, đầu tư vào **data pipeline, validation và observability** mang
lại ROI cao hơn nhiều so với việc chỉ tinh chỉnh prompt — "garbage in, garbage
out" vẫn đúng trong kỷ nguyên AI Agent.

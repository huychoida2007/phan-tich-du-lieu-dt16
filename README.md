# Đồ án Phân tích Dữ liệu Điện ảnh (IMDb/TMDB)
> **Bài tập lớn môn Lập trình Python cho Phân tích Dữ liệu - Mã đề tài: DT16**

## 👥 Thông tin nhóm (Team Members)
| STT | Họ và Tên | Mã Sinh Viên | Vai trò / Nhiệm vụ | Link GitHub Cá Nhân |
|---|---|---|---|---|
| 1 | Lê Quốc Huy (Nhóm trưởng) | 3120225066 | Xây dựng lớp `MovieDataLoader` (đọc file CSV/JSON), lớp `DataCleaner` (làm sạch dữ liệu) và viết Chương 1, 2 Báo cáo Word. | [GitHub](https://github.com/huychoida2007) |
| 2 | Hoàng Đình Quảng | 3120225125 | Xây dựng lớp `MovieAnalyzer` (vẽ 3 biểu đồ đầu tiên), viết nhận xét dữ liệu và thiết kế Slide thuyết trình. Xây dựng giao diện Dashboard (`app.py`) dựa trên logic xử lý dữ liệu và biểu đồ có sẵn | [GitHub](https://github.com/WelizK) |
| 3 | Nguyễn Huỳnh Tấn Khoa | 3120225071 | Xây dựng lớp `MovieAnalyzer` (vẽ 2 biểu đồ cuối), làm phần Nâng cao (mô hình Học máy `MovieRevenuePredictor`) và viết Chương 3 Báo cáo Word. | [GitHub](https://github.com/Krigin07) |
| 4 | Võ Hoàng Phúc | 3120225121 | Tối ưu hóa code OOP, bắt lỗi Exception, viết file `README.md` và hoàn thiện Chương 4, 5 Báo cáo Word. | [GitHub](https://github.com/ShanYuLR) |

## 📝 Giới thiệu dự án (Description)

📦 **Dự án phân tích bộ dữ liệu điện ảnh từ TMDB** nhằm khám phá các yếu tố then chốt quyết định sự thành công của một dự án phim (ngân sách, doanh thu, thời lượng , điểm đánh giá). Toàn bộ quy trình — từ làm sạch dữ liệu, trực quan hóa đến dự đoán doanh thu — đều được thực hiện bằng Python trên Jupyter Notebook và đóng gói thành Dashboard tương tác bằng Streamlit.

---

## ✨ Các chức năng đáp ứng yêu cầu đề bài (Features)

- [x] Đọc và thu thập dữ liệu từ 02 định dạng khác nhau (`.csv` và `.json`).
- [x] Áp dụng Lập trình hướng đối tượng (OOP) để xây dựng các lớp xử lý chuyên biệt (`MovieDataLoader`, `DataCleaner`, `MovieAnalyzer`, `MovieRevenuePredictor`).
- [x] Tiền xử lý và làm sạch dữ liệu: xử lý ngoại lệ (try/except), loại bỏ dữ liệu thiếu/rác, bóc tách chuỗi JSON lồng ghép phức tạp.
- [x] Trực quan hóa dữ liệu bằng 05 loại biểu đồ khác nhau (Heatmap, Scatter, Bar, Line, Histogram) kèm diễn giải ý nghĩa chi tiết.
- [x] **Nâng cao:** Huấn luyện mô hình Học máy (Hồi quy tuyến tính - Linear Regression) để dự đoán doanh thu phòng vé.
- [x] **Bổ sung:** Xây dựng Dashboard tương tác bằng Streamlit (`app.py`) theo mô hình MVC, có menu điều hướng và cache dữ liệu.

---

## 💻 Công nghệ & Thư viện sử dụng (Technologies)

| Thành phần | Chi tiết |
|---|---|
| Ngôn ngữ | Python 3 |
| Môi trường lập trình | Jupyter Notebook / Visual Studio Code |
| Xử lý dữ liệu | `pandas`, `numpy`, `ast` |
| Trực quan hóa | `matplotlib`, `seaborn` |
| Học máy | `scikit-learn` |
| Dashboard | `streamlit` |

---

## 📂 Cấu trúc thư mục (Project Structure)

Mã nguồn được tổ chức gọn gàng để giảng viên có thể dễ dàng chạy file từ đầu đến cuối (Run All):

```bash
 📦 Nhom01_DT16/
 ┣ 📂data/                      # 📥 Thư mục chứa dữ liệu thô
 ┃ ┣ 📜tmdb_5000_movies.csv     #    - Dữ liệu bảng phim (Định dạng CSV)
 ┃ ┗ 📜tmdb_5000_credits.json   #    - Dữ liệu credits (Định dạng JSON)
 ┣ 📂core/                      # 🧱 Các lớp xử lý OOP (phục vụ Streamlit)
 ┃ ┣ 📜data_loader.py           #    - Class MovieDataLoader
 ┃ ┣ 📜data_cleaner.py          #    - Class DataCleaner
 ┃ ┣ 📜analyzer.py              #    - Class MovieAnalyzer
 ┃ ┗ 📜predictor.py             #    - Class MovieRevenuePredictor
 ┣ 📜main_notebook.ipynb        # 📓 File Jupyter Notebook chính chứa toàn bộ quy trình
 ┣ 📜app.py                     # 🖥️ Giao diện Dashboard tương tác bằng Streamlit
 ┣ 📜requirements.txt           # 📋 File khai báo các thư viện cần thiết
 ┗ 📜README.md                  # 📖 Tài liệu mô tả dự án và hướng dẫn chạy code
```

---

## 🚀 Hướng dẫn cài đặt và chạy (Installation)

### 1️⃣ Cài đặt môi trường
- Đảm bảo máy tính đã cài đặt **Python 3** và **Visual Studio Code** (hoặc Jupyter).

### 2️⃣ Cài đặt thư viện
Mở Terminal tại thư mục dự án và chạy lệnh sau để cài đặt các thư viện phụ thuộc:

```bash
pip install -r requirements.txt
```

### 3️⃣ Chạy Jupyter Notebook
- Mở file `main_notebook.ipynb` bằng VS Code hoặc Jupyter.
- Chọn Kernel Python phù hợp.
- Chọn lệnh **Restart & Run All** (hoặc bấm chạy tuần tự từng ô) để xem:
  - Dữ liệu được nạp và làm sạch
  - 5 biểu đồ phân tích
  - Kết quả của mô hình Học máy

---

## ➕ Bổ sung: Chạy Dashboard tương tác (Streamlit)

Ngoài file `main_notebook.ipynb`, dự án còn được đóng gói thêm thành một dashboard tương tác bằng Streamlit (file `app.py` + thư mục `core/`). Cách chạy:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Trình duyệt sẽ tự động mở tại `http://localhost:8501`, dùng menu ở thanh bên để chuyển giữa 3 mục:
- **Giới thiệu** — Tổng quan và thống kê dữ liệu
- **Phân tích & Biểu đồ** — 5 biểu đồ phân tích cốt lõi
- **Mô hình Dự đoán** — Kết quả mô hình Học máy

> **Lưu ý:** Nếu dùng PowerShell (VS Code trên Windows) và gặp lỗi khi nối lệnh bằng `&&`, hãy chạy 2 lệnh trên riêng từng dòng, hoặc thay `&&` bằng `;`.

---

## 🤖 Mô hình Học máy — Dự đoán Doanh thu (Nâng cao)

Dự án áp dụng mô hình **Hồi quy tuyến tính (Linear Regression)** từ `scikit-learn` để dự đoán doanh thu phim dựa trên các đặc trưng:
- `budget` (ngân sách)
- `popularity` (độ phổ biến)
- `vote_average` (điểm đánh giá)
- `vote_count` (số lượt đánh giá)
- `runtime` (thời lượng)

Dữ liệu được chia **80% huấn luyện / 20% kiểm thử**.

### Các chỉ số đánh giá mô hình
| Chỉ số | Ý nghĩa |
|---|---|
| **R²** (Hệ số xác định) | Tỷ lệ phần trăm sự biến động doanh thu mà mô hình giải thích được. |
| **RMSE** (Sai số căn phương trung bình) | Đo độ lệch tổng thể giữa dự đoán và thực tế (đơn vị USD). |
| **MAE** (Sai số tuyệt đối trung bình) | Sai số tuyệt đối trung bình — dễ diễn giải hơn RMSE. |

**Đánh giá:** Mô hình giải thích được phần lớn sự biến động doanh thu. Tuy nhiên, sai số RMSE vẫn còn cao do doanh thu phim chịu ảnh hưởng bởi nhiều yếu tố khó lượng hóa (kịch bản, marketing, thời điểm ra mắt...).

---

## 📋 Tóm tắt quy trình dự án

```text
📥 Nạp dữ liệu (CSV + JSON)
   ↓
🧹 Làm sạch & gộp dữ liệu (DataCleaner)
   ↓
📊 Phân tích & Trực quan hóa (5 biểu đồ)
   ↓
🤖 Dự đoán doanh thu (Linear Regression)
   ↓
🖥️ Dashboard tương tác (Streamlit)
```

---

## 📌 Ghi chú

- **Mã đề tài:** DT16
- **Nhóm thực hiện:** Nhóm 01
- **Môn học:** Lập trình Python cho Phân tích Dữ liệu
- **Năm học:** 2025 - 2026

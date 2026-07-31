# Đồ án Phân tích Dữ liệu Điện ảnh (IMDb/TMDB)
> **Bài tập lớn môn Lập trình Python cho Phân tích Dữ liệu - Mã đề tài: DT16**

## 👥 Thông tin nhóm (Team Members)
| STT | Họ và Tên | Mã Sinh Viên | Vai trò / Nhiệm vụ | Link GitHub Cá Nhân |
|---|---|---|---|
| 1 | Lê Quốc Huy (Nhóm trưởng) | 3120225066 | Xây dựng lớp `MovieDataLoader` (đọc file CSV/JSON), lớp `DataCleaner` (làm sạch dữ liệu) và viết Chương 1, 2 Báo cáo Word. | [GitHub](https://github.com/huychoida2007) |
| 2 | Hoàng Đình Quảng | 3120225125 | Xây dựng lớp `MovieAnalyzer` (vẽ 4 biểu đồ: Heatmap, Scatter, Bar, Line), viết nhận xét dữ liệu và thiết kế Slide thuyết trình. |
| 3 | Nguyễn Huỳnh Tấn Khoa | 3120225071 | Xây dựng lớp `MovieAnalyzer` (vẽ 3 biểu đồ: Histogram, Thống kê Diễn viên, Phân tích Thập kỷ), làm phần Nâng cao (mô hình Học máy `MovieRevenuePredictor`) và viết Chương 3 Báo cáo Word. |
| 4 | Võ Hoàng Phúc | 3120225121 | Tối ưu hóa code chuẩn OOP, bắt lỗi Exception, viết file `README.md` và hoàn thiện Chương 4, 5 Báo cáo Word. |

## 📝 Giới thiệu dự án (Description)
Dự án phân tích bộ dữ liệu điện ảnh từ TMDB để khám phá các yếu tố then chốt gắn liền với thành công của một dự án điện ảnh (ngân sách, doanh thu, thời lượng, điểm đánh giá). Toàn bộ quy trình từ làm sạch dữ liệu, trực quan hóa đến dự đoán doanh thu đều được thực hiện thông qua mã nguồn Python trên Jupyter Notebook một cách trực quan.

## ✨ Các chức năng đáp ứng yêu cầu đề bài (Features)
- [x] Đọc và thu thập dữ liệu từ 02 định dạng khác nhau (`.csv` và `.json`).
- [x] Áp dụng Lập trình hướng đối tượng (OOP) để xây dựng các lớp xử lý chuyên biệt (`MovieDataLoader`, `DataCleaner`, `MovieAnalyzer`, `MovieRevenuePredictor`).
- [x] Tiền xử lý và làm sạch dữ liệu: xử lý ngoại lệ (try/except), loại bỏ dữ liệu thiếu/rác, bóc tách chuỗi JSON lồng ghép phức tạp.
- [x] Trực quan hóa dữ liệu bằng 07 biểu đồ và phân tích khác nhau (Heatmap, Scatter, Bar, Line, Histogram, Top Cast, Decade Trend) kèm diễn giải ý nghĩa chi tiết.
- [x] **Nâng cao:** Huấn luyện mô hình Học máy (Hồi quy tuyến tính - Linear Regression) để dự đoán doanh thu phòng vé.

## 💻 Công nghệ & Thư viện sử dụng (Technologies)
* **Ngôn ngữ:** Python 3
* **Môi trường lập trình:** Jupyter Notebook / Visual Studio Code
* **Thư viện xử lý dữ liệu:** `pandas`, `numpy`, `ast`
* **Thư viện trực quan hóa:** `matplotlib`, `seaborn`
* **Thư viện Học máy:** `scikit-learn`

## 📂 Cấu trúc thư mục (Project Structure)

Mã nguồn được tổ chức gọn gàng để giảng viên có thể dễ dàng chạy file từ đầu đến cuối (Run All):

```bash
Nhom01_DT16/
 ┣ 📂data/                      # Thư mục chứa dữ liệu thô
 ┃ ┣ 📜tmdb_5000_movies.csv     # Dữ liệu bảng phim (Định dạng CSV)
 ┃ ┗ 📜tmdb_5000_credits.json   # Dữ liệu credits (Định dạng JSON)
 ┣ 📜main_notebook.ipynb        # File code Jupyter Notebook chính chứa toàn bộ quy trình
 ┣ 📜requirements.txt           # File khai báo các thư viện cần thiết
 ┗ 📜README.md                  # Tài liệu mô tả dự án và hướng dẫn chạy code

```

## 🚀 Hướng dẫn cài đặt và chạy (Installation)
1. **Cài đặt môi trường:** Đảm bảo máy tính đã cài đặt Python và Visual Studio Code (hoặc Jupyter).
2. **Cài đặt thư viện:** Mở Terminal tại thư mục dự án và chạy lệnh sau để cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
3. **Chạy ứng dụng:**

-  file main_notebook.ipynb bằng VS Code hoặc Jupyter.

- Chọn Kernel Python phù hợp.

- Chọn lệnh Restart & Run All (hoặc bấm chạy tuần tự từng ô) để xem dữ liệu được làm sạch, 5 biểu đồ phân tích và kết quả của mô hình Học máy.
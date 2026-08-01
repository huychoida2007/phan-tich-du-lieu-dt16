"""
app.py
Ứng dụng Streamlit: Dashboard Phân tích Dữ liệu Điện ảnh (IMDb/TMDB) - Đề tài DT16.
Chạy bằng: streamlit run app.py
"""
import streamlit as st
import pandas as pd

from core.data_loader import MovieDataLoader
from core.data_cleaner import DataCleaner
from core.analyzer import MovieAnalyzer
from core.predictor import MovieRevenuePredictor

# ============================================================
# CẤU HÌNH TRANG
# ============================================================
st.set_page_config(
    page_title="Phân tích Dữ liệu Điện ảnh - DT16",
    page_icon="🎬",
    layout="wide",
)

DATA_DIR = "data"
MOVIES_FILE = "tmdb_5000_movies.csv"
CREDITS_FILE = "tmdb_5000_credits.json"


# ============================================================
# HÀM NẠP & XỬ LÝ DỮ LIỆU (CACHE để tránh giật lag)
# ============================================================
@st.cache_data(show_spinner="Đang nạp và làm sạch dữ liệu...")
def load_and_process_data(data_dir: str = DATA_DIR) -> pd.DataFrame:
    """Nạp dữ liệu thô, gộp, làm sạch và trả về df_master hoàn chỉnh."""
    loader = MovieDataLoader(data_dir=data_dir)
    df_movies = loader.load_csv(MOVIES_FILE)
    df_credits = loader.load_json(CREDITS_FILE)

    # Sửa lỗi chiều dữ liệu JSON (nếu bị xoay ngang: 3 dòng, N cột)
    if df_credits.shape[0] == 3 and df_credits.shape[1] > 3:
        df_credits = df_credits.T.reset_index(drop=True)

    cleaner = DataCleaner(df_movies, df_credits)
    df_master = cleaner.merge_datasets()
    df_master = cleaner.clean_basic_anomalies()
    df_master = cleaner.process_all_json_columns()
    df_master = df_master.loc[:, ~df_master.columns.duplicated()]
    return df_master


@st.cache_resource(show_spinner="Đang huấn luyện mô hình...")
def train_model(df: pd.DataFrame):
    """Huấn luyện mô hình hồi quy tuyến tính (cache theo dữ liệu đầu vào)."""
    predictor = MovieRevenuePredictor(df)
    return predictor.train_and_evaluate()


# ============================================================
# SIDEBAR - MENU ĐIỀU HƯỚNG
# ============================================================
st.sidebar.title("🎬 DT16 - Movie Analytics")
menu = st.sidebar.radio(
    "Điều hướng",
    ["Giới thiệu", "Phân tích & Biểu đồ", "Mô hình Dự đoán"],
)

st.sidebar.markdown("---")
st.sidebar.caption("Bài tập lớn môn Lập trình Python cho Phân tích Dữ liệu")
st.sidebar.caption("Nhóm 01 - Mã đề tài DT16")

# Nạp dữ liệu 1 lần duy nhất, dùng chung cho mọi tab (nhờ cache)
try:
    df_master = load_and_process_data()
    data_ready = not df_master.empty
except Exception as e:
    data_ready = False
    st.sidebar.error(f"Lỗi nạp dữ liệu: {e}")

if not data_ready:
    st.error(
        "⚠️ Không tìm thấy hoặc không nạp được dữ liệu. "
        f"Vui lòng đặt 2 file `{MOVIES_FILE}` và `{CREDITS_FILE}` vào thư mục `data/`."
    )
    st.stop()


# ============================================================
# TAB 1: GIỚI THIỆU
# ============================================================
if menu == "Giới thiệu":
    st.title("🎬 Phân tích Dữ liệu Điện ảnh (IMDb/TMDB)")
    st.markdown("**Bài tập lớn môn Lập trình Python cho Phân tích Dữ liệu — Mã đề tài: DT16**")

    st.markdown(
        """
        Dự án phân tích bộ dữ liệu điện ảnh từ TMDB để khám phá các yếu tố then chốt
        gắn liền với thành công của một dự án điện ảnh (ngân sách, doanh thu, thời lượng,
        điểm đánh giá). Toàn bộ quy trình từ làm sạch dữ liệu, trực quan hóa đến dự đoán
        doanh thu được đóng gói theo mô hình **MVC** và triển khai thành dashboard tương tác
        bằng **Streamlit**.
        """
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Số bộ phim (sau làm sạch)", f"{df_master.shape[0]:,}")
    col2.metric("Số cột dữ liệu", df_master.shape[1])
    col3.metric("Doanh thu TB", f"${df_master['revenue'].mean():,.0f}")
    col4.metric("Ngân sách TB", f"${df_master['budget'].mean():,.0f}")

    st.markdown("### 📋 Xem trước dữ liệu đã làm sạch")
    st.dataframe(
        df_master[["title", "budget", "revenue", "profit", "genres", "vote_average"]].head(10),
        use_container_width=True,
    )

    st.markdown("### 👥 Thông tin nhóm")
    st.dataframe(
        pd.DataFrame(
            {
                "STT": [1, 2, 3, 4],
                "Họ và Tên": [
                    "Lê Quốc Huy (Nhóm trưởng)",
                    "Hoàng Đình Quảng",
                    "Nguyễn Huỳnh Tấn Khoa",
                    "Võ Hoàng Phúc",
                ],
                "Mã Sinh Viên": ["3120225066", "3120225125", "3120225071", "3120225121"],
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# TAB 2: PHÂN TÍCH & BIỂU ĐỒ
# ============================================================
elif menu == "Phân tích & Biểu đồ":
    st.title("📊 Phân tích & Trực quan hóa Dữ liệu")
    st.caption("5 câu hỏi phân tích cốt lõi, minh họa bằng 5 loại biểu đồ khác nhau.")

    analyzer = MovieAnalyzer(df_master)

    # --- Hàng 1: Heatmap + Scatter ---
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.subheader("1️⃣ Tương quan giữa các chỉ số")
        st.pyplot(analyzer.chart_1_correlation_heatmap())
        st.caption(
            "📌 Ngân sách, Doanh thu và Lợi nhuận có tương quan thuận rất mạnh; "
            "Điểm đánh giá gần như không tương quan tuyến tính với ngân sách."
        )
    with row1_col2:
        st.subheader("2️⃣ Ngân sách vs Doanh thu")
        st.pyplot(analyzer.chart_2_scatter_budget_revenue())
        st.caption(
            "📌 Phim ngân sách lớn có xu hướng doanh thu cao hơn, "
            "nhưng rủi ro thất thu với các bom tấn vẫn đáng kể."
        )

    st.markdown("---")

    # --- Hàng 2: Bar chart lợi nhuận theo thể loại (full width) ---
    st.subheader("3️⃣ Top 10 Thể loại có Lợi nhuận trung bình cao nhất")
    with st.container():
        st.pyplot(analyzer.chart_3_bar_profit_by_genre())
        st.caption("📌 Animation, Fantasy và Adventure dẫn đầu về lợi nhuận trung bình.")

    st.markdown("---")

    # --- Hàng 3: Line chart + Histogram ---
    row3_col1, row3_col2 = st.columns(2)
    with row3_col1:
        st.subheader("4️⃣ Xu hướng Thời lượng phim (1980-2016)")
        st.pyplot(analyzer.chart_4_line_runtime_trend())
        st.caption("📌 Thời lượng tăng nhẹ qua các thập niên rồi chững lại gần đây.")
    with row3_col2:
        st.subheader("5️⃣ Phân bố điểm đánh giá phim 'Bom xịt'")
        st.pyplot(analyzer.chart_5_histogram_flops())
        st.caption("📌 Đa số phim lỗ vốn không hẳn kém chất lượng (điểm trung bình 5.5-6.5).")

    st.markdown("---")
    with st.expander("➕ Xem thêm 2 biểu đồ mở rộng (Bonus)"):
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            st.subheader("6️⃣ Top 10 Diễn viên theo Doanh thu")
            st.pyplot(analyzer.chart_6_top_actors_revenue())
        with b_col2:
            st.subheader("7️⃣ Tài chính trung bình theo Thập kỷ")
            st.pyplot(analyzer.chart_7_financials_by_decade())


# ============================================================
# TAB 3: MÔ HÌNH DỰ ĐOÁN
# ============================================================
elif menu == "Mô hình Dự đoán":
    st.title("🤖 Dự đoán Doanh thu Phim bằng Học máy")
    st.markdown(
        """
        Mô hình **Hồi quy tuyến tính (Linear Regression)** dự đoán doanh thu (`revenue`)
        dựa trên: `budget`, `popularity`, `vote_average`, `vote_count`, `runtime`.
        Dữ liệu được chia 80% huấn luyện / 20% kiểm thử.
        """
    )

    result = train_model(df_master)

    m1, m2 = st.columns(2)
    m1.metric("R-squared (R²)", f"{result['r2']:.4f}")
    m2.metric("RMSE (USD)", f"{result['rmse']:,.0f}")

    col_chart, col_coef = st.columns([2, 1])
    with col_chart:
        st.subheader("Doanh thu Thực tế vs. Dự đoán")
        st.pyplot(result["fig"])
    with col_coef:
        st.subheader("Hệ số hồi quy")
        coef_df = pd.DataFrame(
            {"Đặc trưng": list(result["coefficients"].keys()),
             "Hệ số": list(result["coefficients"].values())}
        )
        st.dataframe(coef_df, use_container_width=True, hide_index=True)

    st.info(
        f"📌 **Đánh giá:** R² = {result['r2']:.2f} nghĩa là mô hình giải thích được "
        f"khoảng {result['r2']*100:.0f}% sự biến động doanh thu. Sai số RMSE vẫn còn cao "
        "do doanh thu phim còn chịu ảnh hưởng bởi nhiều yếu tố khó lượng hóa "
        "(kịch bản, marketing, thời điểm ra mắt...)."
    )

"""
core/analyzer.py
Lớp phân tích và trực quan hóa dữ liệu điện ảnh.
Mỗi hàm chart_* trả về một đối tượng matplotlib Figure để app.py (Streamlit)
có thể nhúng trực tiếp bằng st.pyplot(fig).
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class MovieAnalyzer:
    """
    Lớp phân tích và trực quan hóa dữ liệu điện ảnh.
    Giải quyết các câu hỏi phân tích bằng nhiều loại biểu đồ khác nhau.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        # Tạo thêm cột 'release_year' (Năm phát hành) từ 'release_date'
        self.df["release_date"] = pd.to_datetime(self.df["release_date"], errors="coerce")
        self.df["release_year"] = self.df["release_date"].dt.year

        # Xử lý lỗi trùng cột (ví dụ cột 'title' bị lặp sau khi merge)
        self.df = self.df.loc[:, ~self.df.columns.duplicated()]

        sns.set_theme(style="whitegrid")

    def chart_1_correlation_heatmap(self):
        """1. Bản đồ nhiệt (Heatmap): Tương quan giữa các biến số."""
        cols = ["budget", "revenue", "profit", "vote_average", "popularity", "runtime"]
        corr_matrix = self.df[cols].corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        ax.set_title("Bản đồ nhiệt tương quan giữa các chỉ số điện ảnh", fontsize=14)
        fig.tight_layout()
        return fig

    def chart_2_scatter_budget_revenue(self):
        """2. Biểu đồ phân tán (Scatter Plot): Ngân sách vs Doanh thu."""
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=self.df, x="budget", y="revenue", alpha=0.5, color="blue", ax=ax)
        sns.regplot(data=self.df, x="budget", y="revenue", scatter=False, color="red", ax=ax)

        ax.set_title("Tương quan giữa Ngân sách và Doanh thu", fontsize=14)
        ax.set_xlabel("Ngân sách (USD)", fontsize=12)
        ax.set_ylabel("Doanh thu (USD)", fontsize=12)
        fig.tight_layout()
        return fig

    def chart_3_bar_profit_by_genre(self):
        """3. Biểu đồ cột (Bar Chart): Top 10 Thể loại có Lợi nhuận trung bình cao nhất."""
        df_genres = self.df.assign(genres=self.df["genres"].str.split(", ")).explode("genres")
        df_genres = df_genres[df_genres["genres"] != ""]

        genre_profit = (
            df_genres.groupby("genres")["profit"].mean().sort_values(ascending=False).head(10)
        )

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(
            x=genre_profit.values,
            y=genre_profit.index,
            hue=genre_profit.index,
            palette="viridis",
            legend=False,
            ax=ax,
        )
        ax.set_title("Top 10 Thể loại phim mang lại Lợi nhuận trung bình cao nhất", fontsize=14)
        ax.set_xlabel("Lợi nhuận trung bình (USD)", fontsize=12)
        ax.set_ylabel("Thể loại", fontsize=12)
        fig.tight_layout()
        return fig

    def chart_4_line_runtime_trend(self):
        """4. Biểu đồ đường (Line Chart): Xu hướng thời lượng phim qua các năm."""
        df_trend = self.df[(self.df["release_year"] >= 1980) & (self.df["release_year"] <= 2016)]
        yearly_runtime = df_trend.groupby("release_year")["runtime"].mean().reset_index()

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(
            data=yearly_runtime,
            x="release_year",
            y="runtime",
            marker="o",
            color="purple",
            linewidth=2,
            ax=ax,
        )
        ax.set_title("Xu hướng Thời lượng phim trung bình (1980 - 2016)", fontsize=14)
        ax.set_xlabel("Năm phát hành", fontsize=12)
        ax.set_ylabel("Thời lượng trung bình (Phút)", fontsize=12)
        fig.tight_layout()
        return fig

    def chart_5_histogram_flops(self):
        """5. Biểu đồ phân phối (Histogram): Phân bố điểm đánh giá của các phim 'Bom xịt' (Lỗ vốn)."""
        df_flops = self.df[self.df["profit"] < 0]

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df_flops["vote_average"], bins=20, kde=True, color="orange", ax=ax)
        ax.set_title("Phân bố Điểm đánh giá (Vote Average) của các phim Lỗ vốn", fontsize=14)
        ax.set_xlabel("Điểm đánh giá (0 - 10)", fontsize=12)
        ax.set_ylabel("Số lượng phim", fontsize=12)
        fig.tight_layout()
        return fig

    def chart_6_top_actors_revenue(self):
        """6 (Bonus). Top 10 diễn viên mang lại tổng doanh thu phòng vé cao nhất."""
        df_cast = self.df.assign(cast=self.df["cast"].str.split(", ")).explode("cast")
        df_cast = df_cast[df_cast["cast"] != ""]

        top_actors = (
            df_cast.groupby("cast")["revenue"].sum().sort_values(ascending=False).head(10)
        )

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(
            x=top_actors.values,
            y=top_actors.index,
            hue=top_actors.index,
            palette="magma",
            legend=False,
            ax=ax,
        )
        ax.set_title("Top 10 Diễn viên mang lại Tổng doanh thu phòng vé cao nhất", fontsize=14)
        ax.set_xlabel("Tổng doanh thu (USD)", fontsize=12)
        ax.set_ylabel("Diễn viên (Cast)", fontsize=12)
        fig.tight_layout()
        return fig

    def chart_7_financials_by_decade(self):
        """7 (Bonus). Trung bình Ngân sách/Doanh thu/Lợi nhuận theo thập kỷ."""
        df_decade = self.df.copy()
        df_decade["decade"] = (df_decade["release_year"] // 10) * 10
        df_decade = df_decade[(df_decade["decade"] >= 1980) & (df_decade["decade"] <= 2010)]

        decade_stats = (
            df_decade.groupby("decade")[["budget", "revenue", "profit"]].mean().reset_index()
        )
        decade_melted = decade_stats.melt(id_vars="decade", var_name="Metric", value_name="Amount")
        metric_names = {"budget": "Ngân sách", "revenue": "Doanh thu", "profit": "Lợi nhuận"}
        decade_melted["Metric"] = decade_melted["Metric"].map(metric_names)

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=decade_melted, x="decade", y="Amount", hue="Metric", palette="muted", ax=ax)
        ax.set_title("Trung bình Ngân sách, Doanh thu và Lợi nhuận theo Thập kỷ (1980s - 2010s)", fontsize=14)
        ax.set_xlabel("Thập kỷ (Decade)", fontsize=12)
        ax.set_ylabel("Số tiền trung bình (USD)", fontsize=12)
        ax.legend(title="Chỉ số tài chính")
        fig.tight_layout()
        return fig

    # =============================================================
    # CÁC HÀM PHÂN TÍCH BỔ SUNG (Main Task 1)
    # =============================================================

    def plot_rating_distribution(self):
        """Histogram: Phân phối điểm đánh giá (vote_average) của toàn bộ phim."""
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(
            data=self.df, x="vote_average", bins=30, kde=True, color="steelblue", ax=ax
        )
        ax.axvline(
            self.df["vote_average"].mean(),
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Trung bình: {self.df['vote_average'].mean():.2f}",
        )
        ax.legend()
        ax.set_title("Phân phối Điểm đánh giá (Vote Average) của toàn bộ phim", fontsize=14)
        ax.set_xlabel("Điểm đánh giá (0 - 10)", fontsize=12)
        ax.set_ylabel("Số lượng phim", fontsize=12)
        fig.tight_layout()
        return fig

    def plot_top_actors(self):
        """Top diễn viên và đạo diễn mang lại tổng doanh thu phòng vé cao nhất."""
        # --- Top 10 diễn viên ---
        df_cast = self.df.assign(
            cast=self.df["cast"].str.split(", ")
        ).explode("cast")
        df_cast = df_cast[df_cast["cast"] != ""]
        top_actors = (
            df_cast.groupby("cast")["revenue"].sum().sort_values(ascending=False).head(10)
        )

        # --- Top 10 đạo diễn ---
        df_dir = self.df.assign(
            crew=self.df["crew"].str.split(", ")
        ).explode("crew")
        df_dir = df_dir[df_dir["crew"] != ""]
        top_directors = (
            df_dir.groupby("crew")["revenue"].sum().sort_values(ascending=False).head(10)
        )

        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        sns.barplot(
            x=top_actors.values,
            y=top_actors.index,
            hue=top_actors.index,
            palette="magma",
            legend=False,
            ax=axes[0],
        )
        axes[0].set_title("Top 10 Diễn viên theo Tổng doanh thu", fontsize=13)
        axes[0].set_xlabel("Tổng doanh thu (USD)", fontsize=11)
        axes[0].set_ylabel("Diễn viên", fontsize=11)

        sns.barplot(
            x=top_directors.values,
            y=top_directors.index,
            hue=top_directors.index,
            palette="viridis",
            legend=False,
            ax=axes[1],
        )
        axes[1].set_title("Top 10 Đạo diễn theo Tổng doanh thu", fontsize=13)
        axes[1].set_xlabel("Tổng doanh thu (USD)", fontsize=11)
        axes[1].set_ylabel("Đạo diễn", fontsize=11)

        fig.suptitle("Top Diễn viên & Đạo diễn mang lại Doanh thu cao nhất", fontsize=15, y=1.02)
        fig.tight_layout()
        return fig

    def plot_decade_trends(self):
        """Phân tích xu hướng phát triển phim qua các thập kỷ."""
        df_decade = self.df.copy()
        df_decade["decade"] = (df_decade["release_year"] // 10) * 10
        df_decade = df_decade[
            (df_decade["decade"] >= 1980) & (df_decade["decade"] <= 2010)
        ]

        decade_stats = (
            df_decade.groupby("decade")
            .agg(
                movie_count=("title", "count"),
                avg_revenue=("revenue", "mean"),
                avg_budget=("budget", "mean"),
            )
            .reset_index()
        )

        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Cột: Số lượng phim theo thập kỷ
        bars = sns.barplot(
            data=decade_stats,
            x="decade",
            y="movie_count",
            color="skyblue",
            ax=ax1,
            alpha=0.7,
        )
        ax1.set_xlabel("Thập kỷ (Decade)", fontsize=12)
        ax1.set_ylabel("Số lượng phim", fontsize=12, color="steelblue")
        ax1.tick_params(axis="y", labelcolor="steelblue")

        # Thêm nhãn số lượng lên đầu mỗi cột
        for bar, count in zip(bars.patches, decade_stats["movie_count"]):
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{int(count)}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color="steelblue",
            )

        # Đường: Doanh thu & Ngân sách trung bình trên trục phụ
        ax2 = ax1.twinx()
        sns.lineplot(
            data=decade_stats,
            x="decade",
            y="avg_revenue",
            marker="o",
            color="crimson",
            linewidth=2.5,
            label="Doanh thu TB",
            ax=ax2,
        )
        sns.lineplot(
            data=decade_stats,
            x="decade",
            y="avg_budget",
            marker="s",
            color="darkorange",
            linewidth=2.5,
            label="Ngân sách TB",
            ax=ax2,
        )
        ax2.set_ylabel("Số tiền trung bình (USD)", fontsize=12)
        ax2.tick_params(axis="y")
        ax2.legend(title="Chỉ số tài chính", loc="upper left")

        ax1.set_title(
            "Xu hướng phát triển điện ảnh theo Thập kỷ (1980s - 2010s)", fontsize=14
        )
        fig.tight_layout()
        return fig

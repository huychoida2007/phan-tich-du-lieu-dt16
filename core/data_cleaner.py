"""
core/data_cleaner.py
Lớp chuyên dụng để làm sạch và biến đổi dữ liệu điện ảnh TMDB.
"""
import ast
import pandas as pd


class DataCleaner:
    """
    Lớp chuyên dụng để làm sạch và biến đổi dữ liệu điện ảnh TMDB.
    """

    def __init__(self, df_movies: pd.DataFrame, df_credits: pd.DataFrame):
        self.df_movies = df_movies
        self.df_credits = df_credits
        self.df_merged = pd.DataFrame()

    def merge_datasets(self) -> pd.DataFrame:
        """Gộp 2 tập dữ liệu movies và credits lại với nhau."""
        if "id" in self.df_credits.columns:
            self.df_credits = self.df_credits.rename(columns={"id": "movie_id"})

        # Bỏ cột 'title' trùng lặp bên credits (nếu có) để tránh sinh cột
        # 'title_x' / 'title_y' hoặc 2 cột 'title' trùng tên sau khi gộp
        if "title" in self.df_credits.columns and "title" in self.df_movies.columns:
            self.df_credits = self.df_credits.drop(columns=["title"])

        try:
            self.df_merged = self.df_movies.merge(
                self.df_credits, left_on="id", right_on="movie_id"
            )
        except KeyError:
            self.df_merged = pd.concat([self.df_movies, self.df_credits], axis=1)

        return self.df_merged

    def clean_basic_anomalies(self) -> pd.DataFrame:
        """Xử lý giá trị thiếu, trùng lặp và loại bỏ doanh thu/ngân sách = 0."""
        # 1. Bỏ dòng trùng lặp
        self.df_merged = self.df_merged.drop_duplicates()

        # 2. Loại bỏ các phim có budget hoặc revenue = 0 (bắt buộc theo đề)
        self.df_merged = self.df_merged[
            (self.df_merged["budget"] > 0) & (self.df_merged["revenue"] > 0)
        ]

        # 3. Bỏ các dòng thiếu dữ liệu ở các cột quan trọng
        self.df_merged = self.df_merged.dropna(subset=["release_date", "title"])

        # 4. Điền giá trị thiếu cho cột runtime bằng median
        if "runtime" in self.df_merged.columns:
            median_runtime = self.df_merged["runtime"].median()
            self.df_merged["runtime"] = self.df_merged["runtime"].fillna(median_runtime)

        return self.df_merged

    def extract_json_names(self, column_name: str):
        """
        Hàm phụ trợ: Bóc tách thuộc tính 'name' từ chuỗi JSON lồng trong các cột.
        Ví dụ: '[{"id": 28, "name": "Action"}]' -> ['Action']
        """

        def parse_string(obj_str):
            if pd.isna(obj_str):
                return []
            try:
                obj_list = ast.literal_eval(obj_str)
                return [item["name"] for item in obj_list]
            except (ValueError, SyntaxError):
                return []

        if column_name in self.df_merged.columns:
            self.df_merged[column_name] = self.df_merged[column_name].apply(parse_string)
            self.df_merged[column_name] = self.df_merged[column_name].apply(
                lambda x: ", ".join(x)
            )

    def extract_top_actors(self, column_name: str = "cast", top_n: int = 3):
        """
        Hàm phụ trợ: Bóc tách Top N diễn viên chính (theo thứ tự 'order')
        từ cột cast. Ví dụ: top 3 diễn viên dẫn đầu danh sách.
        """

        def parse_top_actors(obj_str):
            if pd.isna(obj_str):
                return ""
            try:
                obj_list = ast.literal_eval(obj_str)
                # Sắp xếp theo 'order' (0 = diễn viên chính) và lấy top N
                sorted_cast = sorted(obj_list, key=lambda x: x.get("order", 999))
                top_names = [item["name"] for item in sorted_cast[:top_n]]
                return ", ".join(top_names)
            except (ValueError, SyntaxError, KeyError, TypeError):
                return ""

        if column_name in self.df_merged.columns:
            self.df_merged[column_name] = self.df_merged[column_name].apply(parse_top_actors)

    def extract_director(self, column_name: str = "crew"):
        """
        Hàm phụ trợ: Bóc tách tên Đạo diễn (Director) từ cột crew
        bằng cách lọc theo 'job' == 'Director'.
        """

        def parse_director(obj_str):
            if pd.isna(obj_str):
                return ""
            try:
                obj_list = ast.literal_eval(obj_str)
                directors = [
                    item["name"] for item in obj_list if item.get("job") == "Director"
                ]
                return ", ".join(directors)
            except (ValueError, SyntaxError, KeyError, TypeError):
                return ""

        if column_name in self.df_merged.columns:
            self.df_merged[column_name] = self.df_merged[column_name].apply(parse_director)

    def standardize_dates(self):
        """Chuẩn hóa cột release_date và trích xuất release_year, release_month."""
        if "release_date" in self.df_merged.columns:
            self.df_merged["release_date"] = pd.to_datetime(
                self.df_merged["release_date"], errors="coerce"
            )
            self.df_merged["release_year"] = self.df_merged["release_date"].dt.year
            self.df_merged["release_month"] = self.df_merged["release_date"].dt.month

    def process_all_json_columns(self) -> pd.DataFrame:
        """Xử lý hàng loạt các cột chứa chuỗi JSON phức tạp."""
        # Các cột lấy toàn bộ danh sách name
        columns_to_extract = [
            "genres",
            "keywords",
            "production_companies",
            "production_countries",
        ]
        for col in columns_to_extract:
            self.extract_json_names(col)

        # Cột cast: chỉ lấy Top 3 diễn viên chính
        self.extract_top_actors("cast", top_n=3)

        # Cột crew: chỉ lấy tên Đạo diễn (Director)
        self.extract_director("crew")

        # Chuẩn hóa ngày phát hành và trích xuất năm/tháng
        self.standardize_dates()

        # Tính thêm cột Lợi nhuận (Profit) để phục vụ phân tích sau này
        self.df_merged["profit"] = self.df_merged["revenue"] - self.df_merged["budget"]

        return self.df_merged

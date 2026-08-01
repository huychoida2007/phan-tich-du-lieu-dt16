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

    def process_all_json_columns(self) -> pd.DataFrame:
        """Xử lý hàng loạt các cột chứa chuỗi JSON phức tạp."""
        columns_to_extract = [
            "genres",
            "keywords",
            "production_companies",
            "production_countries",
            "cast",
            "crew",
        ]
        for col in columns_to_extract:
            self.extract_json_names(col)

        # Tính thêm cột Lợi nhuận (Profit) để phục vụ phân tích sau này
        self.df_merged["profit"] = self.df_merged["revenue"] - self.df_merged["budget"]

        return self.df_merged

"""
core/predictor.py
Lớp xây dựng mô hình học máy (Hồi quy tuyến tính) để dự đoán doanh thu phim.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

FEATURES = ["budget", "popularity", "vote_average", "vote_count", "runtime"]


class MovieRevenuePredictor:
    """Lớp xây dựng mô hình học máy dự đoán doanh thu phim."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.model = LinearRegression()

    def prepare_data(self):
        """Chuẩn bị dữ liệu: Lựa chọn đặc trưng và chia tập Train/Test (80/20)."""
        self.df = self.df.dropna(subset=FEATURES + ["revenue"])
        X = self.df[FEATURES]
        y = self.df["revenue"]
        # Chia dữ liệu: 80% huấn luyện, 20% kiểm thử
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_and_evaluate(self):
        """
        Huấn luyện mô hình, đánh giá sai số và trả về kết quả.
        Trả về dict: {r2, rmse, mae, fig, y_test, y_pred, coefficients}
        """
        X_train, X_test, y_train, y_test = self.prepare_data()

        # 1. Huấn luyện mô hình Hồi quy tuyến tính
        self.model.fit(X_train, y_train)

        # 2. Dự đoán trên tập kiểm thử
        y_pred = self.model.predict(X_test)

        # 3. Đánh giá mô hình: R², RMSE, MAE
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)

        # 4. Trực quan hóa So sánh Thực tế vs Dự đoán
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(y_test, y_pred, alpha=0.6, color="seagreen")

        max_val = max(y_test.max(), y_pred.max())
        ax.plot([0, max_val], [0, max_val], "r--", lw=2)

        ax.set_title("Mô hình Học máy: Doanh thu Thực tế vs. Dự đoán", fontsize=14)
        ax.set_xlabel("Doanh thu Thực tế (USD)", fontsize=12)
        ax.set_ylabel("Doanh thu Dự đoán (USD)", fontsize=12)
        fig.tight_layout()

        return {
            "r2": r2,
            "rmse": rmse,
            "mae": mae,
            "fig": fig,
            "y_test": y_test,
            "y_pred": y_pred,
            "coefficients": dict(zip(FEATURES, self.model.coef_)),
        }
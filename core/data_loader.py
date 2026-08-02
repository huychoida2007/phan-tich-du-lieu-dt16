"""
core/data_loader.py
Lớp chịu trách nhiệm nạp dữ liệu điện ảnh từ nhiều định dạng khác nhau (CSV, JSON).
"""
import os
import json
import pandas as pd


class MovieDataLoader:
    """
    Lớp chịu trách nhiệm nạp dữ liệu điện ảnh từ nhiều định dạng khác nhau (CSV, JSON).
    Hỗ trợ xử lý ngoại lệ an toàn khi file không tồn tại hoặc lỗi định dạng.
    """

    def __init__(self, data_dir: str = "data"):
        """Khởi tạo với đường dẫn tới thư mục chứa dữ liệu."""
        self.data_dir = data_dir

    def load_csv(self, filename: str) -> pd.DataFrame:
        """Đọc dữ liệu từ file CSV và trả về DataFrame."""
        filepath = os.path.join(self.data_dir, filename)
        try:
            df = pd.read_csv(filepath)
            return df
        except FileNotFoundError:
            print(f"LỖI: Không tìm thấy file {filepath}. Vui lòng kiểm tra lại thư mục data.")
            return pd.DataFrame()
        except Exception as e:
            print(f"LỖI KHÔNG XÁC ĐỊNH khi nạp {filepath}: {e}")
            return pd.DataFrame()

    def load_json(self, filename: str) -> pd.DataFrame:
        """Đọc dữ liệu từ file JSON và chuyển đổi thành DataFrame."""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
            df = pd.DataFrame(data)
            return df
        except FileNotFoundError:
            print(f"LỖI: Không tìm thấy file {filepath}. Vui lòng kiểm tra lại thư mục data.")
            return pd.DataFrame()
        except json.JSONDecodeError:
            print(f"LỖI: Định dạng file {filepath} không phải là JSON chuẩn.")
            return pd.DataFrame()
        except Exception as e:
            print(f"LỖI KHÔNG XÁC ĐỊNH khi nạp {filepath}: {e}")
            return pd.DataFrame()

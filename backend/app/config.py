# src/core/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env
load_dotenv()

class Config:
    """Cấu hình tập trung cho hệ thống E-commerce Market Agent (Tiki Focus)"""
    
    # --- GOOGLE GEMINI AI CONFIG ---
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    @classmethod
    def validate_api_key(cls) -> bool:
        """Kiểm tra xem API Key của Gemini có hợp lệ hay không"""
        return bool(cls.GOOGLE_API_KEY) and cls.GOOGLE_API_KEY != 'GOOGLE_API_KEY'
    
    @classmethod
    def get_api_key_preview(cls) -> str:
        """Hiển thị chuỗi preview an toàn cho API Key trên logs/giao diện"""
        key = cls.GOOGLE_API_KEY
        if key and len(key) > 10:
            return f"{key[:10]}...{key[-5:]}"
        return "❌ Không có"
    
    # --- RELATIONAL DATABASE CONFIG (MySQL) ---
    # Ưu tiên lấy từ biến môi trường, mặc định kết nối tới localhost
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://root:root@localhost:3306/tiki_market_agent?charset=utf8mb4"
    )
    
    # --- CRAWLER SETTINGS ---
    # Giới hạn số lượng sản phẩm mỗi lượt quét (mặc định 20 để tối ưu tốc độ LangGraph/FastAPI)
    MAX_PRODUCTS = int(os.getenv("MAX_PRODUCTS", 20))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", 3))
    
    # --- PLATFORMS ---
    @classmethod
    def get_platforms(cls):
        """Danh sách sàn hỗ trợ (Hiện tại tập trung sâu vào Tiki)"""
        return {
            'tiki': 'Tiki (Active)',
        }
        
    # --- LOGGING ---
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # --- HỆ THỐNG PATHS (Giữ lại nếu Node Report cần lưu tạm văn bản) ---
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    REPORTS_DIR = DATA_DIR / "reports"
    
    @classmethod
    def ensure_directories(cls):
        """Tạo các thư mục lưu trữ báo cáo cục bộ nếu cần thiết"""
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
# src/core/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Cấu hình ứng dụng"""
    
    # Google Gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    @classmethod
    def validate_api_key(cls) -> bool:
        """Kiểm tra API Key"""
        return bool(cls.GOOGLE_API_KEY) and cls.GOOGLE_API_KEY != "AIzaSyDl3LI7S0phFe74J9umakY9qL8HHoJM2zk"
    
    @classmethod
    def get_api_key_preview(cls) -> str:
        """Preview API Key"""
        key = cls.GOOGLE_API_KEY
        if key and len(key) > 10:
            return f"{key[:10]}...{key[-5:]}"
        return "❌ Không có"
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    REPORTS_DIR = DATA_DIR / "reports"
    
    # Crawler
    MAX_PRODUCTS = int(os.getenv("MAX_PRODUCTS", 100))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", 3))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def ensure_directories(cls):
        """Tạo thư mục"""
        cls.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_platforms(cls):
        """Danh sách sàn TMĐT"""
        return {
            'tiki': 'Tiki',
            'shopee': 'Shopee',
            'lazada': 'Lazada'
        }
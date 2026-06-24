# src/utils/logger.py

import logging
import sys
from pathlib import Path
from datetime import datetime

from src.core.config import Config

def setup_logging():
    """Cấu hình logging cho toàn bộ ứng dụng"""
    
    # Tạo thư mục logs nếu chưa tồn tại
    log_dir = Config.BASE_DIR / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Tạo tên file log theo ngày
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Cấu hình logging
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding='utf-8')
        ]
    )
    
    # Giảm log từ các thư viện khác
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)

def get_logger(name: str) -> logging.Logger:
    """
    Lấy logger cho module
    
    Args:
        name: Tên module
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)

# Setup logging khi import
setup_logging()
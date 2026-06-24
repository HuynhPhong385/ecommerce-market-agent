# src/utils/file_utils.py

import json
from pathlib import Path
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

class FileUtils:
    """Tiện ích xử lý file"""
    
    @staticmethod
    def save_json(filepath: Path, data: Any, indent: int = 2) -> None:
        """
        Lưu dữ liệu dạng JSON
        
        Args:
            filepath: Đường dẫn file
            data: Dữ liệu cần lưu
            indent: Số spaces indent
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            logger.info(f"✅ Đã lưu file: {filepath}")
        except Exception as e:
            logger.error(f"❌ Lỗi khi lưu file {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def load_json(filepath: Path) -> Any:
        """
        Đọc dữ liệu từ file JSON
        
        Args:
            filepath: Đường dẫn file
            
        Returns:
            Dữ liệu đọc được
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"✅ Đã đọc file: {filepath}")
            return data
        except Exception as e:
            logger.error(f"❌ Lỗi khi đọc file {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def save_text(filepath: Path, content: str) -> None:
        """
        Lưu nội dung dạng text
        
        Args:
            filepath: Đường dẫn file
            content: Nội dung cần lưu
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ Đã lưu file: {filepath}")
        except Exception as e:
            logger.error(f"❌ Lỗi khi lưu file {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def load_text(filepath: Path) -> str:
        """
        Đọc nội dung từ file text
        
        Args:
            filepath: Đường dẫn file
            
        Returns:
            Nội dung file
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"✅ Đã đọc file: {filepath}")
            return content
        except Exception as e:
            logger.error(f"❌ Lỗi khi đọc file {filepath}: {str(e)}")
            raise
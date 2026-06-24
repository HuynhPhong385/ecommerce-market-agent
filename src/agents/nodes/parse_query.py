# src/agents/nodes/parse_query.py

import re
import logging
from typing import List, Dict

from src.agents.state import AgentState
from src.core.config import Config

logger = logging.getLogger(__name__)

def parse_query(state: AgentState) -> AgentState:
    """
    Node 1: Phân tích câu hỏi của người dùng
    """
    logger.info("Dang phan tich cau hoi...")
    
    query = state['user_query'].lower()
    state['current_step'] = 'parsing'
    
    # ✅ Luôn là Tiki
    state['platform'] = 'tiki'
    
    # Trích xuất category và keywords
    category, keywords = extract_category_and_keywords(query)
    state['category'] = category
    state['keywords'] = keywords
    
    # Trích xuất số lượng sản phẩm
    max_products = extract_max_products(query)
    state['max_products'] = max_products
    
    logger.info(f"Category: {category}, Keywords: {keywords}")
    
    return state

def extract_category_and_keywords(query: str) -> tuple:
    """Trích xuất category và keywords từ câu hỏi"""
    categories = [
        'giay', 'dien thoai', 'laptop', 'may tinh', 'thoi trang',
        'quan ao', 'gia dung', 'sach', 'do choi', 'my pham',
        'thuc pham', 'do uong', 'suc khoe', 'the thao',
        'tai nghe', 'loa', 'dong ho', 'kinh mat'
    ]
    
    words = query.split()
    category = 'san pham'
    keywords = []
    
    # Tìm category
    for i, word in enumerate(words):
        if word in categories:
            category = word
            if i > 0:
                keywords.append(words[i-1])
            if i < len(words) - 1:
                keywords.append(words[i+1])
    
    # Nếu không có category, lấy từ cuối cùng
    if category == 'san pham':
        category = words[-1] if words else 'san pham'
    
    # Clean keywords
    keywords = [k for k in keywords if k not in ['cua', 'va', 'voi', 'tren']]
    if not keywords:
        keywords = [category]
    
    return category, keywords

def extract_max_products(query: str) -> int | None:
    """Trích xuất số lượng sản phẩm từ câu hỏi"""
    patterns = [
        r'(\d+)\s*(?:san pham|sp|items|products)',
        r'(?:lay|cao)\s*(\d+)\s*(?:san pham)',
        r'(?:khoang|cua)\s*(\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return int(match.group(1))
    
    return None
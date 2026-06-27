# backend/app/agents/state.py
from typing import List, Dict, Any, TypedDict

class AgentState(TypedDict):
    keyword: str
    product_id_list: List[str]      # Danh sách ID sản phẩm đối thủ lấy từ MySQL
    raw_competitor_data: List[Dict] # Dữ liệu chi tiết của đối thủ phục vụ cho LLM
    price_analysis: Dict[str, Any]  # Kết quả phân tích giá (Min, Max, Avg, Gợi ý giá)
    optimized_description: Dict[str, Any] # Tiêu đề, mô tả mới do AI viết
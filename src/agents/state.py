# src/agents/state.py

from typing import TypedDict, List, Dict, Optional

class AgentState(TypedDict):
    """Trạng thái của Agent trong quá trình xử lý"""
    user_query: str           # Câu hỏi của người dùng
    platform: str             # Sàn TMĐT
    category: str             # Ngành hàng cần phân tích
    keywords: List[str]       # Từ khóa tìm kiếm
    max_products: Optional[int]  # Số lượng sản phẩm tối đa
    raw_data: List[Dict]      # Dữ liệu thô từ crawler
    analyzed_data: Dict       # Dữ liệu đã phân tích
    report: str               # Báo cáo cuối cùng
    error: Optional[str]      # Lỗi nếu có
    current_step: str         # Bước hiện tại
    is_complete: bool         # Trạng thái hoàn thành
    metadata: Dict            # Metadata bổ sung
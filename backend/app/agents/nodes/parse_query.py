# backend/app/agents/nodes/parse_query.py
# Nhiệm vụ: Nhận từ khóa từ Frontend gửi lên, làm sạch chuỗi (ví dụ bỏ ký tự đặc biệt) trước khi đưa vào hệ thống.
from backend.app.agents.state import AgentState

def parse_query_node(state: AgentState) -> dict:
    """Node: Xử lý và chuẩn hóa từ khóa tìm kiếm"""
    raw_keyword = state.get("keyword", "")
    # Làm sạch từ khóa (bỏ khoảng trắng thừa, chuyển chữ thường...)
    clean_keyword = raw_keyword.strip().lower()
    
    print(f"[Node: Parse Query] Đang xử lý từ khóa: {clean_keyword}")
    return {"keyword": clean_keyword}
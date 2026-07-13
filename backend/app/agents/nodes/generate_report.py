# backend/app/agents/nodes/generate_report.py
# Nhiệm vụ: Tổng hợp dữ liệu phân tích giá và sản phẩm đối thủ để nạp vào LLM, xuất ra mô tả sản phẩm và tiêu đề đã được AI tối ưu.

from backend.app.agents.state import AgentState

def generate_report_node(state: AgentState) -> dict:
    """Node: Dùng AI viết lại nội dung bán hàng tối ưu dựa trên thị trường"""
    keyword = state["keyword"]
    price_info = state["price_analysis"]
    
    # Đoạn này bạn tích hợp code gọi LLM (Gemini/OpenAI) của bạn vào
    suggested_title = f"[Giá Tốt Nhất] {keyword.upper()} Cao Cấp - Tối Ưu Phân Khúc Thị Trường"
    suggested_desc = (
        f"### ĐẶC ĐIỂM SẢN PHẨM\n"
        f"- Sản phẩm định vị chiến lược tại mức giá {price_info['suggested_price']}đ\n"
        f"- Phân tích giá trung bình trên sàn Tiki hiện tại: {price_info['average_price']}đ"
    )
    
    return {
        "optimized_description": {
            "title": suggested_title,
            "description": suggested_desc
        }
    }
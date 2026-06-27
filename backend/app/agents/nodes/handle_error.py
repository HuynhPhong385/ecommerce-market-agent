# backend/app/agents/nodes/handle_error.py
# Nhiệm vụ: Node bắt lỗi, nếu các luồng trên bị gãy (ví dụ: mất mạng, API Tiki đổi cấu trúc), 
# hệ thống sẽ chạy vào đây để trả về dữ liệu mẫu nhằm giữ ứng dụng không bị crash.

from backend.app.agents.state import AgentState

def handle_error_node(state: AgentState) -> dict:
    """Node: Xử lý fallback khi hệ thống xảy ra lỗi ngoài ý muốn"""
    print("[Node: Handle Error] Hệ thống phát hiện lỗi, đang kích hoạt chế độ dự phòng...")
    return {
        "price_analysis": {"message": "Dữ liệu đang được đồng bộ lại, vui lòng thử lại sau."},
        "optimized_description": {"title": "Đang cập nhật...", "description": "Hệ thống đang bận."}
    }
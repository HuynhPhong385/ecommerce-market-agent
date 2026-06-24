# src/agents/nodes/handle_error.py

import logging
from datetime import datetime
from src.agents.state import AgentState

logger = logging.getLogger(__name__)

def handle_error(state: AgentState) -> AgentState:
    """
    Node xử lý lỗi
    """
    error = state.get('error', 'Lỗi không xác định')
    logger.error(f"⚠️ Xảy ra lỗi: {error}")
    state['is_complete'] = True
    
    # Tạo báo cáo lỗi
    error_report = f"""
# ❌ Báo cáo lỗi

Rất tiếc, đã xảy ra lỗi trong quá trình xử lý yêu cầu của bạn.

## Thông tin lỗi

**Lỗi:** {error}

**Bước gặp lỗi:** {state.get('current_step', 'Không xác định')}

**Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## Giải pháp đề xuất

1. Kiểm tra lại câu hỏi và thử lại
2. Đảm bảo kết nối Internet ổn định
3. Kiểm tra API Key có hợp lệ không
4. Thử với câu hỏi đơn giản hơn

Nếu vẫn gặp vấn đề, vui lòng liên hệ hỗ trợ.
"""
    state['report'] = error_report
    
    return state
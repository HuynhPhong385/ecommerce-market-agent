# src/agents/nodes/analyze_data.py

import logging
from src.agents.state import AgentState
from src.core.tools import EcommerceTools

logger = logging.getLogger(__name__)

def analyze_data(state: AgentState) -> AgentState:
    """
    Node 3: Phân tích dữ liệu
    """
    logger.info("📊 Đang phân tích dữ liệu...")
    state['current_step'] = 'analyzing'
    
    if state.get('error'):
        return state
    
    try:
        tools = EcommerceTools()
        analysis = tools.analyze_trends(state['raw_data'])
        state['analyzed_data'] = analysis
        logger.info("✅ Phân tích hoàn tất")
        
    except Exception as e:
        error_msg = f"Lỗi phân tích: {str(e)}"
        state['error'] = error_msg
        logger.error(error_msg)
    
    return state
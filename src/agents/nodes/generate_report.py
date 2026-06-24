# src/agents/nodes/generate_report.py

import logging
from src.agents.state import AgentState
from src.core.tools import EcommerceTools

logger = logging.getLogger(__name__)

def generate_report(state: AgentState) -> AgentState:
    """
    Node 4: Tạo báo cáo
    """
    logger.info("📝 Đang tạo báo cáo...")
    state['current_step'] = 'generating_report'
    
    if state.get('error'):
        return state
    
    try:
        tools = EcommerceTools()
        report = tools.generate_report(
            analysis=state['analyzed_data'],
            query=state['user_query']
        )
        
        state['report'] = report
        state['is_complete'] = True
        logger.info("✅ Báo cáo đã được tạo")
        
    except Exception as e:
        error_msg = f"Lỗi tạo báo cáo: {str(e)}"
        state['error'] = error_msg
        logger.error(error_msg)
    
    return state
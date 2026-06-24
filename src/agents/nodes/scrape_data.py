# src/agents/nodes/scrape_data.py

import logging
from src.agents.state import AgentState
from src.core.tools import EcommerceTools  # ✅ Import đúng

logger = logging.getLogger(__name__)

def scrape_data(state: AgentState) -> AgentState:
    """
    Node 2: Cào dữ liệu từ sàn TMĐT
    """
    logger.info("🕷️ Đang cào dữ liệu...")
    state['current_step'] = 'scraping'
    
    try:
        tools = EcommerceTools()  # ✅ Khởi tạo
        data = tools.scrape_ecommerce_data(  # ✅ Method tồn tại
            platform=state['platform'],
            category=state['category'],
            keywords=state['keywords'],
            max_products=state.get('max_products')
        )
        
        state['raw_data'] = data
        logger.info(f"✅ Đã cào được {len(data)} sản phẩm")
        
    except Exception as e:
        error_msg = f"Lỗi cào dữ liệu: {str(e)}"
        state['error'] = error_msg
        logger.error(error_msg)
    
    return state
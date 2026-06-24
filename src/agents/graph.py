# src/agents/nodes/scrape_data.py

import logging
from src.agents.state import AgentState
from src.core.tools import EcommerceTools

logger = logging.getLogger(__name__)

def scrape_data(state: AgentState) -> AgentState:
    """
    Node 2: Cào dữ liệu từ Tiki
    """
    logger.info("Dang cào du lieu tu Tiki...")
    state['current_step'] = 'scraping'
    
    try:
        tools = EcommerceTools()
        
        # ✅ Chỉ dùng Tiki
        data = tools.scrape_ecommerce_data(
            platform='tiki',  # Luôn là tiki
            category=state['category'],
            keywords=state['keywords'],
            max_products=state.get('max_products')
        )
        
        state['raw_data'] = data
        state['platform'] = 'tiki'
        logger.info(f"Da cào duoc {len(data)} san pham tu Tiki")
        
    except Exception as e:
        error_msg = f"Loi cào du lieu: {str(e)}"
        state['error'] = error_msg
        logger.error(error_msg)
    
    return state
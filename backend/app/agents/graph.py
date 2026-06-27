# backend/app/agents/graph.py
from langgraph.graph import StateGraph, END
from backend.app.agents.state import AgentState
# Import tất cả các node từ thư mục nodes đã chia nhỏ
from backend.app.agents.nodes import (
    parse_query_node,
    scrape_data_node,
    analyze_data_node,
    generate_report_node
)

def create_market_agent_graph():
    workflow = StateGraph(AgentState)
    
    # Đăng ký các node đã tách file vào Graph
    workflow.add_node("parse_query", parse_query_node)
    workflow.add_node("scrape_data", scrape_data_node)
    workflow.add_node("analyze_data", analyze_data_node)
    workflow.add_node("generate_report", generate_report_node)
    
    # Thiết lập luồng chạy tuần tự từ file này sang file khác
    workflow.set_entry_point("parse_query")
    workflow.add_edge("parse_query", "scrape_data")
    workflow.add_edge("scrape_data", "analyze_data")
    workflow.add_edge("analyze_data", "generate_report")
    workflow.add_edge("generate_report", END)
    
    return workflow.compile()

agent_graph = create_market_agent_graph()
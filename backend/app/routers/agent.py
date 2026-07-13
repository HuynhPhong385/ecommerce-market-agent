# backend/app/routers/agent.py

from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.agents.graph import agent_graph, AgentState
from typing import Optional
from fastapi import Query

router = APIRouter(
    #prefix="/api/v1/agent",  # Định nghĩa tiền tố đường dẫn cho tất cả các endpoint trong file này
    tags=["Market Agent"]    # Gắn nhãn để phân loại rõ ràng trên giao diện tài liệu tự động Swagger UI (/docs)
)

class AnalysisRequest(BaseModel):
    keyword: str # Cho phép keyword trống
@router.get("/")
def agent_home():
    return {"message": "Agent router is active!"}
@router.post("/run-analysis")
async def run_market_analysis(
    request: Optional[AnalysisRequest] = Body(None),
    db: Session = Depends(get_db)
    ):
    # 1. Lấy từ khóa an toàn
    #keyword = request.keyword if request else None
    
    # 2. Kiểm tra lỗi nếu keyword trống
    if request is None or not request.keyword or not request.keyword.strip():
        raise HTTPException(status_code=400, detail="Từ khóa tìm kiếm không được để trống!")
    
    # Lấy keyword sau khi đã kiểm tra
    keyword = request.keyword  # Bây giờ đã an toàn
    
    print(f"\n[API] Bắt đầu kích hoạt luồng Market Agent cho từ khóa: '{keyword}'")
    try: 
        initial_state: AgentState = {
            "keyword": keyword, # Dùng biến keyword
            "product_id_list": [],
            "raw_competitor_data": [],
            "price_analysis": {},
            "optimized_description": {}
        }
        
        final_output = agent_graph.invoke(initial_state) 
        
        print("[API] LangGraph đã hoàn thành toàn bộ chu kỳ xử lý dữ liệu.")
        
        return {
            "status": "success",
            "message": f"Phân tích thành công từ khóa '{keyword}'", # Dùng biến keyword
            "data": {
                "keyword": final_output.get("keyword"),
                "total_products_scraped": len(final_output.get("product_id_list", [])),
                "price_trends": final_output.get("price_analysis"),
                "ai_optimized_content": final_output.get("optimized_description")
            }
        }
        
    except Exception as e:
        print(f"❌ [API ERROR] Luồng xử lý LangGraph gặp sự cố: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
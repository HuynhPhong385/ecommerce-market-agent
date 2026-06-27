# backend/app/agents/nodes/analyze_data.py
# Nhiệm vụ: Đọc ngược lại dữ liệu sạch từ MySQL lên bằng danh sách product_id_list để tính toán các chỉ số phân tích giá (Min, Max, Avg, gợi ý giá cạnh tranh).

import numpy as np
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models import TikiProduct
from backend.app.agents.state import AgentState

def analyze_data_node(state: AgentState) -> dict:
    """Node: Phân tích phân phối giá từ dữ liệu MySQL"""
    product_ids = state["product_id_list"]
    db: Session = SessionLocal()
    
    try:
        # Lấy danh sách sản phẩm vừa cào ra khỏi DB
        products = db.query(TikiProduct).filter(TikiProduct.tiki_id.in_(product_ids)).all()
        
        raw_competitor_data = []
        prices = []
        
        for p in products:
            prices.append(p.price)
            raw_competitor_data.append({
                "name": p.name,
                "price": p.price,
                "brand": p.brand,
                "rating": p.rating,
                "sold_count": p.sold_count
            })
            
        if not prices:
            return {"price_analysis": {"error": "Không tìm thấy dữ liệu giá"}}
            
        analysis = {
            "lowest_price": min(prices),
            "highest_price": max(prices),
            "average_price": int(np.mean(prices)),
            "suggested_price": int(np.mean(prices) * 0.97), # Định giá thấp hơn thị trường 3%
            "total_analyzed": len(prices)
        }
        
        return {
            "raw_competitor_data": raw_competitor_data,
            "price_analysis": analysis
        }
    finally:
        db.close()
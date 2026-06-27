# backend/app/routers/agent.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.agents.graph import agent_graph, AgentState

# 1. Khởi tạo APIRouter để gom nhóm các API liên quan đến Agent lại với nhau
# Sau này ở file main.py chỉ cần include router này vào là xong, giúp code sạch sẽ
router = APIRouter(
    prefix="/api/v1/agent",  # Định nghĩa tiền tố đường dẫn cho tất cả các endpoint trong file này
    tags=["Market Agent"]    # Gắn nhãn để phân loại rõ ràng trên giao diện tài liệu tự động Swagger UI (/docs)
)

# 2. Định nghĩa Schema dữ liệu đầu vào (Request Body) bằng Pydantic
# Giúp FastAPI tự động kiểm tra xem React có gửi đúng cấu trúc dữ liệu lên hay không
class AnalysisRequest(BaseModel):
    keyword: str  # Từ khóa sản phẩm người dùng nhập trên giao diện (ví dụ: "chuột logitech")

# 3. Định nghĩa API Endpoint chính thức để kích hoạt Market Agent
@router.post("/run-analysis")
def run_market_analysis(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    [POST API] Kích hoạt toàn bộ luồng xử lý tự động của LangGraph:
    Làm sạch từ khóa -> Gọi Crawler cào Tiki -> Lưu vào MySQL -> Phân tích giá -> AI viết bài chuẩn SEO.
    """
    
    # Bước 3.1: Kiểm tra tính hợp lệ của từ khóa đầu vào từ Frontend gửi lên
    # Nếu người dùng để trống hoặc chỉ gõ khoảng trắng, trả về lỗi 400 (Bad Request) ngay lập tức
    if not request.keyword or not request.keyword.strip():
        raise HTTPException(
            status_code=400, 
            detail="Từ khóa tìm kiếm không được để trống!"
        )
    
    try:
        print(f"\n[API] Bắt đầu kích hoạt luồng Market Agent cho từ khóa: '{request.keyword}'")
        
        # Bước 3.2: Khởi tạo trạng thái ban đầu (Initial State) cho đồ thị LangGraph
        # Trạng thái này phải khớp với cấu trúc bộ nhớ 'AgentState' mà ta đã định nghĩa bằng TypedDict
        initial_state: AgentState = {
            "keyword": request.keyword,
            "product_id_list": [],      # Node 2 (scrape) sẽ điền danh sách ID vào đây
            "raw_competitor_data": [],  # Node 3 (analyze) sẽ điền dữ liệu thô từ MySQL vào đây
            "price_analysis": {},       # Node 3 (analyze) sẽ điền kết quả tính toán giá vào đây
            "optimized_description": {} # Node 4 (report) sẽ điền bài viết do AI tạo vào đây
        }
        
        # Bước 3.3: Kích hoạt chạy toàn bộ Graph bằng hàm .invoke()
        # Hàm này sẽ block luồng để đợi LangGraph chạy tuần tự qua các file node:
        # parse_query.py -> scrape_data.py -> analyze_data.py -> generate_report.py
        final_output = agent_graph.invoke(initial_state) 
        
        print("🎉 [API] LangGraph đã hoàn thành toàn bộ chu kỳ xử lý dữ liệu.")
        
        # Bước 3.4: Trả cấu trúc JSON kết quả cuối cùng về cho React Frontend hiển thị lên Dashboard
        return {
            "status": "success",
            "message": f"Phân tích thành công từ khóa '{request.keyword}'",
            "data": {
                "keyword": final_output.get("keyword"),
                # Trả về danh sách ID sản phẩm vừa cào và cập nhật trong MySQL
                "total_products_scraped": len(final_output.get("product_id_list", [])),
                # Trả về các chỉ số Min, Max, Avg, Gợi ý giá thu thập được sau khi tính toán dữ liệu DB
                "price_trends": final_output.get("price_analysis"),
                # Trả về tiêu đề và mô tả sản phẩm tối ưu mà AI (Gemini) đã sinh ra
                "ai_optimized_content": final_output.get("optimized_description")
            }
        }
        
    except Exception as e:
        # Bước 3.5: Phòng thủ nếu có bất kỳ lỗi gì xảy ra trong quá trình chạy Graph (mất mạng, lỗi SQL...)
        # In log chi tiết ở backend và trả về lỗi 500 (Internal Server Error) để tránh sập app Frontend
        print(f"❌ [API ERROR] Luồng xử lý LangGraph gặp sự cố nghiêm trọng: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Hệ thống Agent gặp lỗi khi xử lý dữ liệu: {str(e)}"
        )
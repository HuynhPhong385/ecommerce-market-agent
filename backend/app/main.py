# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import agent  # Import router vừa tạo ở trên

# Khởi tạo ứng dụng FastAPI chính
app = FastAPI(
    title="Tiki Market Agent System API",
    description="Hệ thống Backend tự động hóa cào dữ liệu, phân tích giá MySQL và tối ưu nội dung bằng LangGraph",
    version="1.0.0"
)

# CẤU HÌNH CORS (Cross-Origin Resource Sharing)
# Bắt buộc phải có phần này thì React Frontend (thường chạy ở port 5173 hoặc 3000) 
# mới có quyền gọi API xuống FastAPI Backend (chạy ở port 8000) mà không bị trình duyệt chặn.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Cho phép tất cả các nguồn truy cập (Trong môi trường dev)
    allow_credentials=True,
    allow_methods=["*"],      # Cho phép tất cả các phương thức HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],      # Cho phép truyền mọi cấu trúc Headers
)

# Đăng ký (nhúng) router của Agent vào ứng dụng chính
# Giờ đây bạn có thể truy cập API tại đường dẫn: http://localhost:8000/api/v1/agent/run-analysis
app.include_router(agent.router)

# Endpoint kiểm tra trạng thái hoạt động cơ bản của Server (Health Check)
@app.get("/")
def read_root():
    return {"status": "online", "message": "FastAPI MySQL Backend is running smoothly!"}
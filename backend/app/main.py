# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import agent
from backend.app.routers import dashboard

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
    allow_origins=["http://localhost:5173"], # Chỉ cho phép frontend này gọi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký (nhúng) router của Agent vào ứng dụng chính
# http://localhost:8000/api/v1/agent/run-analysis
# Ví dụ trong main.py
app.include_router(agent.router, prefix="/api/v1/agent")
app.include_router(dashboard.router, prefix="/api/v1/dashboard")

# Endpoint kiểm tra trạng thái hoạt động cơ bản của Server (Health Check)
@app.get("/")
def read_root():
    return {"status": "online", "message": "FastAPI MySQL Backend is running smoothly!"}
# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.config import Config

# Khởi tạo Engine kết nối MySQL với cơ chế tự động tối ưu connection pool
engine = create_engine(
    Config.DATABASE_URL, 
    pool_pre_ping=True,  # Kiểm tra kết nối còn sống không trước khi truy vấn
    pool_recycle=3600    # Tự động làm mới kết nối sau 1 giờ để tránh lỗi mất kết nối từ MySQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency dùng cho FastAPI Routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
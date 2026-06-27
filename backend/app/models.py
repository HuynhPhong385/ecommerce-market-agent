# backend/app/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, Date, ForeignKey, create_engine
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
Base = declarative_base()

class TikiProduct(Base):
    __tablename__ = "tiki_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tiki_id = Column(String(50), unique=True, nullable=False, index=True) # ID từ Tiki
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    original_price = Column(Float)
    brand = Column(String(100))
    category = Column(String(100), index=True)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    sold_count = Column(Integer, default=0)
    url = Column(String(500))
    image_url = Column(String(500))
    scraped_at = Column(DateTime, default=datetime.utcnow)
    extra_data = Column(JSON) # Lưu các thông tin mở rộng (sku, seller, discount_rate...)
    history = relationship("PriceHistory", back_populates="product")

class PriceHistory(Base):
    __tablename__ = 'price_history'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('tiki_products.id'), index=True) # Index giúp vẽ biểu đồ cực nhanh
    price = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow) # Nên dùng DateTime thay vì Date để theo dõi biến động giá trong ngày
    product = relationship("Product", back_populates="history")
class DailySummary(Base):
    __tablename__ = 'daily_summary'
    id = Column(Integer, primary_key=True)
    report_date = Column(Date, index=True) # Index theo ngày để truy vấn theo khoảng thời gian (7 ngày, 30 ngày)
    category = Column(String(100), index=True) 
    total_revenue = Column(Float, default=0.0)
    total_products_sold = Column(Integer, default=0)

engine = create_engine('sqlite:///tiki_market_agent.db')
Base.metadata.create_all(engine)
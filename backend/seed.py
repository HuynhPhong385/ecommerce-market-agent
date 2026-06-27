from app.models import engine, TikiProduct, PriceHistory, DailySummary
from sqlalchemy.orm import sessionmaker
import random
from datetime import datetime, timedelta

Session = sessionmaker(bind=engine)
session = Session()

# 1. Tạo dữ liệu mẫu
categories = ['Điện thoại', 'Laptop', 'Bàn phím']
for i in range(10):
    p = TikiProduct(name=f"Sản phẩm {i}", category=random.choice(categories))
    session.add(p)
    session.flush() # Để lấy p.id ngay lập tức

    # 2. Thêm lịch sử giá 30 ngày
    for day in range(30):
        h = PriceHistory(
            product_id=p.id,
            price=random.uniform(1000000, 20000000),
            date=datetime.now() - timedelta(days=day)
        )
        session.add(h)

session.commit()
print(" Đã tạo xong Database và dữ liệu giả!")
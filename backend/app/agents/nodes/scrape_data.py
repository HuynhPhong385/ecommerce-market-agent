# backend/app/agents/nodes/scrape_data.py
# Nhiệm vụ: Gọi trực tiếp Class tiki_crawler cũ của bạn, cào dữ liệu thời gian thực và ghi đè/thêm mới vào cơ sở dữ liệu MySQL.

from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models import TikiProduct
from backend.scrapers.tiki_crawler import TikiCrawler
from backend.app.agents.state import AgentState

def scrape_data_node(state: AgentState) -> dict:
    """Node: Cào dữ liệu từ Tiki dựa trên từ khóa và lưu vào MySQL"""
    keyword = state["keyword"]
    print(f"[Node: Scrape Data] Tiến hành cào dữ liệu Tiki cho: {keyword}")
    
    crawler = TikiCrawler()
    # Chạy hàm scrape cũ của bạn (mặc định lấy keyword làm category hoặc truyền linh hoạt)
    scraped_data = crawler.scrape(category=keyword, keywords=[keyword])
    
    db: Session = SessionLocal()
    product_ids = []
    
    try:
        for item in scraped_data:
            product_ids.append(item['id'])
            # Kiểm tra trùng trong DB
            existing_product = db.query(TikiProduct).filter(TikiProduct.tiki_id == item['id']).first()
            
            if existing_product:
                existing_product.price = item['price']
                existing_product.sold_count = item['sold_count']
                existing_product.reviews_count = item['reviews_count']
                existing_product.rating = item['rating']
                existing_product.extra_data = item['extra']
            else:
                new_product = TikiProduct(
                    tiki_id=item['id'],
                    name=item['name'],
                    price=item['price'],
                    original_price=item['original_price'],
                    brand=item['brand'],
                    category=item['category'],
                    rating=item['rating'],
                    reviews_count=item['reviews_count'],
                    sold_count=item['sold_count'],
                    url=item['url'],
                    image_url=item['image_url'],
                    extra_data=item['extra']
                )
                db.add(new_product)
        db.commit()
        
        return {"product_id_list": product_ids}
    except Exception as e:
        db.rollback()
        print(f"[Node: Scrape Data] Gặp lỗi lưu DB: {str(e)}")
        raise e
    finally:
        db.close()
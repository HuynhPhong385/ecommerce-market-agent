# tasks/sync_dashboard.py
from backend.scrapers.tiki_crawler import TikiCrawler
from backend.app.database import SessionLocal
from backend.app.models import DailySummary
from datetime import date
import unicodedata
# def remove_accents(input_str):
#     if not input_str:
#         return ""
#     # Chuyển đổi sang Unicode dạng phân tách, loại bỏ dấu và chuyển lại thành string
#     s = unicodedata.normalize('NFD', input_str)
#     s = ''.join([c for c in s if not unicodedata.combining(c)])
#     return s
def sync_dashboard_data():
    crawler = TikiCrawler()
    db = SessionLocal()
    categories = ["Dien tu", "Do gia dung", "Do choi", "Thoi trang", "My pham"]

    for cat in categories:
        # 1. Cào dữ liệu cho danh mục đó
        data = crawler.scrape(category=cat, keywords=[cat]) 

        # 2. Tính tổng doanh thu/số lượng (Tổng hợp trước khi lưu)
        print(f"DEBUG - Dữ liệu thô của {cat}: {data[:2]}") 
        total_revenue = sum([p.get('price', 0) * p.get('sold_count', 0) for p in data])

        # Đồng thời sửa luôn việc gán giá trị cho DB ở dòng 22 (nếu cần)
        new_entry = DailySummary(
            report_date=date.today(),
            category=cat,
            total_revenue=total_revenue,
            total_products_sold=sum([p.get('sold_count', 0) for p in data]) # Đừng quên thêm cột này!
        )
        db.add(new_entry)

    db.commit()
    db.close()

if __name__ == "__main__":
    print("Bắt đầu quá trình đồng bộ dữ liệu Dashboard...")
    sync_dashboard_data()
    print("Đã hoàn tất!")
from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from backend.app.database import get_db, SessionLocal
from backend.app.models import TikiProduct, PriceHistory, DailySummary
from backend.scrapers.tiki_crawler import TikiCrawler
from sqlalchemy import func, and_
from datetime import datetime, timedelta, date

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    today = date.today()
    this_week_start = today - timedelta(days=7)
    last_week_start = today - timedelta(days=14)

    # Helper tính tăng trưởng an toàn
    def get_growth(curr, prev):
        if prev == 0: return 0.0
        return round(((curr - prev) / prev) * 100, 1)

    # Tính toán doanh thu (ví dụ)
    rev_now = db.query(func.sum(DailySummary.total_revenue)).filter(DailySummary.report_date >= this_week_start).scalar() or 0
    rev_prev = db.query(func.sum(DailySummary.total_revenue)).filter(DailySummary.report_date >= last_week_start, DailySummary.report_date < this_week_start).scalar() or 0

    return {
        "revenue": {"value": round(rev_now), "growth": get_growth(rev_now, rev_prev)},
        "totalProducts": {"value": db.query(TikiProduct).count(), "growth": 0.0},
        "totalShops": {"value": 1250, "growth": 0.0},
        "reviewAvg": {"value": 4.8, "growth": 0.0}
    }
today = date.today()

@router.get("/chart-data")
def get_chart_data(db: Session = Depends(get_db)):
    # 1. Định nghĩa mốc thời gian
    today = datetime.now().date() 
    yesterday = today - timedelta(days=1)
    seven_days_ago = today - timedelta(days=7)
    
    # 2. Truy vấn dữ liệu trong khoảng 7 ngày (không tính hôm nay)
    # Lấy từ 05/07 đến 11/07
    rows = db.query(DailySummary).filter(
        and_(
            DailySummary.report_date >= seven_days_ago,
            DailySummary.report_date <= yesterday
        )
    ).all()
    
    # 3. Chuyển đổi dữ liệu sang định dạng: 
    # [{"date": "2026-07-11", "Dien tu": 100, "Do gia dung": 200, ...}, ...]
    data_dict = {}
    
    for row in rows:
        date_str = str(row.report_date)
        if date_str not in data_dict:
            data_dict[date_str] = {"date": date_str}
        
        # Gán doanh thu vào đúng danh mục
        data_dict[date_str][row.category] = row.total_revenue
        
    # Chuyển từ dictionary sang list
    chart_data = list(data_dict.values())
    
    # Sắp xếp lại theo ngày tăng dần
    chart_data.sort(key=lambda x: x["date"])
    
    return chart_data
@router.post("/crawl")
async def trigger_crawling(payload: dict, background_tasks: BackgroundTasks):
    keyword = payload.get("keyword")
    
    # Khởi tạo class crawler
    crawler = TikiCrawler()
    
    # Chạy ngầm phương thức run của class
    background_tasks.add_task(crawler.run, keyword)
    
    return {"status": "success", "message": f"Crawler đã nhận lệnh cho: {keyword}"}
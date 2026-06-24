# src/core/tools.py

import json
import logging
from datetime import datetime
from typing import List, Dict, Optional

from src.core.config import Config
from src.core.llm import generate_text
from src.crawler.tiki_crawler import TikiCrawler
#from src.crawler.fptshop_crawler import FPTShopCrawler
from src.crawler.shopee_crawler import ShopeeCrawler
#from src.crawler.sendo_crawler import SendoCrawler
from src.utils.file_utils import FileUtils

logger = logging.getLogger(__name__)

class EcommerceTools:
    """Công cụ cho AI Agent - Hỗ trợ nhiều sàn"""
    
    def __init__(self):
        Config.ensure_directories()
        
        # Đăng ký các crawler
        self.crawlers = {
            'tiki': TikiCrawler(),
            #'fptshop': FPTShopCrawler(),
            #'sendo': SendoCrawler(),
            #'shopee': ShopeeCrawler(),  # Thêm sau
            # 'lazada': LazadaCrawler(),  # Thêm sau
        }
        
        self.file_utils = FileUtils()
        logger.info("Khoi tao EcommerceTools thanh cong")
    
    def get_supported_platforms(self) -> List[str]:
        """Lấy danh sách sàn hỗ trợ"""
        return list(self.crawlers.keys())
    
    def scrape_ecommerce_data(
        self,
        platform: str,
        category: str,
        keywords: List[str],
        max_products: Optional[int] = None
    ) -> List[Dict]:
        """Cào dữ liệu từ sàn TMĐT"""
        platform = platform.lower()
        
        if platform not in self.crawlers:
            raise ValueError(f"San {platform} chua duoc ho tro. Ho tro: {self.get_supported_platforms()}")
        
        logger.info(f"Bat dau crawl {platform} - Category: {category}")
        
        crawler = self.crawlers[platform]
        data = crawler.scrape(
            category=category,
            keywords=keywords,
            max_products=max_products
        )
        
        # Lưu dữ liệu
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{platform}_{category}_{timestamp}.json"
        filepath = Config.RAW_DATA_DIR / filename
        self.file_utils.save_json(filepath, data)
        
        logger.info(f"Da luu {len(data)} san pham vao {filepath}")
        return data
    
    def analyze_trends(self, data: List[Dict]) -> Dict:
        """Phân tích xu hướng"""
        logger.info("Dang phan tich du lieu...")
        
        if not data:
            return self._empty_analysis()
        
        # Tính toán
        total = len(data)
        prices = [p.get('price', 0) for p in data if p.get('price', 0) > 0]
        
        # Phân phối giá
        price_ranges = {
            'under_100k': 0,
            '100k_200k': 0,
            '200k_500k': 0,
            '500k_1m': 0,
            'above_1m': 0
        }
        
        brands = {}
        ratings = []
        
        for product in data:
            price = product.get('price', 0)
            if price < 100000:
                price_ranges['under_100k'] += 1
            elif price < 200000:
                price_ranges['100k_200k'] += 1
            elif price < 500000:
                price_ranges['200k_500k'] += 1
            elif price < 1000000:
                price_ranges['500k_1m'] += 1
            else:
                price_ranges['above_1m'] += 1
            
            brand = product.get('brand', 'Khác')
            brands[brand] = brands.get(brand, 0) + 1
            
            rating = product.get('rating', 0)
            if rating:
                ratings.append(float(rating))
        
        # Top brands
        top_brands = dict(sorted(brands.items(), key=lambda x: x[1], reverse=True)[:10])
        
        # Rating
        rating_analysis = {
            'average': sum(ratings) / len(ratings) if ratings else 0,
            'total': len(ratings),
            'max': max(ratings) if ratings else 0,
            'min': min(ratings) if ratings else 0
        }
        
        return {
            'total_products': total,
            'average_price': sum(prices) / len(prices) if prices else 0,
            'price_range': {
                'min': min(prices) if prices else 0,
                'max': max(prices) if prices else 0,
            },
            'price_distribution': price_ranges,
            'top_brands': top_brands,
            'rating_analysis': rating_analysis,
            'sample_products': data[:10],
            'analysis_time': datetime.now().isoformat()
        }
    
    def generate_report(self, analysis: Dict, query: str) -> str:
        """Tạo báo cáo bằng Gemini"""
        logger.info("Dang tao bao cao...")
        
        try:
            # Chuẩn bị dữ liệu
            analysis_json = json.dumps(analysis, ensure_ascii=False, indent=2)
            if len(analysis_json) > 8000:
                summary = {
                    'total_products': analysis.get('total_products'),
                    'average_price': analysis.get('average_price'),
                    'top_brands': analysis.get('top_brands'),
                    'price_distribution': analysis.get('price_distribution'),
                }
                analysis_json = json.dumps(summary, ensure_ascii=False, indent=2)
            
            system_prompt = """Bạn là chuyên gia phân tích thị trường thương mại điện tử.

Hãy phân tích dữ liệu và tạo báo cáo chi tiết với các phần sau:

1. TỔNG QUAN THỊ TRƯỜNG
   - Quy mô thị trường
   - Xu hướng chung

2. PHÂN TÍCH GIÁ CẢ
   - Mức giá trung bình
   - Phân phối giá
   - So sánh các phân khúc

3. THƯƠNG HIỆU NỔI BẬT
   - Top thương hiệu
   - Thị phần

4. ĐÁNH GIÁ KHÁCH HÀNG
   - Điểm trung bình
   - Nhận xét chung

5. CƠ HỘI VÀ THÁCH THỨC
   - Cơ hội cho người bán mới
   - Thách thức cạnh tranh

6. KHUYẾN NGHỊ
   - Chiến lược giá
   - Chiến lược sản phẩm

Sử dụng tiếng Việt, trình bày rõ ràng, có cấu trúc.
Nếu dữ liệu ít, hãy tập trung phân tích những gì có sẵn."""

            prompt = f"""Câu hỏi: {query}

Dữ liệu phân tích:
{analysis_json}

Hãy tạo báo cáo chi tiết."""

            report = generate_text(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=4000  # Tăng lên 4000
            )
            
            # Lưu báo cáo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.md"
            filepath = Config.REPORTS_DIR / filename
            
            full_report = f"""# Bao cao phan tich thi truong

**Ngay tao:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
**Cau hoi:** {query}
**AI:** Google Gemini

---
{report}

---
*Bao cao duoc tao boi Ecommerce Market Intelligence Agent*
"""
            self.file_utils.save_text(filepath, full_report)
            
            return report
            
        except Exception as e:
            logger.error(f"Loi tao bao cao: {str(e)}")
            return self._fallback_report(analysis, query)
    
    def _empty_analysis(self) -> Dict:
        """Phân tích rỗng"""
        return {
            'total_products': 0,
            'average_price': 0,
            'price_range': {'min': 0, 'max': 0},
            'price_distribution': {},
            'top_brands': {},
            'rating_analysis': {},
            'sample_products': [],
            'analysis_time': datetime.now().isoformat()
        }
    
    def _fallback_report(self, analysis: Dict, query: str) -> str:
        """Báo cáo fallback"""
        total = analysis.get('total_products', 0)
        
        report = f"""
# Bao cao phan tich thi truong

**Cau hoi:** {query}

## Thong ke co ban
- Tong san pham: {total}
- Gia trung binh: {analysis.get('average_price', 0):,.0f} VND

## Thuong hieu
"""
        for brand, count in list(analysis.get('top_brands', {}).items())[:10]:
            report += f"- {brand}: {count} san pham\n"
        
        return report
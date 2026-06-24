# src/crawler/fptshop_crawler.py

import time
import logging
import requests
from typing import List, Dict, Optional
from datetime import datetime

from src.crawler.base_crawler import BaseCrawler
from src.core.config import Config

logger = logging.getLogger(__name__)

class (BaseCrawler):
    """Crawler cho FPT Shop - Rất dễ vì có API đơn giản"""
    
    def __init__(self):
        super().__init__()
        self.platform_name = 'fptshop'
        self.base_url = "https://fptshop.com.vn"
        self.api_url = "https://fptshop.com.vn/api/v1"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Referer': 'https://fptshop.com.vn/',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        logger.info("Khoi tao FPT Shop Crawler thanh cong")
    
    def scrape(
        self,
        category: str,
        keywords: List[str],
        max_products: Optional[int] = None
    ) -> List[Dict]:
        """Cào dữ liệu từ FPT Shop"""
        self.category_name = category
        max_items = max_products or Config.MAX_PRODUCTS
        
        logger.info(f"Bat dau crawl FPT Shop - Category: {category}")
        
        all_products = []
        
        try:
            # FPT Shop có API category tốt
            category_id = self._get_category_id(category)
            if category_id:
                products = self._get_products_by_category(category_id, max_items)
                if products:
                    all_products.extend(products)
            
            # Nếu không có, thử tìm kiếm
            if not all_products:
                for keyword in keywords[:2]:
                    if len(all_products) >= max_items:
                        break
                    products = self._search_products(keyword, max_items - len(all_products))
                    if products:
                        all_products.extend(products)
                    time.sleep(1)
            
            # Chuẩn hóa
            standardized = []
            seen_ids = set()
            
            for product in all_products[:max_items]:
                product_id = product.get('id')
                if product_id and str(product_id) not in seen_ids:
                    std = self.standardize_product(product)
                    if not std.get('category'):
                        std['category'] = category
                    standardized.append(std)
                    seen_ids.add(str(product_id))
            
            logger.info(f"Da crawl {len(standardized)} san pham tu FPT Shop")
            
            if not standardized:
                return self.get_sample_data(category, max_items)
            
            return standardized
            
        except Exception as e:
            logger.error(f"Loi crawl FPT Shop: {str(e)}")
            return self.get_sample_data(category, max_items)
    
    def _get_category_id(self, category_name: str) -> Optional[str]:
        """Lấy category ID từ tên"""
        category_mapping = {
            'dien thoai': '241',
            'laptop': '242',
            'tablet': '243',
            'phu kien': '244',
            'dong ho': '245',
            'tai nghe': '246',
            'samsung': '247',
            'apple': '248',
            'xiaomi': '249',
            'oppo': '250',
        }
        
        for key, cat_id in category_mapping.items():
            if key in category_name.lower():
                return cat_id
        return None
    
    def _get_products_by_category(self, category_id: str, limit: int) -> List[Dict]:
        """Lấy sản phẩm theo category"""
        try:
            url = f"{self.api_url}/products"
            params = {
                'category_id': category_id,
                'limit': limit,
                'page': 1,
                'sort': 'sold_desc',
            }
            
            response = self.session.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'data' in data:
                    return data['data']
                if data and 'products' in data:
                    return data['products']
            return []
            
        except Exception as e:
            logger.error(f"Loi lay san pham theo category: {str(e)}")
            return []
    
    def _search_products(self, keyword: str, limit: int) -> List[Dict]:
        """Tìm kiếm sản phẩm"""
        try:
            url = f"{self.api_url}/search"
            params = {
                'q': keyword,
                'limit': limit,
                'page': 1,
            }
            
            response = self.session.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'data' in data:
                    return data['data']
                if data and 'products' in data:
                    return data['products']
            return []
            
        except Exception as e:
            logger.error(f"Loi tim kiem: {str(e)}")
            return []
    
    def standardize_product(self, product: Dict) -> Dict:
        """Chuẩn hóa sản phẩm FPT Shop"""
        price = product.get('price', product.get('sale_price', 0))
        original_price = product.get('original_price', product.get('price', price))
        
        return {
            'id': str(product.get('id', '')),
            'name': product.get('name', product.get('title', '')),
            'price': self._parse_price(price),
            'original_price': self._parse_price(original_price),
            'brand': product.get('brand', product.get('brand_name', 'Khác')),
            'category': product.get('category', self.category_name),
            'rating': self._parse_rating(product.get('rating', product.get('rating_average', 0))),
            'reviews_count': self._parse_int(product.get('reviews_count', product.get('review_count', 0))),
            'sold_count': self._parse_int(product.get('sold_count', product.get('quantity_sold', 0))),
            'url': product.get('url', ''),
            'image_url': product.get('image_url', product.get('thumbnail', '')),
            'platform': self.platform_name,
            'scraped_at': datetime.now().isoformat(),
            'extra': {
                'seller': 'FPT Shop',
                'in_stock': product.get('in_stock', True),
                'discount': product.get('discount_percent', 0),
            }
        }
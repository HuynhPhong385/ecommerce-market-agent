# src/crawler/shopee_crawler.py

import time
import logging
import requests
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urlencode
import json
import re

from src.crawler.base_crawler import BaseCrawler
from src.core.config import Config

logger = logging.getLogger(__name__)

class ShopeeCrawler(BaseCrawler):
    """Crawler cho Shopee.vn"""
    
    def __init__(self):
        super().__init__()
        self.platform_name = 'shopee'
        self.base_url = "https://shopee.vn"
        self.api_url = "https://shopee.vn/api/v4"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://shopee.vn/',
            'Origin': 'https://shopee.vn',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Cookies cần thiết
        self.session.cookies.set('SPC_F', '123456')
        self.session.cookies.set('SPC_CD', 'shopee.vn')
        
        logger.info("Khoi tao Shopee Crawler thanh cong")
    
    def scrape(
        self,
        category: str,
        keywords: List[str],
        max_products: Optional[int] = None
    ) -> List[Dict]:
        """Cào dữ liệu từ Shopee"""
        self.category_name = category
        max_items = max_products or Config.MAX_PRODUCTS
        
        logger.info(f"Bat dau crawl Shopee - Category: {category}, Keywords: {keywords}")
        
        all_products = []
        
        try:
            for keyword in keywords[:3]:
                if len(all_products) >= max_items:
                    break
                
                products = self._search_products(
                    keyword=keyword,
                    limit=min(max_items - len(all_products), 30)
                )
                
                if products:
                    all_products.extend(products)
                    logger.info(f"Tim thay {len(products)} san pham cho '{keyword}'")
                else:
                    # Thử search không dấu
                    keyword_no_accent = self._remove_accent(keyword)
                    if keyword_no_accent != keyword:
                        products = self._search_products(keyword_no_accent, limit=20)
                        if products:
                            all_products.extend(products)
                            logger.info(f"Tim thay {len(products)} san pham cho '{keyword_no_accent}'")
                
                time.sleep(1.5)
            
            # Chuẩn hóa
            standardized = []
            seen_ids = set()
            
            for product in all_products[:max_items]:
                product_id = product.get('itemid') or product.get('id')
                if product_id and str(product_id) not in seen_ids:
                    std = self.standardize_product(product)
                    if not std.get('category'):
                        std['category'] = category
                    standardized.append(std)
                    seen_ids.add(str(product_id))
            
            logger.info(f"Da crawl {len(standardized)} san pham tu Shopee")
            
            if not standardized:
                return self.get_sample_data(category, max_items)
            
            return standardized
            
        except Exception as e:
            logger.error(f"Loi crawl Shopee: {str(e)}")
            return self.get_sample_data(category, max_items)
    
    def _search_products(self, keyword: str, limit: int = 30) -> List[Dict]:
        """Tìm kiếm sản phẩm trên Shopee"""
        try:
            # Endpoint search của Shopee
            search_url = f"{self.api_url}/search/search_items"
            
            params = {
                'keyword': keyword,
                'limit': limit,
                'page': 0,
                'sort_by': 'sales',  # Bán chạy
                'order': 'desc',
                'version': '2',
            }
            
            response = self.session.get(search_url, params=params, timeout=Config.REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'items' in data:
                    items = data['items']
                    products = []
                    for item in items:
                        if 'item_basic' in item:
                            product = item['item_basic']
                            # Thêm shop info
                            if 'shop_info' in item:
                                product['shop_info'] = item['shop_info']
                            products.append(product)
                    return products
                elif data and 'data' in data and 'items' in data['data']:
                    return data['data']['items']
            
            return []
            
        except Exception as e:
            logger.error(f"Loi tim kiem Shopee: {str(e)}")
            return []
    
    def _remove_accent(self, text: str) -> str:
        """Bỏ dấu tiếng Việt"""
        import unicodedata
        text = unicodedata.normalize('NFKD', text)
        text = ''.join([c for c in text if not unicodedata.combining(c)])
        return text
    
    def standardize_product(self, product: Dict) -> Dict:
        """Chuẩn hóa sản phẩm Shopee"""
        # Lấy ID
        product_id = str(product.get('itemid', product.get('id', '')))
        
        # Lấy tên
        name = product.get('name', product.get('title', ''))
        
        # Lấy giá
        price = product.get('price', 0)
        if price and isinstance(price, int):
            price = price / 100000  # Shopee lưu giá * 100000
        else:
            price = self._parse_price(price)
        
        # Lấy giá gốc
        original_price = product.get('price_before_discount', 0)
        if original_price and isinstance(original_price, int):
            original_price = original_price / 100000
        
        # Lấy thương hiệu
        brand = product.get('brand', '')
        if not brand:
            brand = product.get('shop_info', {}).get('shop_name', 'Khác')
        
        # Lấy rating
        rating = product.get('item_rating', {}).get('rating_star', 0)
        if isinstance(rating, (int, float)):
            rating = float(rating)
        else:
            rating = self._parse_rating(rating)
        
        # Lấy số lượng đánh giá
        review_count = product.get('item_rating', {}).get('rating_count', [0])
        if isinstance(review_count, list):
            review_count = sum(review_count) if review_count else 0
        else:
            review_count = self._parse_int(review_count)
        
        # Lấy số lượng bán
        sold_count = product.get('sold', 0)
        if isinstance(sold_count, int):
            sold_count = sold_count
        else:
            sold_count = self._parse_int(sold_count)
        
        # Lấy URL
        url = f"{self.base_url}/{product.get('shop_info', {}).get('shop_id', '')}/{product_id}"
        
        # Lấy hình ảnh
        image_url = product.get('image', '')
        if image_url:
            image_url = f"https://cf.shopee.vn/file/{image_url}"
        
        return {
            'id': product_id,
            'name': name,
            'price': int(price),
            'original_price': int(original_price) if original_price else int(price),
            'brand': brand if brand and brand != 'Khác' else 'Khác',
            'category': product.get('category', self.category_name),
            'rating': round(rating, 1),
            'reviews_count': review_count,
            'sold_count': sold_count,
            'url': url,
            'image_url': image_url,
            'platform': self.platform_name,
            'scraped_at': datetime.now().isoformat(),
            'extra': {
                'seller': product.get('shop_info', {}).get('shop_name', ''),
                'in_stock': product.get('stock', 0) > 0 if 'stock' in product else True,
                'discount': product.get('discount', 0),
            }
        }
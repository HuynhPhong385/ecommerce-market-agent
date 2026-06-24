# src/crawler/tiki_crawler.py

import json
import time
import logging
import requests
from typing import List, Dict, Optional, Any
from datetime import datetime
from urllib.parse import urlencode

from src.crawler.base_crawler import BaseCrawler
from src.core.config import Config

logger = logging.getLogger(__name__)

class TikiCrawler(BaseCrawler):
    """Crawler cho Tiki.vn - Hoàn chỉnh"""
    
    def __init__(self):
        super().__init__()
        self.platform_name = 'tiki'
        self.base_url = "https://tiki.vn"
        self.api_url = "https://tiki.vn/api/v2"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Referer': 'https://tiki.vn/',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Cache
        self.category_cache = {}
        self.category_id = None
        
        logger.info("Khoi tao Tiki Crawler thanh cong")
    
    def scrape(
        self,
        category: str,
        keywords: List[str],
        max_products: Optional[int] = None
    ) -> List[Dict]:
        """Cào dữ liệu từ Tiki"""
        self.category_name = category
        max_items = max_products or Config.MAX_PRODUCTS
        
        logger.info(f"Bat dau crawl Tiki - Category: {category}, Keywords: {keywords}")
        
        all_products = []
        
        try:
            # Tìm category ID
            self.category_id = self._get_category_id(category)
            if self.category_id:
                logger.info(f"Tim thay category ID: {self.category_id}")
            
            # Lấy sản phẩm theo từ khóa
            for keyword in keywords[:3]:
                if len(all_products) >= max_items:
                    break
                
                products = self._search_products(
                    keyword=keyword,
                    limit=min(max_items - len(all_products), 50)
                )
                
                if products:
                    all_products.extend(products)
                    logger.info(f"Tim thay {len(products)} san pham cho '{keyword}'")
                else:
                    # Fallback: lấy theo category
                    products = self._get_products_by_category(
                        limit=min(max_items - len(all_products), 50)
                    )
                    if products:
                        all_products.extend(products)
                
                time.sleep(1)  # Tránh bị chặn
            
            # Chuẩn hóa và loại bỏ trùng
            standardized = []
            seen_ids = set()
            
            for product in all_products[:max_items]:
                product_id = product.get('id')
                if product_id and product_id not in seen_ids:
                    std = self.standardize_product(product)
                    # Thêm category nếu bị trống
                    if not std.get('category'):
                        std['category'] = category
                    standardized.append(std)
                    seen_ids.add(product_id)
            
            logger.info(f"Da crawl {len(standardized)} san pham tu Tiki")
            return standardized
            
        except Exception as e:
            logger.error(f"Loi crawl Tiki: {str(e)}")
            return self.get_sample_data(category, max_items)
    
    def _search_products(self, keyword: str, limit: int = 50) -> List[Dict]:
        """Tìm kiếm sản phẩm theo từ khóa"""
        try:
            params = {
                'q': keyword,
                'limit': limit,
                'page': 1,
                'sort': 'top_seller',
            }
            
            response = self._make_request('/products', params)
            
            if response and 'data' in response:
                return response['data']
            return []
            
        except Exception as e:
            logger.error(f"Loi tim kiem '{keyword}': {str(e)}")
            return []
    
    def _get_products_by_category(self, limit: int = 50) -> List[Dict]:
        """Lấy sản phẩm theo category"""
        if not self.category_id:
            return []
        
        try:
            params = {
                'category': self.category_id,
                'limit': limit,
                'page': 1,
                'sort': 'top_seller',
            }
            
            response = self._make_request('/products', params)
            
            if response and 'data' in response:
                return response['data']
            return []
            
        except Exception as e:
            logger.error(f"Loi lay san pham theo category: {str(e)}")
            return []
    
    def _get_category_id(self, category_name: str) -> Optional[str]:
        """Lấy ID của category"""
        # Kiểm tra cache
        if category_name in self.category_cache:
            return self.category_cache[category_name]
        
        try:
            response = self._make_request('/categories')
            
            if response:
                categories = response if isinstance(response, list) else response.get('data', [])
                
                # Tìm category
                for cat in categories:
                    # Tên chính xác
                    if cat.get('name', '').lower() == category_name.lower():
                        cat_id = str(cat.get('id'))
                        self.category_cache[category_name] = cat_id
                        return cat_id
                    
                    # Tìm trong children
                    if 'children' in cat:
                        for child in cat['children']:
                            if child.get('name', '').lower() == category_name.lower():
                                cat_id = str(child.get('id'))
                                self.category_cache[category_name] = cat_id
                                return cat_id
                
                # Tìm category chứa từ khóa
                for cat in categories:
                    if category_name.lower() in cat.get('name', '').lower():
                        cat_id = str(cat.get('id'))
                        self.category_cache[category_name] = cat_id
                        return cat_id
            
            return None
            
        except Exception as e:
            logger.error(f"Loi lay category ID: {str(e)}")
            return None
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Thực hiện request tới Tiki API"""
        url = f"{self.api_url}{endpoint}"
        
        try:
            if params:
                url = f"{url}?{urlencode(params)}"
            
            response = self.session.get(url, timeout=Config.REQUEST_TIMEOUT)
            
            # ✅ SỬA: Chấp nhận cả status 200 và 400 (vẫn có data)
            if response.status_code in [200, 400]:
                try:
                    data = response.json()
                    # Nếu có error nhưng vẫn có data thì lấy data
                    if 'error' in data and 'data' in data:
                        return {'data': data['data']}
                    return data
                except:
                    return None
            elif response.status_code == 429:
                logger.warning("Bi gioi han rate, cho 5s...")
                time.sleep(5)
                return self._make_request(endpoint, params)
            else:
                logger.warning(f"Status {response.status_code}: {response.text[:100]}")
                return None
                
        except Exception as e:
            logger.error(f"Loi request: {str(e)}")
            return None
    
    def standardize_product(self, product: Dict) -> Dict:
        """Chuẩn hóa sản phẩm Tiki"""
        # Lấy category từ nhiều nguồn
        category = ''
        if isinstance(product.get('category'), dict):
            category = product.get('category', {}).get('name', '')
        if not category:
            category = product.get('primary_category', {}).get('name', '')
        if not category:
            category = self.category_name
        
        # Lấy brand
        brand = product.get('brand_name', '')
        if not brand:
            brand = product.get('brand', {})
            if isinstance(brand, dict):
                brand = brand.get('name', '')
        if not brand:
            brand = 'Khác'
        
        # Lấy URL
        url = product.get('url', '')
        if url and not url.startswith('http'):
            url = f"{self.base_url}{url}"
        
        # Lấy hình ảnh
        image_url = product.get('thumbnail_url', '')
        if not image_url:
            image_url = product.get('image', {}).get('large_url', '')
        
        return {
            'id': str(product.get('id', '')),
            'name': product.get('name', ''),
            'price': self._parse_price(product.get('price', 0)),
            'original_price': self._parse_price(product.get('original_price', 0)),
            'brand': brand,
            'category': category,
            'rating': self._parse_rating(product.get('rating_average', 0)),
            'reviews_count': self._parse_int(product.get('review_count', 0)),
            'sold_count': self._parse_int(product.get('quantity_sold', {}).get('value', 0)),
            'url': url,
            'image_url': image_url,
            'platform': self.platform_name,
            'scraped_at': datetime.now().isoformat(),
            'extra': {
                'sku': product.get('sku', ''),
                'discount_rate': product.get('discount_rate', 0),
                'is_authentic': product.get('is_authentic', False),
                'seller': product.get('seller', {}).get('name', '') if isinstance(product.get('seller'), dict) else '',
                'inventory_status': product.get('inventory_status', {}),
                'short_description': product.get('short_description', ''),
            }
        }
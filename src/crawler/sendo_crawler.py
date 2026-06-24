# src/crawler/sendo_crawler.py - Hoàn chỉnh

import time
import logging
import requests
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urlencode
import json

from src.crawler.base_crawler import BaseCrawler
from src.core.config import Config

logger = logging.getLogger(__name__)

class SendoCrawler(BaseCrawler):
    """Crawler cho Sen Đỏ (sendo.vn)"""
    
    def __init__(self):
        super().__init__()
        self.platform_name = 'sendo'
        self.base_url = "https://www.sendo.vn"
        
        # Headers giả lập trình duyệt đầy đủ
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.sendo.vn/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Upgrade-Insecure-Requests': '1',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Thêm cookie để giả lập người dùng
        self.session.cookies.set('_gcl_au', '1.1.123456789.123456789')
        self.session.cookies.set('_ga', 'GA1.2.123456789.123456789')
        
        logger.info("Khoi tao Sendo Crawler thanh cong")
    
    def scrape(
        self,
        category: str,
        keywords: List[str],
        max_products: Optional[int] = None
    ) -> List[Dict]:
        """Cào dữ liệu từ Sen Đỏ"""
        self.category_name = category
        max_items = max_products or Config.MAX_PRODUCTS
        
        logger.info(f"Bat dau crawl Sen Do - Category: {category}, Keywords: {keywords}")
        
        all_products = []
        
        try:
            # Sử dụng từ khóa để tìm kiếm
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
                    # Thử tìm kiếm với từ khóa khác
                    logger.info(f"Khong tim thay san pham cho '{keyword}', thu cach khac...")
                
                time.sleep(2)  # Delay để tránh bị chặn
            
            # Nếu không có sản phẩm, thử crawl trực tiếp từ category
            if not all_products:
                logger.info("Thu crawl truc tiep tu danh muc...")
                products = self._get_products_from_category(category, max_items)
                if products:
                    all_products.extend(products)
            
            # Chuẩn hóa
            standardized = []
            seen_ids = set()
            
            for product in all_products[:max_items]:
                product_id = product.get('id') or product.get('product_id')
                if product_id and str(product_id) not in seen_ids:
                    std = self.standardize_product(product)
                    if not std.get('category'):
                        std['category'] = category
                    standardized.append(std)
                    seen_ids.add(str(product_id))
            
            logger.info(f"Da crawl {len(standardized)} san pham tu Sen Do")
            
            # Nếu không có dữ liệu, trả về mẫu
            if not standardized:
                logger.warning("Khong co du lieu tu Sen Do, tra ve du lieu mau")
                return self.get_sample_data(category, max_items)
            
            return standardized
            
        except Exception as e:
            logger.error(f"Loi crawl Sen Do: {str(e)}")
            return self.get_sample_data(category, max_items)
    
    def _search_products(self, keyword: str, limit: int = 30) -> List[Dict]:
        """Tìm kiếm sản phẩm trên Sen Đỏ"""
        try:
            # Sen Đỏ sử dụng API search khác
            # Thử endpoint chính thức
            search_url = f"{self.base_url}/api/v2/search"
            
            params = {
                'q': keyword,
                'limit': limit,
                'page': 1,
                'sortType': 'selling'  # Bán chạy
            }
            
            # Thử với headers khác
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Referer': f'{self.base_url}/tim-kiem?q={keyword}',
                'X-Requested-With': 'XMLHttpRequest',
            }
            
            response = self.session.get(
                search_url,
                params=params,
                headers=headers,
                timeout=Config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data and 'data' in data:
                        products = data['data']
                        if isinstance(products, list):
                            return products
                        elif isinstance(products, dict) and 'items' in products:
                            return products['items']
                except:
                    # Nếu không parse được JSON, thử parse HTML
                    return self._parse_html_products(response.text)
            
            # Thử endpoint khác
            return self._search_products_v2(keyword, limit)
            
        except Exception as e:
            logger.error(f"Loi tim kiem Sen Do: {str(e)}")
            return []
    
    def _search_products_v2(self, keyword: str, limit: int = 30) -> List[Dict]:
        """Tìm kiếm sản phẩm với endpoint khác"""
        try:
            # Endpoint dự phòng
            search_url = f"{self.base_url}/api/product/search"
            
            params = {
                'keyword': keyword,
                'limit': limit,
                'page': 1
            }
            
            response = self.session.get(search_url, params=params, timeout=Config.REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data and 'products' in data:
                        return data['products']
                    if data and 'data' in data:
                        return data['data']
                except:
                    pass
            
            return []
            
        except Exception as e:
            logger.error(f"Loi search v2: {str(e)}")
            return []
    
    def _parse_html_products(self, html: str) -> List[Dict]:
        """Parse sản phẩm từ HTML (fallback)"""
        products = []
        
        try:
            # Tìm các item product trong HTML
            import re
            
            # Tìm pattern sản phẩm
            pattern = r'data-product-id="([^"]+)".*?data-product-name="([^"]+)".*?data-price="([^"]+)"'
            matches = re.findall(pattern, html, re.DOTALL)
            
            for match in matches:
                product = {
                    'id': match[0],
                    'name': match[1],
                    'price': match[2],
                    'brand': 'Khác',
                }
                products.append(product)
            
            logger.info(f"Parsed {len(products)} products from HTML")
            
        except Exception as e:
            logger.error(f"Loi parse HTML: {str(e)}")
        
        return products
    
    def _get_products_from_category(self, category: str, limit: int = 30) -> List[Dict]:
        """Lấy sản phẩm từ danh mục"""
        try:
            # Chuyển category sang URL friendly
            cat_url = category.lower().replace(' ', '-')
            
            url = f"{self.base_url}/danh-muc/{cat_url}"
            
            response = self.session.get(url, timeout=Config.REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                # Parse HTML để lấy sản phẩm
                products = self._parse_html_products(response.text)
                return products[:limit]
            
            return []
            
        except Exception as e:
            logger.error(f"Loi lay san pham tu category: {str(e)}")
            return []
    
    def standardize_product(self, product: Dict) -> Dict:
        """Chuẩn hóa sản phẩm Sen Đỏ"""
        # Lấy ID
        product_id = str(product.get('id') or product.get('product_id') or '')
        
        # Lấy tên
        name = product.get('name') or product.get('product_name') or product.get('title', '')
        
        # Lấy giá
        price = product.get('price') or product.get('sale_price') or product.get('final_price', 0)
        original_price = product.get('original_price') or product.get('price_before_discount', price)
        
        # Lấy thương hiệu
        brand = product.get('brand') or product.get('brand_name') or product.get('seller', 'Khác')
        if isinstance(brand, dict):
            brand = brand.get('name', 'Khác')
        
        # Lấy hình ảnh
        image_url = product.get('image_url') or product.get('thumbnail') or product.get('image', '')
        if isinstance(image_url, list):
            image_url = image_url[0] if image_url else ''
        
        # Lấy URL
        url = product.get('url') or product.get('product_url', '')
        if url and not url.startswith('http'):
            url = f"{self.base_url}{url}"
        
        return {
            'id': product_id,
            'name': name,
            'price': self._parse_price(price),
            'original_price': self._parse_price(original_price),
            'brand': brand if brand and brand != 'Khác' else 'Khác',
            'category': product.get('category', self.category_name),
            'rating': self._parse_rating(product.get('rating', product.get('rating_average', 0))),
            'reviews_count': self._parse_int(product.get('reviews_count', product.get('review_count', 0))),
            'sold_count': self._parse_int(product.get('sold_count', product.get('quantity_sold', 0))),
            'url': url,
            'image_url': image_url,
            'platform': self.platform_name,
            'scraped_at': datetime.now().isoformat(),
            'extra': {
                'seller': product.get('seller_name', ''),
                'in_stock': product.get('in_stock', True),
                'discount': product.get('discount_percent', 0),
            }
        }
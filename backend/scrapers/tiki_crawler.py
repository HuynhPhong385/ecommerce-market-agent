# src/crawler/tiki_crawler.py

import time
import logging
import requests
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class TikiCrawler:
    """Crawler tối ưu cho Tiki.vn - Phiên bản tích hợp MySQL & LangGraph"""
    
    def __init__(self):
        self.platform_name = 'tiki'
        self.base_url = "https://tiki.vn"
        self.api_url = "https://tiki.vn/api/v2"
        
        # Headers chuẩn hóa giả lập trình duyệt để tránh bị chặn
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Referer': 'https://tiki.vn/',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.category_cache = {}
        
        logger.info("Khởi tạo Tiki Crawler thành công.")
    
    def scrape(self, category: str, keywords: List[str], max_products: int = 20) -> List[Dict]:
        """
        Hàm chính kích hoạt tiến trình cào dữ liệu.
        - category: Tên danh mục do người dùng nhập hoặc suy luận từ từ khóa.
        - keywords: Danh sách từ khóa tìm kiếm gửi từ Frontend React.
        - max_products: Giới hạn số lượng sản phẩm lưu vào DB để tối ưu thời gian phản hồi.
        """
        logger.info(f"Bắt đầu crawl Tiki - Category: {category}, Keywords: {keywords}")
        all_products = []
        
        try:
            # 1. Tìm kiếm và phân giải Category ID từ Tiki API
            category_id = self._get_category_id(category)
            if category_id:
                logger.info(f"Tìm thấy hệ thống Category ID của Tiki: {category_id}")
            
            # 2. Vòng lặp quét dữ liệu dựa trên danh sách từ khóa tìm kiếm
            for keyword in keywords[:3]:  # Chỉ giới hạn quét tối đa 3 từ khóa liên quan để tránh timeout
                if len(all_products) >= max_products:
                    break
                
                products = self._search_products(
                    keyword=keyword,
                    limit=min(max_products - len(all_products), 50)
                )
                
                if products:
                    all_products.extend(products)
                    logger.info(f"Tìm thấy {len(products)} sản phẩm thô cho từ khóa '{keyword}'")
                else:
                    # Tuyến phòng thủ dự phòng (Fallback): Lấy sản phẩm phổ biến theo danh mục nếu tìm kiếm rỗng
                    if category_id:
                        products = self._get_products_by_category(
                            category_id=category_id,
                            limit=min(max_products - len(all_products), 50)
                        )
                        if products:
                            all_products.extend(products)
                
                time.sleep(1)  # Giãn cách 1 giây giữa các request để phòng chống Anti-bot cơ bản
            
            # 3. Tiến hành chuẩn hóa cấu trúc dữ liệu và loại bỏ các ID trùng lặp
            standardized_list = []
            seen_ids = set()
            
            for product in all_products[:max_products]:
                product_id = str(product.get('id', ''))
                if product_id and product_id not in seen_ids:
                    std_product = self.standardize_product(product, default_category=category)
                    standardized_list.append(std_product)
                    seen_ids.add(product_id)
            
            logger.info(f"Hoàn thành xử lý sạch. Tổng cộng {len(standardized_list)} sản phẩm sẵn sàng đẩy vào MySQL.")
            return standardized_list
            
        except Exception as e:
            logger.error(f"Xảy ra lỗi nghiêm trọng khi crawl Tiki: {str(e)}")
            return []
    
    def _search_products(self, keyword: str, limit: int = 50) -> List[Dict]:
        """Gọi API tìm kiếm nội bộ của Tiki dựa trên thuật toán sắp xếp bán chạy nhất"""
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
            logger.error(f"Lỗi truy vấn tìm kiếm cho từ khóa '{keyword}': {str(e)}")
            return []
    
    def _get_products_by_category(self, category_id: str, limit: int = 50) -> List[Dict]:
        """Truy vấn sản phẩm trực tiếp từ ID danh mục của Tiki"""
        try:
            params = {
                'category': category_id,
                'limit': limit,
                'page': 1,
                'sort': 'top_seller',
            }
            response = self._make_request('/products', params)
            if response and 'data' in response:
                return response['data']
            return []
        except Exception as e:
            logger.error(f"Lỗi lấy sản phẩm theo danh mục ID {category_id}: {str(e)}")
            return []
    
    def _get_category_id(self, category_name: str) -> Optional[str]:
        """Phân tích cây thư mục của Tiki để lấy mã ID số tương ứng"""
        if category_name in self.category_cache:
            return self.category_cache[category_name]
        
        try:
            response = self._make_request('/categories')
            if response:
                categories = response if isinstance(response, list) else response.get('data', [])
                
                # Tìm kiếm trực tiếp tầng 1
                for cat in categories:
                    if cat.get('name', '').lower() == category_name.lower():
                        cat_id = str(cat.get('id'))
                        self.category_cache[category_name] = cat_id
                        return cat_id
                    
                    # Quét sâu xuống danh mục con tầng 2 (Children)
                    if 'children' in cat:
                        for child in cat['children']:
                            if child.get('name', '').lower() == category_name.lower():
                                cat_id = str(child.get('id'))
                                self.category_cache[category_name] = cat_id
                                return cat_id
            return None
        except Exception as e:
            logger.error(f"Lỗi phân giải cây danh mục: {str(e)}")
            return None
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Thực hiện HTTP Request tới endpoint API của Tiki kèm bộ lọc mã lỗi"""
        url = f"{self.api_url}{endpoint}"
        try:
            if params:
                url = f"{url}?{urlencode(params)}"
            
            response = self.session.get(url, timeout=10)
            
            # Khắc phục lỗi: Chấp nhận cả mã 400 nếu Tiki đính kèm dữ liệu dự phòng trong payload
            if response.status_code in [200, 400]:
                try:
                    data = response.json()
                    if 'error' in data and 'data' in data:
                        return {'data': data['data']}
                    return data
                except:
                    return None
            elif response.status_code == 429:
                logger.warning("Bị kích hoạt cơ chế giới hạn tần suất (429 Rate Limit). Tạm dừng 5 giây...")
                time.sleep(5)
                return self._make_request(endpoint, params)
            else:
                logger.warning(f"Tiki phản hồi trạng thái bất thường {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Lỗi kết nối mạng vật lý tới Tiki API: {str(e)}")
            return None
    
    def standardize_product(self, product: Dict, default_category: str) -> Dict:
        """
        Hàm lõi chuẩn hóa dữ liệu thô phức tạp từ Tiki về cấu trúc phẳng (Flat Dictionary)
        Giúp quá trình map dữ liệu vào các cột MySQL của SQLAlchemy diễn ra an toàn.
        """
        # Bóc tách tên Danh mục
        category = ''
        if isinstance(product.get('category'), dict):
            category = product.get('category', {}).get('name', '')
        if not category:
            category = product.get('primary_category', {}).get('name', '')
        if not category:
            category = default_category
            
        # Bóc tách tên Thương hiệu (Brand)
        brand = product.get('brand_name', '')
        if not brand:
            brand_obj = product.get('brand', {})
            if isinstance(brand_obj, dict):
                brand = brand_obj.get('name', '')
        if not brand:
            brand = 'Không rõ thương hiệu'
            
        # Chuẩn hóa đường dẫn URL sản phẩm
        url = product.get('url', '')
        if url and not url.startswith('http'):
            url = f"{self.base_url}/{url}" if url.startswith('/') else f"{self.base_url}/{url}"
            
        # Xử lý ảnh đại diện hiển thị lên React Dashboard
        image_url = product.get('thumbnail_url', '')
        if not image_url and isinstance(product.get('image'), dict):
            image_url = product.get('image', {}).get('large_url', '')
            
        # Ép kiểu an toàn tránh lỗi Null Pointer / Kiểu dữ liệu không đồng nhất ở DB
        try:
            price = float(product.get('price', 0))
            original_price = float(product.get('original_price', 0))
            rating = float(product.get('rating_average', 0.0))
            reviews_count = int(product.get('review_count', 0))
            
            # Xử lý số lượng bán (Tiki lưu lồng trong object quantity_sold)
            sold_count = 0
            sold_obj = product.get('quantity_sold', {})
            if isinstance(sold_obj, dict):
                sold_count = int(sold_obj.get('value', 0))
        except (ValueError, TypeError):
            price, original_price, rating, reviews_count, sold_count = 0.0, 0.0, 0.0, 0, 0

        # Trả về Dictionary sạch khớp hoàn toàn với MySQL Model đã cấu trúc ở lượt trước
        return {
            'id': str(product.get('id', '')),
            'name': product.get('name', 'Sản phẩm chưa có tên'),
            'price': price,
            'original_price': original_price,
            'brand': brand,
            'category': category,
            'rating': rating,
            'reviews_count': reviews_count,
            'sold_count': sold_count,
            'url': url,
            'image_url': image_url,
            'platform': self.platform_name,
            'scraped_at': datetime.now(),
            'extra': {
                'sku': str(product.get('sku', '')),
                'discount_rate': int(product.get('discount_rate', 0)),
                'is_authentic': bool(product.get('is_authentic', False)),
                'seller': product.get('seller', {}).get('name', '') if isinstance(product.get('seller'), dict) else '',
                'short_description': product.get('short_description', ''),
            }
        }
# src/crawler/base_crawler.py

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseCrawler(ABC):
    """Base class cho các crawler"""
    
    def __init__(self):
        self.platform_name = self.__class__.__name__.replace('Crawler', '').lower()
        self.session = None
        self.category_name = ''
        logger.info(f"Khoi tao crawler: {self.platform_name}")
    
    @abstractmethod
    def scrape(
        self,
        category: str,
        keywords: List[str],
        max_products: Optional[int] = None
    ) -> List[Dict]:
        """Cào dữ liệu từ sàn TMĐT"""
        pass
    
    def standardize_product(self, product: Dict) -> Dict:
        """Chuẩn hóa dữ liệu sản phẩm về format chung"""
        return {
            'id': str(product.get('id', '')),
            'name': product.get('name', ''),
            'price': self._parse_price(product.get('price', 0)),
            'original_price': self._parse_price(product.get('original_price', 0)),
            'brand': product.get('brand', 'Khác'),
            'category': product.get('category', self.category_name),
            'rating': self._parse_rating(product.get('rating', 0)),
            'reviews_count': self._parse_int(product.get('reviews_count', 0)),
            'sold_count': self._parse_int(product.get('sold_count', 0)),
            'url': product.get('url', ''),
            'image_url': product.get('image_url', ''),
            'platform': self.platform_name,
            'scraped_at': datetime.now().isoformat(),
            'extra': product.get('extra', {})
        }
    
    def _parse_price(self, price: Any) -> int:
        """Chuyển đổi giá về int"""
        if isinstance(price, (int, float)):
            return int(price)
        if isinstance(price, str):
            # Xóa ký tự đặc biệt
            price = price.replace('.', '').replace(',', '').replace('₫', '').strip()
            try:
                return int(price)
            except:
                return 0
        return 0
    
    def _parse_rating(self, rating: Any) -> float:
        """Chuyển đổi rating về float"""
        if isinstance(rating, (int, float)):
            return float(rating)
        if isinstance(rating, str):
            try:
                return float(rating.replace(',', '.'))
            except:
                return 0.0
        return 0.0
    
    def _parse_int(self, value: Any) -> int:
        """Chuyển đổi về int"""
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value.replace('.', '').replace(',', ''))
            except:
                return 0
        return 0
    
    def get_sample_data(self, category: str, count: int) -> List[Dict]:
        """Tạo dữ liệu mẫu (fallback)"""
        brands = ['Nike', 'Adidas', 'Puma', 'Xiaomi', 'Samsung', 'Apple', 'Sony', 'LG']
        products = []
        
        for i in range(min(count, 50)):
            brand = brands[i % len(brands)]
            price = 100000 + (i * 25000) + (i % 5) * 50000
            
            products.append({
                'id': f'{self.platform_name}_{i+1}_{int(datetime.now().timestamp())}',
                'name': f'{brand} {category.title()} Model {i+1}',
                'price': price,
                'original_price': price + (i % 3) * 50000,
                'brand': brand,
                'category': category,
                'rating': round(4 + (i % 5) * 0.2, 1),
                'reviews_count': 100 + i * 30,
                'sold_count': 50 + i * 20,
                'url': f'https://{self.platform_name}.vn/product/{i+1}',
                'image_url': f'https://via.placeholder.com/300x300?text={brand}+{i+1}',
                'platform': self.platform_name,
                'scraped_at': datetime.now().isoformat(),
                'extra': {
                    'discount_rate': (i % 5) * 5,
                    'seller': f'Seller {i % 10 + 1}',
                    'in_stock': i % 3 != 0
                }
            })
        
        return products
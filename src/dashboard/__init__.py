# src/dashboard/__init__.py

from src.dashboard.pages.dashboard import render_dashboard
from src.dashboard.pages.products import render_products
from src.dashboard.pages.ai_analyst import render_ai_analyst
from src.dashboard.pages.reports import render_reports
from src.dashboard.pages.settings import render_settings

__all__ = [
    'render_dashboard',
    'render_products',
    'render_ai_analyst',
    'render_reports',
    'render_settings'
]
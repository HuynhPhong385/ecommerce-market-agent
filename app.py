# app.py

import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime

# Import từ cấu trúc src/dashboard
from src.dashboard.config import set_page_config, get_css
from src.dashboard.pages import (
    render_dashboard,
    render_products,
    render_ai_analyst,
    render_reports,
    render_settings
)

# ==================== CONFIG ====================
set_page_config()

# ==================== CSS ====================
st.markdown(get_css(), unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem 0;">
        <div style="font-size: 1.4rem; font-weight: 700; color: #1a1a2e;">
            📊 Ecommerce AI
        </div>
        <div style="font-size: 0.6rem; color: #8898aa; margin-top: -0.2rem;">
            Market Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        None,
        ["Tổng quan", "Products", "AI Analyst", "Reports", "Settings"],
        icons=["house-fill", "box-fill", "robot", "file-earmark-text", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background": "transparent",
                "border": "none",
            },
            "icon": {
                "color": "#8898aa",
                "font-size": "16px",
            },
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "4px 0",
                "padding": "10px 16px",
                "border-radius": "10px",
                "color": "#8898aa",
                "background": "transparent",
                "transition": "all 0.2s",
            },
            "nav-link-selected": {
                "background": "#e8f0fe",
                "color": "#4a90d9",
                "font-weight": "600",
            },
            "nav-link:hover": {
                "background": "#f0f2f5",
                "color": "#1a1a2e",
            },
        }
    )
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # User info
    st.markdown("""
    <div style="padding: 0.5rem 0;">
        <div style="display: flex; align-items: center; gap: 0.8rem;">
            <div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #4a90d9, #667eea); display: flex; align-items: center; justify-content: center; font-weight: 700; color: white; font-size: 0.9rem;">
                A
            </div>
            <div>
                <div style="color: #1a1a2e; font-weight: 600; font-size: 0.85rem;">Admin User</div>
                <div style="color: #8898aa; font-size: 0.6rem;">Pro Plan</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status
    st.markdown("""
    <div style="padding: 0.5rem 0; margin-top: 0.5rem; background: #f0f2f5; border-radius: 8px; padding: 0.8rem;">
        <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #555;">
            <span>Trạng thái:</span>
            <span style="font-weight: 600; color: #00a86b;">Hoạt động</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #555; margin-top: 0.2rem;">
            <span>Cập nhật:</span>
            <span style="font-weight: 600;">5 phút trước</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== RENDER ====================
if selected == "Dashboard":
    render_dashboard()
elif selected == "Products":
    render_products()
elif selected == "AI Analyst":
    render_ai_analyst()
elif selected == "Reports":
    render_reports()
elif selected == "Settings":
    render_settings()

# ==================== FOOTER ====================
st.markdown(f"""
<div class="footer">
    <strong>Ecommerce AI - Market Intelligence Agent</strong><br>
    Google Gemini + LangGraph + Streamlit | Dữ liệu từ Tiki.vn
</div>
""", unsafe_allow_html=True)
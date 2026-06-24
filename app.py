# app.py

import streamlit as st
import json
from datetime import datetime
import sys
from pathlib import Path

# Thêm src vào path
sys.path.append(str(Path(__file__).parent))

from src.agents.graph import run_agent_sync
from src.core.config import Config
from src.core.llm import get_model_info

# ==================== CẤU HÌNH PAGE ====================

st.set_page_config(
    page_title="Ecommerce Market Intelligence Agent",
    page_icon="📊",
    layout="wide"
)

# ==================== CSS TÙY CHỈNH ====================

st.markdown("""
<style>
    /* Reset và font */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #1a1a2e;
        padding: 1.5rem 0 0.5rem 0;
        letter-spacing: -0.5px;
        border-bottom: 3px solid #e8e8e8;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 1.5rem;
    }
    
    /* Cards */
    .metric-card {
        background: #ffffff;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #e8e8e8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #888;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-top: 0.3rem;
    }
    
    /* Report container */
    .report-container {
        background: #ffffff;
        padding: 2rem 2.5rem;
        border-radius: 12px;
        border: 1px solid #e8e8e8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-top: 1rem;
        line-height: 1.8;
        color: #2d2d2d;
    }
    
    .report-container h1 {
        color: #1a1a2e;
        font-size: 2rem;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 0.5rem;
    }
    
    .report-container h2 {
        color: #2d2d2d;
        font-size: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .report-container h3 {
        color: #3d3d3d;
        font-size: 1.2rem;
        margin-top: 1rem;
    }
    
    .report-container p {
        margin: 0.8rem 0;
    }
    
    .report-container ul, .report-container ol {
        margin: 0.8rem 0;
        padding-left: 1.5rem;
    }
    
    .report-container li {
        margin: 0.4rem 0;
    }
    
    .report-container strong {
        color: #1a1a2e;
    }
    
    /* Buttons */
    .stButton > button {
        background: #1a1a2e;
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #2d2d4e;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(26, 26, 46, 0.2);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Input */
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e8e8e8;
        font-size: 1rem;
        padding: 0.8rem;
        transition: border-color 0.2s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #1a1a2e;
        box-shadow: none;
    }
    
    /* Number input */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e8e8e8;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #1a1a2e;
        box-shadow: none;
    }
    
    /* Status indicators */
    .status-success {
        color: #00a86b;
        font-weight: 600;
    }
    
    .status-error {
        color: #e74c3c;
        font-weight: 600;
    }
    
    .status-warning {
        color: #f39c12;
        font-weight: 600;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #f8f9fa;
    }
    
    .sidebar-section {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        border: 1px solid #e8e8e8;
        margin-bottom: 1rem;
    }
    
    .sidebar-section-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        color: #888;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-item {
        padding: 0.4rem 0;
        color: #2d2d2d;
        font-size: 0.9rem;
    }
    
    .sidebar-item strong {
        color: #1a1a2e;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #aaa;
        font-size: 0.8rem;
        padding: 2rem 0 0.5rem 0;
        border-top: 1px solid #f0f0f0;
        margin-top: 2rem;
    }
    
    /* Divider */
    .divider {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #e0e0e0, transparent);
        margin: 1.5rem 0;
    }
    
    /* Example query buttons */
    .example-btn {
        background: #f8f9fa !important;
        color: #1a1a2e !important;
        border: 1px solid #e8e8e8 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 0.8rem !important;
        text-align: left !important;
        border-radius: 6px !important;
        margin: 0.2rem 0 !important;
    }
    
    .example-btn:hover {
        background: #e8e8e8 !important;
        border-color: #1a1a2e !important;
    }
</style>
""", unsafe_allow_html=True)


# ==================== HEADER ====================

st.markdown('<div class="main-header">Ecommerce Market AI Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Phân tích thị trường thông minh với AI Agent</div>', unsafe_allow_html=True)


# ==================== SIDEBAR ====================

with st.sidebar:
    st.markdown("## Cấu hình")
    
    # Thông tin API
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Trạng thái API</div>', unsafe_allow_html=True)
    
    model_info = get_model_info()
    if model_info['api_key_set']:
        st.markdown('<div class="sidebar-item"><span class="status-success">●</span> <strong>Gemini</strong> Đã kết nối</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-item">Model: {model_info["model"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-item"><span class="status-error">●</span> <strong>Chua co API Key</strong></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-item" style="color:#e74c3c;font-size:0.8rem;">Vui long them GOOGLE_API_KEY vao file .env</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Thống kê
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Thống kê</div>', unsafe_allow_html=True)
    
    # Đếm số báo cáo
    reports_dir = Config.REPORTS_DIR
    if reports_dir.exists():
        reports = list(reports_dir.glob("*.md"))
        st.markdown(f'<div class="sidebar-item">Tổng báo cáo: <strong>{len(reports)}</strong></div>', unsafe_allow_html=True)
        
        # Báo cáo gần nhất
        if reports:
            latest = max(reports, key=lambda x: x.stat().st_mtime)
            st.markdown(f'<div class="sidebar-item" style="font-size:0.8rem;color:#888;">Moi nhat: {latest.name[:20]}...</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sidebar-item">Chua co bao cao</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Gợi ý câu hỏi
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-title">Goi y cau hoi</div>', unsafe_allow_html=True)
    
    example_queries = [
        "Phan tich nganh hang Giay the thao nam tren Tiki",
        "Danh gia thi truong Dien thoai thong minh tren Tiki",
        "Xu huong Laptop gaming tren Shopee hien nay",
        "Phan tich sach kinh doanh tren Tiki",
        "Thong ke giay the thao nu tren Shopee",
        "Phan tich thi truong tai nghe Bluetooth"
    ]
    
    for query in example_queries:
        if st.button(query, key=query, use_container_width=True, type="secondary"):
            st.session_state.query = query
    
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== MAIN CONTENT ====================

col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_area(
        "Nhap cau hoi phan tich:",
        value=st.session_state.get('query', ''),
        placeholder="Vi du: Phan tich nganh hang Giay the thao nam tren Tiki hien tai",
        height=80,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("---")
    max_products = st.number_input(
        "So luong san pham",
        min_value=10,
        max_value=500,
        value=100,
        step=10
    )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        analyze_btn = st.button("Phan tich", use_container_width=True, type="primary")
    with col_btn2:
        clear_btn = st.button("Xoa", use_container_width=True)
    
    if clear_btn:
        st.session_state.query = ""
        st.rerun()

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ==================== PROCESS ====================

if analyze_btn and query:
    with st.spinner("Dang phan tich du lieu..."):
        try:
            # Chạy agent
            result = run_agent_sync(query, max_products)
            
            if result['success']:
                st.markdown("---")
                
                # Hiển thị kết quả
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">San TMĐT</div>
                        <div class="metric-value">{}</div>
                    </div>
                    """.format(result['data']['platform'].title()), unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Nganh hang</div>
                        <div class="metric-value">{}</div>
                    </div>
                    """.format(result['data']['category']   .title()), unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">San pham</div>
                        <div class="metric-value">{}</div>
                    </div>
                    """.format(result['data']['total_products']), unsafe_allow_html=True)
                
                with col4:
                    avg_price = result['data']['analysis'].get('average_price', 0)
                    if avg_price > 0:
                        price_str = f"{avg_price:,.0f} VND"
                    else:
                        price_str = "Chua co du lieu"
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-label">Gia trung binh</div>
                        <div class="metric-value" style="font-size:1.2rem;">{}</div>
                    </div>
                    """.format(price_str), unsafe_allow_html=True)
                
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                
                # Hiển thị báo cáo
                st.markdown("## Bao cao phan tich")
                st.markdown('<div class="report-container">{}</div>'.format(result['report']), unsafe_allow_html=True)
                
                # Nút tải xuống
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Tai bao cao (Markdown)",
                        data=f"# Bao cao phan tich\n\n{result['report']}",
                        file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                
                # Hiển thị dữ liệu JSON
                with st.expander("Xem du lieu phan tich (JSON)"):
                    st.json(result['data']['analysis'])
                
            else:
                st.markdown("---")
                st.markdown(f'<div style="background:#fee;padding:1rem 1.5rem;border-radius:8px;border-left:4px solid #e74c3c;">')
                st.markdown(f'**Loi:** {result["error"]}')
                st.markdown(f'Vui long kiem tra lai cau hoi hoac thu lai sau.')
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.markdown("---")
            st.markdown(f'<div style="background:#fee;padding:1rem 1.5rem;border-radius:8px;border-left:4px solid #e74c3c;">')
            st.markdown(f'**Loi he thong:** {str(e)}')
            st.markdown('</div>', unsafe_allow_html=True)

elif analyze_btn and not query:
    st.warning("Vui long nhap cau hoi de phan tich")


# ==================== FOOTER ====================

st.markdown("---")
st.markdown("""
<div class="footer">
    <strong>Ecommerce Market Intelligence Agent</strong><br>
    Cong nghe: Google Gemini + LangGraph + Streamlit
</div>
""", unsafe_allow_html=True)
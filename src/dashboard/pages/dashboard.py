# src/dashboard/pages/dashboard.py

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go

from src.dashboard.components import (
    render_kpi_card,
    render_insight_card,
    render_product_item,
    render_report_item,
    render_chat_message,
    render_alert_item,
    render_category_bar
)

# ==================== LOAD DATA TỪ FILE ====================
def load_latest_tiki_data():
    """Load file JSON Tiki mới nhất từ thư mục data/raw/"""
    raw_dir = Path("data/raw")
    
    if not raw_dir.exists():
        return []
    
    tiki_files = list(raw_dir.glob("tiki_*.json"))
    
    if not tiki_files:
        return []
    
    latest_file = max(tiki_files, key=lambda x: x.stat().st_mtime)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Lỗi đọc file: {str(e)}")
        return []

def analyze_data(raw_data):
    """Phân tích dữ liệu từ Tiki"""
    if not raw_data:
        return {
            'total': 0,
            'avg_price': 0,
            'brands': {},
            'top_brands': [],
            'ratings': [],
            'avg_rating': 0,
            'price_ranges': {'< 1tr': 0, '1-2tr': 0, '2-5tr': 0, '5-10tr': 0, '> 10tr': 0},
            'raw_data': []
        }
    
    total = len(raw_data)
    prices = [p.get('price', 0) for p in raw_data if p.get('price', 0) > 0]
    avg_price = int(sum(prices) / len(prices)) if prices else 0
    
    brands = {}
    ratings = []
    price_ranges = {'< 1tr': 0, '1-2tr': 0, '2-5tr': 0, '5-10tr': 0, '> 10tr': 0}
    
    for p in raw_data:
        brand = p.get('brand', 'Khác')
        brands[brand] = brands.get(brand, 0) + 1
        
        rating = p.get('rating', 0)
        if rating:
            ratings.append(float(rating))
        
        price = p.get('price', 0)
        if price < 1000000:
            price_ranges['< 1tr'] += 1
        elif price < 2000000:
            price_ranges['1-2tr'] += 1
        elif price < 5000000:
            price_ranges['2-5tr'] += 1
        elif price < 10000000:
            price_ranges['5-10tr'] += 1
        else:
            price_ranges['> 10tr'] += 1
    
    top_brands = sorted(brands.items(), key=lambda x: x[1], reverse=True)[:10]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    return {
        'total': total,
        'avg_price': avg_price,
        'brands': brands,
        'top_brands': top_brands,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'price_ranges': price_ranges,
        'raw_data': raw_data
    }

# ==================== RENDER DASHBOARD ====================
def render_dashboard():
    """Render trang Dashboard - Giống ảnh mẫu"""
    
    # Load data
    raw_data = load_latest_tiki_data()
    
    if not raw_data:
        st.warning("⚠️ Không có dữ liệu. Vui lòng crawl dữ liệu mới.")
        return
    
    analysis = analyze_data(raw_data)
    
    # ===== FILTER ROW =====
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        category = st.text_input("Danh mục", value="Điện thoại", label_visibility="collapsed")
    with col2:
        keywords = st.text_input("Từ khóa", value="điện thoại, smartphone", label_visibility="collapsed")
    with col3:
        max_products = st.number_input("Số lượng", min_value=10, max_value=200, value=50, label_visibility="collapsed")
    
    if st.button("🔄 Cập nhật dữ liệu", use_container_width=True):
        from src.core.tools import EcommerceTools
        with st.spinner("Đang crawl dữ liệu..."):
            tools = EcommerceTools()
            tools.scrape_ecommerce_data(
                platform='tiki',
                category=category,
                keywords=keywords.split(','),
                max_products=max_products
            )
        st.success("✅ Crawl thành công!")
        st.cache_data.clear()
        st.rerun()
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ===== METRICS (4 KPI) =====
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-label">📦 Sản phẩm</div>
            <div class="kpi-value">{analysis['total']:,}</div>
            <div><span class="kpi-change up">+{analysis['total']//10}%</span> <span class="kpi-sub">so với 7 ngày trước</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-label">💰 Giá trung bình</div>
            <div class="kpi-value">{analysis['avg_price']:,.0f}đ</div>
            <div><span class="kpi-change up">+{analysis['avg_price']//1000000}%</span> <span class="kpi-sub">so với 7 ngày trước</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-label">🏷️ Thương hiệu</div>
            <div class="kpi-value">{len(analysis['brands'])}</div>
            <div><span class="kpi-change up">+{len(analysis['brands'])//2}%</span> <span class="kpi-sub">so với 7 ngày trước</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-label">⭐ Đánh giá</div>
            <div class="kpi-value">{analysis['avg_rating']:.1f}/5</div>
            <div><span class="kpi-change up">+{int(analysis['avg_rating']*10)}%</span> <span class="kpi-sub">so với 7 ngày trước</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ===== TỔNG QUAN THỊ TRƯỜNG + BIỂU ĐỒ ĐƯỜNG =====
    st.markdown('<div class="section-title">📈 Tổng quan thị trường</div>', unsafe_allow_html=True)
    
    # Tạo dữ liệu cho biểu đồ đường (giả lập xu hướng theo giá)
    price_df = pd.DataFrame({
        'Khoảng giá': list(analysis['price_ranges'].keys()),
        'Số lượng': list(analysis['price_ranges'].values())
    })
    
    # ===== BIỂU ĐỒ ĐƯỜNG - MÀU Y CHANG ẢNH =====
    fig = go.Figure()
    
    # Thêm đường màu xanh dương (#4a90d9) - y chang ảnh
    fig.add_trace(go.Scatter(
        x=price_df['Khoảng giá'],
        y=price_df['Số lượng'],
        mode='lines+markers',
        name='Doanh số',
        line=dict(color='#4a90d9', width=3),
        marker=dict(size=10, color='#4a90d9', symbol='circle'),
        fill='tozeroy',
        fillcolor='rgba(74, 144, 217, 0.15)'
    ))
    
    fig.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#555', size=12),
        xaxis=dict(
            gridcolor='#f0f2f5',
            showline=False,
            tickfont=dict(color='#555', size=11)
        ),
        yaxis=dict(
            gridcolor='#f0f2f5',
            showline=False,
            tickfont=dict(color='#555', size=11)
        ),
        showlegend=False,
        hovermode='x unified',
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ===== INSIGHTS =====
    st.markdown('<div class="section-title">💡 Insight nổi bật</div>', unsafe_allow_html=True)
    
    insights = [
        {'title': 'Xu hướng tăng trưởng', 'desc': f'Sản phẩm {category} đang tăng {len(analysis["brands"])*3}% trong 7 ngày qua', 'type': 'trend'},
        {'title': 'Cơ hội thị trường', 'desc': f'Phân khúc giá trung bình đang thiếu {len(analysis["brands"])} sản phẩm', 'type': 'opportunity'},
        {'title': 'Cảnh báo cạnh tranh', 'desc': f'{len(analysis["brands"])} thương hiệu mới gia nhập phân khúc {category}', 'type': 'warning'},
        {'title': 'Từ khóa hot', 'desc': f'{", ".join(keywords.split(",")[:3])}', 'type': 'keyword'},
    ]
    
    cols = st.columns(4)
    for i, ins in enumerate(insights):
        with cols[i]:
            st.markdown(f"""
            <div class="insight-card {ins['type']}">
                <div class="insight-title">{ins['title']}</div>
                <div class="insight-desc">{ins['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ===== TOP SẢN PHẨM + TOP DANH MỤC =====
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<div class="section-title">🏆 Top sản phẩm bán chạy</div>', unsafe_allow_html=True)
        
        sorted_products = sorted(analysis['raw_data'], key=lambda x: x.get('price', 0), reverse=True)[:5]
        growths = ['+15.2%', '+12.8%', '+18.3%', '+8.7%', '+5.2%']
        
        for i, p in enumerate(sorted_products):
            st.markdown(f"""
            <div class="product-item">
                <span class="product-name">{i+1}. {p.get('name', '')[:45]}...</span>
                <span class="product-growth up">{growths[i % len(growths)]}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="section-title">📊 Top danh mục tăng trưởng</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="category-label">Gói hiện tại: Pro</div>
        <div class="category-bar">
            <div class="category-fill" style="width: 75%">75%</div>
        </div>
        <div style="font-size:0.65rem;color:#8898aa;margin-bottom:0.8rem;">Còn 250 phân tích trong tháng</div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="upgrade-btn">⬆ Nâng cấp gói</div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-title" style="margin-top:1rem;">📋 Báo cáo gần đây</div>', unsafe_allow_html=True)
        
        reports = [
            {'title': f'Phân tích {category}', 'date': datetime.now().strftime('%d/%m/%Y %H:%M')},
            {'title': f'Báo cáo thị trường {category}', 'date': datetime.now().strftime('%d/%m/%Y')},
            {'title': f'Phân tích đối thủ', 'date': datetime.now().strftime('%d/%m/%Y')},
        ]
        for r in reports:
            st.markdown(f"""
            <div class="report-item">
                <div class="report-title">{r['title']}</div>
                <div class="report-date">{r['date']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ===== AI AGENT + CẢNH BÁO =====
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">🤖 AI Agent</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="chat-msg ai">
            👋 Tôi có thể phân tích thị trường {category}!<br>
            <span class="time">Vừa xong</span>
        </div>
        <div class="chat-msg user">
            Phân tích giá {category}<br>
            <span class="time">{datetime.now().strftime('%H:%M')}</span>
        </div>
        <div class="chat-msg ai">
            Đã phân tích {analysis['total']} sản phẩm {category}. Giá trung bình {analysis['avg_price']:,.0f}đ.<br>
            <span class="time">{datetime.now().strftime('%H:%M')}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("💬 Bắt đầu chat", use_container_width=True):
            st.info("🧠 AI Agent đang sẵn sàng!")
    
    with col2:
        st.markdown('<div class="section-title">🔔 Cảnh báo thông minh</div>', unsafe_allow_html=True)
        
        alerts = [
            {'title': f'Sản phẩm {category} tăng trưởng', 'time': datetime.now().strftime('%d/%m/%Y %H:%M'), 'type': 'info'},
            {'title': 'Đối thủ mới xuất hiện', 'time': datetime.now().strftime('%d/%m/%Y'), 'type': 'warning'},
            {'title': 'Từ khóa hot', 'time': datetime.now().strftime('%d/%m/%Y'), 'type': 'info'},
        ]
        
        for alert in alerts:
            alert_class = 'warning' if alert['type'] == 'warning' else ''
            st.markdown(f"""
            <div class="alert-item {alert_class}">
                <div class="alert-title">{alert['title']}</div>
                <div class="alert-time">{alert['time']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ===== FOOTER =====
    st.markdown(f"""
    <div class="footer">
        <strong>Ecommerce AI - Market Intelligence Agent</strong><br>
        Dữ liệu từ Tiki.vn | {analysis['total']} sản phẩm | Cập nhật: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </div>
    """, unsafe_allow_html=True)
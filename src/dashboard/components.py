# src/dashboard/components.py

import streamlit as st

def render_kpi_card(label, value, change=None, sub=None):
    """Render KPI card"""
    if change:
        change_class = 'up' if '+' in str(change) else 'down'
        change_html = f'<span class="kpi-change {change_class}">{change}</span>'
    else:
        change_html = ''
    
    sub_html = f'<span class="kpi-sub">{sub}</span>' if sub else ''
    
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div>{change_html} {sub_html}</div>
    </div>
    """, unsafe_allow_html=True)

def render_insight_card(title, description, type_="trend"):
    """Render insight card"""
    st.markdown(f"""
    <div class="insight-card {type_}">
        <div class="insight-title">{title}</div>
        <div class="insight-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)

def render_product_item(name, price, growth=None):
    """Render product item"""
    growth_html = f'<span class="product-growth up">{growth}</span>' if growth else ''
    st.markdown(f"""
    <div class="product-item">
        <span class="product-name">{name}</span>
        <div>
            <span style="color:#1a1a2e;font-weight:600;margin-right:0.5rem;">{price:,.0f}đ</span>
            {growth_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_report_item(title, date):
    """Render report item"""
    st.markdown(f"""
    <div class="report-item">
        <div class="report-title">{title}</div>
        <div class="report-date">{date}</div>
    </div>
    """, unsafe_allow_html=True)

def render_chat_message(message, sender, time):
    """Render chat message"""
    msg_class = 'user' if sender == 'user' else 'ai'
    st.markdown(f"""
    <div class="chat-msg {msg_class}">
        {message}
        <span class="time">{time}</span>
    </div>
    """, unsafe_allow_html=True)

def render_alert_item(title, time, type_="info"):
    """Render alert item"""
    alert_class = 'warning' if type_ == 'warning' else ''
    st.markdown(f"""
    <div class="alert-item {alert_class}">
        <div class="alert-title">{title}</div>
        <div class="alert-time">{time}</div>
    </div>
    """, unsafe_allow_html=True)

def render_category_bar(name, value, remaining=None):
    """Render category bar"""
    remaining_html = f'<div style="font-size:0.65rem;color:#8898aa;margin-bottom:0.5rem;">Còn {remaining} phân tích trong tháng</div>' if remaining else ''
    st.markdown(f"""
    <div class="category-label">{name}</div>
    <div class="category-bar">
        <div class="category-fill" style="width: {value}%">{value}%</div>
    </div>
    {remaining_html}
    """, unsafe_allow_html=True)
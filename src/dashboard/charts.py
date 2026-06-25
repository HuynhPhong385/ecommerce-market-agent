# src/dashboard/charts.py

import plotly.graph_objects as go
import pandas as pd

def create_price_chart(price_ranges: dict):
    """Biểu đồ phân phối giá"""
    df = pd.DataFrame({
        'Khoảng giá': list(price_ranges.keys()),
        'Số lượng': list(price_ranges.values())
    })
    
    fig = go.Figure(data=[
        go.Bar(
            x=df['Khoảng giá'],
            y=df['Số lượng'],
            marker_color='#4a90d9',
            text=df['Số lượng'],
            textposition='outside',
            textfont=dict(color='#555', size=12)
        )
    ])
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#555', size=12),
        xaxis=dict(
            gridcolor='#f0f2f5',
            tickfont=dict(size=12, color='#555'),
            showline=False,
        ),
        yaxis=dict(
            gridcolor='#f0f2f5',
            tickfont=dict(size=12, color='#555'),
            showline=False,
            title=dict(text='Số sản phẩm', font=dict(color='#8898aa', size=12))
        ),
        showlegend=False,
    )
    return fig

def create_brand_chart(top_brands: list, total: int):
    """Biểu đồ top thương hiệu"""
    if not top_brands:
        return None
    
    brands = [b[0] for b in top_brands[:10]]
    counts = [b[1] for b in top_brands[:10]]
    
    fig = go.Figure(data=[
        go.Bar(
            x=brands,
            y=counts,
            marker_color='#667eea',
            text=counts,
            textposition='outside',
            textfont=dict(color='#555', size=11)
        )
    ])
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#555', size=11),
        xaxis=dict(
            gridcolor='#f0f2f5',
            tickfont=dict(size=11, color='#555'),
            showline=False,
        ),
        yaxis=dict(
            gridcolor='#f0f2f5',
            tickfont=dict(size=11, color='#555'),
            showline=False,
            title=dict(text='Số sản phẩm', font=dict(color='#8898aa', size=11))
        ),
        showlegend=False,
    )
    return fig
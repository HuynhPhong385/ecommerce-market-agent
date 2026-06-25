# src/dashboard/config.py

import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="Ecommerce AI - Dashboard",
        page_icon="📊",
        layout="wide"
    )

def get_css():
    return """
    <style>
        /* Main */
        .main {
            background: #f5f7fb;
            padding: 0rem 1rem;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background: #ffffff;
            border-right: 1px solid #e8ecf1;
        }
        
        /* Glass card */
        .glass-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 1.5rem 1.8rem;
            border: 1px solid #e8ecf1;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            height: 100%;
            transition: all 0.2s;
        }
        .glass-card:hover {
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            transform: translateY(-2px);
        }
        
        /* KPI */
        .kpi-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #8898aa;
            font-weight: 600;
        }
        .kpi-value {
            font-size: 2rem;
            font-weight: 700;
            color: #1a1a2e;
            margin: 0.2rem 0;
        }
        .kpi-change {
            font-size: 0.8rem;
            font-weight: 600;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            display: inline-block;
        }
        .kpi-change.up { color: #00a86b; background: #e8f5ef; }
        .kpi-change.down { color: #e74c3c; background: #fde8e8; }
        .kpi-sub {
            font-size: 0.65rem;
            color: #8898aa;
        }
        
        /* Section title */
        .section-title {
            font-size: 1rem;
            font-weight: 700;
            color: #1a1a2e;
            margin: 1.5rem 0 1rem 0;
        }
        
        /* Insight */
        .insight-card {
            background: #ffffff;
            padding: 0.8rem 1.2rem;
            border-radius: 10px;
            border-left: 3px solid #4a90d9;
            margin-bottom: 0.5rem;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04);
            border: 1px solid #e8ecf1;
        }
        .insight-card.trend { border-left-color: #4a90d9; }
        .insight-card.opportunity { border-left-color: #00a86b; }
        .insight-card.warning { border-left-color: #f39c12; }
        .insight-card.keyword { border-left-color: #9b59b6; }
        .insight-title {
            font-size: 0.6rem;
            text-transform: uppercase;
            color: #8898aa;
            font-weight: 600;
        }
        .insight-desc {
            font-size: 0.85rem;
            color: #2d2d2d;
            font-weight: 500;
            margin: 0.2rem 0 0 0;
        }
        
        /* Product */
        .product-item {
            background: #ffffff;
            padding: 0.6rem 1rem;
            border-radius: 8px;
            border: 1px solid #e8ecf1;
            margin-bottom: 0.4rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .product-name {
            font-size: 0.85rem;
            color: #2d2d2d;
            font-weight: 500;
        }
        .product-growth.up { color: #00a86b; font-weight: 600; }
        .product-growth.down { color: #e74c3c; font-weight: 600; }
        
        /* Report */
        .report-item {
            padding: 0.4rem 0;
            border-bottom: 1px solid #f0f2f5;
        }
        .report-item:last-child { border-bottom: none; }
        .report-title {
            font-size: 0.8rem;
            color: #2d2d2d;
            font-weight: 500;
        }
        .report-date {
            font-size: 0.6rem;
            color: #8898aa;
        }
        
        /* Chat */
        .chat-container {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 0.8rem;
            max-height: 280px;
            overflow-y: auto;
            border: 1px solid #e8ecf1;
        }
        .chat-msg {
            margin-bottom: 0.5rem;
            padding: 0.5rem 0.8rem;
            border-radius: 10px;
            max-width: 88%;
            font-size: 0.8rem;
        }
        .chat-msg.user {
            background: #4a90d9;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .chat-msg.ai {
            background: #ffffff;
            color: #2d2d2d;
            border: 1px solid #e8ecf1;
        }
        .chat-msg .time {
            font-size: 0.5rem;
            opacity: 0.6;
            display: block;
            margin-top: 0.15rem;
        }
        
        /* Category bar */
        .category-label {
            font-size: 0.75rem;
            color: #555;
            font-weight: 500;
            margin-bottom: 0.2rem;
        }
        .category-bar {
            background: #f0f2f5;
            border-radius: 6px;
            height: 22px;
            overflow: hidden;
            margin: 0.3rem 0;
        }
        .category-fill {
            background: linear-gradient(90deg, #4a90d9, #667eea);
            height: 100%;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 0.5rem;
            color: white;
            font-size: 0.65rem;
            font-weight: 600;
        }
        
        /* Alert */
        .alert-item {
            background: #ffffff;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            border: 1px solid #e8ecf1;
            margin-bottom: 0.4rem;
            border-left: 3px solid #4a90d9;
        }
        .alert-item.warning { border-left-color: #f39c12; }
        .alert-title {
            font-size: 0.8rem;
            color: #2d2d2d;
            font-weight: 500;
        }
        .alert-time {
            font-size: 0.6rem;
            color: #8898aa;
        }
        
        /* Upgrade button */
        .upgrade-btn {
            background: linear-gradient(135deg, #4a90d9, #667eea);
            color: white;
            padding: 0.5rem 1.5rem;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            margin: 0.5rem 0;
        }
        
        /* Divider */
        .divider {
            border: none;
            height: 1px;
            background: linear-gradient(to right, transparent, #e0e0e0, transparent);
            margin: 1rem 0;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #8898aa;
            font-size: 0.65rem;
            padding: 1.5rem 0 0.5rem 0;
            border-top: 1px solid #e8ecf1;
            margin-top: 1.5rem;
        }
    </style>
    """
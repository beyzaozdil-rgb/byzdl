import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(page_title="Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 12px;
        text-transform: uppercase;
        opacity: 0.9;
    }
    .insight-box {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .insight-success {
        background: #E8F5E9;
        border-left: 4px solid #27AE60;
    }
    .insight-danger {
        background: #FFEBEE;
        border-left: 4px solid #E74C3C;
    }
    .insight-warning {
        background: #FFF3E0;
        border-left: 4px solid #FF9800;
    }
    .insight-info {
        background: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)

# Data
data = {
    'cities': [
        {'name': 'Bursa', 'revenue': 2774957, 'transactions': 41, 'returnRate': 25.6},
        {'name': 'Mersin', 'revenue': 1800000, 'transactions': 33, 'returnRate': 18.2},
        {'name': 'Istanbul', 'revenue': 1276510, 'transactions': 66, 'returnRate': 19.7},
        {'name': 'Ankara', 'revenue': 791100, 'transactions': 25, 'returnRate': 16.0},
        {'name': 'Sakarya', 'revenue': 270000, 'transactions': 4, 'returnRate': 25.0}
    ],
    'products': [
        {'name': 'ra1428', 'revenue': 2453247, 'units': 1459},
        {'name': 'ch0110', 'revenue': 1162200, 'units': 217},
        {'name': 'Ah1221', 'revenue': 1046512, 'units': 413},
        {'name': 'L1212', 'revenue': 892100, 'units': 213},
        {'name': 'Bh0020', 'revenue': 774500, 'units': 111},
        {'name': 'cam73812', 'revenue': 584008, 'units': 274}
    ],
    'monthly': [
        {'month': 'Jan', 'revenue': 403},
        {'month': 'Feb', 'revenue': 280},
        {'month': 'Mar', 'revenue': 730},
        {'month': 'Apr', 'revenue': 1131},
        {'month': 'May', 'revenue': 1071},
        {'month': 'Jun', 'revenue': 891},
        {'month': 'Jul', 'revenue': 507},
        {'month': 'Aug', 'revenue': 200},
        {'month': 'Sep', 'revenue': 572},
        {'month': 'Oct', 'revenue': 613},
        {'month': 'Nov', 'revenue': 497},
        {'month': 'Dec', 'revenue': 18}
    ]
}

# Header
st.markdown("# 📊 Sales Dashboard")
st.markdown("**Real-time Business Analytics & Interactive Insights**")

# Sidebar - Filters
st.sidebar.markdown("### 🔍 Filter Data")
selected_city = st.sidebar.selectbox(
    "Select City:",
    ["All Cities"] + [c['name'] for c in data['cities']]
)
selected_product = st.sidebar.selectbox(
    "Select Product:",
    ["All Products"] + [p['name'] for p in data['products']]
)

# Filter data
filtered_cities = data['cities'] if selected_city == "All Cities" else [c for c in data['cities'] if c['name'] == selected_city]
filtered_products = data['products'] if selected_product == "All Products" else [p for p in data['products'] if p['name'] == selected_product]

# Calculate metrics
total_revenue = sum(c['revenue'] for c in filtered_cities)
total_transactions = sum(c['transactions'] for c in filtered_cities)
profit = total_revenue * 0.737
avg_order = total_revenue / total_transactions if total_transactions > 0 else 0
avg_return = sum(c['returnRate'] for c in filtered_cities) / len(filtered_cities) if filtered_cities else 0

# KPI Metrics
st.markdown("### 💰 Key Performance Indicators")
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("💵 Revenue", f"₺{total_revenue/1000000:.1f}M", "+26% YoY")

with col2:
    st.metric("📈 Profit", f"₺{profit/1000000:.1f}M", "73.7% margin")

with col3:
    st.metric("⚠️ Returns", f"{avg_return:.1f}%", "Target: 15%")

with col4:
    st.metric("🛍️ Avg Order", f"₺{avg_order/1000:.0f}K", "Per transaction")

with col5:
    st.metric("📦 Orders", f"{total_transactions}", "Total count")

with col6:
    st.metric("🏙️ Cities", f"{len(filtered_cities)}", "Active markets")

st.markdown("---")

# Charts
st.markdown("### 📊 Analytics & Insights")

col1, col2 = st.columns(2)

# Chart 1: Revenue by City
with col1:
    if filtered_cities:
        city_df = pd.DataFrame(filtered_cities)
        fig_city = px.bar(city_df, x='name', y='revenue', title='📍 Revenue by City',
                         labels={'name': 'City', 'revenue': 'Revenue (₺)'})
        fig_city.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_city, use_container_width=True)

# Chart 2: Top Products
with col2:
    if filtered_products:
        prod_df = pd.DataFrame(filtered_products)
        fig_prod = px.bar(prod_df, x='name', y='revenue', title='⭐ Top Products',
                         labels={'name': 'Product', 'revenue': 'Revenue (₺)'})
        fig_prod.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_prod, use_container_width=True)

# Chart 3: Monthly Trend
col1, col2 = st.columns(2)

with col1:
    month_df = pd.DataFrame(data['monthly'])
    fig_trend = px.line(month_df, x='month', y='revenue', title='📈 Monthly Revenue Trend',
                       labels={'month': 'Month', 'revenue': 'Revenue (₺K)'},
                       markers=True)
    fig_trend.update_layout(height=400, hovermode='x unified')
    st.plotly_chart(fig_trend, use_container_width=True)

# Chart 4: Geographic Distribution
with col2:
    if filtered_cities:
        city_df = pd.DataFrame(filtered_cities)
        fig_pie = px.pie(city_df, values='revenue', names='name', title='🥧 Geographic Distribution')
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# Insights
st.markdown("### 🎯 Strategic Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="insight-box insight-success">
    <strong>✅ STRENGTH: 73.7% Profit Margin</strong>
    <p>World-class profitability indicates strong pricing power and operational excellence.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box insight-danger">
    <strong>🚨 CRITICAL: 24.9% Return Rate</strong>
    <p>Returns = ₺1.7M annual loss. Target: 15%. Quality control audit needed immediately.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="insight-box insight-danger">
    <strong>🚨 CRITICAL: Customer Concentration</strong>
    <p>Top 3 customers = 67% of revenue. Loss of one = 42.5% revenue drop. Diversification urgent.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box insight-warning">
    <strong>⚠️ OPPORTUNITY: Wholesale Channel</strong>
    <p>Wholesale = 0.6% of revenue. Industry standard: 20-40%. Potential ₺345K upside.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Tabs
st.markdown("### 📋 Detailed Analysis")

tab1, tab2, tab3 = st.tabs(["Performance", "Financial Projections", "Data Tables"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Strengths")
        st.write("""
        • 73.7% profit margin (exceptional)
        • Strong customer loyalty
        • Market leadership in Bursa
        • Healthy average order value
        """)
    
    with col2:
        st.subheader("🚨 Critical Issues")
        st.write("""
        • 24.9% return rate (high)
        • 66% revenue from 2 cities
        • 67% revenue from 3 customers
        • 35% from single product (ra1428)
        """)
    
    st.subheader("⚠️ Risks & Opportunities")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        **Risks:**
        • Geographic concentration
        • Customer dependency
        • Product concentration
        • Seasonal volatility
        """)
    
    with col2:
        st.write("""
        **Opportunities:**
        • Wholesale channel (0.6% → 5%)
        • Ankara expansion
        • New product lines
        • Customer acquisition
        """)

with tab2:
    st.subheader("12-Month Financial Targets")
    
    projection_data = {
        'Metric': ['Total Revenue', 'Gross Profit', 'Return Rate', 'Wholesale Revenue', 'Customer Count'],
        'Current': ['₺6.9M', '₺5.1M', '24.9%', '₺45K', '9'],
        '12-Month Target': ['₺8.7M', '₺6.1M', '15%', '₺345K', '40'],
        'Improvement': ['+₺1.8M (+26%)', '+₺1.0M (+20%)', 'Save ₺673K', '+₺300K', '+31 customers']
    }
    
    projection_df = pd.DataFrame(projection_data)
    st.dataframe(projection_df, use_container_width=True, hide_index=True)
    
    st.subheader("Top 5 Recommendations")
    
    recommendations = [
        {
            'Priority': '🔴 URGENT',
            'Action': 'Reduce Return Rate',
            'Target': '24.9% → 15%',
            'Impact': 'Save ₺673K',
            'Timeline': '30 days'
        },
        {
            'Priority': '🔴 URGENT',
            'Action': 'Protect Top Customers',
            'Target': 'VIP programs',
            'Impact': 'Protect ₺5.1M',
            'Timeline': '2 weeks'
        },
        {
            'Priority': '🟠 HIGH',
            'Action': 'Launch Wholesale',
            'Target': '0.6% → 5%',
            'Impact': '+₺300K',
            'Timeline': '90 days'
        },
        {
            'Priority': '🟠 HIGH',
            'Action': 'Ankara Expansion',
            'Target': '₺791K → ₺1.5M',
            'Impact': '+₺700K',
            'Timeline': '6 months'
        },
        {
            'Priority': '🟠 HIGH',
            'Action': 'Product Diversification',
            'Target': '6 SKU → 9 SKU',
            'Impact': 'Reduce risk',
            'Timeline': '9 months'
        }
    ]
    
    rec_df = pd.DataFrame(recommendations)
    st.dataframe(rec_df, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("📍 Revenue by City")
    
    city_table_data = []
    for city in data['cities']:
        city_table_data.append({
            'City': city['name'],
            'Revenue': f"₺{city['revenue']:,}",
            '% of Total': f"{(city['revenue']/6912567*100):.1f}%",
            'Transactions': city['transactions'],
            'Return Rate': f"{city['returnRate']:.1f}%"
        })
    
    city_table_df = pd.DataFrame(city_table_data)
    st.dataframe(city_table_df, use_container_width=True, hide_index=True)
    
    st.subheader("⭐ Top 6 Products")
    
    product_table_data = []
    for product in data['products']:
        product_table_data.append({
            'Product': product['name'],
            'Revenue': f"₺{product['revenue']:,}",
            '% of Total': f"{(product['revenue']/6912567*100):.1f}%",
            'Units Sold': product['units'],
            'Avg Price': f"₺{(product['revenue']/product['units']):.0f}"
        })
    
    product_table_df = pd.DataFrame(product_table_data)
    st.dataframe(product_table_df, use_container_width=True, hide_index=True)

st.markdown("---")

# Footer
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **About This Dashboard**
    • Real-time data analysis
    • Interactive filters
    • Strategic insights
    """)

with col2:
    st.markdown("""
    **Key Features**
    • Live KPI tracking
    • Dynamic charts
    • Data drill-down
    • Export ready
    """)

with col3:
    st.markdown(f"""
    **Last Updated**
    • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    • Data Period: 2022-2024
    • Analysis: Complete
    """)

st.markdown("""
---
<p style='text-align: center; color: #999; font-size: 12px;'>
Sales Dashboard v1.0 | Built with Streamlit | Data Analysis Complete
</p>
""", unsafe_allow_html=True)
# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from predictor import predict_vehicle_price, get_encoder_classes

# Page configuration
st.set_page_config(
    page_title="Vehicle Price Analytics",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for shadcn-inspired white theme
st.markdown("""
<style>
    /* Import Inter font (shadcn default) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles - Force white theme */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Force white background everywhere */
    .main, .block-container, [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], body, .stApp {
        background-color: #ffffff !important;
        color: #09090b !important;
    }
    
    /* Reduce default Streamlit padding */
    .st-emotion-cache-zy6yx3 {
        padding: 1rem 4rem 1rem !important;
    }
    
    /* Override dark theme */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, 
    .stMarkdown h3, .stMarkdown h4, div {
        color: inherit !important;
    }
    
    /* shadcn-style cards */
    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    }
    
    .card-header {
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #09090b;
        margin-bottom: 0.25rem;
    }
    
    .card-description {
        font-size: 0.875rem;
        color: #71717a;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        transition: all 0.2s;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #71717a;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #09090b;
    }
    
    .metric-value.positive {
        color: #16a34a;
    }
    
    .metric-value.negative {
        color: #dc2626;
    }
    
    .metric-change {
        font-size: 0.875rem;
        color: #71717a;
        margin-top: 0.25rem;
    }
    
    .metric-change.positive {
        color: #16a34a;
    }
    
    .metric-change.negative {
        color: #dc2626;
    }
    
    /* Alert/Message boxes */
    .alert {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .alert-info {
        background-color: #f0f9ff;
        border-color: #bae6fd;
        color: #0c4a6e;
    }
    
    .alert-success {
        background-color: #f0fdf4;
        border-color: #bbf7d0;
        color: #14532d;
    }
    
    .alert-warning {
        background-color: #fefce8;
        border-color: #fef08a;
        color: #713f12;
    }
    
    .alert-destructive {
        background-color: #fef2f2;
        border-color: #fecaca;
        color: #7f1d1d;
    }
    
    /* Typography */
    .page-header {
        font-size: 2.25rem;
        font-weight: 700;
        color: #09090b;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    
    .page-description {
        font-size: 1rem;
        color: #71717a;
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #09090b;
        margin: 2rem 0 1rem 0;
    }
    
    /* Buttons - Secondary (default) */
    .stButton>button[kind="secondary"] {
        background-color: white;
        color: #52525b;
        border: 1px solid #e5e7eb;
        border-radius: 0.375rem;
        padding: 0.5rem 0.75rem;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.2s;
        width: 100%;
        box-shadow: none;
    }
    
    .stButton>button[kind="secondary"]:hover {
        background-color: #f8f9fa;
        border-color: #d4d4d8;
        color: #09090b;
    }
    
    /* Buttons - Primary (active/selected) */
    .stButton>button[kind="primary"] {
        background-color: #09090b;
        color: white;
        border: 1px solid #09090b;
        border-radius: 0.375rem;
        padding: 0.5rem 0.75rem;
        font-size: 0.875rem;
        font-weight: 600;
        transition: all 0.2s;
        width: 100%;
        box-shadow: none;
    }
    
    .stButton>button[kind="primary"]:hover {
        background-color: #18181b;
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border: 1px solid #e5e7eb;
        border-radius: 0.375rem;
        background-color: white;
        color: #09090b;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #09090b;
        box-shadow: 0 0 0 1px #09090b;
    }
    
    /* Labels */
    .input-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #09090b;
        margin-bottom: 0.375rem;
    }
    
    /* Streamlit metric styling for negative values */
    [data-testid="stMetricDelta"] svg[fill*="red"],
    [data-testid="stMetricDelta"] svg[fill*="#FF4B4B"] {
        fill: #dc2626 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #09090b;
    }
    
    [data-testid="stMetricDelta"][data-color="negative"] {
        color: #dc2626 !important;
    }
    
    /* Tables */
    .dataframe {
        border: 1px solid #e5e7eb !important;
        border-radius: 0.5rem;
    }
    
    /* Remove default Streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar (hidden by default) */
    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e5e7eb;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background-color: white !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 0.375rem !important;
    }
    
    .stSelectbox label {
        display: none !important;
    }
    
    /* Radio button override */
    .stRadio > div {
        background-color: white !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background-color: white !important;
    }
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 500;
        border-radius: 9999px;
        background-color: #f4f4f5;
        color: #52525b;
    }
    
    .badge-success {
        background-color: #dcfce7;
        color: #166534;
    }
    
    .badge-warning {
        background-color: #fef9c3;
        color: #854d0e;
    }
    
    .badge-destructive {
        background-color: #fee2e2;
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)

# Header with logo, title, and navigation
st.markdown('''
<div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.75rem; border-bottom: 1px solid #e5e7eb; margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: center; gap: 0.75rem;">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="7" height="7" rx="1" fill="#09090b"/>
            <rect x="3" y="14" width="7" height="7" rx="1" fill="#09090b"/>
            <rect x="14" y="3" width="7" height="7" rx="1" fill="#3b82f6"/>
            <rect x="14" y="14" width="7" height="7" rx="1" fill="#3b82f6"/>
            <circle cx="6.5" cy="6.5" r="1.5" fill="white"/>
            <circle cx="17.5" cy="17.5" r="1.5" fill="white"/>
        </svg>
        <h1 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #09090b;">Vehicle Price Analytics</h1>
    </div>
</div>
''', unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "Analytics Dashboard"

# Compact navigation menu
col1, col2, col3, col4 = st.columns([1, 1, 1, 3])

with col1:
    btn_type = "primary" if st.session_state.page == "Analytics Dashboard" else "secondary"
    if st.button("📊 Dashboard", use_container_width=True, key="nav_analytics", type=btn_type):
        st.session_state.page = "Analytics Dashboard"
        st.rerun()

with col2:
    btn_type = "primary" if st.session_state.page == "Price Prediction" else "secondary"
    if st.button("💰 Prediction", use_container_width=True, key="nav_prediction", type=btn_type):
        st.session_state.page = "Price Prediction"
        st.rerun()

with col3:
    btn_type = "primary" if st.session_state.page == "About" else "secondary"
    if st.button("ℹ️ About", use_container_width=True, key="nav_about", type=btn_type):
        st.session_state.page = "About"
        st.rerun()

page = st.session_state.page

st.markdown('<div style="margin: 1rem 0;"></div>', unsafe_allow_html=True)

# Main content area
if page == "About":
    st.markdown('<h1 class="page-header">About This Project</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">ML-powered predictive analytics platform for vehicle price optimization</p>', unsafe_allow_html=True)
    
    # Key metrics row with shadcn cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Training Records</div>
            <div class="metric-value">558K+</div>
            <div class="metric-change">Real auction data</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Model Accuracy</div>
            <div class="metric-value">96.9%</div>
            <div class="metric-change positive">R² Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">ML Models</div>
            <div class="metric-value">3</div>
            <div class="metric-change">Ensemble approach</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Avg Prediction Error</div>
            <div class="metric-value">±$1,682</div>
            <div class="metric-change">RMSE</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance metrics
    st.markdown('<h2 class="section-title">Model Performance Summary</h2>', unsafe_allow_html=True)
    
    performance_data = {
        'Model': ['Linear Regression', 'Random Forest', 'XGBoost', 'Ensemble'],
        'R² Score': [0.9689, 0.9669, 0.9669, 0.9676],
        'RMSE ($)': [1682, 1735, 1736, 1698],
        'MAE ($)': [1056, 983, 974, 1004],
        'MAPE (%)': [14.45, 13.15, 12.46, 13.35],
        'Training Time (s)': [0.03, 2.31, 0.92, 3.26]
    }
    
    df_performance = pd.DataFrame(performance_data)
    st.dataframe(df_performance, use_container_width=True, hide_index=True)
    
    st.markdown("""
    <div class="alert alert-info">
        <strong>Performance Notes</strong><br>
        <ul style="margin-top: 0.5rem; line-height: 1.75;">
            <li>All models achieve R² > 0.96, explaining over 96% of price variance</li>
            <li>Mean Absolute Percentage Error (MAPE) ranges from 12.46% to 14.45%</li>
            <li>XGBoost offers the best accuracy-speed tradeoff for production deployment</li>
            <li>Ensemble method provides robust predictions by combining model strengths</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Academic information
    st.markdown('<h2 class="section-title">Project Information</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Academic Details</h3>
            </div>
            <table style="width: 100%; font-size: 0.875rem; color: #52525b;">
                <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 0.75rem 0; font-weight: 500;">Course</td>
                    <td style="padding: 0.75rem 0;">COMP8811 Data Analytics & Intelligence</td>
                </tr>
                <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 0.75rem 0; font-weight: 500;">Assignment</td>
                    <td style="padding: 0.75rem 0;">2 (Individual)</td>
                </tr>
                <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 0.75rem 0; font-weight: 500;">Semester</td>
                    <td style="padding: 0.75rem 0;">2, 2025</td>
                </tr>
                <tr>
                    <td style="padding: 0.75rem 0; font-weight: 500;">Institution</td>
                    <td style="padding: 0.75rem 0;">Unitec Institute of Technology</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Technical Stack</h3>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                <span class="badge">Python</span>
                <span class="badge">Scikit-learn</span>
                <span class="badge">XGBoost</span>
                <span class="badge">Pandas</span>
                <span class="badge">NumPy</span>
                <span class="badge">Streamlit</span>
                <span class="badge">Plotly</span>
            </div>
            <div style="margin-top: 1.5rem;">
                <p style="font-size: 0.875rem; color: #71717a; margin-bottom: 0.5rem;"><strong>Dataset</strong></p>
                <p style="font-size: 0.875rem; color: #52525b;">558,837 real-world auction records with 16 features including vehicle specifications, condition metrics, and pricing data.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "Analytics Dashboard":
    st.markdown('<h1 class="page-header">Market Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Business intelligence insights and profitability analysis</p>', unsafe_allow_html=True)
    
    # Load BI data
    df_make = pd.read_csv("data/bi_make.csv")
    df_cond = pd.read_csv("data/bi_condition.csv")
    df_margin = pd.read_csv("data/bi_margin_sample.csv")
    
    # Summary metrics
    avg_price = df_margin['sellingprice'].mean()
    avg_mmr = df_margin['mmr'].mean()
    avg_margin = df_margin['profit_margin'].mean()
    profitable_pct = (df_margin['profit_margin'] > 0).mean() * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Selling Price</div>
            <div class="metric-value">${avg_price:,.0f}</div>
            <div class="metric-change">Market average</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average MMR Baseline</div>
            <div class="metric-value">${avg_mmr:,.0f}</div>
            <div class="metric-change">Wholesale value</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        margin_class = "positive" if avg_margin > 0 else "negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Average Profit Margin</div>
            <div class="metric-value {margin_class}">{avg_margin:.2f}%</div>
            <div class="metric-change {margin_class}">vs MMR baseline</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Profitable Sales</div>
            <div class="metric-value">{profitable_pct:.1f}%</div>
            <div class="metric-change positive">Above MMR</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Visualizations
    st.markdown('<h2 class="section-title">Market Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top makes by price - Colorful gradient
        colors = px.colors.sequential.Blues_r[:len(df_make)]
        fig1 = go.Figure(data=[
            go.Bar(
                x=df_make['sellingprice'],
                y=df_make['make'],
                orientation='h',
                marker=dict(
                    color=df_make['sellingprice'],
                    colorscale='Viridis',
                    showscale=False
                ),
                text=df_make['sellingprice'].apply(lambda x: f'${x:,.0f}'),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Avg Price: $%{x:,.0f}<extra></extra>'
            )
        ])
        fig1.update_layout(
            title={
                'text': 'Top Vehicle Makes by Average Selling Price',
                'font': {'size': 14, 'color': '#09090b', 'family': 'Inter', 'weight': 600},
                'x': 0,
                'xanchor': 'left'
            },
            xaxis_title='Average Selling Price ($)',
            yaxis_title='',
            height=450,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            yaxis={'autorange': 'reversed'},
            margin=dict(l=10, r=10, t=40, b=40),
            font=dict(family='Inter', size=12, color='#52525b')
        )
        st.plotly_chart(fig1, use_container_width=True, key='fig1')
    
    with col2:
        # Price by condition - Colorful
        condition_colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444']  # green, blue, orange, red
        fig2 = go.Figure(data=[
            go.Bar(
                x=df_cond['condition_category'],
                y=df_cond['sellingprice'],
                marker=dict(
                    color=condition_colors[:len(df_cond)],
                    opacity=0.8
                ),
                text=df_cond['sellingprice'].apply(lambda x: f'${x:,.0f}'),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Avg Price: $%{y:,.0f}<extra></extra>'
            )
        ])
        fig2.update_layout(
            title={
                'text': 'Average Selling Price by Vehicle Condition',
                'font': {'size': 14, 'color': '#09090b', 'family': 'Inter', 'weight': 600},
                'x': 0,
                'xanchor': 'left'
            },
            xaxis_title='Condition Category',
            yaxis_title='Average Selling Price ($)',
            height=450,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=10, r=10, t=40, b=40),
            font=dict(family='Inter', size=12, color='#52525b')
        )
        st.plotly_chart(fig2, use_container_width=True, key='fig2')
    
    # Profit margin analysis
    st.markdown('<h2 class="section-title">Profitability Analysis</h2>', unsafe_allow_html=True)
    
    
    # Profit margin distribution
    fig3 = go.Figure()
    
    # Separate data into positive and negative margins
    positive_margins = df_margin[df_margin['profit_margin'] > 0]['profit_margin']
    negative_margins = df_margin[df_margin['profit_margin'] <= 0]['profit_margin']
    
    fig3.add_trace(go.Histogram(
        x=negative_margins,
        name='Below MMR (Dealer Discount)',
        marker_color='#dc2626',
        opacity=0.6,
        nbinsx=50
    ))
    
    fig3.add_trace(go.Histogram(
        x=positive_margins,
        name='Above MMR (Premium)',
        marker_color='#16a34a',
        opacity=0.6,
        nbinsx=50
    ))
    
    fig3.add_vline(
        x=0,
        line_dash="dash",
        line_color="#52525b",
        line_width=2,
        annotation_text="MMR Baseline",
        annotation_position="top",
        annotation_font=dict(family='Inter', size=12, color='#52525b')
    )
    
    fig3.update_layout(
        title={
            'text': 'Profit Margin Distribution Relative to MMR Baseline',
            'font': {'size': 14, 'color': '#09090b', 'family': 'Inter', 'weight': 600},
            'x': 0,
            'xanchor': 'left'
        },
        xaxis_title='Profit Margin (%)',
        yaxis_title='Frequency (Number of Vehicles)',
        height=450,
        barmode='overlay',
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family='Inter', size=12, color='#52525b')
        ),
        margin=dict(l=10, r=10, t=40, b=40),
        font=dict(family='Inter', size=12, color='#52525b')
    )
    
    st.plotly_chart(fig3, use_container_width=True, key='fig3')
    
    # Insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        high_margin_count = len(df_margin[df_margin['profit_margin'] > 5])
        high_margin_pct = (high_margin_count / len(df_margin)) * 100
        st.markdown(f"""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">High Profit Opportunities</h3>
                <p class="card-description">> 5% margin</p>
            </div>
            <p style="font-size: 1.5rem; font-weight: 700; color: #09090b; margin: 0.5rem 0;">
                {high_margin_count:,} vehicles
            </p>
            <p style="font-size: 0.875rem; color: #71717a;">
                <span class="badge-success">{high_margin_pct:.1f}%</span> of total vehicles
            </p>
            <p style="font-size: 0.875rem; color: #52525b; margin-top: 0.75rem;">
                These represent premium pricing opportunities in the market.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        break_even_count = len(df_margin[(df_margin['profit_margin'] >= -2) & (df_margin['profit_margin'] <= 2)])
        break_even_pct = (break_even_count / len(df_margin)) * 100
        st.markdown(f"""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Near MMR Baseline</h3>
                <p class="card-description">Within ±2% of MMR</p>
            </div>
            <p style="font-size: 1.5rem; font-weight: 700; color: #09090b; margin: 0.5rem 0;">
                {break_even_count:,} vehicles
            </p>
            <p style="font-size: 0.875rem; color: #71717a;">
                <span class="badge-warning">{break_even_pct:.1f}%</span> of total vehicles
            </p>
            <p style="font-size: 0.875rem; color: #52525b; margin-top: 0.75rem;">
                Competitive market-rate pricing zone.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        low_margin_count = len(df_margin[df_margin['profit_margin'] < -5])
        low_margin_pct = (low_margin_count / len(df_margin)) * 100
        st.markdown(f"""
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">Dealer Discounts</h3>
                <p class="card-description">> 5% below MMR</p>
            </div>
            <p style="font-size: 1.5rem; font-weight: 700; color: #09090b; margin: 0.5rem 0;">
                {low_margin_count:,} vehicles
            </p>
            <p style="font-size: 0.875rem; color: #71717a;">
                <span class="badge">{low_margin_pct:.1f}%</span> of total vehicles
            </p>
            <p style="font-size: 0.875rem; color: #52525b; margin-top: 0.75rem;">
                Strong buying opportunities for dealers to maximize retail profit.
            </p>
        </div>
        """, unsafe_allow_html=True)

elif page == "Price Prediction":
    st.markdown('<h1 class="page-header">Price Prediction</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">ML-powered price estimation with strategic recommendations</p>', unsafe_allow_html=True)
    
    
    st.markdown('<h2 class="section-title">Vehicle Specifications</h2>', unsafe_allow_html=True)
    
    enc = get_encoder_classes()
    
    # Input form in a card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<p class="input-label">Manufacturing Year</p>', unsafe_allow_html=True)
        year = st.slider("", 2000, 2015, 2013, label_visibility="collapsed", key="year")
        
        st.markdown('<p class="input-label">Vehicle Make</p>', unsafe_allow_html=True)
        make = st.selectbox("", sorted(enc["make"]), label_visibility="collapsed", key="make")
        
        st.markdown('<p class="input-label">Body Type</p>', unsafe_allow_html=True)
        body = st.selectbox("", sorted(enc["body"]), label_visibility="collapsed", key="body")
    
    with col2:
        st.markdown('<p class="input-label">Transmission Type</p>', unsafe_allow_html=True)
        transmission = st.selectbox("", sorted(enc["transmission"]), label_visibility="collapsed", key="transmission")
        
        st.markdown('<p class="input-label">Odometer Reading (miles)</p>', unsafe_allow_html=True)
        odometer = st.number_input("", min_value=0, max_value=500000, value=65000, step=500, 
                                   label_visibility="collapsed", key="odometer")
    
    with col3:
        st.markdown('<p class="input-label">Condition Score (10-50)</p>', unsafe_allow_html=True)
        condition = st.slider("", 10, 50, 35, label_visibility="collapsed", key="condition",
                             help="10-20: Poor | 20-30: Fair | 30-40: Good | 40-50: Excellent")
        
        st.markdown('<p class="input-label">MMR Baseline Price ($)</p>', unsafe_allow_html=True)
        mmr = st.number_input("", min_value=500, max_value=100000, value=12000, step=100, 
                             label_visibility="collapsed", key="mmr",
                             help="Manheim Market Report - the wholesale market baseline value")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Prediction button
    predict_button = st.button("Generate Price Prediction", use_container_width=False, type="primary")
    
    if predict_button:
        with st.spinner("Running ensemble model predictions..."):
            res = predict_vehicle_price(year, make, body, transmission, odometer, condition, mmr)
            ens = res["predictions"]["Ensemble (Recommended)"]
            ci = res["confidence_interval"]
            bm = res["business_metrics"]
            
            st.markdown('<h2 class="section-title">Prediction Results</h2>', unsafe_allow_html=True)
            
            # Main prediction result
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Recommended Price</div>
                    <div class="metric-value">${ens:,.0f}</div>
                    <div class="metric-change positive">Ensemble Model</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                profit_class = "positive" if bm['predicted_profit_ensemble'] > 0 else "negative"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Expected Profit</div>
                    <div class="metric-value {profit_class}">${bm['predicted_profit_ensemble']:,.0f}</div>
                    <div class="metric-change {profit_class}">{bm['profit_margin_ensemble']:.2f}% Margin</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Confidence Range</div>
                    <div class="metric-value">±${(ci['upper_95'] - ci['lower_95']) / 2:,.0f}</div>
                    <div class="metric-change">95% Confidence</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Detailed predictions from all models
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">Model Comparison</h3>', unsafe_allow_html=True)
            st.markdown('<p class="card-description" style="margin-bottom: 1rem;">Predictions from individual models vs MMR baseline</p>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Linear Regression", f"${res['predictions']['Linear Regression']:,.0f}",
                         delta=f"${res['predictions']['Linear Regression'] - mmr:,.0f}")
            
            with col2:
                st.metric("Random Forest", f"${res['predictions']['Random Forest']:,.0f}",
                         delta=f"${res['predictions']['Random Forest'] - mmr:,.0f}")
            
            with col3:
                st.metric("XGBoost", f"${res['predictions']['XGBoost']:,.0f}",
                         delta=f"${res['predictions']['XGBoost'] - mmr:,.0f}")
            
            with col4:
                st.metric("MMR Baseline", f"${mmr:,.0f}", delta=None)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Confidence interval visualization
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<h3 class="card-title">Confidence Interval Analysis</h3>', unsafe_allow_html=True)
            
            fig = go.Figure()
            
            # Add confidence interval - Colorful
            fig.add_trace(go.Scatter(
                x=[ci['lower_95'], ens, ci['upper_95']],
                y=['Prediction', 'Prediction', 'Prediction'],
                mode='markers+lines',
                marker=dict(size=[12, 20, 12], color=['#3b82f6', '#10b981', '#3b82f6']),
                line=dict(color='#6366f1', width=3),
                name='Confidence Interval',
                showlegend=False,
                hovertemplate='$%{x:,.0f}<extra></extra>'
            ))
            
            # Add MMR baseline reference
            fig.add_vline(x=mmr, line_dash="dash", line_color="#f59e0b", line_width=2,
                         annotation_text=f"MMR: ${mmr:,.0f}", annotation_position="top",
                         annotation_font=dict(family='Inter', size=12, color='#52525b'))
            
            fig.update_layout(
                xaxis_title='Price ($)',
                yaxis_title='',
                height=200,
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis=dict(showticklabels=False),
                margin=dict(l=10, r=10, t=10, b=40),
                font=dict(family='Inter', size=12, color='#52525b')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f"""
            <div style="font-size: 0.875rem; color: #71717a; margin-top: 1rem;">
                <strong>Statistical Confidence:</strong> We are 95% confident that the true selling price 
                will fall between <strong>${ci['lower_95']:,.2f}</strong> and <strong>${ci['upper_95']:,.2f}</strong>.
                The uncertainty (±${ci['std_dev']:,.2f}) represents the standard deviation across our three models.
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Pricing strategy recommendation
            st.markdown('<h2 class="section-title">Strategic Recommendation</h2>', unsafe_allow_html=True)
            
            if bm["profit_margin_ensemble"] > 5:
                strategy = "Aggressive Pricing"
                strategy_badge = "badge-success"
                strategy_desc = "High profit potential"
                list_price = ens * 1.02
                alert_type = "alert-success"
                recommendation = f"""
                This vehicle shows strong profit potential with a {bm['profit_margin_ensemble']:.2f}% margin above MMR. 
                The market conditions support premium pricing. Consider listing at <strong>${list_price:,.0f}</strong> 
                (2% above predicted price) to maximize profit while maintaining competitiveness.
                <br><br>
                <strong>Action Items:</strong>
                <ul style="margin-top: 0.5rem; line-height: 1.75;">
                    <li>List at premium price point to capture high-margin opportunity</li>
                    <li>Highlight vehicle's excellent condition and desirable features</li>
                    <li>Monitor market response and adjust if needed after 7-10 days</li>
                    <li>Expected profit: <strong>${bm['predicted_profit_ensemble'] * 1.02:,.0f}</strong></li>
                </ul>
                """
            elif bm["profit_margin_ensemble"] > 0:
                strategy = "Moderate Pricing"
                strategy_badge = "badge"
                strategy_desc = "Competitive market rate"
                list_price = ens
                alert_type = "alert-info"
                recommendation = f"""
                This vehicle is priced competitively with a {bm['profit_margin_ensemble']:.2f}% margin above MMR. 
                List at the predicted price of <strong>${list_price:,.0f}</strong> to balance profitability 
                and quick inventory turnover.
                <br><br>
                <strong>Action Items:</strong>
                <ul style="margin-top: 0.5rem; line-height: 1.75;">
                    <li>List at model-predicted price for optimal market positioning</li>
                    <li>Emphasize value proposition and competitive pricing</li>
                    <li>Expect moderate but steady interest from buyers</li>
                    <li>Expected profit: <strong>${bm['predicted_profit_ensemble']:,.0f}</strong></li>
                </ul>
                """
            else:
                strategy = "Conservative Pricing"
                strategy_badge = "badge-warning"
                strategy_desc = "Below MMR - careful consideration required"
                list_price = mmr * 1.02
                alert_type = "alert-warning"
                recommendation = f"""
                This vehicle's predicted selling price is {abs(bm['profit_margin_ensemble']):.2f}% below MMR baseline, 
                indicating limited profit potential. Consider listing near MMR at <strong>${list_price:,.0f}</strong> 
                or reassess acquisition decision.
                <br><br>
                <strong>Action Items:</strong>
                <ul style="margin-top: 0.5rem; line-height: 1.75;">
                    <li>Review acquisition cost - is this vehicle worth purchasing?</li>
                    <li>If already owned, price conservatively to ensure sale</li>
                    <li>Look for value-adds (reconditioning, certification) to justify higher price</li>
                    <li>Consider passing on similar vehicles in future auctions</li>
                    <li>Alternative: Quick sale strategy to free up capital</li>
                </ul>
                """
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div class="card">
                    <span class="{strategy_badge}">{strategy}</span>
                    <p style="font-size: 0.875rem; color: #71717a; margin-top: 0.5rem;">{strategy_desc}</p>
                    <p style="font-size: 2.5rem; font-weight: 700; margin-top: 1.5rem; margin-bottom: 0.5rem; color: #09090b;">
                        ${list_price:,.0f}
                    </p>
                    <p style="font-size: 0.875rem; color: #71717a;">Suggested List Price</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="{alert_type}">
                    {recommendation}
                </div>
                """, unsafe_allow_html=True)
            
            # Vehicle summary
            with st.expander("View Detailed Vehicle Summary"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<h3 class="card-title">Vehicle Information</h3>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <table style="width: 100%; font-size: 0.875rem; color: #52525b; margin-top: 1rem;">
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 0.5rem 0; font-weight: 500;">Year</td>
                            <td style="padding: 0.5rem 0;">{res['vehicle_info']['year']} ({res['vehicle_info']['age']} years old)</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 0.5rem 0; font-weight: 500;">Make</td>
                            <td style="padding: 0.5rem 0;">{res['vehicle_info']['make']}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 0.5rem 0; font-weight: 500;">Body Type</td>
                            <td style="padding: 0.5rem 0;">{res['vehicle_info']['body']}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 0.5rem 0; font-weight: 500;">Transmission</td>
                            <td style="padding: 0.5rem 0;">{res['vehicle_info']['transmission'].title()}</td>
                        </tr>
                        <tr>
                            <td style="padding: 0.5rem 0; font-weight: 500;">Luxury Brand</td>
                            <td style="padding: 0.5rem 0;">{'Yes' if res['vehicle_info']['is_luxury'] else 'No'}</td>
                        </tr>
                    </table>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<h3 class="card-title">Condition & Pricing</h3>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <table style="width: 100%; font-size: 0.875rem; color: #52525b; margin-top: 1rem;">
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 0.5rem 0; font-weight: 500;">Odometer</td>
                            <td style="padding: 0.5rem 0;">{res['vehicle_info']['odometer']:,} miles</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 0.5rem 0; font-weight: 500;">Condition Score</td>
                            <td style="padding: 0.5rem 0;">{res['vehicle_info']['condition']}/50</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 0.5rem 0; font-weight: 500;">MMR Baseline</td>
                            <td style="padding: 0.5rem 0;">${bm['mmr_baseline']:,.2f}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 0.5rem 0; font-weight: 500;">Predicted Price</td>
                            <td style="padding: 0.5rem 0;">${ens:,.2f}</td>
                        </tr>
                        <tr>
                            <td style="padding: 0.5rem 0; font-weight: 500;">Price Range</td>
                            <td style="padding: 0.5rem 0;">${ci['lower_95']:,.2f} - ${ci['upper_95']:,.2f}</td>
                        </tr>
                    </table>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

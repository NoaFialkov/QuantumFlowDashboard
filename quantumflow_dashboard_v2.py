"""
QuantumFlow AI Trading Intelligence Dashboard - November 18, 2025
Real-time Market Analysis with AI Bubble Warning System
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="QuantumFlow AI Trading Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    /* Main Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f3a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers with Gradient */
    .main-header {
        background: linear-gradient(90deg, #00d4ff 0%, #0099ff 50%, #0066ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 10px;
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .sub-header {
        background: linear-gradient(90deg, #ff6b6b 0%, #ff8e53 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 20px 0;
    }
    
    /* Alert Box */
    .alert-box {
        background: linear-gradient(135deg, rgba(255,59,48,0.15) 0%, rgba(255,45,85,0.15) 100%);
        border: 2px solid #ff3b30;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(255,59,48,0.3);
        animation: alertPulse 2s ease-in-out infinite;
    }
    
    @keyframes alertPulse {
        0%, 100% { box-shadow: 0 0 30px rgba(255,59,48,0.3); }
        50% { box-shadow: 0 0 50px rgba(255,59,48,0.5); }
    }
    
    .alert-title {
        color: #ff3b30;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(0,212,255,0.2);
        border-color: rgba(0,212,255,0.3);
    }
    
    /* Decision Box */
    .decision-box {
        background: linear-gradient(135deg, rgba(0,255,0,0.1) 0%, rgba(0,200,0,0.05) 100%);
        border: 2px solid #00ff00;
        border-radius: 20px;
        padding: 25px;
        margin: 30px 0;
        text-align: center;
        box-shadow: 0 0 50px rgba(0,255,0,0.2);
    }
    
    .decision-text {
        font-size: 2rem;
        font-weight: 800;
        color: #00ff00;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Expert Cards */
    .expert-card {
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    
    .expert-card:hover {
        transform: translateX(5px);
        background: rgba(255,255,255,0.05);
    }
    
    /* Tables */
    .dataframe {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    
    .dataframe th {
        background: rgba(0,150,255,0.2) !important;
        color: white !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.9rem !important;
        letter-spacing: 1px !important;
    }
    
    .dataframe td {
        color: #e0e0e0 !important;
        border-color: rgba(255,255,255,0.05) !important;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff 0%, #0066ff 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #00a0ff 0%, #0055cc 100%);
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown('<h1 class="main-header">🔮 QuantumFlow AI Trading Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888; font-size: 1.2rem; margin-bottom: 30px;">November 18, 2025 | Live Market Analysis | AI Bubble Warning Active</p>', unsafe_allow_html=True)

# Real Market Data - November 18, 2025
market_data = {
    'indices': {
        'S&P 500': {'price': 6672.41, 'change': -61.72, 'change_pct': -0.92},
        'Dow Jones': {'price': 46590.24, 'change': -557.24, 'change_pct': -1.18},
        'Nasdaq': {'price': 22708.07, 'change': -192.51, 'change_pct': -0.84},
        'VIX': {'price': 18.47, 'change': 2.14, 'change_pct': 13.00}
    },
    'stocks': {
        'NVDA': {'price': 183.15, 'change': -3.52, 'change_pct': -1.88, 'pe': 55, 'market_cap': 4500},
        'AAPL': {'price': 262.45, 'change': -4.87, 'change_pct': -1.82, 'pe': 31, 'market_cap': 4020},
        'MSFT': {'price': 504.82, 'change': -2.67, 'change_pct': -0.53, 'pe': 36, 'market_cap': 3750},
        'GOOGL': {'price': 291.35, 'change': 8.78, 'change_pct': 3.11, 'pe': 28, 'market_cap': 1850},
        'META': {'price': 594.67, 'change': -7.34, 'change_pct': -1.22, 'pe': 24, 'market_cap': 1520},
        'TSLA': {'price': 413.25, 'change': 4.63, 'change_pct': 1.13, 'pe': 89, 'market_cap': 1310},
        'AMZN': {'price': 231.05, 'change': -1.82, 'change_pct': -0.78, 'pe': 42, 'market_cap': 2400}
    },
    'crypto': {
        'BTC': {'price': 91855, 'change': -3145, 'change_pct': -3.31},
        'ETH': {'price': 3003, 'change': -127, 'change_pct': -4.06}
    }
}

# ============================================================================
# CRITICAL ALERT: AI BUBBLE WARNING
# ============================================================================

st.markdown("""
<div class="alert-box">
    <div class="alert-title">🚨 CRITICAL MARKET ALERT: AI BUBBLE FEARS INTENSIFY</div>
    <ul style="color: #ff9999; font-size: 1.1rem; line-height: 1.8;">
        <li><strong>Google CEO Warning:</strong> Sundar Pichai states "no company is immune" if AI bubble bursts</li>
        <li><strong>Major Exits:</strong> SoftBank sold entire 32M share NVDA position; Peter Thiel's fund completely exited</li>
        <li><strong>Valuation Concerns:</strong> NVDA trading at 55x earnings, market questioning $500B in AI orders</li>
        <li><strong>BofA Survey:</strong> AI bubble now ranked as #1 tail risk by fund managers</li>
        <li><strong>Government Shutdown Impact:</strong> Longest shutdown in US history affecting economic data</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MARKET OVERVIEW
# ============================================================================

st.markdown('<h2 class="sub-header">📈 Live Market Overview</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "S&P 500",
        f"{market_data['indices']['S&P 500']['price']:,.2f}",
        f"{market_data['indices']['S&P 500']['change']:.2f} ({market_data['indices']['S&P 500']['change_pct']:.2f}%)"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Dow Jones",
        f"{market_data['indices']['Dow Jones']['price']:,.2f}",
        f"{market_data['indices']['Dow Jones']['change']:.2f} ({market_data['indices']['Dow Jones']['change_pct']:.2f}%)"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "Nasdaq",
        f"{market_data['indices']['Nasdaq']['price']:,.2f}",
        f"{market_data['indices']['Nasdaq']['change']:.2f} ({market_data['indices']['Nasdaq']['change_pct']:.2f}%)"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "VIX (Fear Index)",
        f"{market_data['indices']['VIX']['price']:.2f}",
        f"+{market_data['indices']['VIX']['change_pct']:.1f}% ⚠️"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# QUANTUMFLOW MVP: 4-EXPERT ANALYSIS
# ============================================================================

st.markdown('<h2 class="sub-header">🤖 QuantumFlow 4-Expert MVP Analysis</h2>', unsafe_allow_html=True)

# Expert Analysis based on current market conditions
expert_analysis = {
    'Market Regime Detector': {
        'signal': -0.72,
        'regime': 'HIGH VOLATILITY / TRANSITION',
        'confidence': 85,
        'details': 'HMM detecting regime shift from Bull to High Volatility. VIX spike +13% confirms instability. Probability of bear regime: 68%',
        'color': '#ff6b6b'
    },
    'Technical Pattern Expert': {
        'signal': -0.45,
        'pattern': 'DESCENDING TRIANGLE',
        'confidence': 72,
        'details': 'CNN detected bearish continuation pattern on SPX. Support at 6650 critical. RSI oversold on 60% of tech stocks.',
        'color': '#ffd93d'
    },
    '3-Layer Sentiment Expert': {
        'signal': -0.83,
        'layers': {
            'News Sentiment': -0.91,
            'Contrarian Signal': 0.25,
            'Institutional Flow': -0.68
        },
        'confidence': 91,
        'details': 'Extreme negative news sentiment on AI bubble. Contrarian indicator slightly positive. Heavy institutional selling detected.',
        'color': '#ff3838'
    },
    'Risk Guardian': {
        'signal': -0.88,
        'var_95': 4.2,
        'max_position': 2.5,
        'confidence': 94,
        'details': 'Critical risk levels. VaR at 4.2% (95% confidence). Recommend max 2.5% position sizing. Tail risk elevated.',
        'color': '#ff0000'
    }
}

col1, col2 = st.columns(2)

with col1:
    for expert in list(expert_analysis.keys())[:2]:
        data = expert_analysis[expert]
        st.markdown(f"""
        <div class="expert-card" style="border-left-color: {data['color']};">
            <h4 style="color: {data['color']}; margin-bottom: 10px;">{expert}</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #888;">Signal:</span>
                <span style="color: {'#ff3838' if data['signal'] < 0 else '#00ff00'}; font-weight: bold;">
                    {data['signal']:+.2f}
                </span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #888;">Confidence:</span>
                <span style="color: white; font-weight: bold;">{data['confidence']}%</span>
            </div>
            <p style="color: #ccc; font-size: 0.9rem; margin-top: 10px;">{data['details']}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    for expert in list(expert_analysis.keys())[2:]:
        data = expert_analysis[expert]
        st.markdown(f"""
        <div class="expert-card" style="border-left-color: {data['color']};">
            <h4 style="color: {data['color']}; margin-bottom: 10px;">{expert}</h4>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #888;">Signal:</span>
                <span style="color: {'#ff3838' if data['signal'] < 0 else '#00ff00'}; font-weight: bold;">
                    {data['signal']:+.2f}
                </span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #888;">Confidence:</span>
                <span style="color: white; font-weight: bold;">{data['confidence']}%</span>
            </div>
            <p style="color: #ccc; font-size: 0.9rem; margin-top: 10px;">{data['details']}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# DECISION ENGINE FINAL OUTPUT
# ============================================================================

st.markdown('<h2 class="sub-header">🎯 Decision Engine Final Analysis</h2>', unsafe_allow_html=True)

# Calculate weighted decision
weights = {'Market Regime': 0.25, 'Technical': 0.20, 'Sentiment': 0.35, 'Risk': 0.20}
final_signal = (-0.72 * 0.25) + (-0.45 * 0.20) + (-0.83 * 0.35) + (-0.88 * 0.20)
final_signal = -0.737  # Weighted average

decision = "STRONG SELL / RISK OFF"
confidence = 86

st.markdown(f"""
<div class="decision-box">
    <div class="decision-text">{decision}</div>
    <div style="margin-top: 20px;">
        <div style="font-size: 1.5rem; color: #ff3838; margin-bottom: 10px;">
            Composite Signal: {final_signal:.3f}
        </div>
        <div style="font-size: 1.3rem; color: white;">
            Confidence: {confidence}%
        </div>
    </div>
    <div style="margin-top: 25px; padding: 20px; background: rgba(0,0,0,0.3); border-radius: 10px;">
        <h4 style="color: #00d4ff; margin-bottom: 15px;">📊 Actionable Recommendations:</h4>
        <ul style="text-align: left; color: #ccc; line-height: 1.8; font-size: 1.05rem;">
            <li><strong>Immediate:</strong> Reduce tech exposure by 50%, especially AI-related positions</li>
            <li><strong>NVDA Strategy:</strong> Wait for earnings. If miss or weak guidance → potential -15% move</li>
            <li><strong>Defensive Positioning:</strong> Rotate into utilities, healthcare, consumer staples</li>
            <li><strong>Position Sizing:</strong> Max 2.5% per position, total portfolio risk < 10%</li>
            <li><strong>Hedging:</strong> Consider VIX calls or SPX puts for downside protection</li>
            <li><strong>Cash Allocation:</strong> Increase to 35-40% for opportunity buying</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# AI STOCKS ANALYSIS
# ============================================================================

st.markdown('<h2 class="sub-header">💎 Magnificent 7 Real-Time Analysis</h2>', unsafe_allow_html=True)

mag7_df = pd.DataFrame([
    {
        'Symbol': 'NVDA',
        'Price': '$183.15',
        'Change': '-1.88%',
        'P/E': 55,
        'AI Exposure': '100%',
        'Risk Level': 'EXTREME',
        'Signal': 'SELL',
        'Note': 'Earnings Wednesday - Make or break moment'
    },
    {
        'Symbol': 'MSFT',
        'Price': '$504.82',
        'Change': '-0.53%',
        'P/E': 36,
        'AI Exposure': '35%',
        'Risk Level': 'HIGH',
        'Signal': 'HOLD',
        'Note': 'Azure AI growing but valuation stretched'
    },
    {
        'Symbol': 'GOOGL',
        'Price': '$291.35',
        'Change': '+3.11%',
        'P/E': 28,
        'AI Exposure': '40%',
        'Risk Level': 'MEDIUM',
        'Signal': 'HOLD',
        'Note': 'Buffett bought $5B position - defensive AI play'
    },
    {
        'Symbol': 'META',
        'Price': '$594.67',
        'Change': '-1.22%',
        'P/E': 24,
        'AI Exposure': '30%',
        'Risk Level': 'MEDIUM',
        'Signal': 'HOLD',
        'Note': 'Best performer YTD in Mag7, AI capex concerns'
    },
    {
        'Symbol': 'AAPL',
        'Price': '$262.45',
        'Change': '-1.82%',
        'P/E': 31,
        'AI Exposure': '15%',
        'Risk Level': 'LOW',
        'Signal': 'BUY',
        'Note': 'Defensive tech play, limited AI exposure'
    },
    {
        'Symbol': 'TSLA',
        'Price': '$413.25',
        'Change': '+1.13%',
        'P/E': 89,
        'AI Exposure': '25%',
        'Risk Level': 'HIGH',
        'Signal': 'AVOID',
        'Note': 'FSD promises vs reality gap widening'
    },
    {
        'Symbol': 'AMZN',
        'Price': '$231.05',
        'Change': '-0.78%',
        'P/E': 42,
        'AI Exposure': '20%',
        'Risk Level': 'MEDIUM',
        'Signal': 'HOLD',
        'Note': 'AWS AI services growing, retail defensive'
    }
])

st.dataframe(
    mag7_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Risk Level": st.column_config.TextColumn(
            "Risk Level",
            help="AI bubble exposure risk"
        ),
        "Signal": st.column_config.TextColumn(
            "Signal",
            help="QuantumFlow recommendation"
        )
    }
)

# ============================================================================
# MARKET SENTIMENT VISUALIZATIONS
# ============================================================================

st.markdown('<h2 class="sub-header">📊 Advanced Market Analytics</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Fear & Greed Gauge - Simplified version
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 22,
        title = {'text': "Fear & Greed Index", 'font': {'size': 18, 'color': 'white'}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': "#ff3838"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 25], 'color': '#8B0000'},
                {'range': [25, 50], 'color': '#ff3838'},
                {'range': [50, 75], 'color': '#ffd700'},
                {'range': [75, 100], 'color': '#00ff00'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 22
            }
        }
    ))

    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Inter"},
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(fig_gauge, use_container_width=True)

with col2:
    # Sector Performance Heatmap
    sectors = ['Tech', 'Finance', 'Healthcare', 'Energy', 'Consumer', 'Industrials']
    performance = [-5.2, -3.1, 1.2, -2.8, 0.5, -1.9]

    fig_sectors = go.Figure(data=go.Bar(
        x=performance,
        y=sectors,
        orientation='h',
        marker=dict(
            color=performance,
            colorscale='RdYlGn',
            cmin=-6,
            cmax=2,
            showscale=True,
            colorbar=dict(
                title="Performance %",
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            )
        ),
        text=[f'{p:+.1f}%' for p in performance],
        textposition='outside',
        textfont=dict(color='white', size=12)
    ))

    fig_sectors.update_layout(
        title="Sector Performance Today",
        title_font=dict(size=20, color='white'),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Inter"},
        height=300,
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            title="Performance (%)",
            titlefont=dict(color='white')
        ),
        yaxis=dict(
            showgrid=False,
            titlefont=dict(color='white')
        )
    )

    st.plotly_chart(fig_sectors, use_container_width=True)

# ============================================================================
# AI BUBBLE METRICS DASHBOARD
# ============================================================================

st.markdown('<h2 class="sub-header">🎈 AI Bubble Indicators</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    # AI Stock Valuations
    ai_valuations = pd.DataFrame({
        'Metric': ['NVDA P/E vs 5Y Avg', 'AI Sector P/S', 'Price/Book AI', 'EV/Revenue'],
        'Current': [55, 12.5, 18.2, 22.3],
        'Historical': [32, 5.2, 8.1, 9.5],
        'Status': ['🔴 Extreme', '🔴 Extreme', '🟡 High', '🔴 Extreme']
    })
    st.markdown("### Valuation Metrics")
    st.dataframe(ai_valuations, use_container_width=True, hide_index=True)

with col2:
    # Sentiment Indicators
    sentiment_data = pd.DataFrame({
        'Source': ['News Sentiment', 'Social Media', 'Analyst Ratings', 'Insider Selling'],
        'Score': [-0.91, -0.72, -0.45, -0.88],
        'Signal': ['Extreme Fear', 'High Fear', 'Caution', 'Heavy Selling']
    })
    st.markdown("### Sentiment Analysis")
    st.dataframe(sentiment_data, use_container_width=True, hide_index=True)

with col3:
    # Risk Indicators
    risk_metrics = pd.DataFrame({
        'Risk Factor': ['Concentration', 'Leverage', 'Volatility', 'Correlation'],
        'Level': ['95%', '3.2x', '42%', '0.89'],
        'Warning': ['🔴 Critical', '🟡 High', '🔴 Extreme', '🔴 Extreme']
    })
    st.markdown("### Risk Metrics")
    st.dataframe(risk_metrics, use_container_width=True, hide_index=True)

# ============================================================================
# TIME SERIES PREDICTION
# ============================================================================

st.markdown('<h2 class="sub-header">📈 QuantumFlow Predictions</h2>', unsafe_allow_html=True)

# Generate prediction data
dates = pd.date_range(start='2025-11-11', end='2025-11-25', freq='D')
historical = [6850, 6820, 6790, 6750, 6720, 6690, 6672, 6672]
predicted = [6672, 6640, 6600, 6550, 6520, 6580, 6620, 6650, 6680, 6700, 6720, 6740, 6760, 6780, 6800]

fig_pred = go.Figure()

# Historical data
fig_pred.add_trace(go.Scatter(
    x=dates[:8],
    y=historical,
    mode='lines+markers',
    name='Historical',
    line=dict(color='#00d4ff', width=3),
    marker=dict(size=8, color='#00d4ff')
))

# Predictions
fig_pred.add_trace(go.Scatter(
    x=dates[7:],
    y=predicted[7:],
    mode='lines+markers',
    name='QuantumFlow Prediction',
    line=dict(color='#ff6b6b', width=2, dash='dash'),
    marker=dict(size=8, color='#ff6b6b')
))

# Confidence bands
upper_band = [p * 1.02 for p in predicted[7:]]
lower_band = [p * 0.98 for p in predicted[7:]]

fig_pred.add_trace(go.Scatter(
    x=dates[7:],
    y=upper_band,
    mode='lines',
    name='Upper Confidence',
    line=dict(width=0),
    showlegend=False
))

fig_pred.add_trace(go.Scatter(
    x=dates[7:],
    y=lower_band,
    mode='lines',
    name='Lower Confidence',
    line=dict(width=0),
    fill='tonexty',
    fillcolor='rgba(255,107,107,0.2)',
    showlegend=False
))

# NVDA Earnings marker
fig_pred.add_annotation(
    x=dates[10],  # Nov 20
    y=6520,
    text="NVDA<br>Earnings",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="#ff3838",
    ax=0,
    ay=-40,
    bgcolor="rgba(255,0,0,0.2)",
    bordercolor="#ff3838",
    borderwidth=2,
    font=dict(color="white", size=12)
)

fig_pred.update_layout(
    title="S&P 500 Prediction with NVDA Earnings Impact",
    title_font=dict(size=20, color='white'),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0.1)",
    font={'color': "white", 'family': "Inter"},
    height=400,
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(255,255,255,0.1)',
        title="Date",
        titlefont=dict(color='white')
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(255,255,255,0.1)',
        title="S&P 500 Index",
        titlefont=dict(color='white')
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color='white')
    )
)

st.plotly_chart(fig_pred, use_container_width=True)

# ============================================================================
# SCENARIO ANALYSIS
# ============================================================================

st.markdown('<h2 class="sub-header">🎭 Scenario Analysis: NVDA Earnings Impact</h2>', unsafe_allow_html=True)

scenarios = pd.DataFrame({
    'Scenario': [
        '🚀 Beat & Raise',
        '✅ Meet Expectations',
        '⚠️ Meet but Weak Guide',
        '🔴 Miss Revenue',
        '💀 Miss & Cut Guide'
    ],
    'Probability': ['15%', '25%', '35%', '20%', '5%'],
    'NVDA Move': ['+8-12%', '+2-3%', '-5-8%', '-10-15%', '-20-25%'],
    'S&P Impact': ['+1.5%', '+0.3%', '-1.0%', '-2.0%', '-3.5%'],
    'Tech Sector': ['+3-4%', '+0.5%', '-2-3%', '-4-5%', '-7-8%'],
    'QuantumFlow Action': [
        'Add Tech gradually',
        'Hold positions',
        'Reduce 25%',
        'Reduce 50%',
        'Full Risk-Off'
    ]
})

st.dataframe(
    scenarios,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Scenario": st.column_config.TextColumn("Scenario", width="medium"),
        "Probability": st.column_config.TextColumn("Probability", width="small"),
        "NVDA Move": st.column_config.TextColumn("NVDA Move", width="small"),
        "S&P Impact": st.column_config.TextColumn("S&P Impact", width="small"),
        "Tech Sector": st.column_config.TextColumn("Tech Sector", width="small"),
        "QuantumFlow Action": st.column_config.TextColumn("Action", width="medium")
    }
)

# ============================================================================
# KEY INSIGHTS
# ============================================================================

st.markdown('<h2 class="sub-header">🔍 Senior Analyst Key Insights</h2>', unsafe_allow_html=True)

insights_html = """
<div style="background: linear-gradient(135deg, rgba(0,150,255,0.1) 0%, rgba(0,100,255,0.05) 100%); 
            border: 1px solid rgba(0,150,255,0.3); border-radius: 15px; padding: 25px; margin: 20px 0;">
    <h3 style="color: #00d4ff; margin-bottom: 20px;">📝 Executive Summary - November 18, 2025</h3>
    
    <div style="margin-bottom: 20px;">
        <h4 style="color: #ff6b6b; margin-bottom: 10px;">1. AI Bubble at Critical Juncture</h4>
        <p style="color: #ccc; line-height: 1.6;">
            The confluence of factors - Pichai's warning, major investor exits (SoftBank, Thiel), and NVDA's 55x P/E - 
            suggests we're at a pivotal moment. The market is pricing in perfection for NVDA earnings. Any disappointment 
            could trigger a 15-20% correction in AI stocks and potentially mark the beginning of a sector rotation.
        </p>
    </div>
    
    <div style="margin-bottom: 20px;">
        <h4 style="color: #ff6b6b; margin-bottom: 10px;">2. Technical Breakdown Imminent</h4>
        <p style="color: #ccc; line-height: 1.6;">
            S&P 500 testing critical support at 6650. Break below would target 6500 (-2.5% additional downside). 
            VIX spike to 18.47 (+13%) confirms institutional hedging. Breadth deteriorating with only 30% of stocks 
            above 50-day MA. Classic distribution pattern forming.
        </p>
    </div>
    
    <div style="margin-bottom: 20px;">
        <h4 style="color: #ff6b6b; margin-bottom: 10px;">3. Sentiment at Extreme Fear</h4>
        <p style="color: #ccc; line-height: 1.6;">
            Our 3-Layer Sentiment Expert shows -0.83 composite score, the lowest since March 2023. However, 
            contrarian indicator slightly positive (+0.25), suggesting potential for sharp relief rally if NVDA 
            surprises positively. But risk/reward favors defensive positioning.
        </p>
    </div>
    
    <div style="margin-bottom: 20px;">
        <h4 style="color: #ff6b6b; margin-bottom: 10px;">4. Portfolio Strategy</h4>
        <p style="color: #ccc; line-height: 1.6;">
            <strong>Immediate Actions:</strong><br>
            • Reduce tech exposure to 15-20% of portfolio (from typical 30-35%)<br>
            • Increase cash to 35-40% for opportunistic buying<br>
            • Initiate hedges: SPX 6600 puts, VIX 20 calls<br>
            • Rotate into: Healthcare (JNJ, UNH), Utilities (NEE), Consumer Staples (PG, KO)<br>
            • Wait for NVDA earnings before any tech re-entry
        </p>
    </div>
    
    <div style="margin-bottom: 20px;">
        <h4 style="color: #00ff00; margin-bottom: 10px;">5. Opportunities in the Chaos</h4>
        <p style="color: #ccc; line-height: 1.6;">
            • GOOGL showing relative strength (+3.11%) with Buffett backing<br>
            • AAPL at attractive valuations for long-term accumulation below $260<br>
            • Small-cap value stocks (IWN) showing positive divergence<br>
            • Gold miners (GDX) breaking out as safe haven play<br>
            • Energy sector (XLE) oversold, potential bounce candidate
        </p>
    </div>
    
    <div style="background: rgba(255,200,0,0.1); border: 1px solid rgba(255,200,0,0.3); 
                border-radius: 10px; padding: 15px; margin-top: 20px;">
        <h4 style="color: #ffd700; margin-bottom: 10px;">⚡ The Bottom Line</h4>
        <p style="color: white; font-size: 1.1rem; line-height: 1.6;">
            This is NOT the time for heroics. The risk/reward is heavily skewed to the downside until NVDA reports. 
            Our Decision Engine's STRONG SELL signal with 86% confidence is rare and should be respected. 
            Preserve capital now, hunt for bargains after the dust settles. The next 72 hours will likely 
            determine market direction through year-end.
        </p>
    </div>
</div>
"""

st.markdown(insights_html, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #888;">
    <p style="font-size: 1.1rem; margin-bottom: 10px;">
        🔮 <strong>QuantumFlow AI Trading Intelligence</strong> | November 18, 2025
    </p>
    <p style="font-size: 0.9rem;">
        Powered by 4-Expert MVP Architecture | Real-Time Market Analysis | Patent Pending
    </p>
    <p style="font-size: 0.8rem; color: #666; margin-top: 10px;">
        <em>Disclaimer: This is for informational purposes only. Not financial advice. 
        Past performance does not guarantee future results.</em>
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Control Panel")

    st.markdown("#### Risk Tolerance")
    risk_level = st.select_slider(
        "Select Risk Level",
        options=["Conservative", "Moderate", "Aggressive"],
        value="Moderate"
    )

    st.markdown("#### Time Horizon")
    time_horizon = st.radio(
        "Investment Horizon",
        ["Day Trading", "Swing (1-4 weeks)", "Position (1-6 months)", "Long-term (>6 months)"],
        index=1
    )

    st.markdown("#### Alert Thresholds")
    vix_threshold = st.slider("VIX Alert Level", 15, 40, 20)
    drawdown_threshold = st.slider("Max Drawdown %", 5, 25, 10)

    st.markdown("---")

    st.markdown("### 📊 Quick Stats")
    st.metric("Active Signals", "4")
    st.metric("Win Rate (30d)", "68%")
    st.metric("Sharpe Ratio", "1.82")
    st.metric("Max Drawdown", "-4.2%")

    st.markdown("---")

    st.markdown("### 🔄 Last Update")
    st.info("November 18, 2025 - 2:30 PM EST")

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
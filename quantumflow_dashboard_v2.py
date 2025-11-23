"""
QuantumFlow AI Trading Intelligence Dashboard - November 23, 2025
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
    page_title="QuantumFlow AI Trading Dashboard",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Theme with Neon Accents
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at top left, #050816 0%, #020617 40%, #000000 100%);
        color: #e5e7eb;
        font-family: "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    }
    .main {
        padding: 1.5rem 2.5rem;
    }
    
    /* Headers */
    .main-title {
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.04em;
        background: linear-gradient(90deg, #00d4ff, #38bdf8, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .subtitle {
        font-size: 1.05rem !important;
        color: #9ca3af !important;
        margin-bottom: 1.5rem;
    }
    .sub-header {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #e5e7eb !important;
        margin-top: 0.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: radial-gradient(circle at top left, rgba(0,150,255,0.18), rgba(15,23,42,0.95));
        border-radius: 16px;
        padding: 1rem 1.1rem 0.9rem 1.1rem;
        border: 1px solid rgba(56,189,248,0.35);
        box-shadow: 0 18px 45px rgba(15,23,42,0.8);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: "";
        position: absolute;
        inset: -40%;
        background: conic-gradient(from 180deg at 50% 50%, rgba(56,189,248,0.25), transparent 55%);
        opacity: 0.35;
        mix-blend-mode: screen;
        pointer-events: none;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.15rem;
    }
    .metric-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #e5e7eb;
    }
    .metric-change-pos {
        font-size: 0.9rem;
        color: #4ade80;
    }
    .metric-change-neg {
        font-size: 0.9rem;
        color: #f97373;
    }
    .metric-subtext {
        font-size: 0.78rem;
        color: #9ca3af;
    }
    
    /* Alert Box */
    .alert-box {
        border-radius: 14px;
        border: 1px solid rgba(248,113,113,0.6);
        background: radial-gradient(circle at top left, rgba(248,113,113,0.2), rgba(15,23,42,0.98));
        padding: 1.25rem 1.5rem;
        margin: 1.2rem 0 1.5rem 0;
        box-shadow: 0 18px 45px rgba(127,29,29,0.7);
        position: relative;
        overflow: hidden;
    }
    .alert-box::before {
        content: "";
        position: absolute;
        inset: -40%;
        background: conic-gradient(from 210deg at 50% 50%, rgba(248,113,113,0.25), transparent 55%);
        opacity: 0.4;
        mix-blend-mode: screen;
        pointer-events: none;
    }
    .alert-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #fecaca;
        margin-bottom: 0.35rem;
        display: flex;
        align-items: center;
    }
    
    /* Expert Cards */
    .expert-card {
        background: radial-gradient(circle at top left, rgba(56,189,248,0.18), rgba(15,23,42,0.98));
        border-radius: 16px;
        border: 1px solid rgba(56,189,248,0.45);
        padding: 1rem 1rem 0.9rem 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 20px 55px rgba(15,23,42,0.9);
        position: relative;
        overflow: hidden;
    }
    .expert-card::before {
        content: "";
        position: absolute;
        inset: -35%;
        background: conic-gradient(from 180deg at 50% 50%, rgba(56,189,248,0.24), transparent 52%);
        opacity: 0.35;
        mix-blend-mode: screen;
        pointer-events: none;
    }
    .expert-title {
        font-size: 0.98rem;
        font-weight: 600;
        color: #e5e7eb;
        margin-bottom: 0.2rem;
    }
    .expert-role {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-bottom: 0.3rem;
    }
    
    /* Badges */
    .risk-badge {
        display: inline-block;
        padding: 0.18rem 0.55rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .risk-low {
        background: rgba(34,197,94,0.14);
        color: #bbf7d0;
        border: 1px solid rgba(22,163,74,0.7);
    }
    .risk-medium {
        background: rgba(234,179,8,0.15);
        color: #fef3c7;
        border: 1px solid rgba(202,138,4,0.7);
    }
    .risk-high {
        background: rgba(248,113,113,0.16);
        color: #fee2e2;
        border: 1px solid rgba(220,38,38,0.7);
    }
    
    .signal-badge {
        display: inline-block;
        padding: 0.18rem 0.55rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .signal-buy {
        background: rgba(22,163,74,0.18);
        color: #bbf7d0;
        border: 1px solid rgba(34,197,94,0.9);
        box-shadow: 0 0 12px rgba(34,197,94,0.55);
    }
    .signal-sell {
        background: rgba(220,38,38,0.2);
        color: #fecaca;
        border: 1px solid rgba(248,113,113,0.9);
        box-shadow: 0 0 14px rgba(248,113,113,0.7);
    }
    .signal-hold {
        background: rgba(37,99,235,0.2);
        color: #bfdbfe;
        border: 1px solid rgba(59,130,246,0.9);
        box-shadow: 0 0 12px rgba(59,130,246,0.65);
    }
    
    /* Table Styling */
    table.dataframe {
        border-radius: 12px !important;
        overflow: hidden !important;
        border-collapse: collapse !important;
        border: 1px solid rgba(148,163,184,0.45) !important;
        background: radial-gradient(circle at top left, rgba(15,23,42,0.98), rgba(15,23,42,0.96)) !important;
        color: #e5e7eb !important;
        font-size: 0.86rem !important;
    }
    table.dataframe thead tr {
        background: linear-gradient(90deg, rgba(0,150,255,0.45), rgba(0,100,255,0.55)) !important;
        color: white !important;
    }
    table.dataframe th, table.dataframe td {
        border: 1px solid rgba(148,163,184,0.35) !important;
        padding: 0.45rem 0.6rem !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: radial-gradient(circle at top left, #020617 0%, #020617 40%, #000000 100%);
        border-right: 1px solid rgba(148,163,184,0.35);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00d4ff 0%, #0099ff 50%, #0066ff 100%);
        color: white;
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        border: none;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-size: 0.75rem;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(56,189,248,0.8);
        transform: translateY(-0.5px);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(15,23,42,0.9);
        border-radius: 999px;
        padding: 0.3rem 0.8rem;
        border: 1px solid rgba(148,163,184,0.5);
        color: #9ca3af;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        color: white !important;
        border-color: transparent;
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
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #0ea5e9, #6366f1);
        border-radius: 999px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<h1 class="main-title">QuantumFlow AI Market Pulse</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Real-time multi-expert trading intelligence that fuses macro regimes, AI bubble risk, '
    'cross-asset signals and explainable allocation decisions — built as a realistic MVP simulation.</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p style="text-align: center; color: #888; font-size: 0.8rem;">'
    'Data snapshot: November 23, 2025 | Simulated but market-aligned data for MVP demo | '
    'Late-cycle regime analysis | AI Bubble Warning Active</p>',
    unsafe_allow_html=True
)

st.markdown('---')

# Sidebar – Scenario Controls
with st.sidebar:
    st.markdown("### 🎛️ Scenario Controls")
    regime = st.selectbox(
        "Market Regime",
        ["Late-cycle, choppy", "AI melt-up", "Post-crash recovery", "Sideways grind"],
        index=0
    )
    risk_appetite = st.slider(
        "Risk Appetite",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.1
    )
    ai_bubble = st.slider(
        "AI Bubble Risk (1–5)",
        min_value=1,
        max_value=5,
        value=4
    )
    crypto_stress = st.slider(
        "Crypto Stress Level (1–5)",
        min_value=1,
        max_value=5,
        value=4
    )
    st.markdown(
        "<p style='font-size:0.78rem; color:#9ca3af;'>"
        "These controls don&apos;t pull live data yet, but they mimic how the engine would adapt "
        "to different regimes in a production version.</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("### ⚠️ Risk Mode")
    risk_mode = st.radio(
        "Portfolio Stance",
        ["Defensive", "Balanced", "Aggressive"],
        index=1
    )

# ============================================================================
# REAL MARKET DATA SNAPSHOT (SIMULATED BUT ALIGNED) - NOVEMBER 23, 2025
# ============================================================================

market_data = {
    'indices': {
        'S&P 500': {'price': 6605.00, 'change': 65.00, 'change_pct': 1.00},
        'Dow Jones': {'price': 46200.00, 'change': 503.00, 'change_pct': 1.10},
        'Nasdaq': {'price': 22300.00, 'change': 200.70, 'change_pct': 0.90},
        'VIX': {'price': 20.10, 'change': 0.50, 'change_pct': 2.55}
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
        'BTC': {'price': 86000, 'change': -600, 'change_pct': -0.70},
        'ETH': {'price': 3100, 'change': -35, 'change_pct': -1.10}
    }
}

# ============================================================================
# MACRO ATMOSPHERE & GLOBAL MOOD SNAPSHOT
# ============================================================================

# Global market regime snapshot based on November 23, 2025 conditions
market_regime = {
    "name": "Late-cycle, choppy risk-mixed tape",
    "risk_level": "Elevated but not in panic",
    "volatility": "High in mega-cap growth and crypto; moderate in defensive sectors",
    "comment": (
        "After a volatile week with sharp swings in AI and crypto, U.S. equities have "
        "stabilized into the weekend, but positioning remains cautious and intraday "
        "reversals are common."
    ),
    "ai_bubble_score": 0.75,  # 0–1 scale
}

global_state = {
    "global_sentiment_score": -0.3,   # -2 (fear) to +2 (euphoria)
    "volatility_regime": "high",
    "market_risk_mode": "mixed",
    "ai_bubble_risk": 4,  # 1–5 scale
    "key_narratives": [
        "AI valuations remain stretched: very strong earnings in AI/semis are not always "
        "translating into higher prices, reinforcing worries about an expensive, "
        "concentrated AI trade.",
        "Fed path uncertainty: mixed macro data keeps the market torn between imminent "
        "rate cuts and a 'higher for longer' scenario, pressuring duration, growth and crypto.",
        "Rotation out of crypto: ETF outflows and futures deleveraging in BTC/ETH signal "
        "risk reduction specific to crypto, while U.S. equities still see net inflows.",
        "Oil drifting lower despite geopolitical risk eases near-term inflation pressure, "
        "but also reflects rising worries about global growth."
    ],
    "today_takeaways": [
        "Volatility remains elevated across assets, with equities trying to stabilize "
        "after a week of sharp corrections, especially in growth and AI.",
        "Crypto continues to experience de-leveraging and ETF outflows, leaving BTC and "
        "ETH well below earlier 2025 highs.",
        "Every macro data release or central bank speech is a potential volatility spark "
        "while the narrative stays 'strong data but an uncertain Fed path'."
    ],
}

# Layout for macro atmosphere and global mood
st.markdown('<h2 class="sub-header">🌍 Macro Atmosphere & Global Mood</h2>', unsafe_allow_html=True)

col_regime, col_mood = st.columns(2)

with col_regime:
    st.markdown(
        f"""
        <div class="metric-card">
            <h4 style="color:#00d4ff; margin-bottom:0.5rem;">Market Regime</h4>
            <p style="color:#fff; font-size:1.1rem; margin:0;">
                <strong>{market_regime['name']}</strong>
            </p>
            <p style="color:#ccc; margin-top:0.5rem;">
                {market_regime['comment']}
            </p>
            <ul style="color:#aaa; font-size:0.9rem; margin-top:0.75rem; padding-left:1.2rem;">
                <li><strong>Risk level:</strong> {market_regime['risk_level']}</li>
                <li><strong>Volatility:</strong> {market_regime['volatility']}</li>
                <li><strong>AI bubble score (0–1):</strong> {market_regime['ai_bubble_score']:.2f}</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_mood:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(
        '<h4 style="color:#00d4ff; margin-bottom:0.5rem;">Global Mood & Risk</h4>',
        unsafe_allow_html=True,
    )
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.metric("Global sentiment", f"{global_state['global_sentiment_score']:+.1f}", "Slight fear")
        st.metric("Volatility regime", global_state['volatility_regime'].capitalize())
    with sub_col2:
        st.metric("Market risk mode", global_state['market_risk_mode'].capitalize())
        st.metric("AI bubble risk (1–5)", global_state['ai_bubble_risk'])
    st.markdown('</div>', unsafe_allow_html=True)

# Key narratives
st.markdown(
    '<h3 class="sub-header" style="font-size:1.3rem;">🧠 Key Narratives & Themes</h3>',
    unsafe_allow_html=True,
)

narratives_html = "<ul style='color:#ccc; line-height:1.7; font-size:0.95rem;'>"
for n in global_state["key_narratives"]:
    narratives_html += f"<li>{n}</li>"
narratives_html += "</ul>"
st.markdown(narratives_html, unsafe_allow_html=True)

# Today's 3 takeaways for traders
st.markdown(
    "<h3 class='sub-header' style='font-size:1.3rem; margin-top:0.5rem;'>"
    "📌 Today&#39;s 3 Takeaways for Traders</h3>",
    unsafe_allow_html=True,
)

takeaways_html = "<ol style='color:#ccc; line-height:1.7; font-size:0.95rem;'>"
for t in global_state["today_takeaways"]:
    takeaways_html += f"<li>{t}</li>"
takeaways_html += "</ol>"
st.markdown(takeaways_html, unsafe_allow_html=True)

# ============================================================================
# CRITICAL ALERT: AI BUBBLE WARNING
# ============================================================================

st.markdown("""
<div class="alert-box">
    <div class="alert-title">🚨 CRITICAL MARKET ALERT: AI BUBBLE FEARS INTENSIFY</div>
    <ul style="color: #ff9999; font-size: 1.1rem; line-height: 1.8;">
        <li><strong>Stretched AI valuations:</strong> Mega-cap AI and semis show very strong earnings, but price action is increasingly choppy and de-linked from fundamentals.</li>
        <li><strong>Bubble risk elevated:</strong> Flows remain concentrated in a narrow cluster of AI leaders, creating asymmetric drawdown risk if sentiment turns.</li>
        <li><strong>Macro uncertainty:</strong> Confusion around the Fed's path keeps discount rates, valuations and risk premia unstable.</li>
        <li><strong>Cross-asset warning:</strong> Crypto de-leveraging and ETF outflows illustrate how quickly risk appetite can reverse when fear rises.</li>
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

st.markdown('<h2 class="sub-header">🤖 QuantumFlow 4-Expert Decision Engine (NVDA Focus)</h2>', unsafe_allow_html=True)
st.markdown(
    "<p style='color:#9ca3af; font-size:0.95rem;'>"
    "This section demonstrates how four specialized AI experts (News, Technicals, Macro-Regime, Risk) "
    "converge into one unified trade decision on a key AI stock (NVDA) as a proxy for the AI bubble.</p>",
    unsafe_allow_html=True
)

# Sample Expert Opinions (Static but realistic and explainable)
experts_data = [
    {
        "name": "News & Sentiment Expert",
        "role": "LLM + news API scanning headlines, transcripts and social sentiment",
        "view": "NEGATIVE",
        "signal": "SELL",
        "confidence": 0.82,
        "rationale": (
            "Recent headlines highlight bubble fears, valuation concerns and high expectations "
            "for AI demand. Retail positioning is crowded and options activity is euphoric."
        )
    },
    {
        "name": "Technical Expert",
        "role": "Pattern recognition, trend/momentum, volatility regime detection",
        "view": "MIXED/REVERSAL",
        "signal": "SELL RALLIES",
        "confidence": 0.78,
        "rationale": (
            "Price made a lower high vs. recent peak, momentum is rolling over and realized "
            "volatility is rising. Distribution days are increasing, suggesting smart money selling into strength."
        )
    },
    {
        "name": "Macro & Regime Expert",
        "role": "Links NVDA/AI trade to rates, growth expectations and cross-asset flows",
        "view": "CAUTIOUS",
        "signal": "UNDERWEIGHT",
        "confidence": 0.74,
        "rationale": (
            "Late-cycle environment with elevated rates and tighter financial conditions makes long-duration "
            "growth trades vulnerable. Any macro disappointment could hit high-multiple AI names first."
        )
    },
    {
        "name": "Risk & Positioning Expert",
        "role": "Stop-loss logic, crowding metrics, max drawdown control",
        "view": "RISK-AVERSE",
        "signal": "REDUCE EXPOSURE",
        "confidence": 0.88,
        "rationale": (
            "Positioning is extremely crowded, skew is rich and downside tails are underpriced. "
            "From a capital preservation standpoint, risk is asymmetric to the downside."
        )
    },
]

col_left, col_right = st.columns([2, 1.4])

with col_left:
    for expert in experts_data:
        view_color = "#f97373" if expert["view"] in ["NEGATIVE", "RISK-AVERSE"] else "#facc15"
        st.markdown(
            f"""
            <div class="expert-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.1rem;">
                    <div>
                        <div class="expert-title">{expert['name']}</div>
                        <div class="expert-role">{expert['role']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:0.8rem; color:{view_color}; font-weight:600;">View: {expert['view']}</div>
                        <div style="font-size:0.78rem; color:#9ca3af;">Confidence: {expert['confidence']*100:.0f}%</div>
                    </div>
                </div>
                <div style="margin-top:0.3rem; font-size:0.86rem; color:#e5e7eb;">
                    {expert['rationale']}
                </div>
                <div style="margin-top:0.5rem;">
                    <span class="signal-badge signal-sell">{expert['signal']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

with col_right:
    st.markdown(
        """
        <div class="metric-card" style="margin-bottom:0.85rem;">
            <div class="metric-label">ENGINE OUTPUT</div>
            <div class="metric-value" style="color:#fecaca;">STRONG SELL ⚠️</div>
            <div class="metric-subtext" style="margin-top:0.5rem;">
                4/4 experts aligned on downside risk. Bubble risk elevated, volatility rising.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="metric-card" style="margin-bottom:0.85rem;">
            <div class="metric-label">RECOMMENDED STANCE</div>
            <div class="metric-value" style="color:#fed7aa;">UNDERWEIGHT AI LEADERS</div>
            <div class="metric-subtext" style="margin-top:0.5rem;">
                Keep core exposure but avoid chasing breakouts. Use rallies to reduce position size.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">STOP & POSITIONING</div>
            <div class="metric-subtext" style="margin-top:0.3rem;">
                <ul style="padding-left:1.1rem;">
                    <li>Max single-name allocation: 5–7% of portfolio</li>
                    <li>Tighten stops below recent support</li>
                    <li>Prefer baskets/ETFs over concentrated bets</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================================
# SAMPLE AI-CENTRIC WATCHLIST
# ============================================================================

ai_watchlist_data = [
    {
        'Symbol': 'NVDA',
        'Price': '$183.15',
        'Change': '-1.88%',
        'P/E': 55,
        'AI Exposure': '70%',
        'Risk Level': 'HIGH',
        'Signal': 'SELL',
        'Note': 'Crowded AI leader, asymmetric downside risk'
    },
    {
        'Symbol': 'MSFT',
        'Price': '$504.82',
        'Change': '-0.53%',
        'P/E': 36,
        'AI Exposure': '60%',
        'Risk Level': 'MEDIUM',
        'Signal': 'HOLD',
        'Note': 'Core AI infrastructure, balanced risk-reward'
    },
    {
        'Symbol': 'GOOGL',
        'Price': '$291.35',
        'Change': '+3.11%',
        'P/E': 28,
        'AI Exposure': '40%',
        'Risk Level': 'MEDIUM',
        'Signal': 'HOLD',
        'Note': 'Defensive AI play with strong core ads business'
    },
    {
        'Symbol': 'META',
        'Price': '$594.67',
        'Change': '-1.22%',
        'P/E': 24,
        'AI Exposure': '30%',
        'Risk Level': 'MEDIUM',
        'Signal': 'HOLD',
        'Note': 'Top performer YTD in Mag7; watching AI capex'
    },
    {
        'Symbol': 'TSLA',
        'Price': '$413.25',
        'Change': '+1.13%',
        'P/E': 89,
        'AI Exposure': '35%',
        'Risk Level': 'HIGH',
        'Signal': 'SELL RALLIES',
        'Note': 'High-multiple story stock with AI/autonomy optionality'
    },
    {
        'Symbol': 'AMD',
        'Price': '$176.45',
        'Change': '-2.05%',
        'P/E': 48,
        'AI Exposure': '50%',
        'Risk Level': 'HIGH',
        'Signal': 'HOLD / SPEC BUY',
        'Note': 'Second-derivative AI play; more volatile than NVDA'
    },
]

ai_watchlist_df = pd.DataFrame(ai_watchlist_data)

# Apply styling for risk & signal columns
def style_watchlist(df):
    def color_risk(val):
        if val == "HIGH":
            color = "rgba(248,113,113,0.2)"
            border = "rgba(248,113,113,0.7)"
            text = "#fecaca"
        elif val == "MEDIUM":
            color = "rgba(234,179,8,0.18)"
            border = "rgba(234,179,8,0.7)"
            text = "#fef9c3"
        else:
            color = "rgba(22,163,74,0.18)"
            border = "rgba(22,163,74,0.7)"
            text = "#dcfce7"
        return f"background:{color}; color:{text}; border:1px solid {border}; border-radius:20px; text-align:center;"

    def color_signal(val):
        if "SELL" in val:
            color = "rgba(248,113,113,0.2)"
            border = "rgba(248,113,113,0.7)"
            text = "#fecaca"
        elif "BUY" in val:
            color = "rgba(34,197,94,0.2)"
            border = "rgba(34,197,94,0.7)"
            text = "#bbf7d0"
        else:
            color = "rgba(59,130,246,0.2)"
            border = "rgba(59,130,246,0.7)"
            text = "#bfdbfe"
        return f"background:{color}; color:{text}; border:1px solid {border}; border-radius:20px; text-align:center;"

    styled = df.style.hide(axis="index")
    styled = styled.set_table_attributes('class="dataframe"')
    styled = styled.set_properties(
        subset=pd.IndexSlice[:, ["Symbol", "Price", "Change", "P/E", "AI Exposure"]],
        **{"text-align": "center"}
    )
    styled = styled.applymap(color_risk, subset=pd.IndexSlice[:, ["Risk Level"]])
    styled = styled.applymap(color_signal, subset=pd.IndexSlice[:, ["Signal"]])
    styled = styled.set_properties(subset=pd.IndexSlice[:, ["Note"]], **{"text-align": "left"})
    return styled

st.markdown('<h2 class="sub-header">🧬 AI-Centric Watchlist (Simulation)</h2>', unsafe_allow_html=True)
st.markdown(
    "<p style='color:#9ca3af; font-size:0.9rem;'>"
    "Static but realistic snapshot to show how QuantumFlow would highlight crowded AI trades, risk levels "
    "and engine-generated signals in a production version.</p>",
    unsafe_allow_html=True
)

st.dataframe(style_watchlist(ai_watchlist_df), use_container_width=True)

# ============================================================================
# SIMULATED PREDICTION: S&P 500 PATH UNDER AI BUBBLE STRESS
# ============================================================================

# We keep dates as a DatetimeIndex but avoid Plotly shapes that try to "average" timestamps
dates = pd.date_range(datetime(2025, 11, 1), periods=20, freq="D")
spx_prices = np.linspace(6700, 6550, 20) + np.random.normal(0, 20, 20)

# Simulated stressed future path (downward drift, higher vol)
future_dates = pd.date_range(dates[-1] + timedelta(days=1), periods=15, freq="D")
predicted_path = spx_prices[-1] + np.cumsum(np.random.normal(-8, 18, len(future_dates)))

fig_pred = go.Figure()

fig_pred.add_trace(
    go.Scatter(
        x=dates,
        y=spx_prices,
        mode="lines+markers",
        name="Historical SPX (simulated)",
        line=dict(color="rgba(96,165,250,0.9)", width=2),
        marker=dict(size=5, color="rgba(129,140,248,0.95)")
    )
)

fig_pred.add_trace(
    go.Scatter(
        x=future_dates,
        y=predicted_path,
        mode="lines+markers",
        name="QuantumFlow Stress Path",
        line=dict(color="rgba(248,113,113,0.95)", width=3, dash="dash"),
        marker=dict(size=5, color="rgba(248,113,113,0.9)")
    )
)

fig_pred.update_layout(
    title="S&P 500 Stress-Path Simulation under Elevated AI Bubble Risk",
    title_font=dict(size=20, color='white'),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,23,42,0.8)",
    font={'color': "white", 'family': "Inter"},
    height=420,
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(148,163,184,0.35)',
        zeroline=False
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(148,163,184,0.35)',
        zeroline=False
    ),
    legend=dict(
        bgcolor="rgba(15,23,42,0.7)",
        bordercolor="rgba(148,163,184,0.5)",
        borderwidth=1
    )
)

st.markdown('<h2 class="sub-header">📉 S&P 500 Stress Scenario (AI Bubble Unwind)</h2>', unsafe_allow_html=True)
st.plotly_chart(fig_pred, use_container_width=True)
# ============================================================================
# EXECUTIVE SUMMARY / INVESTMENT COMMITTEE STYLE VIEW
# ============================================================================

st.markdown("## 📝 Executive Summary - November 23, 2025")

st.markdown(
"""
**1. AI Trade Still Powerful, But Fragile**

Mega-cap AI and semiconductor leaders remain at the heart of the equity rally,  
but price action has become choppy and increasingly de-linked from fundamentals.  
Valuations are stretched and the market is highly sensitive to any hint of slowing  
demand or reduced AI capex. Bubble risk is elevated, but not yet in full unwind mode.

---

**2. Macro & Rates: Higher Volatility, Not Full Risk-Off**

Mixed macro data keeps the Fed path uncertain: investors are torn between an imminent  
rate-cut cycle and a *"higher for longer"* scenario. This uncertainty translates into a  
**high volatility regime** and a **mixed risk mode** across assets – no clean risk-on  
or risk-off. Sector rotation dominates: quality, cash flow and balance-sheet strength  
matter more than chasing every spike.

---

**3. Crypto De-Leveraging & ETF Outflows**

Bitcoin and Ethereum have given back a large portion of their 2025 gains as leveraged  
positions are unwound and ETF flows turn negative. This is more of a **targeted risk  
reduction in crypto** than a broad-market capitulation – but it highlights how quickly  
risk appetite can reverse when funding costs are high and narratives crack.

---

> ⚡ **The Bottom Line**  
> This is a late-cycle, high-volatility environment with elevated AI bubble risk and  
> visible stress in crypto. It is a market for **selective risk-taking**, not blind  
> aggression. QuantumFlow's Decision Engine is designed exactly for this regime:  
> combine macro, technicals, news flow and risk constraints to size positions  
> intelligently, lean into high-conviction ideas, and avoid crowded trades where  
> downside is asymmetric.
"""
)


# ============================================================================
# FOOTER / WHY QUANTUMFLOW IS DIFFERENT
# ============================================================================

st.markdown("---")
st.markdown(
    """
    <div style="margin-top: 10px; font-size:0.9rem; color:#9ca3af;">
        🔮 <strong>QuantumFlow AI Trading Intelligence</strong> | November 23, 2025<br>
        This dashboard is a realistic MVP simulation: the architecture, expert logic and UX are designed
        to scale into a fully-automated system that ingests <em>live</em> macro, cross-asset prices, 
        news &amp; sentiment feeds (including Perplexity-style LLM retrieval), and outputs explainable,
        risk-aware portfolio decisions.
    </div>
    """,
    unsafe_allow_html=True
)

st.info("November 23, 2025 - 10:00 AM EST | Simulation mode: No real trades executed yet.")

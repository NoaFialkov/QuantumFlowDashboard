"""
QuantumFlow AI Trading Intelligence Dashboard - November 19, 2025
Real-time inspired demo with AI Bubble / Magnificent 7 / Alternatives view
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --------------------
# PAGE CONFIG & STYLE
# --------------------
st.set_page_config(
    page_title="QuantumFlow – AI Trading CoPilot",
    page_icon="💹",
    layout="wide",
)

PRIMARY = "#1E3A8A"
ACCENT = "#06B6D4"
DANGER = "#FF3B30"
SUCCESS = "#16A34A"
BG_DARK = "#050816"

st.markdown(
    f"""
    <style>
    .main {{
        background: radial-gradient(circle at top, #020617 0%, #020617 35%, #020617 100%);
        color: #E5E7EB;
    }}
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 2rem;
    }}
    h1, h2, h3, h4 {{
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: #E5E7EB;
    }}
    .metric-card {{
        background: linear-gradient(145deg, #020617, #0B1120);
        border-radius: 16px;
        padding: 16px 18px;
        border: 1px solid rgba(148,163,184,0.35);
        box-shadow: 0 10px 30px rgba(15,23,42,0.9);
    }}
    .alert-box {{
        background: linear-gradient(135deg, rgba(255,59,48,0.18) 0%, rgba(255,45,85,0.18) 100%);
        border: 1px solid rgba(248,113,113,0.95);
        border-radius: 18px;
        padding: 20px;
        margin-top: 10px;
        margin-bottom: 22px;
        box-shadow: 0 0 35px rgba(248,113,113,0.28);
        color: #FEE2E2;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------
# SIDEBAR – USER PROFILE
# --------------------
st.sidebar.title("👤 Investor Profile")

risk_profile = st.sidebar.radio(
    "Risk Profile",
    options=["Conservative", "Moderate", "Aggressive"],
    index=1,
)

capital = st.sidebar.number_input(
    "Portfolio Size (USD)", min_value=5000, max_value=5_000_000, step=5000, value=100_000
)

focus_ai = st.sidebar.checkbox("Highlight AI / Magnificent 7 risk", value=True)
focus_alt = st.sidebar.checkbox("Show Alternatives when Tech is Weak", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "🔍 **Demo Note:** Data is a realistic snapshot-style mock inspired by "
    "today's market conditions around AI bubble fears, Nvidia earnings, "
    "and flows into gold / commodities."
)

# --------------------
# MOCK DATA (INSPIRED BY 19.11.2025)
# --------------------
today_str = "2025-11-19"

# Market overview: indices + gold + oil
market_overview = pd.DataFrame([
    # price, daily %, ytd %, type, quantumflow view
    ["S&P 500",      6617,  -0.8,  21.0, "Index",       "Risk-off drift ahead of NVDA earnings"],
    ["Nasdaq 100",  24250, -1.2,  32.0, "Index",       "Tech-heavy, hit hardest by AI unwind"],
    ["Magnificent 7 Index", -1, -1.0, 48.0, "Basket", "Crowded AI trade correcting, stress elevated"],
    ["Gold (oz)",   4094,   0.6,  54.0, "Commodity",   "Safe-haven bid returns, benefiting from risk-off"],
    ["WTI Crude",     57,  -0.4, -18.0, "Commodity",   "Bearish tone, oversupply fears into 2026"],
],
    columns=["Asset", "Level", "DailyChangePct", "YTD%", "Type", "Comment"]
)

# For the Mag 7 table we'll use approximate demo values
mag7_data = pd.DataFrame([
    ["AAPL",  285,  -0.9,  28.0, "Reduce",   "Over-owned, modest downside risk as rates expectations reset"],
    ["MSFT",  430,  -2.7,  46.0, "Hold",     "Still high quality; wait for clarity post NVDA & Fed minutes"],
    ["NVDA",  181,  -2.8, 120.0, "Watch",    "High expectations into Q3 AI earnings; volatility expected"],
    ["GOOGL", 284,  -0.3,  39.0, "Hold",     "Less exposed to pure AI bubble, but momentum cooling"],
    ["AMZN",  168,  -4.4,  42.0, "Trim",     "E-commerce + AI infra; profit-taking and macro worries"],
    ["META",  495,  -1.5,  65.0, "Reduce",   "High beta to risk sentiment, sentiment still bullish but fragile"],
    ["TSLA",  210,  -3.1,  11.0, "High-Risk","EV + AI bet; momentum broken, only for aggressive risk"],
],
    columns=["Ticker", "Price", "Daily%", "YTD%", "QF_Action", "Narrative"]
)

# Alternative plays when tech is shaky
alts_data = pd.DataFrame([
    ["GLD",     "Gold ETF",         "Defensive / Safe-haven", "BUY",  7.0,  6.0, 12.0,
     "Flows rotating from crowded AI names into gold as macro uncertainty rises."],
    ["XLE",     "Energy Select",    "Energy / Oil & Gas",     "BUY",  5.0,  8.0, 15.0,
     "Valuations reasonable vs growth; benefits if inflation and energy shocks reappear."],
    ["XLU",     "Utilities",        "Defensive Yield",        "ACCUMULATE", 4.0, 4.0, 9.0,
     "Lower volatility alternative to AI; income plus partial inflation hedge."],
    ["SHY",     "Short-Term Treas.", "Cash-like / Rates",     "HOLD",  3.0,  0.0, 0.0,
     "For de-risking portions of the portfolio while waiting for better entry in risk assets."],
],
    columns=["Ticker", "Name", "Theme", "QF_Signal", "SuggestedSize%", "StopLoss%", "TakeProfit%", "Rationale"]
)

# Example trade ideas
trade_ideas = pd.DataFrame([
    ["GLD",  "BUY",        "Defensive rotation from AI bubble risk",       0.08, 0.06, 0.12],
    ["NVDA", "SPECULATE",  "Earnings catalyst – only for Aggressive risk", 0.03, 0.10, 0.20],
    ["XLE",  "BUY",        "Energy lagged vs tech, attractive risk/reward", 0.06, 0.08, 0.15],
    ["AAPL", "TRIM",       "Crowded mega-cap, partial profit-taking",      0.03, 0.05, 0.10],
],
    columns=["Ticker", "Action", "Reason", "PositionSize", "StopLoss%", "TakeProfit%"]
)

# Adjust sizing per risk profile
risk_multiplier = {"Conservative": 0.6, "Moderate": 1.0, "Aggressive": 1.4}[risk_profile]
trade_ideas["AdjPositionSize"] = (trade_ideas["PositionSize"] * risk_multiplier).round(3)

# --------------------
# HEADER
# --------------------
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("### 💠 QuantumFlow")
    st.caption("AI-Powered Trading Intelligence for Real Investors")
with col_title:
    st.markdown(
        f"""
        <h1>Market Brain – Live Demo ({today_str})</h1>
        <p style="color:#9CA3AF;">
            AI bubble fears, Magnificent 7 pullback, Nvidia earnings on deck, and a renewed bid in gold.
            QuantumFlow synthesizes it all into clear, risk-aware actions for your portfolio.
        </p>
        """,
        unsafe_allow_html=True,
    )

# --------------------
# TOP: MARKET PULSE + AI BUBBLE ALERT
# --------------------
st.markdown("## 🧭 Market Pulse & AI Bubble Monitor")

c1, c2, c3, c4, c5 = st.columns(5)
cards = [c1, c2, c3, c4, c5]

for card, (_, row) in zip(cards, market_overview.iterrows()):
    with card:
        change_color = SUCCESS if row["DailyChangePct"] > 0 else DANGER
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-size:0.9rem; color:#9CA3AF;">{row['Type']}</div>
                <div style="font-size:1.2rem; font-weight:600; margin-top:2px;">{row['Asset']}</div>
                <div style="font-size:1.0rem; margin-top:4px;">
                    Level: <b>{row['Level']}</b>
                </div>
                <div style="font-size:0.95rem; margin-top:4px; color:{change_color};">
                    {row['DailyChangePct']}% today
                </div>
                <div style="font-size:0.8rem; margin-top:2px; color:#A5B4FC;">
                    YTD: {row['YTD%']}%
                </div>
                <div style="font-size:0.75rem; margin-top:6px; color:#9CA3AF;">
                    {row['Comment']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# AI Bubble Alert box
st.markdown(
    """
    <div class="alert-box">
        <h3>⚠️ AI Bubble Stress: Elevated</h3>
        <p style="margin-top:6px; font-size:0.95rem;">
        Tech-heavy indices have logged multiple down days as investors question AI valuations,
        trim exposure to the Magnificent 7, and wait for Nvidia's high-stakes earnings release.
        QuantumFlow flags: <b>reduce concentration risk</b>, rotate part of gains into gold,
        quality energy and defensive sectors, and avoid oversized single-name bets.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------
# MAGNIFICENT 7 – RISK & OPPORTUNITY
# --------------------
st.markdown("## 🌌 Magnificent 7 – Risk & Opportunity Map")

left, right = st.columns([2, 3])

with left:
    st.markdown("#### Per-stock Signals")
    st.dataframe(
        mag7_data.style.background_gradient(
            subset=["Daily%"], cmap="RdYlGn"
        ).format(
            {"Price": "${:,.2f}", "Daily%": "{:+.2f}%", "YTD%": "{:+.1f}%"}
        ),
        use_container_width=True,
        hide_index=True,
    )

with right:
    st.markdown("#### Daily Move vs YTD Performance")
    fig_mag7 = go.Figure()
    fig_mag7.add_trace(go.Bar(
        x=mag7_data["Ticker"],
        y=mag7_data["Daily%"],
        name="Daily %",
        marker_line_width=0,
    ))
    fig_mag7.add_trace(go.Scatter(
        x=mag7_data["Ticker"],
        y=mag7_data["YTD%"],
        mode="lines+markers",
        name="YTD %",
        yaxis="y2"
    ))
    fig_mag7.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#020617",
        height=340,
        margin=dict(l=40, r=40, t=40, b=40),
        yaxis=dict(title="Daily % move"),
        yaxis2=dict(
            title="YTD %",
            overlaying="y",
            side="right",
        ),
        legend=dict(orientation="h", y=1.15),
    )
    st.plotly_chart(fig_mag7, use_container_width=True)

st.markdown(
    """
    <p style="color:#9CA3AF; font-size:0.9rem; margin-top:-10px;">
    QuantumFlow treats the Magnificent 7 as a <b>crowded macro factor</b>, not just 7 tickers.
    When crowding + volatility + stretched YTD gains align, the engine shifts from
    “chasing AI beta” to “protecting capital and reallocating intelligently”.
    </p>
    """,
    unsafe_allow_html=True,
)

# --------------------
# ALTERNATIVE PLAYS WHEN TECH IS SHAKY
# --------------------
if focus_alt:
    st.markdown("## 🛡️ Alternatives When AI & Tech Sell Off")

    col_alt_table, col_alt_chart = st.columns([2, 2])

    with col_alt_table:
        st.markdown("#### Defensive & Rotational Ideas")
        st.dataframe(
            alts_data.style.format(
                {
                    "SuggestedSize%": "{:.1f}%",
                    "StopLoss%": "{:.1f}%",
                    "TakeProfit%": "{:.1f}%"
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    with col_alt_chart:
        st.markdown("#### Suggested Allocation by Theme")
        fig_alloc = px.bar(
            alts_data,
            x="Theme",
            y="SuggestedSize%",
            color="QF_Signal",
            title="Suggested slice of portfolio by theme (before risk-profile adjustment)",
        )
        fig_alloc.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#020617",
            height=340,
            margin=dict(l=40, r=40, t=40, b=40),
        )
        st.plotly_chart(fig_alloc, use_container_width=True)

# --------------------
# TRADE IDEAS – HOW THE ENGINE TALKS TO THE USER
# --------------------
st.markdown("## 🎯 QuantumFlow Trade Ideas (Demo)")

st.markdown(
    f"""
    <p style="color:#9CA3AF; font-size:0.9rem;">
    Based on your selected risk profile (<b>{risk_profile}</b>) and current market regime,
    QuantumFlow would size trades differently. Below you see position sizes already adjusted
    by a risk multiplier, assuming a portfolio of <b>${capital:,.0f}</b>.
    </p>
    """,
    unsafe_allow_html=True,
)

trade_ideas_view = trade_ideas.copy()
trade_ideas_view["NominalSize($)"] = (trade_ideas_view["AdjPositionSize"] * capital).round(0)
trade_ideas_view["AdjPositionSize%"] = (trade_ideas_view["AdjPositionSize"] * 100).round(1)

st.dataframe(
    trade_ideas_view[["Ticker", "Action", "Reason", "AdjPositionSize%", "NominalSize($)", "StopLoss%", "TakeProfit%"]]
    .rename(columns={
        "AdjPositionSize%": "Position Size (%)",
        "NominalSize($)": "Approx. Capital",
    })
    .style.format(
        {
            "Position Size (%)": "{:.1f}%",
            "Approx. Capital": "${:,.0f}",
            "StopLoss%": "{:.1f}%",
            "TakeProfit%": "{:.1f}%",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

st.markdown(
    """
    <p style="color:#6B7280; font-size:0.85rem; margin-top:8px;">
    In the full product, each idea comes from the multi-expert Decision Engine:
    news momentum, technical setup, market regime and risk module all contribute
    weighted opinions. For this demo, we show how the final output looks and feels
    to a sophisticated retail investor who wants clear, explainable, risk-aware actions.
    </p>
    """,
    unsafe_allow_html=True,
)

# --------------------
# EXPLAINABILITY PANEL
# --------------------
st.markdown("## 🧠 Why This Changes the Game for Retail Investors")

st.markdown(
    """
    - 🔎 **From Noise to Narrative** – Instead of endless charts and news feeds,
      QuantumFlow summarizes AI bubble stress, macro regime and sector rotations
      into a single coherent story for the investor.
    - 🧩 **Multi-Expert Brain** – Behind each signal stands a News Expert, Technical Expert,
      Market Regime Expert and Risk Expert – orchestrated into one decision.
    - 🎯 **Actionable, Not Just Informative** – Every view ends in:
      what to do, how much to size, where to cut losses, and what alternatives exist.
    - 🛡️ **Risk-As-First-Class Citizen** – User-defined risk profile drives sizing and
      asset selection, putting capital protection on par with return.
    """
)

"""
QuantumFlow AI Trading Intelligence Dashboard - Decision Engine & BL-style Portfolio
MVP version using daily JSON snapshot from Perplexity.
"""

import json
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------------
# 1. PASTE YOUR DAILY JSON SNAPSHOT FROM PERPLEXITY HERE
# ---------------------------------------------------------------------
# כל יום:
#   - לוקחים את ה-JSON המלא ש-Perplexity מחזיר
#   - מדביקים בין ה-triple quotes של RAW_JSON
#   - מריצים מחדש את הדאשבורד
#
# כרגע שמתי כאן את ה-JSON ששלחת (24.11.2025) כ-default.

RAW_JSON = r"""{
"date": "2025-11-24",
"market_regime": {
"overall_regime_name": "fragile bounce, rate cut hopes",
"global_sentiment_score": -0.5,
"market_risk_mode": "mixed",
"volatility_regime": "normal",
"short_comment": "Markets staged a modest rebound after last week's sharp reversal, driven by potential Fed rate cuts and continued AI sector volatility. Sentiment remains cautious as holiday trading begins."
},
"risk_indicators": {
"vix_level": 18.6,
"vix_1y_percentile": 54,
"move_level": 116.1,
"ig_spread_bps": 129.8,
"hy_spread_bps": 390.9,
"credit_comment": "Credit spreads remain stable, but rates volatility highlights risk ahead of Fed decision."
},
"cross_assets": [
{
"name": "S&P 500",
"ticker": "SPX",
"region": "US",
"asset_class": "EquityIndex",
"level": 6471.54,
"chg_1d_pct": 0.08,
"chg_5d_pct": 0.32,
"chg_1m_pct": -1.5,
"chg_ytd_pct": 12.7,
"realized_vol_30d_pct": 15.5,
"drawdown_from_1y_high_pct": 5.6
},
{
"name": "Nasdaq 100",
"ticker": "NDX",
"region": "US",
"asset_class": "EquityIndex",
"level": 23849.04,
"chg_1d_pct": 0.04,
"chg_5d_pct": 1.33,
"chg_1m_pct": -1.3,
"chg_ytd_pct": 15.2,
"realized_vol_30d_pct": 18.7,
"drawdown_from_1y_high_pct": 7.1
},
{
"name": "10Y US Treasury Yield",
"ticker": "US10Y",
"region": "US",
"asset_class": "Rates",
"level": 4.10,
"chg_1d_pct": -0.73,
"chg_5d_pct": -1.2,
"chg_1m_pct": 2.9,
"chg_ytd_pct": -7.3,
"realized_vol_30d_pct": 9.1,
"drawdown_from_1y_high_pct": 8.3
},
{
"name": "Gold",
"ticker": "XAUUSD",
"region": "Global",
"asset_class": "Commodity",
"level": 4056.85,
"chg_1d_pct": -0.12,
"chg_5d_pct": 1.02,
"chg_1m_pct": 1.89,
"chg_ytd_pct": 55.41,
"realized_vol_30d_pct": 12.2,
"drawdown_from_1y_high_pct": 3.9
},
{
"name": "Bitcoin",
"ticker": "BTCUSD",
"region": "Crypto",
"asset_class": "Crypto",
"level": 87700,
"chg_1d_pct": 1.0,
"chg_5d_pct": -13.5,
"chg_1m_pct": -5.3,
"chg_ytd_pct": 38.1,
"realized_vol_30d_pct": 44.7,
"drawdown_from_1y_high_pct": 30.8
}
],
"asset_expert_matrix": [
{
"ticker": "NVDA",
"name": "NVIDIA",
"asset_class": "Equity",
"price": 173.5,
"chg_1d_pct": -0.14,
"chg_5d_pct": -2.8,
"chg_1m_pct": 2.1,
"chg_ytd_pct": 42.5,
"realized_vol_30d_pct": 35.3,
"drawdown_from_1y_high_pct": 15.7,
"macro_score": 0.7,
"technical_score": 0.4,
"sentiment_score": 0.3,
"risk_score": -0.6,
"short_rationale": "Strong AI demand but valuation risk; volatility high after earnings; cautious sentiment post recent correction."
},
{
"ticker": "MSFT",
"name": "Microsoft",
"asset_class": "Equity",
"price": 384.2,
"chg_1d_pct": 0.07,
"chg_5d_pct": 1.2,
"chg_1m_pct": 2.6,
"chg_ytd_pct": 29.8,
"realized_vol_30d_pct": 21.3,
"drawdown_from_1y_high_pct": 6.1,
"macro_score": 0.5,
"technical_score": 0.7,
"sentiment_score": 0.55,
"risk_score": -0.3,
"short_rationale": "Cloud momentum; MSFT holding above key support levels; moderate risk."
},
{
"ticker": "AAPL",
"name": "Apple",
"asset_class": "Equity",
"price": 196.5,
"chg_1d_pct": 0.03,
"chg_5d_pct": -0.8,
"chg_1m_pct": -1.4,
"chg_ytd_pct": 14.1,
"realized_vol_30d_pct": 17.6,
"drawdown_from_1y_high_pct": 8.3,
"macro_score": 0.3,
"technical_score": 0.3,
"sentiment_score": 0.2,
"risk_score": -0.25,
"short_rationale": "Growth concerns linger; technical support tested; risk profile stable, sentiment subdued."
},
{
"ticker": "BTCUSD",
"name": "Bitcoin",
"asset_class": "Crypto",
"price": 87700,
"chg_1d_pct": 1.0,
"chg_5d_pct": -13.5,
"chg_1m_pct": -5.3,
"chg_ytd_pct": 38.1,
"realized_vol_30d_pct": 44.7,
"drawdown_from_1y_high_pct": 30.8,
"macro_score": -0.1,
"technical_score": -0.4,
"sentiment_score": -0.35,
"risk_score": -0.70,
"short_rationale": "Large drawdown from highs; ETF outflows signal capitulation; high volatility and extreme fear dominate."
},
{
"ticker": "ETHUSD",
"name": "Ethereum",
"asset_class": "Crypto",
"price": 2835,
"chg_1d_pct": 0.6,
"chg_5d_pct": -8.2,
"chg_1m_pct": 3.1,
"chg_ytd_pct": 29.4,
"realized_vol_30d_pct": 39.8,
"drawdown_from_1y_high_pct": 18.4,
"macro_score": 0.1,
"technical_score": 0.13,
"sentiment_score": 0.05,
"risk_score": -0.45,
"short_rationale": "ETH outperforming BTC; flows stabilize post recent selling; technical support holds above $2,800."
}
],
"crypto_snapshot": [
{
"ticker": "BTCUSD",
"name": "Bitcoin",
"price": 87700,
"chg_1d_pct": 1.0,
"chg_7d_pct": -13.9,
"chg_1m_pct": -5.3,
"dominance_comment": "BTC rebounding after technical bounce; dominance under pressure from major altcoins."
},
{
"ticker": "ETHUSD",
"name": "Ethereum",
"price": 2835,
"chg_1d_pct": 0.6,
"chg_7d_pct": -7.7,
"chg_1m_pct": 3.1,
"relative_to_btc_comment": "ETH moderately outperforming BTC in current volatility; maintains key supports."
},
{
"ticker": "SOLUSD",
"name": "Solana",
"price": 133,
"chg_1d_pct": 2.5,
"chg_7d_pct": 0.2,
"chg_1m_pct": 9.9,
"dominance_comment": "SOL shows resilience after broader crypto correction; flows remain positive."
},
{
"ticker": "XRPUSD",
"name": "XRP",
"price": 2.09,
"chg_1d_pct": 2.65,
"chg_7d_pct": -3.6,
"chg_1m_pct": 4.7,
"dominance_comment": "XRP steady after resistance rejection; bears neutralized."
}
],
"key_narratives": [
"Fed rate cut probability surges, boosting risk appetite heading into holiday trading.",
"Crypto markets stabilize after sharp drawdown; altcoins lead tentative rebound.",
"AI and tech remain volatile as concerns over valuations linger post-earnings."
]
}"""

# ---------------------------------------------------------------------
# 2. PARSE JSON SAFELY
# ---------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_snapshot(raw: str):
    try:
        data = json.loads(raw)
        return data, None
    except Exception as e:
        return None, str(e)

data, parse_error = load_snapshot(RAW_JSON)

st.set_page_config(
    page_title="QuantumFlow AI Trading Dashboard",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------
# 3. BASIC STYLING
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }
    .subtitle {
        color: #9ca3af;
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        border-radius: 14px;
        padding: 0.9rem 1.0rem;
        border: 1px solid rgba(148,163,184,0.6);
        background: radial-gradient(circle at top left, rgba(15,23,42,0.95), rgba(15,23,42,0.98));
    }
    .metric-label {
        font-size: 0.78rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.09em;
    }
    .metric-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e5e7eb;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #9ca3af;
    }
    .badge {
        display: inline-block;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .badge-riskoff { background: rgba(239,68,68,0.16); color: #fecaca; border: 1px solid rgba(239,68,68,0.7); }
    .badge-mixed { background: rgba(234,179,8,0.16); color: #fef3c7; border: 1px solid rgba(234,179,8,0.7); }
    .badge-riskon { background: rgba(34,197,94,0.16); color: #bbf7d0; border: 1px solid rgba(34,197,94,0.7); }

    .badge-high { background: rgba(248,113,113,0.16); color: #fecaca; border: 1px solid rgba(248,113,113,0.7); }
    .badge-normal { background: rgba(59,130,246,0.16); color: #bfdbfe; border: 1px solid rgba(59,130,246,0.7); }
    .badge-low { background: rgba(34,197,94,0.16); color: #bbf7d0; border: 1px solid rgba(34,197,94,0.7); }

    table.dataframe {
        border-radius: 12px !important;
        border-collapse: collapse !important;
        border: 1px solid rgba(148,163,184,0.5) !important;
        background: rgba(15,23,42,0.98) !important;
        color: #e5e7eb !important;
        font-size: 0.85rem !important;
    }
    table.dataframe thead tr {
        background: linear-gradient(90deg, rgba(15,118,110,0.9), rgba(37,99,235,0.9)) !important;
    }
    table.dataframe th, table.dataframe td {
        border: 1px solid rgba(148,163,184,0.4) !important;
        padding: 0.35rem 0.55rem !important;
        text-align: center !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="main-title">QuantumFlow Market Pulse</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Multi-expert daily snapshot with an automated decision engine and '
    'Black–Litterman style portfolio tilt.</p>',
    unsafe_allow_html=True,
)

if parse_error:
    st.error("JSON parsing error – please check RAW_JSON.\n\n" + parse_error)
    st.stop()

# ---------------------------------------------------------------------
# 4. UNPACK DATA
# ---------------------------------------------------------------------
mr = data.get("market_regime", {})
ri = data.get("risk_indicators", {})
cross_assets = data.get("cross_assets", [])
asset_matrix = data.get("asset_expert_matrix", [])
crypto = data.get("crypto_snapshot", [])
narratives = data.get("key_narratives", [])

snapshot_date_str = data.get("date", "")
try:
    snapshot_dt = datetime.strptime(snapshot_date_str, "%Y-%m-%d").date()
except Exception:
    snapshot_dt = snapshot_date_str

st.write(f"**Data snapshot date:** {snapshot_dt}")

# ---------------------------------------------------------------------
# 5. TOP PANEL – MARKET REGIME & RISK
# ---------------------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Market Regime</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="metric-value">{mr.get("overall_regime_name", "N/A").title()}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="metric-sub">{mr.get("short_comment", "")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    risk_mode = mr.get("market_risk_mode", "mixed")
    vol_regime = mr.get("volatility_regime", "normal")
    sent = mr.get("global_sentiment_score", 0.0)

    risk_badge_class = "badge-mixed"
    if risk_mode == "risk-off":
        risk_badge_class = "badge-riskoff"
    elif "risk-on" in risk_mode:
        risk_badge_class = "badge-riskon"

    vol_badge_class = "badge-normal"
    if vol_regime == "high":
        vol_badge_class = "badge-high"
    elif vol_regime == "low":
        vol_badge_class = "badge-low"

    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Global Mood</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="metric-value">{sent:+.1f}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="metric-sub">Sentiment score (−2 = panic, +2 = euphoria)</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<span class="badge {risk_badge_class}">Risk mode: {risk_mode}</span> '
        f'&nbsp; <span class="badge {vol_badge_class}">Vol: {vol_regime}</span>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Risk Indicators</div>', unsafe_allow_html=True)
    vix = ri.get("vix_level")
    move = ri.get("move_level")
    ig = ri.get("ig_spread_bps")
    hy = ri.get("hy_spread_bps")
    st.markdown(
        f'<div class="metric-value">VIX: {vix if vix is not None else "N/A"}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="metric-sub">MOVE: {move}, IG: {ig} bps, HY: {hy} bps</div>',
        unsafe_allow_html=True,
    )
    if ri.get("credit_comment"):
        st.markdown(
            f'<div class="metric-sub">{ri["credit_comment"]}</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------------------
# 6. CROSS-ASSET SNAPSHOT
# ---------------------------------------------------------------------
st.subheader("Cross-Asset Snapshot")

if cross_assets:
    ca_df = pd.DataFrame(cross_assets)
    col_order = [
        "name", "ticker", "region", "asset_class",
        "level", "chg_1d_pct", "chg_5d_pct",
        "chg_1m_pct", "chg_ytd_pct",
        "realized_vol_30d_pct", "drawdown_from_1y_high_pct",
    ]
    cols = [c for c in col_order if c in ca_df.columns]
    ca_df = ca_df[cols]
    st.dataframe(
        ca_df.style.format(
            {
                "level": "{:,.2f}",
                "chg_1d_pct": "{:+.2f}%",
                "chg_5d_pct": "{:+.2f}%",
                "chg_1m_pct": "{:+.2f}%",
                "chg_ytd_pct": "{:+.2f}%",
                "realized_vol_30d_pct": "{:.1f}%",
                "drawdown_from_1y_high_pct": "{:.1f}%",
            }
        ).set_table_attributes('class="dataframe"'),
        use_container_width=True,
    )

    # Simple bar chart: YTD performance by asset
    if "chg_ytd_pct" in ca_df.columns and "name" in ca_df.columns:
        fig_ca = px.bar(
            ca_df,
            x="name",
            y="chg_ytd_pct",
            title="Year-to-Date Performance by Asset",
            text="chg_ytd_pct",
        )
        fig_ca.update_layout(
            xaxis_title="",
            yaxis_title="YTD %",
            showlegend=False,
        )
        st.plotly_chart(fig_ca, use_container_width=True)
else:
    st.info("No cross-asset data in JSON.")

# ---------------------------------------------------------------------
# 6b. MARKET NARRATIVE & SENTIMENT
# ---------------------------------------------------------------------
st.subheader("Market Narrative & Sentiment")

main_comment = mr.get("short_comment")
if main_comment:
    st.write(main_comment)

if narratives:
    st.markdown("**Key themes from today's newsflow:**")
    for n in narratives:
        st.markdown(f"- {n}")
else:
    st.write("No narratives provided in snapshot.")

st.markdown("---")

# ---------------------------------------------------------------------
# 7. DECISION ENGINE – MULTI-EXPERT SCORING
# ---------------------------------------------------------------------
st.subheader("QuantumFlow Decision Matrix (per Asset)")

if asset_matrix:
    df = pd.DataFrame(asset_matrix)

    # weights for the four experts
    W_MACRO = 0.30
    W_TECH = 0.30
    W_SENT = 0.20
    W_RISK = 0.20

    for col in ["macro_score", "technical_score", "sentiment_score", "risk_score"]:
        if col not in df.columns:
            df[col] = 0.0

    df["final_score"] = (
        W_MACRO * df["macro_score"]
        + W_TECH * df["technical_score"]
        + W_SENT * df["sentiment_score"]
        + W_RISK * df["risk_score"]
    )

    def map_action(score: float) -> str:
        if score >= 0.40:
            return "STRONG_OVERWEIGHT"
        elif score >= 0.15:
            return "OVERWEIGHT"
        elif score > -0.15:
            return "NEUTRAL"
        elif score > -0.40:
            return "UNDERWEIGHT"
        else:
            return "AVOID"

    df["action"] = df["final_score"].apply(map_action)

    show_cols = [
        "ticker", "name", "asset_class",
        "price",
        "chg_1d_pct", "chg_5d_pct", "chg_1m_pct", "chg_ytd_pct",
        "realized_vol_30d_pct", "drawdown_from_1y_high_pct",
        "macro_score", "technical_score", "sentiment_score", "risk_score",
        "final_score", "action",
    ]
    show_cols = [c for c in show_cols if c in df.columns]

    styled = (
        df[show_cols]
        .sort_values("final_score", ascending=False)
        .style
        .set_table_attributes('class="dataframe"')
        .format(
            {
                "price": "{:,.2f}",
                "chg_1d_pct": "{:+.2f}%",
                "chg_5d_pct": "{:+.2f}%",
                "chg_1m_pct": "{:+.2f}%",
                "chg_ytd_pct": "{:+.2f}%",
                "realized_vol_30d_pct": "{:.1f}%",
                "drawdown_from_1y_high_pct": "{:.1f}%",
                "macro_score": "{:+.2f}",
                "technical_score": "{:+.2f}",
                "sentiment_score": "{:+.2f}",
                "risk_score": "{:+.2f}",
                "final_score": "{:+.2f}",
            }
        )
    )

    st.dataframe(styled, use_container_width=True)

    # ----------------------------------------
    # Expert panel overview (aggregated scores)
    # ----------------------------------------
    st.markdown("### Expert Panel Overview")

    macro_mean = float(df["macro_score"].mean())
    tech_mean = float(df["technical_score"].mean())
    sent_mean = float(df["sentiment_score"].mean())
    risk_mean = float(df["risk_score"].mean())

    def describe_expert(score: float) -> str:
        if score >= 0.5:
            return "Strongly supportive / bullish"
        elif score >= 0.1:
            return "Mildly supportive"
        elif score <= -0.5:
            return "Strongly cautious / defensive"
        elif score <= -0.1:
            return "Mildly cautious"
        else:
            return "Neutral / finely balanced"

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Macro & Regime Expert</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{macro_mean:+.2f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-sub">{describe_expert(macro_mean)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-sub">Focus: growth, inflation, rates, cycle.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Technical Expert</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{tech_mean:+.2f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-sub">{describe_expert(tech_mean)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-sub">Focus: trend, momentum, support/resistance.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Sentiment & News Expert</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{sent_mean:+.2f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-sub">{describe_expert(sent_mean)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-sub">Focus: newsflow, positioning, crowd mood.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Risk & Stress Expert</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{risk_mean:+.2f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-sub">{describe_expert(risk_mean)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-sub">Focus: volatility, leverage, tails.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("No asset_expert_matrix in JSON – Decision Engine cannot run.")

st.markdown("---")

# ---------------------------------------------------------------------
# 8. SIMPLE BLACK–LITTERMAN STYLE PORTFOLIO TILT
# ---------------------------------------------------------------------
st.subheader("Model Portfolio – Prior vs QuantumFlow Posterior")

if asset_matrix:
    # build separate df for portfolio and compute final_score
    df_port = pd.DataFrame(asset_matrix)

    W_MACRO = 0.30
    W_TECH = 0.30
    W_SENT = 0.20
    W_RISK = 0.20

    for col in ["macro_score", "technical_score", "sentiment_score", "risk_score"]:
        if col not in df_port.columns:
            df_port[col] = 0.0

    df_port["final_score"] = (
        W_MACRO * df_port["macro_score"]
        + W_TECH * df_port["technical_score"]
        + W_SENT * df_port["sentiment_score"]
        + W_RISK * df_port["risk_score"]
    )

    prior_weights = {
        "NVDA": 16.0,
        "MSFT": 22.0,
        "AAPL": 22.0,
        "BTCUSD": 20.0,
        "ETHUSD": 20.0,
    }

    rows = []
    tilt_factor = 10.0  # each 0.1 in score = 1% tilt

    for ticker, prior in prior_weights.items():
        row_df = df_port[df_port["ticker"] == ticker]
        if row_df.empty:
            continue

        row = row_df.iloc[0]
        score = row["final_score"]
        tilt = score * tilt_factor
        raw_new = prior + tilt
        if raw_new < 0:
            raw_new = 0.0  # no negative weights in MVP

        rows.append(
            {
                "ticker": ticker,
                "name": row["name"],
                "prior_weight_pct": prior,
                "final_score": score,
                "tilt_pct": tilt,
                "raw_new_weight": raw_new,
            }
        )

    if rows:
        total_raw = sum(r["raw_new_weight"] for r in rows)
        for r in rows:
            r["posterior_weight_pct"] = (
                r["raw_new_weight"] / total_raw * 100.0 if total_raw > 0 else 0.0
            )

        port_df = pd.DataFrame(rows)
        port_df = port_df[
            [
                "ticker",
                "name",
                "prior_weight_pct",
                "final_score",
                "tilt_pct",
                "posterior_weight_pct",
            ]
        ]

        st.dataframe(
            port_df.style.set_table_attributes('class="dataframe"').format(
                {
                    "prior_weight_pct": "{:.1f}%",
                    "tilt_pct": "{:+.1f}%",
                    "posterior_weight_pct": "{:.1f}%",
                    "final_score": "{:+.2f}",
                }
            ),
            use_container_width=True,
        )

        st.markdown(
            "_Interpretation_: prior weights represent a benchmark allocation; "
            "QuantumFlow tilts them up or down based on the multi-expert final score, "
            "then re-normalizes to 100%.",
        )

        # ----------------------------------------
        # Investor profile – blend benchmark & QuantumFlow
        # ----------------------------------------
        st.markdown("### Investor Profile Allocation")

        profile = st.selectbox(
            "Select investor profile",
            ["Conservative", "Balanced", "Aggressive"],
            index=1,
            help="Profiles adjust how strongly we tilt away from the benchmark weights.",
        )

        if profile == "Conservative":
            alpha = 0.4  # 40% QuantumFlow view, 60% benchmark
        elif profile == "Balanced":
            alpha = 0.7  # 70% QuantumFlow, 30% benchmark
        else:  # Aggressive
            alpha = 0.9  # 90% QuantumFlow, 10% benchmark

        w_prior = port_df["prior_weight_pct"].to_numpy(dtype=float)
        w_post = port_df["posterior_weight_pct"].to_numpy(dtype=float)

        blended = alpha * w_post + (1.0 - alpha) * w_prior
        if blended.sum() > 0:
            blended = blended / blended.sum() * 100.0

        port_df["profile_weight_pct"] = blended

        st.dataframe(
            port_df[
                [
                    "ticker",
                    "name",
                    "prior_weight_pct",
                    "posterior_weight_pct",
                    "profile_weight_pct",
                    "final_score",
                ]
            ].style.set_table_attributes('class="dataframe"').format(
                {
                    "prior_weight_pct": "{:.1f}%",
                    "posterior_weight_pct": "{:.1f}%",
                    "profile_weight_pct": "{:.1f}%",
                    "final_score": "{:+.2f}",
                }
            ),
            use_container_width=True,
        )

        # Pie chart for chosen profile
        fig_port = px.pie(
            port_df,
            names="ticker",
            values="profile_weight_pct",
            title=f"Portfolio Allocation – {profile} Profile",
        )
        st.plotly_chart(fig_port, use_container_width=True)

    else:
        st.info("No overlapping tickers between priors and asset_expert_matrix.")
else:
    st.info("No asset_expert_matrix – cannot build portfolio.")

st.markdown("---")

# ---------------------------------------------------------------------
# 9. CRYPTO SNAPSHOT
# ---------------------------------------------------------------------
st.subheader("Crypto Snapshot")

if crypto:
    crypto_df = pd.DataFrame(crypto)

    fmt = {}
    if "price" in crypto_df.columns:
        fmt["price"] = "{:,.2f}"
    if "chg_1d_pct" in crypto_df.columns:
        fmt["chg_1d_pct"] = "{:+.2f}%"
    if "chg_7d_pct" in crypto_df.columns:
        fmt["chg_7d_pct"] = "{:+.2f}%"
    if "chg_1m_pct" in crypto_df.columns:
        fmt["chg_1m_pct"] = "{:+.2f}%"

    styled_crypto = crypto_df.style.set_table_attributes('class="dataframe"')
    if fmt:
        styled_crypto = styled_crypto.format(fmt)

    st.dataframe(styled_crypto, use_container_width=True)
else:
    st.info("No crypto_snapshot in JSON.")

st.markdown("---")

# ---------------------------------------------------------------------
# 10. KEY NARRATIVES (OPTIONAL EXTRA VIEW)
# ---------------------------------------------------------------------
st.subheader("Key Narratives (Quick Reference)")

if narratives:
    for n in narratives:
        st.markdown(f"- {n}")
else:
    st.write("No narratives provided in JSON.")

st.markdown("---")

# ---------------------------------------------------------------------
# 11. TODAY'S PLAYBOOK – RETAIL INVESTOR VIEW
# ---------------------------------------------------------------------
st.subheader("Today's Playbook for Retail Investors")

if asset_matrix:
    df_play = pd.DataFrame(asset_matrix)

    for col in ["macro_score", "technical_score", "sentiment_score", "risk_score"]:
        if col not in df_play.columns:
            df_play[col] = 0.0

    df_play["final_score"] = (
        0.30 * df_play["macro_score"]
        + 0.30 * df_play["technical_score"]
        + 0.20 * df_play["sentiment_score"]
        + 0.20 * df_play["risk_score"]
    )

    def map_action_local(score: float) -> str:
        if score >= 0.40:
            return "STRONG_OVERWEIGHT"
        elif score >= 0.15:
            return "OVERWEIGHT"
        elif score > -0.15:
            return "NEUTRAL"
        elif score > -0.40:
            return "UNDERWEIGHT"
        else:
            return "AVOID"

    df_play["action"] = df_play["final_score"].apply(map_action_local)

    over = df_play[df_play["action"].isin(["STRONG_OVERWEIGHT", "OVERWEIGHT"])]["ticker"].tolist()
    under = df_play[df_play["action"].isin(["UNDERWEIGHT", "AVOID"])]["ticker"].tolist()

    high_vol = []
    if "realized_vol_30d_pct" in df_play.columns:
        high_vol = df_play[df_play["realized_vol_30d_pct"] >= 35]["ticker"].tolist()

    st.markdown("**For long-term investors (multi-year horizon):**")
    if over:
        st.markdown(
            "- Build your core exposure around high-quality names the engine favours: "
            f"**{', '.join(over)}**, with gradual scaling rather than all-in moves."
        )
    else:
        st.markdown(
            "- Maintain diversified exposure; the engine does not show strong long-term conviction today."
        )

    st.markdown("**For tactical / short-term traders (days–weeks):**")
    if high_vol:
        st.markdown(
            f"- Expect large swings in **{', '.join(high_vol)}**; suitable only for active traders "
            "with tight stops and clear risk limits."
        )
    if under:
        st.markdown(
            f"- Treat **{', '.join(under)}** as areas to reduce risk or wait for better entry points; "
            "momentum and risk conditions are unfavourable for now."
        )
    if not high_vol and not under:
        st.markdown("- No clear de-risking zones identified – environment remains mixed and tactical.")
else:
    st.write("Playbook is unavailable – no asset matrix in snapshot.")

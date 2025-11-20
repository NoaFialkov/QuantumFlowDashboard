"""
QuantumFlow – AI Trading CoPilot
Dashboard Demo – November 20, 2025

Fully realistic *simulation* wired to real market narrative:
- Nvidia blows out earnings, AI demand still surging
- AI bubble fears remain elevated but postponed
- Global risk-on move, led by tech and semiconductors

In the product vision, the core brain is a DRL-based Decision Engine
that learns how to weight a set of expert models over time.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="QuantumFlow – AI Trading CoPilot",
    page_icon="💹",
    layout="wide",
)

# --------------------
# SIDEBAR – INVESTOR PROFILE
# --------------------
st.sidebar.title("👤 Investor Profile")

risk_profile = st.sidebar.radio(
    "Risk profile",
    options=["Conservative", "Moderate", "Aggressive"],
    index=1,
)

capital = st.sidebar.number_input(
    "Portfolio size (USD)",
    min_value=5_000,
    max_value=5_000_000,
    step=5_000,
    value=100_000,
)

time_horizon = st.sidebar.selectbox(
    "Primary horizon",
    options=["1 day", "1 week", "1 month", "3–6 months"],
    index=2,
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "This is a **realistic simulation** of how the live QuantumFlow platform will look "
    "once the MVP expert models and DRL-based Decision Engine are fully wired. "
    "Market narrative and magnitudes are based on November 20, 2025 conditions."
)

# --------------------
# MARKET CONTEXT – NOV 20, 2025 (SIMULATED FROM REAL NEWS)
# --------------------
today = datetime(2025, 11, 20)
today_str = today.strftime("%Y-%m-%d")

market_regime = {
    "name": "AI-led Risk-On, Narrow Leadership",
    "risk_level": "Elevated but favorable for bulls",
    "volatility": "High in mega-cap AI & semis, moderate elsewhere",
    "comment": (
        "After Nvidia's blowout earnings and guidance, global equities are rallying. "
        "Leadership is concentrated in AI and semiconductor names, which keeps bubble "
        "fears alive even as fundamentals remain exceptionally strong."
    ),
    # 0–1: how 'stretched' the AI trade feels
    "ai_bubble_score": 0.80,
}

# Macro snapshot for a quick "market mood" read.
macro_assets = pd.DataFrame(
    [
        ["SPY",  "S&P 500",                 "Equity Index",   6700,  +1.2,  22.0],
        ["QQQ",  "Nasdaq 100",              "Equity Index",  24500,  +1.8,  35.0],
        ["NDX7", "Magnificent 7 basket",    "Thematic",          0,  +2.3,  48.0],
        ["SOXX", "Semiconductor ETF",       "Sector ETF",     910,  +3.2,  58.0],
        ["GLD",  "Gold",                    "Commodity",     4025,  -0.4,  49.0],
        ["USO",  "Oil (USO ETF)",           "Commodity",       58,  -0.2, -16.0],
        ["TLT",  "Long Treasuries",         "Bond ETF",       101,  -0.5,  -5.5],
        ["BTC",  "Bitcoin",                 "Crypto",      92000,  +1.8,  80.0],
    ],
    columns=["Ticker", "Name", "Type", "Level", "Daily%", "YTD%"],
)

# --------------------
# DECISION ENGINE – 20 ASSETS UNIFIED SIGNALS (SIMULATED)
# --------------------
signals = pd.DataFrame(
    [
        # ticker, name, asset_class, price, daily%, ytd%,
        # decision, side, pred_return, confidence, base_alloc, stop, take, horizon
        ["AAPL", "Apple", "Mega-cap tech (Quality)", 285,  1.0,  30.0,
         "Trim slightly, keep as core", "Long", 0.02, 0.76, 0.04, -0.07, 0.10, "3–6 months"],
        ["MSFT", "Microsoft", "Core AI & Cloud",     435,  2.1,  47.0,
         "Hold / modest add on dips", "Long", 0.03, 0.82, 0.05, -0.07, 0.12, "3–6 months"],
        ["NVDA", "Nvidia", "AI infrastructure leader", 185, 6.0, 125.0,
         "Overweight but size carefully", "Long", 0.08, 0.74, 0.05, -0.12, 0.22, "1–3 months"],
        ["AMZN", "Amazon", "E-com + Cloud",         170,  1.7,  44.0,
         "Hold; add if pullback >5%", "Long", 0.025, 0.70, 0.04, -0.08, 0.13, "3–6 months"],
        ["META", "Meta", "Social + AI ads",         500,  2.4,  67.0,
         "Reduce a bit after rally", "Long", 0.02, 0.68, 0.03, -0.10, 0.14, "1–3 months"],
        ["GOOGL", "Alphabet", "Search + AI + Cloud", 286,  1.4,  40.0,
         "Hold as diversified AI play", "Long", 0.025, 0.73, 0.05, -0.07, 0.11, "3–6 months"],
        ["TSLA", "Tesla", "EV + optionality",       212,  3.0,  12.0,
         "Speculative satellite position only", "Long", 0.06, 0.56, 0.02, -0.15, 0.25, "1–3 months"],

        ["SPY", "S&P 500 ETF", "Broad US market",   670,  1.2,  22.0,
         "Market-weight / slight overweight", "Long", 0.02, 0.78, 0.10, -0.06, 0.09, "3–6 months"],
        ["QQQ", "Nasdaq 100 ETF", "Growth & Tech",  410,  1.8,  35.0,
         "Overweight vs SPY while AI trend holds", "Long", 0.03, 0.80, 0.08, -0.08, 0.14, "1–3 months"],
        ["SOXX", "Semiconductor ETF", "AI supply chain", 910, 3.2, 58.0,
         "Add on strength; core AI beta", "Long", 0.05, 0.77, 0.06, -0.10, 0.18, "1–3 months"],
        ["XLK", "Tech Select (XLK)", "US tech sector", 220, 2.0, 37.0,
         "Hold; complements QQQ exposure", "Long", 0.025, 0.75, 0.05, -0.08, 0.13, "3–6 months"],
        ["XLE", "Energy Select (XLE)", "Energy / Oil & Gas", 95, -0.3,  8.0,
         "Gradual rotation into value", "Long", 0.03, 0.69, 0.06, -0.09, 0.16, "3–9 months"],
        ["XLP", "Consumer Staples (XLP)", "Defensive", 80, -0.1,  9.0,
         "Maintain as low-volatility buffer", "Long", 0.01, 0.72, 0.04, -0.05, 0.07, "6–12 months"],

        ["GLD", "Gold ETF", "Defensive hedge",      4025, -0.4, 49.0,
         "Trim slightly, keep core hedge", "Long", 0.01, 0.70, 0.05, -0.06, 0.09, "6–12 months"],
        ["USO", "Oil (USO ETF)", "Oil proxy",       58,  -0.2, -16.0,
         "Tactical only, not a core holding", "Long", 0.02, 0.55, 0.03, -0.12, 0.20, "1–3 months"],

        ["TLT", "Long Treasuries", "Duration / Rates", 101, -0.5, -5.5,
         "Small allocation as volatility dampener", "Long", 0.01, 0.65, 0.04, -0.04, 0.06, "6–12 months"],
        ["SHY", "Short-Term Treas.", "Cash-like",   81,   0.1,  3.0,
         "Parking place for dry powder", "Long", 0.003, 0.85, 0.08, -0.01, 0.02, "Any"],

        ["BTC", "Bitcoin", "High-beta macro risk", 92000, 1.8, 80.0,
         "Small, high-risk satellite", "Long", 0.10, 0.52, 0.02, -0.25, 0.40, "1–6 months"],
        ["ETH", "Ethereum", "Crypto platform",     4700,  1.5, 65.0,
         "Even smaller than BTC, only if risk-seeking", "Long", 0.09, 0.50, 0.01, -0.28, 0.42, "1–6 months"],
    ],
    columns=[
        "Ticker", "Name", "AssetClass", "Price", "Daily%", "YTD%",
        "Decision", "Side", "PredictedReturn", "Confidence",
        "BaseAllocation", "StopLoss%", "TakeProfit%", "SuggestedHorizon",
    ],
)

# Scale allocation by risk profile
risk_mult = {"Conservative": 0.6, "Moderate": 1.0, "Aggressive": 1.4}[risk_profile]
signals["SuggestedAllocation%"] = (signals["BaseAllocation"] * risk_mult * 100).round(1)
signals["PositionNotional"] = (signals["SuggestedAllocation%"] / 100.0 * capital).round(0)
signals["Confidence%"] = (signals["Confidence"] * 100).round(1)
signals["PredictedReturn%"] = (signals["PredictedReturn"] * 100).round(1)

# --------------------
# EXPERT BREAKDOWN – 4 EXPERTS FOR A FEW KEY TICKERS
# --------------------
expert_breakdown = {
    "NVDA": {
        "News": {
            "score": 0.8,
            "note": (
                "Blowout quarter and raised guidance; management directly pushed back on "
                "AI bubble fears, stressing durable demand from hyperscalers and enterprises."
            ),
        },
        "Technical": {
            "score": 0.5,
            "note": (
                "Breakout on huge volume after a consolidation; options pricing had implied "
                "a ~7% move and the stock is near the upper end of that range."
            ),
        },
        "Regime": {
            "score": 0.3,
            "note": (
                "Global risk-on move with Nvidia as the AI bellwether; markets treating this "
                "as confirmation that the AI cycle is intact."
            ),
        },
        "Risk": {
            "score": -0.3,
            "note": (
                "Crowded positioning and very high expectations. A single disappointing quarter "
                "could trigger a sharp drawdown, so position size must stay controlled."
            ),
        },
        "final": {
            "score": 0.35,
            "label": "Overweight core AI exposure, but avoid oversized single-name risk.",
        },
    },
    "GLD": {
        "News": {
            "score": -0.1,
            "note": (
                "Risk-on tone post-Nvidia sends some flows away from gold into equities and crypto."
            ),
        },
        "Technical": {
            "score": 0.2,
            "note": (
                "Still in a medium-term uptrend, but short-term momentum has cooled."
            ),
        },
        "Regime": {
            "score": 0.1,
            "note": (
                "Macro uncertainty (rates, growth) remains, so a structural hedge is still justified."
            ),
        },
        "Risk": {
            "score": 0.4,
            "note": (
                "Low correlation to AI mega-caps; helps reduce portfolio tail risk if the AI trade reverses later."
            ),
        },
        "final": {
            "score": 0.15,
            "label": "Maintain a smaller but persistent hedge allocation.",
        },
    },
    "AAPL": {
        "News": {
            "score": 0.1,
            "note": (
                "Stable franchise, less directly tied to the AI boom narrative than Nvidia or Microsoft."
            ),
        },
        "Technical": {
            "score": -0.1,
            "note": (
                "Extended versus longer-term moving averages; some evidence of mild distribution days."
            ),
        },
        "Regime": {
            "score": 0.2,
            "note": (
                "Behaves as a quasi-defensive mega-cap within tech during volatile AI-driven swings."
            ),
        },
        "Risk": {
            "score": -0.2,
            "note": (
                "For many investors Apple is an outsized position; prudent to trim and rebalance into a basket."
            ),
        },
        "final": {
            "score": 0.0,
            "label": "Slight trim and keep as a smaller, diversified core holding.",
        },
    },
}

# --------------------
# HEADER
# --------------------
header_left, header_right = st.columns([2, 3])

with header_left:
    st.markdown("### 💠 QuantumFlow")
    st.markdown("#### AI Trading CoPilot – DRL Decision Engine Demo")

with header_right:
    st.markdown(
        f"""
        <div style="text-align:right; color:#9CA3AF;">
            <div>Market date: <b>{today_str}</b></div>
            <div>Profile: <b>{risk_profile}</b> | Capital: <b>${capital:,.0f}</b> | Horizon: <b>{time_horizon}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# --------------------
# SECTION 1 – MARKET ATMOSPHERE & AI BUBBLE CONTEXT
# --------------------
st.subheader("🧭 Market Atmosphere – Regime & AI Bubble Context")

col_regime, col_ai, col_macro = st.columns([2, 2, 3])

with col_regime:
    st.markdown("##### Regime snapshot")
    st.markdown(f"**Current regime:** {market_regime['name']}")
    st.markdown(f"**Risk level:** {market_regime['risk_level']}")
    st.markdown(f"**Volatility:** {market_regime['volatility']}")
    st.markdown(f"**Comment:** {market_regime['comment']}")

with col_ai:
    st.markdown("##### AI concentration & bubble risk")
    ai_score = market_regime["ai_bubble_score"]
    st.metric("AI bubble stress (0–1)", value=f"{ai_score:.2f}")
    if ai_score > 0.75:
        st.warning(
            "AI leadership remains extremely concentrated: Nvidia and a handful of mega-caps "
            "drive a disproportionate share of index returns. Fundamentals are strong, but "
            "positioning and sentiment are stretched, so risk management and sizing matter a lot."
        )
    else:
        st.info(
            "AI valuations are elevated but not extreme; the market is still differentiating between "
            "winners and weaker stories. The bubble narrative is there, but not at a breaking point."
        )

with col_macro:
    st.markdown("##### Macro & cross-asset snapshot")
    st.dataframe(
        macro_assets.style.format(
            {
                "Level": "{:,.2f}",
                "Daily%": "{:+.2f}%",
                "YTD%": "{:+.1f}%",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "Nvidia's earnings and guidance have triggered a relief rally in tech and semiconductors, "
    "with risk assets broadly bid while safe-haven demand (gold, long bonds) eases."
)

# --------------------
# SECTION 2 – UNIFIED SIGNALS FOR 20 ASSETS
# --------------------
st.subheader("🎯 Unified Signals – 20 Key Assets Across the AI & Macro Landscape")

st.markdown(
    "Each row is a **final decision** from the (simulated) QuantumFlow Decision Engine: "
    "machine-learning forecasts, news momentum, technical structure, market regime and risk module "
    "are already combined into a single, explainable recommendation."
)

display_cols = [
    "Ticker", "Name", "AssetClass", "Price", "Daily%", "YTD%",
    "Decision", "Side", "PredictedReturn%", "Confidence%",
    "SuggestedAllocation%", "PositionNotional",
    "StopLoss%", "TakeProfit%", "SuggestedHorizon",
]

signals_view = (
    signals[display_cols]
    .rename(columns={
        "Daily%": "Daily %",
        "YTD%": "YTD %",
        "PredictedReturn%": "Pred. return",
        "Confidence%": "Confidence",
        "SuggestedAllocation%": "Alloc. %",
        "PositionNotional": "Notional ($)",
        "StopLoss%": "Stop %",
        "TakeProfit%": "Take %",
    })
)

st.dataframe(
    signals_view.style.format(
        {
            "Price": "${:,.2f}",
            "Daily %": "{:+.2f}%",
            "YTD %": "{:+.1f}%",
            "Pred. return": "{:+.1f}%",
            "Confidence": "{:.1f}%",
            "Alloc. %": "{:.1f}%",
            "Notional ($)": "${:,.0f}",
            "Stop %": "{:+.1f}%",
            "Take %": "{:+.1f}%",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Allocations are already scaled to your selected risk profile and portfolio size. "
    "In the live product, these numbers will be recomputed continuously from fresh data and DRL policy updates."
)

# --------------------
# SECTION 3 – DECISION ENGINE & 4-EXPERT DRILL-DOWN
# --------------------
st.subheader("🧠 Decision Engine (DRL) – 4-Expert Breakdown for a Single Asset")

st.markdown(
    "The QuantumFlow Decision Engine is designed as a **DRL policy** that learns how to weight "
    "four expert models over time:\n\n"
    "- **News Expert** – real-time sentiment, velocity and impact of headlines\n"
    "- **Technical Expert** – trend, momentum, volatility and key price levels\n"
    "- **Market Regime Expert** – bull/bear/sideways, concentration and macro backdrop\n"
    "- **Risk Expert** – position sizing, tail risk and portfolio-level constraints\n\n"
    "In this demo, we simulate the final score from these four experts for a subset of assets."
)

selected_ticker = st.selectbox(
    "Select a ticker to inspect the expert breakdown:",
    options=signals["Ticker"].tolist(),
    index=list(signals["Ticker"]).index("NVDA") if "NVDA" in list(signals["Ticker"]) else 0,
)

row = signals[signals["Ticker"] == selected_ticker].iloc[0]

st.markdown(
    f"""
**{selected_ticker} – {row['Name']}**  

- Final decision: **{row['Decision']}** ({row['Side']})  
- Expected move: **{row['PredictedReturn%']:+.1f}%** over {row['SuggestedHorizon']}  
- Model confidence: **{row['Confidence%']:.1f}%**  
- Suggested allocation: **{row['SuggestedAllocation%']:.1f}%** of your portfolio  
  → approx **${row['PositionNotional']:,.0f}**
"""
)

if selected_ticker in expert_breakdown:
    bd = expert_breakdown[selected_ticker]
    # Compute a simple "engine score" as the average of the 4 expert scores
    engine_score = np.mean([
        bd["News"]["score"],
        bd["Technical"]["score"],
        bd["Regime"]["score"],
        bd["Risk"]["score"],
    ])
    st.metric(
        "Decision Engine (simulated DRL) score",
        value=f"{engine_score:+.2f}",
        help=(
            "In production this score will be generated by a DRL policy that learns, over time, "
            "how to weight the four experts to maximize risk-adjusted returns."
        ),
    )

    e_cols = st.columns(4)
    for col, name in zip(e_cols, ["News", "Technical", "Regime", "Risk"]):
        with col:
            score = bd[name]["score"]
            icon = "🟢" if score > 0.1 else "🔴" if score < -0.1 else "⚪"
            st.markdown(f"**{icon} {name} Expert**")
            st.markdown(f"Score: `{score:+.2f}`")
            st.markdown(f"_{bd[name]['note']}_")
    st.markdown("---")
    st.markdown(f"**Final synthesis:** `{bd['final']['score']:+.2f}` → {bd['final']['label']}")
else:
    st.info(
        "In the full product every asset will have a 4-expert breakdown and Decision Engine score. "
        "For this demo, detailed expert commentary is shown for a subset of key tickers (e.g., NVDA, GLD, AAPL)."
    )

# --------------------
# SECTION 4 – PORTFOLIO-LEVEL SIMULATION
# --------------------
st.subheader("📊 Portfolio Simulation – If You Followed QuantumFlow Today")

total_alloc = signals["SuggestedAllocation%"].sum()
weighted_pred_return = (
    (signals["SuggestedAllocation%"] * signals["PredictedReturn%"]).sum()
    / max(total_alloc, 1)
)

col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    st.metric(
        "Total allocated capital",
        value=f"${(total_alloc / 100 * capital):,.0f}",
        delta=f"{total_alloc:.1f}% of portfolio",
    )
with col_p2:
    st.metric(
        "Blended expected return (idea set)",
        value=f"{weighted_pred_return:+.1f}%"
    )
with col_p3:
    st.metric(
        "Number of active ideas",
        value=f"{len(signals)}"
    )

st.markdown(
    "In the production version, this panel will link to full backtests: "
    "Sharpe ratio, maximum drawdown, hit rate, and scenario tests such as "
    "`What if the AI mega-caps drop 20% from here?`"
)

# --------------------
# SECTION 5 – WHY THIS IS DIFFERENT
# --------------------
st.markdown("---")
st.subheader("🚀 Why QuantumFlow Is Not Just Another Trading App")

st.markdown(
    """
- 🧩 **Multi-expert brain** – Instead of a single monolithic model, QuantumFlow combines a News Expert, Technical Expert, Market Regime Expert and Risk Expert, then lets a DRL-based Decision Engine learn how to weight them.
- ✍️ **Explainable by design** – Every recommendation can be decomposed: which headlines drove it, what the chart looks like, what regime we are in, and how risk constraints shaped the final call.
- 🛡️ **Risk as a first-class feature** – Position size, stop-loss and take-profit are derived from volatility, correlation and your risk profile – not from arbitrary fixed percentages.
- 🌐 **AI bubble aware, not AI bubble blind** – The engine understands that Nvidia’s success both powers the rally and concentrates risk. When AI is too crowded, QuantumFlow rotates part of the portfolio into hedges and alternative themes instead of just saying “buy the dip”.
- 🤝 **Built for serious retail investors** – The same decision logic hedge funds use (multi-model, DRL-style orchestration), but in a transparent interface that a self-directed investor can actually understand and act on.
"""
)

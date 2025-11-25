"""
QuantumFlow – Model-Centric MVP Dashboard (v2, UX-Spec Aligned + UX Tweaks)

Changes vs previous version:
- Search + profile moved to sidebar (smaller footprint, toggleable expander)
- HOME: portfolio performance chart + current allocation pie side-by-side
- HOME: optimal allocation comparison + simulation kept below
- Top Picks: BUY/SELL/HOLD decision is more visually prominent
- ASSET DETAIL navigation bug fixed (uses safe rerun wrapper)
- MARKETS: regime + risk cards + mini index charts (S&P, Nasdaq, BTC)
- NEWS: vertical split between news articles + social signals (X / Reddit)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
# Page + Global Style
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="QuantumFlow – AI-Powered Investing",
    page_icon="📈",
    layout="wide",
)


def inject_global_styles():
    st.markdown(
        """
        <style>
        body {
            background-color: #050816;
        }

        .qf-header-title {
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
        }

        .qf-header-subtitle {
            font-size: 13px;
            color: #a0aec0;
        }

        .qf-card {
            background: radial-gradient(circle at top left, rgba(56,189,248,0.16), rgba(15,23,42,0.95));
            border-radius: 16px;
            padding: 1rem 1.2rem;
            border: 1px solid rgba(148,163,184,0.4);
        }

        .qf-section-title {
            font-size: 18px;
            font-weight: 600;
            color: #e5e7eb;
            margin-bottom: 0.25rem;
        }

        .qf-section-subtitle {
            font-size: 12px;
            color: #9ca3af;
            margin-bottom: 0.75rem;
        }

        .qf-pill {
            display: inline-block;
            border-radius: 999px;
            padding: 0.1rem 0.6rem;
            font-size: 11px;
            font-weight: 500;
        }

        .qf-pill-positive {
            background: rgba(22,163,74,0.15);
            color: #4ade80;
        }

        .qf-pill-negative {
            background: rgba(248,113,113,0.15);
            color: #fca5a5;
        }

        .qf-pill-neutral {
            background: rgba(148,163,184,0.3);
            color: #e5e7eb;
        }

        .qf-pill-risk {
            background: rgba(251,191,36,0.18);
            color: #facc15;
        }

        .qf-ticker-pill {
            display: inline-block;
            padding: 0.15rem 0.6rem;
            font-size: 11px;
            border-radius: 999px;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(148,163,184,0.4);
            color: #e5e7eb;
            margin-right: 0.3rem;
        }

        .qf-expert-card {
            border-radius: 14px;
            padding: 0.75rem 0.9rem;
            border: 1px solid rgba(148,163,184,0.5);
            background: radial-gradient(circle at top left, rgba(96,165,250,0.16), rgba(15,23,42,0.95));
        }

        .qf-decision-card {
            border-radius: 16px;
            padding: 1rem 1.2rem;
            border: 1px solid rgba(129,140,248,0.8);
            background: radial-gradient(circle at top, rgba(129,140,248,0.18), rgba(15,23,42,0.98));
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Helpers: rerun wrapper
# -----------------------------------------------------------------------------

def rerun_app():
    """Safe rerun wrapper for different Streamlit versions."""
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        # Older Streamlit versions
        st.experimental_rerun()


# -----------------------------------------------------------------------------
# Session State & Demo Data
# -----------------------------------------------------------------------------

AVAILABLE_TICKERS = [
    "NVDA",
    "AAPL",
    "MSFT",
    "GOOGL",
    "META",
    "TSLA",
    "AMZN",
    "BTC-USD",
    "ETH-USD",
]


def init_session_state():
    if "main_tab" not in st.session_state:
        st.session_state["main_tab"] = "HOME"
    if "view" not in st.session_state:
        st.session_state["view"] = "HOME"  # HOME, MARKETS, NEWS, ASSET_DETAIL
    if "selected_ticker" not in st.session_state:
        st.session_state["selected_ticker"] = None

    # Investment profile
    if "risk_profile" not in st.session_state:
        st.session_state["risk_profile"] = "Moderate"
    if "invest_capital" not in st.session_state:
        st.session_state["invest_capital"] = 25000.0
    if "time_horizon" not in st.session_state:
        st.session_state["time_horizon"] = "Month"  # Day | Week | Month | Year

    # Portfolio data (demo)
    if "portfolio" not in st.session_state:
        st.session_state["portfolio"] = pd.DataFrame(
            [
                {
                    "ticker": "NVDA",
                    "name": "NVIDIA Corp.",
                    "shares": 15,
                    "buy_price": 120.0,
                    "buy_date": "2024-03-01",
                    "current_price": 180.0,
                },
                {
                    "ticker": "AAPL",
                    "name": "Apple Inc.",
                    "shares": 30,
                    "buy_price": 150.0,
                    "buy_date": "2023-11-10",
                    "current_price": 165.0,
                },
                {
                    "ticker": "MSFT",
                    "name": "Microsoft Corp.",
                    "shares": 10,
                    "buy_price": 320.0,
                    "buy_date": "2024-01-20",
                    "current_price": 400.0,
                },
            ]
        )

    if "watchlist" not in st.session_state:
        st.session_state["watchlist"] = [
            "NVDA",
            "AAPL",
            "MSFT",
            "TSLA",
            "META",
            "BTC-USD",
            "ETH-USD",
        ]

    if "show_allocation_simulation" not in st.session_state:
        st.session_state["show_allocation_simulation"] = False


# -----------------------------------------------------------------------------
# Demo Data Providers (to be replaced later with real data)
# -----------------------------------------------------------------------------

def get_demo_global_market_snapshot():
    indices = [
        {"label": "S&P Futures", "price": 4857.25, "pct": +1.2},
        {"label": "Nasdaq Futures", "price": 15890.40, "pct": +1.6},
        {"label": "Dow Futures", "price": 36720.10, "pct": +0.8},
        {"label": "RTY=F", "price": 2051.30, "pct": +0.5},
        {"label": "Crude Oil", "price": 79.30, "pct": -0.4},
        {"label": "Gold", "price": 2320.50, "pct": +0.2},
        {"label": "Silver", "price": 29.10, "pct": -0.6},
        {"label": "EUR/USD", "price": 1.09, "pct": +0.1},
        {"label": "GBP/USD", "price": 1.27, "pct": -0.1},
        {"label": "USD/JPY", "price": 151.8, "pct": +0.3},
        {"label": "10Y Yield", "price": 4.21, "pct": -0.08},
        {"label": "VIX", "price": 18.4, "pct": +12.5},
        {"label": "BTC-USD", "price": 91000, "pct": -3.3},
        {"label": "ETH-USD", "price": 3000, "pct": -4.1},
    ]
    return indices


def get_portfolio_timeseries():
    dates = [datetime.today() - timedelta(days=i) for i in range(90)][::-1]
    base = 10000
    values = []
    val = base
    for _ in dates:
        val = val * (1 + np.random.normal(0.0005, 0.01))
        values.append(val)
    return pd.DataFrame({"date": dates, "value": values})


def compute_portfolio_from_state():
    df = st.session_state["portfolio"].copy()
    if df.empty:
        return df, 0.0
    df["unrealized_pl"] = (df["current_price"] - df["buy_price"]) * df["shares"]
    df["unrealized_pl_pct"] = (df["current_price"] / df["buy_price"] - 1) * 100
    total_value = (df["current_price"] * df["shares"]).sum()
    df["weight_pct"] = df["current_price"] * df["shares"] / total_value * 100
    return df, total_value


def get_demo_expert_views(ticker: str, risk_profile: str, horizon: str):
    base = sum(ord(c) for c in ticker)
    np.random.seed(base)

    def clip(x):
        return float(np.clip(x, -1.0, 1.0))

    views = {
        "Macro & Regime": {
            "score": clip(np.random.normal(0.3, 0.3)),
            "bullets": [
                "Market regime: risk-on, supportive for growth.",
                "Sector showing strong relative strength.",
            ],
        },
        "Technical & Price Action": {
            "score": clip(np.random.normal(0.4, 0.4)),
            "bullets": [
                "Price above key moving averages.",
                "Momentum still positive but monitored.",
            ],
        },
        "News & Sentiment": {
            "score": clip(np.random.normal(0.0, 0.5)),
            "bullets": [
                "Recent headlines skew mostly positive.",
                "Social chatter broadly supportive.",
            ],
        },
        "Risk & Stress": {
            "score": clip(np.random.normal(-0.1, 0.4)),
            "bullets": [
                "Volatility slightly elevated vs long-term.",
                f"Position size adapted to {risk_profile.lower()} profile.",
            ],
        },
    }
    return views


def get_demo_decision(ticker: str, risk_profile: str, horizon: str):
    views = get_demo_expert_views(ticker, risk_profile, horizon)
    scores = [v["score"] for v in views.values()]
    composite = float(np.mean(scores))

    if composite > 0.35:
        action = "BUY"
        conviction = "Strong conviction" if composite > 0.65 else "Moderate conviction"
    elif composite > 0.05:
        action = "HOLD"
        conviction = "Balanced view"
    elif composite > -0.2:
        action = "TRIM"
        conviction = "Cautious"
    else:
        action = "AVOID"
        conviction = "High caution"

    base_alloc = {"Conservative": 0.03, "Moderate": 0.06, "Aggressive": 0.10}[risk_profile]
    suggested_alloc = max(0.0, base_alloc * (0.6 + composite))

    stop_loss_pct = 0.05 if risk_profile == "Conservative" else 0.07 if risk_profile == "Moderate" else 0.09
    take_profit_pct = 0.10 if risk_profile == "Conservative" else 0.13 if risk_profile == "Moderate" else 0.17

    explanation = [
        f"Composite expert score: {composite:+.2f}.",
        "Macro, technical, news and risk experts aligned into a single view.",
        f"Position size and risk envelope tailored to your {risk_profile.lower()} profile.",
    ]

    return {
        "action": action,
        "conviction": conviction,
        "composite": composite,
        "allocation_pct": suggested_alloc * 100,
        "stop_loss_pct": stop_loss_pct * 100,
        "take_profit_pct": take_profit_pct * 100,
        "explanation": explanation,
        "expert_views": views,
    }


def get_demo_news_feed():
    now = datetime.utcnow()
    return [
        {
            "source": "Reuters",
            "time": now - timedelta(minutes=40),
            "headline": "Chipmakers rally as AI demand remains strong",
            "summary": "Semiconductor stocks extend gains after upbeat AI server demand data.",
            "sentiment": "Positive",
            "impact": "High",
            "tickers": ["NVDA", "AMD", "MSFT"],
            "insight": "Likely supportive for AI chip leaders; reinforces bullish view on NVDA.",
        },
        {
            "source": "Bloomberg",
            "time": now - timedelta(hours=2),
            "headline": "Regulators weigh new rules on big tech data practices",
            "summary": "US and EU regulators outline potential new data rules for large platforms.",
            "sentiment": "Negative",
            "impact": "Medium",
            "tickers": ["META", "GOOGL", "AAPL"],
            "insight": "Introduces headline risk; we stay selective in data-heavy names.",
        },
        {
            "source": "CoinDesk",
            "time": now - timedelta(hours=3, minutes=30),
            "headline": "Bitcoin slides after brief run to new local highs",
            "summary": "Crypto markets pull back as traders take profits after a sharp rally.",
            "sentiment": "Negative",
            "impact": "High",
            "tickers": ["BTC-USD", "ETH-USD"],
            "insight": "Short-term pressure after extended run-up; risk-sensitive profiles should size cautiously.",
        },
    ]


def get_demo_model_history(ticker: str):
    today = datetime.today().date()
    rows = []
    for i in range(8):
        date = today - timedelta(days=(i * 7))
        composite = np.random.normal(0.2, 0.5)
        action = "BUY" if composite > 0.25 else "HOLD" if composite > -0.1 else "SELL"
        realized = np.random.normal(0.01 if action == "BUY" else 0.0, 0.03)
        rows.append(
            {
                "date": date,
                "action": action,
                "model_score": composite,
                "realized_return_pct": realized * 100,
            }
        )
    df = pd.DataFrame(rows).sort_values("date", ascending=False)
    df["correct"] = np.where(
        ((df["action"] == "BUY") & (df["realized_return_pct"] > 0))
        | ((df["action"] == "SELL") & (df["realized_return_pct"] < 0)),
        True,
        False,
    )
    return df


def get_demo_sentiment_summary(ticker: str):
    return {
        "score": 0.32,
        "label": "Positive",
        "text": "Recent coverage is skewed positive, driven by strong earnings and AI-related headlines.",
    }


def get_demo_price_and_forecast_series(ticker: str):
    np.random.seed(sum(ord(c) for c in ticker) + 123)
    days_back = 90
    days_forward = 15

    past_dates = [datetime.today() - timedelta(days=i) for i in range(days_back)][::-1]
    price = 100.0
    prices = []
    for _ in past_dates:
        price = price * (1 + np.random.normal(0.0008, 0.02))
        prices.append(price)

    future_dates = [datetime.today() + timedelta(days=i) for i in range(1, days_forward + 1)]
    future_center = []
    future_low = []
    future_high = []
    last_price = prices[-1]
    fc_price = last_price
    for _ in future_dates:
        fc_price = fc_price * (1 + np.random.normal(0.001, 0.015))
        future_center.append(fc_price)
        band = fc_price * 0.03
        future_low.append(fc_price - band)
        future_high.append(fc_price + band)

    return (
        pd.DataFrame({"date": past_dates, "price": prices}),
        pd.DataFrame(
            {
                "date": future_dates,
                "center": future_center,
                "low": future_low,
                "high": future_high,
            }
        ),
    )


def get_demo_index_series(name: str):
    """Demo index timeseries for MARKETS charts."""
    np.random.seed(sum(ord(c) for c in name) + 999)
    days_back = 60
    dates = [datetime.today() - timedelta(days=i) for i in range(days_back)][::-1]
    base = 1000 if "S&P" in name else 1500 if "Nasdaq" in name else 30000
    vals = []
    val = base
    for _ in dates:
        val = val * (1 + np.random.normal(0.0006, 0.012))
        vals.append(val)
    return pd.DataFrame({"date": dates, "value": vals})


def get_demo_social_signals():
    """Demo social signals for NEWS right-hand side."""
    return {
        "aggregate": {
            "score": 0.18,
            "label": "Mildly Positive",
            "text": "Today’s social chatter is modestly positive, concentrated around AI, chips and crypto.",
            "historical": "In similar past clusters, 1D volatility increased by ~2.1% on average for the most-mentioned tickers.",
        },
        "items": [
            {
                "source": "X",
                "handle": "@AI_Investor",
                "time": "1h ago",
                "ticker": "NVDA",
                "sentiment": "Positive",
                "text": "Still crazy how every major AI build-out touches NVIDIA somewhere.",
                "pattern": "Strong AI tweet clusters have historically coincided with short bursts of upside volatility.",
            },
            {
                "source": "Reddit",
                "handle": "r/stocks",
                "time": "3h ago",
                "ticker": "TSLA",
                "sentiment": "Mixed",
                "text": "Debate: is TSLA still a growth stock or just a car company multiple?",
                "pattern": "Mixed sentiment waves often precede choppy sideways action.",
            },
            {
                "source": "X",
                "handle": "@CryptoMacro",
                "time": "5h ago",
                "ticker": "BTC-USD",
                "sentiment": "Negative",
                "text": "Funding rates overheating again; cautious on BTC at these levels.",
                "pattern": "Similar caution clusters historically aligned with short-term pullbacks.",
            },
        ],
    }


# -----------------------------------------------------------------------------
# Navigation Helpers
# -----------------------------------------------------------------------------

def set_page(view: str, main_tab: str = None, ticker: str = None):
    if main_tab is not None:
        st.session_state["main_tab"] = main_tab
    st.session_state["view"] = view
    st.session_state["selected_ticker"] = ticker


def render_sidebar():
    with st.sidebar:
        st.markdown("### QuantumFlow")
        st.markdown(
            "<span style='font-size: 11px; color: #9ca3af;'>AI-guided investing</span>",
            unsafe_allow_html=True,
        )
        # Search
        search_val = st.text_input("🔍 Search ticker", value="", placeholder="e.g. NVDA, BTC-USD")
        if st.button("Go", key="sidebar_search_btn"):
            t = search_val.strip().upper()
            if t in AVAILABLE_TICKERS:
                set_page("ASSET_DETAIL", ticker=t)
                rerun_app()
            else:
                st.warning("Ticker not found in this MVP universe.")

        # Investment profile controls
        with st.expander("👤 My Investment Profile", expanded=True):
            rp = st.radio(
                "Risk appetite",
                options=["Conservative", "Moderate", "Aggressive"],
                index=["Conservative", "Moderate", "Aggressive"].index(st.session_state["risk_profile"]),
            )
            st.session_state["risk_profile"] = rp

            cap = st.number_input(
                "Capital to allocate (USD)",
                min_value=0.0,
                step=1000.0,
                value=float(st.session_state["invest_capital"]),
            )
            st.session_state["invest_capital"] = cap

            horizon = st.radio(
                "Time horizon",
                options=["Day", "Week", "Month", "Year"],
                index=["Day", "Week", "Month", "Year"].index(st.session_state["time_horizon"]),
            )
            st.session_state["time_horizon"] = horizon

            st.markdown(
                "<span style='font-size: 10px; color:#9ca3af;'>All decisions below are tailored to this profile.</span>",
                unsafe_allow_html=True,
            )


def render_top_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="qf-header-title">QuantumFlow</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="qf-header-subtitle">'
            "Model-centric investing: from events and data to clear decisions."
            "</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            "<div class='qf-header-subtitle' style='text-align:right;'>Demo environment</div>",
            unsafe_allow_html=True,
        )


def render_main_nav():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    active = st.session_state["main_tab"]

    with col1:
        if st.button(
            "HOME",
            key="nav_home",
            use_container_width=True,
            type="primary" if active == "HOME" else "secondary",
        ):
            set_page("HOME", main_tab="HOME", ticker=None)

    with col2:
        if st.button(
            "MARKETS",
            key="nav_markets",
            use_container_width=True,
            type="primary" if active == "MARKETS" else "secondary",
        ):
            set_page("MARKETS", main_tab="MARKETS", ticker=None)

    with col3:
        if st.button(
            "NEWS",
            key="nav_news",
            use_container_width=True,
            type="primary" if active == "NEWS" else "secondary",
        ):
            set_page("NEWS", main_tab="NEWS", ticker=None)

    st.markdown("---")


# -----------------------------------------------------------------------------
# Investment Profile Summary (top of HOME + inline string)
# -----------------------------------------------------------------------------

def render_investment_profile_summary_card():
    risk = st.session_state["risk_profile"]
    capital = st.session_state["invest_capital"]
    horizon = st.session_state["time_horizon"]
    horizon_desc = {
        "Day": "the next few sessions",
        "Week": "the coming weeks",
        "Month": "the next 3–6 months",
        "Year": "the next 12+ months",
    }[horizon]
    st.markdown(
        '<div class="qf-section-title">My Investment Profile</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="qf-card">
            <div style="font-size: 13px; color: #9ca3af;">Profile summary</div>
            <div style="font-size: 14px; color: #e5e7eb; margin-top: 4px;">
                You are a <b>{risk}</b> investor, planning to allocate
                <b>${capital:,.0f}</b> over {horizon_desc}.
            </div>
            <div style="font-size: 11px; color: #9ca3af; margin-top: 4px;">
                All recommended position sizes and risk limits below are aligned to this profile.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_investment_profile_summary_inline():
    risk = st.session_state["risk_profile"]
    capital = st.session_state["invest_capital"]
    horizon = st.session_state["time_horizon"]
    return f"{risk} · ${capital:,.0f} capital · {horizon} horizon"


# -----------------------------------------------------------------------------
# HOME – Portfolio, Optimal Allocation, Top Picks, Watchlist, Snapshot
# -----------------------------------------------------------------------------

def render_portfolio_hero():
    df_portfolio, total_value = compute_portfolio_from_state()

    st.markdown(
        '<div class="qf-section-title">My Portfolio & Optimal Allocation</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="qf-section-subtitle">'
        "Built using modern portfolio theory and QuantumFlow expert views, tailored to your profile."
        "</div>",
        unsafe_allow_html=True,
    )

    if df_portfolio.empty:
        st.info("No positions yet. Add at least one position to see allocation and optimization.")
        return

    # Top row: performance chart + current allocation pie
    top_left, top_right = st.columns([2.1, 1.9])

    with top_left:
        df_ts = get_portfolio_timeseries()
        toggle = st.radio(
            "Metric",
            options=["Value", "% Return"],
            horizontal=True,
            key="portfolio_metric_radio",
        )
        base_value = df_ts["value"].iloc[0]
        if toggle == "% Return":
            y = (df_ts["value"] / base_value - 1) * 100
            y_label = "% Return"
        else:
            y = df_ts["value"]
            y_label = "Portfolio value"

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df_ts["date"],
                y=y,
                mode="lines",
                name=y_label,
            )
        )
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=20),
            height=260,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,1)",
            font=dict(color="#e5e7eb"),
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor="rgba(55,65,81,0.5)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '<div style="font-size: 11px; color: #6b7280; margin-top: 4px;">'
            "Simulation only. Model-driven insight, not investment advice."
            "</div>",
            unsafe_allow_html=True,
        )

    with top_right:
        st.markdown(
            '<div style="font-size: 13px; color: #9ca3af;">Current portfolio allocation</div>',
            unsafe_allow_html=True,
        )
        fig_curr = go.Figure(
            data=[
                go.Pie(
                    labels=df_portfolio["ticker"],
                    values=df_portfolio["weight_pct"],
                    hole=0.55,
                )
            ]
        )
        fig_curr.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=260,
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,1)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5,
                font=dict(color="#e5e7eb"),
            ),
        )
        st.plotly_chart(fig_curr, use_container_width=True)
        top_holdings = df_portfolio.sort_values("weight_pct", ascending=False).head(3)
        txt = ", ".join(
            f"{row['ticker']} {row['weight_pct']:.1f}%" for _, row in top_holdings.iterrows()
        )
        st.markdown(
            f'<div style="font-size: 11px; color: #9ca3af;">Top holdings: {txt}</div>',
            unsafe_allow_html=True,
        )

    # Below: optimal allocation comparison + simulation
    st.markdown("")
    st.markdown(
        '<div class="qf-section-subtitle" style="margin-bottom: 0.25rem;">'
        "Compare your current allocation to QuantumFlow’s optimal suggestion."
        "</div>",
        unsafe_allow_html=True,
    )

    tickers = df_portfolio["ticker"].tolist()
    current_weights = df_portfolio["weight_pct"].values
    risk = st.session_state["risk_profile"]
    horizon = st.session_state["time_horizon"]

    qf_scores = []
    for t in tickers:
        d = get_demo_decision(t, risk, horizon)
        qf_scores.append(max(-1.0, min(1.0, d["composite"])))
    qf_scores = np.array(qf_scores)
    shifted = qf_scores - qf_scores.min() + 0.1
    proposed = shifted / shifted.sum() * 100

    optimal_df = pd.DataFrame(
        {
            "ticker": tickers,
            "current_weight_pct": current_weights,
            "proposed_weight_pct": proposed,
        }
    )

    fig_opt = go.Figure()
    fig_opt.add_trace(
        go.Bar(
            x=optimal_df["ticker"],
            y=optimal_df["current_weight_pct"],
            name="Current",
        )
    )
    fig_opt.add_trace(
        go.Bar(
            x=optimal_df["ticker"],
            y=optimal_df["proposed_weight_pct"],
            name="Model",
        )
    )
    fig_opt.update_layout(
        barmode="group",
        margin=dict(l=0, r=0, t=10, b=40),
        height=260,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,1)",
        font=dict(color="#e5e7eb"),
    )
    st.plotly_chart(fig_opt, use_container_width=True)

    st.markdown(
        f"""
        <div style="font-size: 11px; color: #9ca3af; margin-top: 4px;">
            Based on your <b>{risk}</b> profile and <b>{horizon.lower()}</b> horizon,
            we tilt towards stronger QuantumFlow signals and control concentration risk.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Differences + simulation
    optimal_df["diff"] = optimal_df["proposed_weight_pct"] - optimal_df["current_weight_pct"]
    changes = optimal_df.loc[optimal_df["diff"].abs() > 1.0].sort_values("diff", ascending=False)
    if not changes.empty:
        st.markdown(
            '<div style="font-size: 13px; color: #e5e7eb; margin-top: 8px; font-weight: 600;">'
            "Key suggested changes</div>",
            unsafe_allow_html=True,
        )
        for _, row in changes.iterrows():
            arrow = "↑" if row["diff"] > 0 else "↓"
            reason = "stronger signals and supportive fundamentals" if row["diff"] > 0 else "volatility vs your profile"
            st.markdown(
                f"- {arrow} {row['ticker']}: {row['diff']:+.1f}% – {reason}",
            )

    if st.button("Simulate this allocation", key="simulate_alloc_btn"):
        st.session_state["show_allocation_simulation"] = True

    if st.session_state["show_allocation_simulation"]:
        st.markdown("")
        with st.expander("Simulation – Before vs After (demo)", expanded=True):
            sim_df = optimal_df.copy()
            sim_df["current_weight_pct"] = sim_df["current_weight_pct"].round(1)
            sim_df["proposed_weight_pct"] = sim_df["proposed_weight_pct"].round(1)
            st.dataframe(sim_df[["ticker", "current_weight_pct", "proposed_weight_pct"]], hide_index=True)
            st.markdown(
                """
                *Demo metrics (to be replaced with real risk engine):*  
                - Expected annualized return: **+12.4% → +14.8%**  
                - Volatility estimate: **18.1% → 16.9%**  
                - Max drawdown (simulated): **–22% → –19%**
                """,
            )
            st.markdown(
                '<div style="font-size: 11px; color: #6b7280;">'
                "This simulation is a planning tool only. It does not execute any trades."
                "</div>",
                unsafe_allow_html=True,
            )


def render_top_picks():
    st.markdown(
        '<div class="qf-section-title">QuantumFlow Top Picks for You</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="qf-section-subtitle">'
        "Stocks and crypto our Decision Engine currently likes most, given your profile and horizon."
        "</div>",
        unsafe_allow_html=True,
    )

    risk = st.session_state["risk_profile"]
    horizon = st.session_state["time_horizon"]

    rows = []
    for t in AVAILABLE_TICKERS:
        d = get_demo_decision(t, risk, horizon)
        rows.append({"ticker": t, "decision": d})
    rows = sorted(rows, key=lambda r: r["decision"]["composite"], reverse=True)[:8]

    for r in rows:
        t = r["ticker"]
        d = r["decision"]
        score = d["composite"]
        price = np.random.uniform(50, 500)
        daily_pct = np.random.normal(0, 2)
        color = "#4ade80" if daily_pct >= 0 else "#f97373"
        arrow = "▲" if daily_pct >= 0 else "▼"
        sentiment_class = (
            "qf-pill-positive"
            if d["action"] == "BUY"
            else "qf-pill-negative"
            if d["action"] in ["SELL", "AVOID"]
            else "qf-pill-neutral"
        )

        st.markdown(
            f"""
            <div class="qf-card" style="margin-bottom: 0.6rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 13px; font-weight: 600; color: #e5e7eb;">{t}</div>
                    <span class="qf-pill {sentiment_class}" style="font-size: 13px; font-weight: 700;">
                        {d['action']} · {d['conviction']}
                    </span>
                </div>
                <div style="margin-top: 4px; display: flex; justify-content: space-between; align-items: baseline;">
                    <div>
                        <div style="font-size: 18px; font-weight: 600; color: #e5e7eb;">${price:,.2f}</div>
                        <div style="font-size: 11px; color: {color}; margin-top: 2px;">
                            {arrow} {daily_pct:+.2f}%
                        </div>
                    </div>
                    <div style="font-size: 11px; color: #9ca3af; max-width: 55%;">
                        Model score: <b>{score:+.2f}</b><br/>
                        Suggested allocation: <b>{d['allocation_pct']:.1f}%</b> of your portfolio.<br/>
                        Stop-loss: <b>{d['stop_loss_pct']:.1f}%</b> · Take-profit: <b>{d['take_profit_pct']:.1f}%</b>.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View full analysis", key=f"top_pick_{t}"):
            set_page("ASSET_DETAIL", ticker=t)
            rerun_app()


def render_watchlist():
    st.markdown(
        '<div class="qf-section-title">My Watchlist</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="qf-section-subtitle">'
        "Tickers you track, even if they’re not in your portfolio yet."
        "</div>",
        unsafe_allow_html=True,
    )

    watchlist = st.session_state["watchlist"]
    risk = st.session_state["risk_profile"]
    horizon = st.session_state["time_horizon"]

    with st.expander("Add to watchlist"):
        candidates = [t for t in AVAILABLE_TICKERS if t not in watchlist]
        if candidates:
            new_ticker = st.selectbox("Ticker", options=candidates)
            if st.button("Add", key="add_watchlist"):
                watchlist.append(new_ticker)
                st.session_state["watchlist"] = watchlist
                st.success(f"{new_ticker} added to watchlist.")
                rerun_app()
        else:
            st.info("All demo tickers are already in your watchlist.")

    cols = st.columns(2)
    for i, t in enumerate(watchlist):
        col = cols[i % 2]
        with col:
            d = get_demo_decision(t, risk, horizon)
            price = np.random.uniform(50, 500)
            daily_pct = np.random.normal(0, 2)
            color = "#4ade80" if daily_pct >= 0 else "#f97373"
            arrow = "▲" if daily_pct >= 0 else "▼"
            sentiment_class = (
                "qf-pill-positive"
                if d["action"] == "BUY"
                else "qf-pill-negative"
                if d["action"] in ["SELL", "AVOID"]
                else "qf-pill-neutral"
            )

            st.markdown(
                f"""
                <div class="qf-card" style="margin-bottom: 0.6rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 13px; font-weight: 600; color: #e5e7eb;">{t}</div>
                            <div style="font-size: 11px; color: #9ca3af;">
                                QuantumFlow: {d['action']} ({d['composite']:+.2f})
                            </div>
                        </div>
                        <span class="qf-pill {sentiment_class}" style="font-size: 12px; font-weight: 600;">
                            {d['action']}
                        </span>
                    </div>
                    <div style="margin-top: 4px;">
                        <div style="font-size: 16px; font-weight: 600; color: #e5e7eb;">${price:,.2f}</div>
                        <div style="font-size: 11px; color: {color}; margin-top: 2px;">
                            {arrow} {daily_pct:+.2f}%
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("View analysis", key=f"watch_{t}"):
                set_page("ASSET_DETAIL", ticker=t)
                rerun_app()


def render_global_snapshot_compact():
    st.markdown(
        '<div class="qf-section-title">Global market snapshot</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="qf-section-subtitle">'
        "High-level context. Detailed market regime & risk on the MARKETS tab."
        "</div>",
        unsafe_allow_html=True,
    )

    indices = get_demo_global_market_snapshot()
    cols = st.columns(3)
    for i, item in enumerate(indices[:9]):
        col = cols[i % 3]
        with col:
            color = "#4ade80" if item["pct"] >= 0 else "#f97373"
            arrow = "▲" if item["pct"] >= 0 else "▼"
            st.markdown(
                f"""
                <div class="qf-card" style="margin-bottom: 0.6rem;">
                    <div style="font-size: 12px; color: #9ca3af;">{item['label']}</div>
                    <div style="font-size: 16px; font-weight: 600; color: #e5e7eb;">
                        {item['price']:,}
                    </div>
                    <div style="font-size: 11px; color: {color}; margin-top: 2px;">
                        {arrow} {item['pct']:+.2f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div style="font-size: 11px; color: #9ca3af; margin-top: 4px;">'
        "Today the market appears moderately risk-on with volatility elevated but contained (demo summary)."
        "</div>",
        unsafe_allow_html=True,
    )


def render_home():
    render_investment_profile_summary_card()
    st.markdown("")

    left, right = st.columns([2.2, 1.8])
    with left:
        render_portfolio_hero()
        st.markdown("")
        render_top_picks()

    with right:
        render_watchlist()
        st.markdown("")
        render_global_snapshot_compact()


# -----------------------------------------------------------------------------
# ASSET DETAIL – "Ticker Lab"
# -----------------------------------------------------------------------------

def render_asset_detail():
    ticker = st.session_state.get("selected_ticker")
    if not ticker:
        st.warning("No ticker selected. Use HOME, MARKETS or NEWS to pick an asset.")
        return

    risk = st.session_state["risk_profile"]
    horizon = st.session_state["time_horizon"]
    profile_summary = render_investment_profile_summary_inline()
    decision = get_demo_decision(ticker, risk, horizon)
    views = decision["expert_views"]

    # Header
    st.markdown(
        f'<div class="qf-section-title">{ticker} – Ticker Lab</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="qf-section-subtitle">'
        "Fusion of market data with QuantumFlow’s experts and Decision Engine."
        "</div>",
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns([2.5, 2])

    with top_left:
        price = np.random.uniform(80, 500)
        daily_pct = np.random.normal(0, 2)
        color = "#4ade80" if daily_pct >= 0 else "#f97373"
        arrow = "▲" if daily_pct >= 0 else "▼"
        st.markdown(
            f"""
            <div class="qf-card">
                <div style="font-size: 13px; color: #9ca3af;">{ticker}</div>
                <div style="font-size: 26px; font-weight: 700; color: #e5e7eb;">
                    ${price:,.2f}
                </div>
                <div style="font-size: 12px; color: {color}; margin-top: 2px;">
                    {arrow} {daily_pct:+.2f}%
                    <span style="color: #9ca3af; margin-left: 8px;">Demo price – connect Yahoo Finance later.</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_right:
        st.markdown(
            f"""
            <div class="qf-decision-card">
                <div style="font-size: 13px; color: #9ca3af;">QuantumFlow Decision</div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                    <div style="font-size: 18px; font-weight: 700; color: #e5e7eb;">
                        {decision['action']} – {decision['conviction']}
                    </div>
                    <span class="qf-pill {'qf-pill-positive' if decision['action']=='BUY' else 'qf-pill-negative' if decision['action'] in ['SELL','AVOID'] else 'qf-pill-neutral'}">
                        Score {decision['composite']:+.2f} on [-1, +1]
                    </span>
                </div>
                <div style="font-size: 12px; color: #e5e7eb; margin-top: 6px;">
                    Suggested allocation: <b>{decision['allocation_pct']:.1f}%</b> of your portfolio<br/>
                    Risk envelope: stop-loss <b>{decision['stop_loss_pct']:.1f}%</b> below &bull;
                    take-profit band <b>{decision['take_profit_pct']:.1f}%</b> above.
                </div>
                <div style="font-size: 11px; color: #9ca3af; margin-top: 6px;">
                    Profile: {profile_summary}
                </div>
                <ul style="font-size: 11px; color: #9ca3af; margin-top: 6px; padding-left: 18px;">
                    {''.join(f'<li>{line}</li>' for line in decision['explanation'])}
                </ul>
                <div style="font-size: 10px; color: #6b7280; margin-top: 4px;">
                    Model-driven insight, not investment advice.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    # Main chart: price + calls + forecast
    past_df, future_df = get_demo_price_and_forecast_series(ticker)
    show_forecast = st.checkbox("Show model forecast band", value=True)
    show_calls = st.checkbox("Show past model calls", value=True)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=past_df["date"],
            y=past_df["price"],
            mode="lines",
            name="Price (demo)",
        )
    )

    if show_calls:
        hist = get_demo_model_history(ticker)
        for _, row in hist.iterrows():
            dt = datetime.combine(row["date"], datetime.min.time())
            closest_idx = (past_df["date"] - dt).abs().idxmin()
            price_at_call = past_df.loc[closest_idx, "price"]
            marker_symbol = (
                "circle"
                if row["action"] == "BUY"
                else "triangle-up"
                if row["action"] == "SELL"
                else "diamond"
            )
            marker_color = (
                "#22c55e" if row["action"] == "BUY" else "#f97373" if row["action"] == "SELL" else "#e5e7eb"
            )
            fig.add_trace(
                go.Scatter(
                    x=[past_df.loc[closest_idx, "date"]],
                    y=[price_at_call],
                    mode="markers",
                    marker=dict(symbol=marker_symbol, size=9, color=marker_color),
                    name=f"{row['action']} call",
                    hovertemplate=f"{row['date']} – {row['action']}<br>Score {row['model_score']:+.2f}<br>Realized {row['realized_return_pct']:+.2f}%<extra></extra>",
                    showlegend=False,
                )
            )

    if show_forecast:
        fig.add_trace(
            go.Scatter(
                x=future_df["date"],
                y=future_df["center"],
                mode="lines",
                name="Model forecast",
                line=dict(dash="dash"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=list(future_df["date"]) + list(future_df["date"][::-1]),
                y=list(future_df["high"]) + list(future_df["low"][::-1]),
                fill="toself",
                fillcolor="rgba(129,140,248,0.25)",
                line=dict(color="rgba(129,140,248,0)"),
                name="Forecast band",
                showlegend=True,
            )
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=20),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,1)",
        font=dict(color="#e5e7eb"),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(55,65,81,0.5)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        '<div style="font-size: 11px; color: #6b7280;">'
        "Price path, past QuantumFlow calls and a demo forecast band. To be connected to real models later."
        "</div>",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["QuantumFlow Analysis", "Stats & History", "Sentiment & News"])

    with tab1:
        st.markdown(
            '<div class="qf-section-title">How our experts see this asset</div>',
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        expert_items = list(views.items())
        for i, (name, data) in enumerate(expert_items):
            col = c1 if i % 2 == 0 else c2
            score = data["score"]
            if score > 0.4:
                label = "Strongly Bullish"
            elif score > 0.1:
                label = "Bullish"
            elif score > -0.1:
                label = "Neutral"
            elif score > -0.4:
                label = "Bearish"
            else:
                label = "Strongly Bearish"
            with col:
                st.markdown(
                    f"""
                    <div class="qf-expert-card" style="margin-bottom: 0.7rem;">
                        <div style="font-size: 13px; font-weight: 600; color: #e5e7eb;">{name}</div>
                        <div style="font-size: 11px; color: #9ca3af; margin-top: 2px;">View: {label} ({score:+.2f})</div>
                        <div style="margin-top: 6px;">
                            <div style="height: 6px; border-radius: 999px; background: rgba(31,41,55,1); overflow: hidden;">
                                <div style="
                                    width: {int((score + 1) / 2 * 100)}%;
                                    height: 100%;
                                    background: linear-gradient(90deg, #f97373, #22c55e);
                                "></div>
                            </div>
                        </div>
                        <ul style="font-size: 11px; color: #9ca3af; margin-top: 6px; padding-left: 18px;">
                            {''.join(f'<li>{b}</li>' for b in data['bullets'])}
                        </ul>
                        <div style="font-size: 10px; color: #6b7280; margin-top: 4px;">
                            Demo expert view. Later: wired directly to live models.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown(
            '<div style="font-size: 11px; color: #9ca3af; margin-top: 4px;">'
            "Overall, the Decision Engine synthesizes these four views into the single action shown above."
            "</div>",
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            '<div class="qf-section-title">Key stats</div>',
            unsafe_allow_html=True,
        )
        st.info("TODO: Connect to Yahoo Finance for live key statistics (market cap, P/E, 52-week range, etc.).")

        st.markdown(
            '<div class="qf-section-title" style="margin-top: 0.75rem;">QuantumFlow call history</div>',
            unsafe_allow_html=True,
        )
        df_hist = get_demo_model_history(ticker)
        if not df_hist.empty:
            win_rate = df_hist["correct"].mean() * 100
            st.markdown(
                f'<div class="qf-section-subtitle">Demo hit rate ≈ {win_rate:.1f}% over the last {len(df_hist)} calls.</div>',
                unsafe_allow_html=True,
            )
            st.dataframe(df_hist.round(2), hide_index=True, use_container_width=True)
            st.markdown(
                '<div style="font-size: 11px; color: #6b7280; margin-top: 4px;">'
                "Historical performance is illustrative and not a guarantee of future results."
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.info("No model history available yet for this asset.")

    with tab3:
        st.markdown(
            '<div class="qf-section-title">Sentiment & news</div>',
            unsafe_allow_html=True,
        )
        summary = get_demo_sentiment_summary(ticker)
        st.markdown(
            f"""
            <div class="qf-card">
                <div style="font-size: 13px; color: #9ca3af;">Aggregated sentiment (demo)</div>
                <div style="font-size: 16px; font-weight: 600; color: #e5e7eb; margin-top: 4px;">
                    Overall sentiment: {summary['label']} ({summary['score']:+.2f} on [-1, +1])
                </div>
                <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">
                    {summary['text']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("")
        st.markdown(
            '<div class="qf-section-subtitle" style="margin-bottom: 0.5rem;">'
            "Recent stories we scanned that mention this asset (demo feed)."
            "</div>",
            unsafe_allow_html=True,
        )

        feed = get_demo_news_feed()
        related = [item for item in feed if ticker in item["tickers"]]
        if not related:
            st.info("No recent demo stories tied to this ticker yet.")
        else:
            for item in related:
                ts = item["time"].strftime("%Y-%m-%d %H:%M")
                sentiment_class = (
                    "qf-pill-positive"
                    if item["sentiment"] == "Positive"
                    else "qf-pill-negative"
                    if item["sentiment"] == "Negative"
                    else "qf-pill-neutral"
                )
                st.markdown(
                    f"""
                    <div class="qf-card" style="margin-bottom: 0.6rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-size: 12px; color: #9ca3af;">
                                {item['source']} · {ts} UTC
                            </div>
                            <span class="qf-pill {sentiment_class}">
                                Sentiment: {item['sentiment']}
                            </span>
                        </div>
                        <div style="font-size: 13px; font-weight: 600; color: #e5e7eb; margin-top: 4px;">
                            {item['headline']}
                        </div>
                        <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">
                            {item['summary']}
                        </div>
                        <div style="font-size: 12px; color: #e5e7eb; margin-top: 6px;">
                            <span style="font-weight: 600;">QuantumFlow Insight:</span> {item['insight']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# -----------------------------------------------------------------------------
# MARKETS – Regime & Risk + Index Charts + Focus Tickers
# -----------------------------------------------------------------------------

def render_market_regime_overview():
    st.markdown(
        '<div class="qf-section-title">Today’s Market Regime & Risk (demo)</div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns([2, 2])

    with left:
        st.markdown(
            """
            <div class="qf-card">
                <div style="font-size: 13px; color: #9ca3af;">Current regime</div>
                <div style="font-size: 16px; font-weight: 600; color: #e5e7eb; margin-top: 4px;">
                    Bull market – Risk-on bias
                </div>
                <ul style="font-size: 12px; color: #9ca3af; margin-top: 6px; padding-left: 18px;">
                    <li>Volatility moderate; breadth improving.</li>
                    <li>AI/tech leadership continues but concentration risk is high.</li>
                    <li>Rates expectations supportive but sensitive to macro surprises.</li>
                </ul>
                <div style="font-size: 11px; color: #6b7280; margin-top: 4px;">
                    Based on demo regime detector & risk models. Connect your real pipeline later.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="qf-card">
                <div style="font-size: 13px; color: #9ca3af;">Risk dashboard (demo)</div>
                <div style="font-size: 12px; color: #e5e7eb; margin-top: 4px;">
                    Fear/Greed: <b>63 / 100</b> – moderate greed<br/>
                    Market volatility: <b>Medium</b><br/>
                    Tech bubble signal: <b>Elevated</b><br/>
                    Overall market VaR: <b>Moderate</b>
                </div>
                <div style="font-size: 11px; color: #9ca3af; margin-top: 6px;">
                    QuantumFlow summary: Markets are somewhat risk-on, but crowded in mega-cap tech.
                    We favor selective exposure and controlled position sizes.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")
    # Mini index charts
    c1, c2, c3 = st.columns(3)
    for col, name in zip([c1, c2, c3], ["S&P 500", "Nasdaq 100", "BTC-USD"]):
        with col:
            df_idx = get_demo_index_series(name)
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df_idx["date"],
                    y=df_idx["value"],
                    mode="lines",
                    name=name,
                )
            )
            fig.update_layout(
                title=dict(
                    text=name,
                    font=dict(size=11, color="#e5e7eb"),
                    x=0.5,
                    xanchor="center",
                ),
                margin=dict(l=0, r=0, t=20, b=20),
                height=180,
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15,23,42,1)",
                font=dict(color="#e5e7eb"),
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=True, gridcolor="rgba(55,65,81,0.5)")
            st.plotly_chart(fig, use_container_width=True)


def render_markets():
    render_market_regime_overview()
    st.markdown("")

    st.markdown(
        '<div class="qf-section-title">Focus assets</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="qf-section-subtitle">'
        "Curated set of major names (demo universe). Click any row to see full QuantumFlow analysis."
        "</div>",
        unsafe_allow_html=True,
    )

    risk = st.session_state["risk_profile"]
    horizon = st.session_state["time_horizon"]

    focus = ["NVDA", "AAPL", "MSFT", "GOOGL", "META", "AMZN", "TSLA", "BTC-USD", "ETH-USD"]
    data = []
    for t in focus:
        price = np.random.uniform(80, 600)
        daily_pct = np.random.normal(0, 3)
        vol_level = np.random.choice(["Low", "Medium", "High"], p=[0.3, 0.4, 0.3])
        d = get_demo_decision(t, risk, horizon)
        data.append(
            {
                "ticker": t,
                "price": price,
                "daily_pct": daily_pct,
                "volatility": vol_level,
                "action": d["action"],
                "score": d["composite"],
            }
        )

    df = pd.DataFrame(data).sort_values("score", ascending=False)

    for _, row in df.iterrows():
        t = row["ticker"]
        price = row["price"]
        daily_pct = row["daily_pct"]
        vol = row["volatility"]
        action = row["action"]
        score = row["score"]
        color = "#4ade80" if daily_pct >= 0 else "#f97373"
        arrow = "▲" if daily_pct >= 0 else "▼"
        sentiment_class = (
            "qf-pill-positive"
            if action == "BUY"
            else "qf-pill-negative"
            if action in ["SELL", "AVOID"]
            else "qf-pill-neutral"
        )

        st.markdown(
            f"""
            <div class="qf-card" style="margin-bottom: 0.6rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 13px; font-weight: 600; color: #e5e7eb;">{t}</div>
                        <div style="font-size: 11px; color: #9ca3af;">
                            Volatility: {vol} · Model score: {score:+.2f}
                        </div>
                    </div>
                    <span class="qf-pill {sentiment_class}" style="font-size: 12px; font-weight: 600;">
                        {action}
                    </span>
                </div>
                <div style="margin-top: 4px; display: flex; justify-content: space-between; align-items: baseline;">
                    <div>
                        <div style="font-size: 18px; font-weight: 600; color: #e5e7eb;">${price:,.2f}</div>
                        <div style="font-size: 11px; color: {color}; margin-top: 2px;">
                            {arrow} {daily_pct:+.2f}%
                        </div>
                    </div>
                    <div style="font-size: 11px; color: #9ca3af;">
                        News pulse: demo-high<br/>
                        <span style="color: #9ca3af;">Click below for full details.</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View full analysis", key=f"market_{t}"):
            set_page("ASSET_DETAIL", ticker=t)
            rerun_app()


# -----------------------------------------------------------------------------
# NEWS – Articles + Social Signals
# -----------------------------------------------------------------------------

def render_news():
    st.markdown(
        '<div class="qf-section-title">Market news & QuantumFlow insights</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="qf-section-subtitle">'
        "Story-first view of what’s happening, who it affects, and how our model interprets it – across news and social."
        "</div>",
        unsafe_allow_html=True,
    )

    feed = get_demo_news_feed()
    social = get_demo_social_signals()

    left, right = st.columns([2, 1.4])

    with left:
        st.markdown(
            '<div class="qf-section-title" style="font-size: 14px;">News articles & QuantumFlow insight</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="qf-section-subtitle">'
            "Recent stories from major sources, plus our view on their impact."
            "</div>",
            unsafe_allow_html=True,
        )
        for i, item in enumerate(feed):
            ts = item["time"].strftime("%Y-%m-%d %H:%M")
            sentiment_class = (
                "qf-pill-positive"
                if item["sentiment"] == "Positive"
                else "qf-pill-negative"
                if item["sentiment"] == "Negative"
                else "qf-pill-neutral"
            )
            st.markdown(
                f"""
                <div class="qf-card" style="margin-bottom: 0.6rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-size: 12px; color: #9ca3af;">
                            {item['source']} · {ts} UTC
                        </div>
                        <span class="qf-pill {sentiment_class}">
                            Sentiment: {item['sentiment']}
                        </span>
                    </div>
                    <div style="font-size: 14px; font-weight: 600; color: #e5e7eb; margin-top: 4px;">
                        {item['headline']}
                    </div>
                    <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">
                        {item['summary']}
                    </div>
                    <div style="margin-top: 6px;">
                        {''.join(f'<span class="qf-ticker-pill">{t}</span>' for t in item['tickers'])}
                    </div>
                    <div style="font-size: 12px; color: #e5e7eb; margin-top: 6px;">
                        <span style="font-weight: 600;">QuantumFlow Insight:</span> {item['insight']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right:
        st.markdown(
            '<div class="qf-section-title" style="font-size: 14px;">Social signals (X / Reddit)</div>',
            unsafe_allow_html=True,
        )
        agg = social["aggregate"]
        st.markdown(
            f"""
            <div class="qf-card">
                <div style="font-size: 13px; color: #9ca3af;">Aggregated social sentiment (demo)</div>
                <div style="font-size: 15px; font-weight: 600; color: #e5e7eb; margin-top: 4px;">
                    {agg['label']} ({agg['score']:+.2f} on [-1, +1])
                </div>
                <div style="font-size: 12px; color: #9ca3af; margin-top: 4px;">
                    {agg['text']}
                </div>
                <div style="font-size: 11px; color: #9ca3af; margin-top: 6px;">
                    {agg['historical']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("")
        st.markdown(
            '<div class="qf-section-subtitle" style="margin-bottom: 0.3rem;">'
            "Recent demo posts and how similar clusters behaved in the past."
            "</div>",
            unsafe_allow_html=True,
        )

        for item in social["items"]:
            sentiment_class = (
                "qf-pill-positive"
                if item["sentiment"] == "Positive"
                else "qf-pill-negative"
                if item["sentiment"] == "Negative"
                else "qf-pill-neutral"
            )
            st.markdown(
                f"""
                <div class="qf-card" style="margin-bottom: 0.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-size: 12px; color: #9ca3af;">
                            {item['source']} · {item['handle']} · {item['time']}
                        </div>
                        <span class="qf-pill {sentiment_class}">
                            {item['sentiment']}
                        </span>
                    </div>
                    <div style="font-size: 12px; color: #e5e7eb; margin-top: 4px;">
                        <span class="qf-ticker-pill">{item['ticker']}</span> {item['text']}
                    </div>
                    <div style="font-size: 11px; color: #9ca3af; margin-top: 4px;">
                        Historical pattern: {item['pattern']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# -----------------------------------------------------------------------------
# Main App
# -----------------------------------------------------------------------------

def main():
    init_session_state()
    inject_global_styles()
    render_sidebar()
    render_top_header()
    render_main_nav()

    view = st.session_state["view"]

    if view == "HOME":
        render_home()
    elif view == "MARKETS":
        render_markets()
    elif view == "NEWS":
        render_news()
    elif view == "ASSET_DETAIL":
        render_asset_detail()
    else:
        render_home()


if __name__ == "__main__":
    main()

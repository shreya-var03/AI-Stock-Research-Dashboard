import pandas as pd
import streamlit as st

from src.charts import plot_price_chart
from src.data_loader import get_nifty_data, get_stock_data
from src.fundamentals import get_fundamental_data, score_fundamentals
from src.indicators import format_inr
from src.suggestions import generate_timeframe_suggestions
from src.technical_analysis import analyze_stock
from src.decision_engine import (
    generate_investment_memo,
    get_conflict_view,
    get_entry_quality,
    get_watchlist_triggers,
)
from src.backtesting import run_backtests

def filter_chart_data(data, range_label):
    ranges = {
        "1 Week": 5,
        "1 Month": 21,
        "2 Months": 42,
        "3 Months": 63,
        "6 Months": 126,
        "1 Year": 252,
        "5 Years": 252 * 5,
        "10 Years": 252 * 10,
    }

    if range_label == "Full Time Period":
        return data

    rows = ranges.get(range_label)

    if rows is None:
        return data

    return data.tail(min(rows, len(data)))

def show_single_stock_analysis(symbol, period, label):
    with st.spinner(f"Fetching {label} data and calculating indicators..."):
        data = get_stock_data(symbol, period)
        nifty_data = get_nifty_data(period)

    if data is None or len(data) < 220:
        st.error(f"Could not fetch enough {label} data for {symbol}.")
        return

    result = analyze_stock(data, nifty_data)

    with st.spinner("Fetching fundamental data..."):
        fundamental_data = get_fundamental_data(symbol)
        fundamental_score = score_fundamentals(fundamental_data)

    conflict_view = get_conflict_view(result, fundamental_score)
    entry_quality = get_entry_quality(result)
    watchlist_triggers = get_watchlist_triggers(result)
    investment_memo = generate_investment_memo(
        result,
        fundamental_score,
        conflict_view,
        entry_quality,
    )
        
    latest = data.iloc[-1]

    st.subheader(f"{label} Analysis")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Price", format_inr(latest["Close"]))
    col2.metric("50 DMA", format_inr(latest["DMA_50"]))
    col3.metric("200 DMA", format_inr(latest["DMA_200"]))
    col4.metric("RSI", f"{latest['RSI']:.2f}")

    signal_col1, signal_col2, signal_col3 = st.columns(3)
    signal_col1.metric("Signal", result["signal"])
    signal_col2.metric("Score", f"{result['score']}/{result['max_score']}")
    signal_col3.metric("Strength", f"{(result['score'] / result['max_score']) * 100:.0f}%")

    st.info(result["reason"])
    
    st.subheader("Technical + Fundamental Decision View")

    decision_col1, decision_col2, decision_col3 = st.columns(3)
    decision_col1.metric("Decision View", conflict_view["action_view"])
    decision_col2.metric("Technical Strength", f"{conflict_view['technical_strength']:.0f}%")
    decision_col3.metric("Fundamental Strength", f"{conflict_view['fundamental_strength']:.0f}%")

    st.success(conflict_view["verdict"])
    st.write(conflict_view["explanation"])
    
    st.subheader("Entry Quality Score")

    entry_col1, entry_col2, entry_col3 = st.columns(3)
    entry_col1.metric("Entry View", entry_quality["entry_label"])
    entry_col2.metric("Entry Score", f"{entry_quality['score']}/{entry_quality['max_score']}")
    entry_col3.metric("Entry Strength", f"{entry_quality['strength']:.0f}%")

    entry_details_df = pd.DataFrame(
        {
            "Entry Check": [
                "Distance from Support",
                "Distance from Resistance",
            ],
            "Value": [
                f"{entry_quality['distance_from_support']:.2f}%",
                f"{entry_quality['distance_from_resistance']:.2f}%",
            ],
        }
    )
    
    st.subheader("Watchlist Trigger Suggestions")

    watchlist_df = pd.DataFrame(watchlist_triggers)

    st.table(watchlist_df)
    
    st.subheader("Investment Memo")

    for title, memo_text in investment_memo.items():
        st.markdown(
            f"""
            <div class="reason-box">
                <strong>{title}</strong><br>
                {memo_text}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.table(entry_details_df)

    st.markdown("#### Entry Reasoning")

    for reason in entry_quality["reasons"]:
        st.markdown(
            f"""
            <div class="reason-box">
                {reason}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Timeframe-Based View")

    suggestions_df = pd.DataFrame(
        generate_timeframe_suggestions(result),
        columns=["Timeframe", "View", "Reason"],
    )

    st.table(suggestions_df)

    chart_type = st.radio(
        "Chart type",
        ["Line", "Candlestick"],
        horizontal=True,
        key=f"chart_type_{symbol}_{label}",
    )

    chart_range = st.radio(
        "Chart range",
        [
            "1 Week",
            "1 Month",
            "2 Months",
            "3 Months",
            "6 Months",
            "1 Year",
            "5 Years",
            "10 Years",
            "Full Time Period",
        ],
        horizontal=True,
        key=f"chart_range_{symbol}_{label}",
    )

    chart_data = filter_chart_data(data, chart_range)

    chart_config = {
        "scrollZoom": True,
        "displayModeBar": True,
        "doubleClick": "reset",
    }

    st.plotly_chart(
        plot_price_chart(
            chart_data,
            symbol,
            result["support"],
            result["resistance"],
            chart_type=chart_type,
        ),
        use_container_width=True,
        key=f"price_chart_{symbol}_{label}_{chart_type}_{chart_range}",
        config=chart_config,
    )

    st.subheader("Technical Analysis")

    analysis_df = pd.DataFrame(
        result["analysis"],
        columns=["Tier", "Status", "Explanation"],
    )

    st.table(analysis_df)

    st.subheader("Fundamental Analysis")

    fund_col1, fund_col2, fund_col3 = st.columns(3)
    fund_col1.metric("Fundamental Rating", fundamental_score["rating"])
    fund_col2.metric(
        "Fundamental Score",
        f"{fundamental_score['score']}/{fundamental_score['max_score']}",
    )
    fund_col3.metric(
        "Fundamental Strength",
        f"{(fundamental_score['score'] / fundamental_score['max_score']) * 100:.0f}%",
    )

    if fundamental_data is None:
        st.warning("Fundamental data could not be fetched for this stock.")
    else:
        fundamentals_df = pd.DataFrame(
            list(fundamental_data["display"].items()),
            columns=["Metric", "Value"],
        )

        st.dataframe(
            fundamentals_df,
            use_container_width=True,
            hide_index=True,
            height=600,
        )

    fundamental_analysis_df = pd.DataFrame(
        fundamental_score["analysis"],
        columns=["Metric", "Status", "Explanation"],
    )

    st.table(fundamental_analysis_df)
    
    st.subheader("Backtesting Results")

    backtest_results = run_backtests(data)

    if backtest_results.empty:
        st.warning("Not enough data to run backtests.")
    else:
        st.table(backtest_results)

    st.subheader("Support, Resistance & Returns")

    sr_col1, sr_col2, sr_col3, sr_col4 = st.columns(4)
    sr_col1.metric("Support", format_inr(result["support"]))
    sr_col2.metric("Resistance", format_inr(result["resistance"]))
    sr_col3.metric(f"Stock {label} Return", f"{result['stock_return']:.2f}%")
    sr_col4.metric(f"Stock {label} CAGR", f"{result['stock_cagr']:.2f}%")

    nifty_col1, nifty_col2 = st.columns(2)
    nifty_col1.metric(f"Nifty {label} Return", f"{result['nifty_return']:.2f}%")
    nifty_col2.metric(f"Nifty {label} CAGR", f"{result['nifty_cagr']:.2f}%")
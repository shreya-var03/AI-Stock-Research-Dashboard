import streamlit as st

from src.config import SCANNER_MODES
from src.data_loader import get_searchable_stock_list
from src.scanner import run_scanner
from src.theme import apply_custom_theme
from src.views import show_single_stock_analysis


st.set_page_config(
    page_title="AI Stock Research Dashboard",
    layout="wide",
)

theme = st.sidebar.selectbox(
    "Theme",
    ["Light", "Dark", "Beige"],
)

apply_custom_theme(theme)

st.title("AI-Assisted Stock Research & Backtesting Dashboard")
st.caption("Analyze trend, volume, support/resistance, relative strength, momentum, and trend structure.")

mode = st.sidebar.radio(
    "Choose mode",
    [
        "Single Stock Analysis",
        "Nifty 50 Scanner",
        "Nifty 100 Scanner",
        "Nifty 200 Scanner",
    ],
)

st.sidebar.markdown("---")

if mode == "Single Stock Analysis":
    stock_list = get_searchable_stock_list()

    selected_stock = st.selectbox(
        "Search and select stock",
        options=stock_list["Display"].tolist(),
        index=None,
        placeholder="Type a company name or symbol...",
    )

    if selected_stock:
        symbol = stock_list.loc[
            stock_list["Display"] == selected_stock,
            "Symbol",
        ].iloc[0]
    else:
        symbol = None

    if "analyzed_symbol" not in st.session_state:
        st.session_state.analyzed_symbol = None

    if st.button("Analyze Stock", type="primary"):
        if symbol is None:
            st.warning("Please select a stock first.")
            st.stop()

        st.session_state.analyzed_symbol = symbol

    if st.session_state.analyzed_symbol is not None:
        analysis_period = st.radio(
            "Analysis period",
            ["5Y", "10Y"],
            horizontal=True,
            key="single_stock_analysis_period",
        )

        period = "5y" if analysis_period == "5Y" else "10y"

        show_single_stock_analysis(
            st.session_state.analyzed_symbol,
            period,
            analysis_period,
        )

        st.warning("This dashboard is for research and education only. It is not financial advice.")
        
if mode in SCANNER_MODES:
    period_choice = st.sidebar.radio(
        "Scanner period",
        ["5Y", "10Y"],
    )

    period = "5y" if period_choice == "5Y" else "10y"

    run_scanner(mode, period, period_choice)

    st.warning("This scanner is for research and education only. It is not financial advice.")
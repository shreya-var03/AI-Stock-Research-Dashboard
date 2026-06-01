import pandas as pd
import streamlit as st
import yfinance as yf

from src.config import INDEX_SOURCES, SCANNER_MODES
from src.indicators import add_indicators


@st.cache_data(ttl=3600)
def get_stock_data(symbol, period):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval="1d")
    except Exception:
        return None

    if data is None or data.empty:
        return None

    data = data.dropna()

    if data.empty:
        return None

    return add_indicators(data)


@st.cache_data(ttl=3600)
def get_nifty_data(period):
    try:
        nifty = yf.Ticker("^NSEI")
        data = nifty.history(period=period, interval="1d")
    except Exception:
        return None

    if data is None or data.empty:
        return None

    return data.dropna()


@st.cache_data(ttl=86400)
def load_index_stocks(mode):
    source = INDEX_SOURCES[mode]

    try:
        stocks = pd.read_csv(source["url"])
    except Exception:
        try:
            stocks = pd.read_csv(source["local"])
        except FileNotFoundError:
            return None

    if "Company Name" in stocks.columns:
        company_col = "Company Name"
    elif "Company" in stocks.columns:
        company_col = "Company"
    else:
        company_col = stocks.columns[0]

    symbol_col = "Symbol" if "Symbol" in stocks.columns else stocks.columns[1]

    clean = stocks[[company_col, symbol_col]].copy()
    clean.columns = ["Company", "Symbol"]

    clean["Company"] = clean["Company"].astype(str).str.strip()
    clean["Symbol"] = clean["Symbol"].astype(str).str.strip()

    clean["Symbol"] = clean["Symbol"].apply(
        lambda symbol: symbol if symbol.endswith(".NS") else f"{symbol}.NS"
    )

    return clean


def get_searchable_stock_list():
    lists = []

    for mode_name in SCANNER_MODES:
        stocks = load_index_stocks(mode_name)

        if stocks is not None:
            lists.append(stocks)

    if len(lists) == 0:
        return pd.DataFrame(
            [{"Company": "Reliance Industries Ltd.", "Symbol": "RELIANCE.NS"}]
        )

    combined = pd.concat(lists, ignore_index=True)
    combined = combined.drop_duplicates(subset=["Symbol"])
    combined = combined.sort_values(by="Company")
    combined["Display"] = combined["Company"] + " (" + combined["Symbol"] + ")"

    return combined
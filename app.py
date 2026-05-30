import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(
    page_title="AI Stock Research Dashboard",
    layout="wide"
)

st.title("AI-Assisted Stock Research & Backtesting Dashboard")
st.caption("Analyze trend, volume, support/resistance, relative strength, momentum, and trend structure.")

st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        line-height: 1.2;
        white-space: normal;
        overflow-wrap: break-word;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 14px;
    }

    div[data-testid="stMetric"] {
        min-height: 90px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

INDEX_SOURCES = {
    "Nifty 50 Scanner": {
        "name": "Nifty 50",
        "url": "https://archives.nseindia.com/content/indices/ind_nifty50list.csv",
        "local": "nifty50.csv",
    },
    "Nifty 100 Scanner": {
        "name": "Nifty 100",
        "url": "https://archives.nseindia.com/content/indices/ind_nifty100list.csv",
        "local": "nifty100.csv",
    },
    "Nifty 200 Scanner": {
        "name": "Nifty 200",
        "url": "https://archives.nseindia.com/content/indices/ind_nifty200list.csv",
        "local": "nifty200.csv",
    },
}

def apply_custom_theme(theme):
    themes = {
        "Light": {
            "bg": "#f7f9fc",
            "surface": "#ffffff",
            "sidebar": "#eaf1fb",
            "input": "#ffffff",
            "text": "#1f2937",
            "muted": "#64748b",
            "border": "#d7e0ea",
            "primary": "#60a5fa",
            "accent": "#dbeafe",
            "shadow": "0 10px 30px rgba(15, 23, 42, 0.08)",
        },
        "Dark": {
            "bg": "#0b1120",
            "surface": "#151f32",
            "sidebar": "#111827",
            "input": "#1f2937",
            "text": "#f8fafc",
            "muted": "#cbd5e1",
            "border": "#334155",
            "primary": "#22c55e",
            "accent": "#123524",
            "shadow": "0 10px 30px rgba(0, 0, 0, 0.35)",
        },
        "Beige": {
            "bg": "#f6efe3",
            "surface": "#fff8ec",
            "sidebar": "#efe2ce",
            "input": "#fffaf0",
            "text": "#2f2a24",
            "muted": "#6f6257",
            "border": "#d8c3a5",
            "primary": "#b7791f",
            "accent": "#f3dfbd",
            "shadow": "0 10px 30px rgba(85, 60, 35, 0.10)",
        },
    }

    selected = themes[theme]

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background:
                radial-gradient(circle at top left, {selected["accent"]} 0, transparent 280px),
                {selected["bg"]};
            color: {selected["text"]};
        }}

        .block-container {{
            padding-top: 4rem;
            padding-bottom: 3rem;
        }}

        h1 {{
            font-size: 42px;
            font-weight: 800;
            color: {selected["text"]};
            letter-spacing: 0;
        }}

        h2, h3 {{
            color: {selected["text"]};
            font-weight: 700;
            letter-spacing: 0;
        }}

        p, label, span, div {{
            color: {selected["text"]};
        }}

        section[data-testid="stSidebar"] {{
            background:
                linear-gradient(180deg, {selected["sidebar"]}, {selected["surface"]});
            border-right: 1px solid {selected["border"]};
        }}

        section[data-testid="stSidebar"] > div {{
            background: transparent;
        }}

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] div {{
            color: {selected["text"]};
        }}

        div[data-testid="stMetric"] {{
            background-color: {selected["surface"]};
            border: 1px solid {selected["border"]};
            border-radius: 8px;
            padding: 16px 18px;
            box-shadow: {selected["shadow"]};
        }}

        div[data-testid="stMetricLabel"] {{
            color: {selected["muted"]};
            font-size: 13px;
            font-weight: 600;
        }}

        div[data-testid="stMetricValue"] {{
            color: {selected["text"]};
            font-size: 27px;
            line-height: 1.2;
            white-space: normal;
            overflow-wrap: break-word;
            font-weight: 700;
        }}

        div[data-testid="stSelectbox"] div,
        div[data-testid="stSelectbox"] input,
        div[data-baseweb="select"] > div {{
            background-color: {selected["input"]};
            color: {selected["text"]};
            border-color: {selected["border"]};
            border-radius: 8px;
        }}

        div[data-baseweb="popover"] div {{
            background-color: {selected["input"]};
            color: {selected["text"]};
        }}

        div[role="option"] {{
            background-color: {selected["input"]};
            color: {selected["text"]};
        }}

        div[role="option"]:hover {{
            background-color: {selected["accent"]};
        }}

        div[data-testid="stRadio"] label,
        div[data-testid="stRadio"] span,
        div[data-testid="stRadio"] div {{
            color: {selected["text"]};
        }}

        div[data-testid="stRadio"] svg {{
            fill: {selected["primary"]};
        }}

        .stButton > button {{
            background-color: {selected["primary"]};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.55rem 1.1rem;
            font-weight: 700;
            box-shadow: {selected["shadow"]};
        }}

        .stButton > button:hover {{
            background-color: {selected["primary"]};
            color: white;
            border: none;
            opacity: 0.9;
        }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid {selected["border"]};
            border-radius: 8px;
            overflow: hidden;
            box-shadow: {selected["shadow"]};
        }}

        .stAlert {{
            border-radius: 8px;
        }}

        hr {{
            border-color: {selected["border"]};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def format_inr(value):
    if pd.isna(value):
        return "N/A"
    return f"Rs. {value:,.2f}"


def add_indicators(data):
    data = data.copy()

    data["DMA_20"] = data["Close"].rolling(window=20).mean()
    data["DMA_50"] = data["Close"].rolling(window=50).mean()
    data["DMA_200"] = data["Close"].rolling(window=200).mean()
    data["Avg_Volume_20"] = data["Volume"].rolling(window=20).mean()

    delta = data["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    data["RSI"] = 100 - (100 / (1 + rs))

    return data


@st.cache_data(ttl=3600)
def get_stock_data(symbol, period):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period, interval="1d")

    if data.empty:
        return None

    data = data.dropna()
    data = add_indicators(data)
    return data


@st.cache_data(ttl=3600)
def get_nifty_data(period):
    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period=period, interval="1d")

    if data.empty:
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

    if "Symbol" in stocks.columns:
        symbol_col = "Symbol"
    else:
        symbol_col = stocks.columns[1]

    clean = stocks[[company_col, symbol_col]].copy()
    clean.columns = ["Company", "Symbol"]

    clean["Symbol"] = clean["Symbol"].astype(str).str.strip()
    clean["Company"] = clean["Company"].astype(str).str.strip()

    clean["Symbol"] = clean["Symbol"].apply(
        lambda symbol: symbol if symbol.endswith(".NS") else f"{symbol}.NS"
    )

    return clean


def calculate_support_resistance(data, window=90):
    recent = data.tail(window)
    support = recent["Low"].min()
    resistance = recent["High"].max()
    return support, resistance


def calculate_trend_structure(data, lookback=60):
    recent = data.tail(lookback)

    if len(recent) < lookback:
        return "Mixed", "Not enough recent data to judge trend structure."

    first_half = recent.iloc[:lookback // 2]
    second_half = recent.iloc[lookback // 2:]

    old_high = first_half["High"].max()
    old_low = first_half["Low"].min()

    new_high = second_half["High"].max()
    new_low = second_half["Low"].min()

    if new_high > old_high and new_low > old_low:
        return "Bullish", "Higher highs and higher lows."
    elif new_high < old_high and new_low < old_low:
        return "Bearish", "Lower highs and lower lows."
    else:
        return "Mixed", "Trend structure is not clearly bullish or bearish."


def get_final_signal(score, max_score):
    percentage = (score / max_score) * 100

    if percentage >= 75:
        return "Bullish", "The stock passes most major technical filters."
    elif percentage >= 50:
        return "Neutral / Watchlist", "The stock has some strength, but confirmation is still needed."
    else:
        return "Bearish / Avoid for now", "The stock fails several important technical filters."


def analyze_stock(data, nifty_data):
    latest = data.iloc[-1]
    previous = data.iloc[-2]

    score = 0
    max_score = 7
    analysis = []

    current_price = latest["Close"]
    dma_50 = latest["DMA_50"]
    dma_200 = latest["DMA_200"]

    if current_price > dma_200:
        score += 1
        analysis.append(("Trend: Price vs 200 DMA", "Bullish", "Price is above the 200 DMA, showing long-term strength."))
    else:
        analysis.append(("Trend: Price vs 200 DMA", "Bearish", "Price is below the 200 DMA, showing long-term weakness."))

    if dma_50 > dma_200:
        score += 1
        analysis.append(("Trend: 50 DMA vs 200 DMA", "Bullish", "50 DMA is above 200 DMA."))
    else:
        analysis.append(("Trend: 50 DMA vs 200 DMA", "Bearish", "50 DMA is below 200 DMA."))

    volume_ratio = latest["Volume"] / latest["Avg_Volume_20"]

    if latest["Close"] > previous["Close"] and volume_ratio >= 1.5:
        score += 1
        analysis.append(("Volume", "Bullish", f"Price moved up with volume at {volume_ratio:.2f}x the 20-day average."))
    elif volume_ratio >= 1.5:
        analysis.append(("Volume", "Mixed", f"Volume is high at {volume_ratio:.2f}x average, but price did not close strongly."))
    else:
        analysis.append(("Volume", "Weak", f"Volume is only {volume_ratio:.2f}x the 20-day average."))

    support, resistance = calculate_support_resistance(data)

    if current_price > resistance * 0.98:
        score += 1
        analysis.append(("Support & Resistance", "Bullish", "Price is close to or breaking recent resistance."))
    elif current_price < support * 1.05:
        analysis.append(("Support & Resistance", "Watch", "Price is close to support. A breakdown would be negative."))
    else:
        analysis.append(("Support & Resistance", "Neutral", "Price is between recent support and resistance."))

    stock_return = ((data["Close"].iloc[-1] / data["Close"].iloc[0]) - 1) * 100

    if nifty_data is not None:
        nifty_return = ((nifty_data["Close"].iloc[-1] / nifty_data["Close"].iloc[0]) - 1) * 100
    else:
        nifty_return = 0

    if stock_return > nifty_return:
        score += 1
        analysis.append(("Relative Strength", "Bullish", f"Stock return is {stock_return:.2f}% vs Nifty return of {nifty_return:.2f}%."))
    else:
        analysis.append(("Relative Strength", "Weak", f"Stock return is {stock_return:.2f}% vs Nifty return of {nifty_return:.2f}%."))

    rsi = latest["RSI"]

    if rsi >= 60:
        score += 1
        analysis.append(("Momentum", "Bullish", f"RSI is {rsi:.2f}, showing strong momentum."))
    elif rsi >= 45:
        analysis.append(("Momentum", "Neutral", f"RSI is {rsi:.2f}, showing average momentum."))
    else:
        analysis.append(("Momentum", "Weak", f"RSI is {rsi:.2f}, showing weak momentum."))

    structure, structure_reason = calculate_trend_structure(data)

    if structure == "Bullish":
        score += 1
        analysis.append(("Trend Structure", "Bullish", structure_reason))
    elif structure == "Bearish":
        analysis.append(("Trend Structure", "Bearish", structure_reason))
    else:
        analysis.append(("Trend Structure", "Mixed", structure_reason))

    final_signal, final_reason = get_final_signal(score, max_score)

    return {
        "score": score,
        "max_score": max_score,
        "signal": final_signal,
        "reason": final_reason,
        "analysis": analysis,
        "support": support,
        "resistance": resistance,
        "stock_return": stock_return,
        "nifty_return": nifty_return,
        "volume_ratio": volume_ratio,
        "rsi": rsi,
        "current_price": current_price,
        "dma_50": dma_50,
        "dma_200": dma_200,
    }


def plot_price_chart(data, symbol, support=None, resistance=None):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Price"
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["DMA_50"],
        mode="lines",
        name="50 DMA"
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["DMA_200"],
        mode="lines",
        name="200 DMA"
    ))

    if support is not None:
        fig.add_hline(
            y=support,
            line_dash="dash",
            line_color="green",
            annotation_text="Support"
        )

    if resistance is not None:
        fig.add_hline(
            y=resistance,
            line_dash="dash",
            line_color="red",
            annotation_text="Resistance"
        )

    fig.update_layout(
        title=f"{symbol} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        height=600,
        xaxis_rangeslider_visible=False
    )

    return fig
def generate_timeframe_suggestions(result):
    score = result["score"]
    max_score = result["max_score"]
    strength = (score / max_score) * 100

    current_price = result["current_price"]
    dma_50 = result["dma_50"]
    dma_200 = result["dma_200"]
    rsi = result["rsi"]
    volume_ratio = result["volume_ratio"]

    suggestions = []

    if current_price > dma_50 and rsi >= 55 and volume_ratio >= 1.2:
        one_month = "Positive"
        one_month_reason = "Short-term setup looks strong because price is above 50 DMA, RSI supports momentum, and volume is healthy."
    elif current_price < dma_50 or rsi < 45:
        one_month = "Avoid / Wait"
        one_month_reason = "Short-term setup is weak because price is below 50 DMA or RSI momentum is soft."
    else:
        one_month = "Watchlist"
        one_month_reason = "Short-term setup is mixed. Wait for price strength or stronger volume confirmation."

    suggestions.append(("1 Month", one_month, one_month_reason))

    if current_price > dma_50 and current_price > dma_200 and rsi >= 50:
        three_month = "Positive"
        three_month_reason = "Medium-term setup is constructive because price is above both key moving averages and RSI is not weak."
    elif current_price < dma_200:
        three_month = "Avoid / Wait"
        three_month_reason = "Medium-term setup is weak because price is below the 200 DMA."
    else:
        three_month = "Watchlist"
        three_month_reason = "Medium-term view is not clear yet. A move above key moving averages would improve the setup."

    suggestions.append(("3 Months", three_month, three_month_reason))

    if strength >= 65 and current_price > dma_200:
        six_month = "Positive"
        six_month_reason = "Six-month setup looks favorable because the stock passes most filters and remains above the 200 DMA."
    elif strength < 45 or current_price < dma_200:
        six_month = "Avoid / Wait"
        six_month_reason = "Six-month setup is weak because the stock fails several filters or trades below the 200 DMA."
    else:
        six_month = "Watchlist"
        six_month_reason = "Six-month setup is balanced. More confirmation is needed before calling it strong."

    suggestions.append(("6 Months", six_month, six_month_reason))

    if strength >= 70 and result["stock_return"] > result["nifty_return"] and current_price > dma_200:
        one_year = "Positive"
        one_year_reason = "Long-term setup looks strong because the stock is outperforming Nifty and remains in a long-term uptrend."
    elif result["stock_return"] < result["nifty_return"] or current_price < dma_200:
        one_year = "Avoid / Wait"
        one_year_reason = "Long-term setup is weak because the stock is underperforming Nifty or trading below the 200 DMA."
    else:
        one_year = "Watchlist"
        one_year_reason = "Long-term setup is mixed. It may need better relative strength or trend confirmation."

    suggestions.append(("1 Year", one_year, one_year_reason))

    return suggestions

def show_single_stock_analysis(symbol, period, label):
    with st.spinner(f"Fetching {label} data and calculating indicators..."):
        data = get_stock_data(symbol, period)
        nifty_data = get_nifty_data(period)

    if data is None or len(data) < 220:
        st.error(f"Could not fetch enough {label} data for {symbol}.")
        return

    result = analyze_stock(data, nifty_data)
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
    
    st.subheader("Timeframe-Based View")

    suggestions = generate_timeframe_suggestions(result)

    suggestions_df = pd.DataFrame(
        suggestions,
        columns=["Timeframe", "View", "Reason"]
    )

    st.dataframe(
        suggestions_df,
        use_container_width=True,
        hide_index=True
    )

    st.plotly_chart(
        plot_price_chart(data, symbol, result["support"], result["resistance"]),
        use_container_width=True,
        key=f"price_chart_{symbol}_{label}"
    )

    analysis_df = pd.DataFrame(
        result["analysis"],
        columns=["Tier", "Status", "Explanation"]
    )

    st.dataframe(
        analysis_df,
        use_container_width=True,
        hide_index=True
    )

    sr_col1, sr_col2, sr_col3, sr_col4 = st.columns(4)
    sr_col1.metric("Support", format_inr(result["support"]))
    sr_col2.metric("Resistance", format_inr(result["resistance"]))
    sr_col3.metric(f"Stock {label} Return", f"{result['stock_return']:.2f}%")
    sr_col4.metric(f"Nifty {label} Return", f"{result['nifty_return']:.2f}%")


def run_scanner(mode, period, label):
    index_name = INDEX_SOURCES[mode]["name"]

    st.subheader(f"{index_name} Technical Scanner")
    st.write(f"Scan {index_name} stocks using {label} data.")

    stocks = load_index_stocks(mode)

    if stocks is None:
        st.error(f"Could not load {index_name} list. Check internet connection or add a local CSV file.")
        return

    st.dataframe(stocks, use_container_width=True, hide_index=True)

    if st.button(f"Run {index_name} Scan", type="primary"):
        nifty_data = get_nifty_data(period)
        results = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        for index, row in stocks.iterrows():
            company = row["Company"]
            symbol = row["Symbol"]

            status_text.write(f"Scanning {company} ({symbol})...")

            data = get_stock_data(symbol, period)

            if data is not None and len(data) > 220:
                result = analyze_stock(data, nifty_data)

                results.append({
                    "Company": company,
                    "Symbol": symbol,
                    "Signal": result["signal"],
                    "Score": result["score"],
                    "Max Score": result["max_score"],
                    "Strength %": round((result["score"] / result["max_score"]) * 100, 2),
                    "Current Price": round(result["current_price"], 2),
                    "50 DMA": round(result["dma_50"], 2),
                    "200 DMA": round(result["dma_200"], 2),
                    "RSI": round(result["rsi"], 2),
                    "Volume vs 20D Avg": round(result["volume_ratio"], 2),
                    f"{label} Return %": round(result["stock_return"], 2),
                    f"Nifty {label} Return %": round(result["nifty_return"], 2),
                })

            progress_bar.progress((index + 1) / len(stocks))

        status_text.write("Scan completed.")

        if len(results) == 0:
            st.error("No scanner results were generated.")
            return

        scanner_df = pd.DataFrame(results)
        scanner_df = scanner_df.sort_values(
            by=["Score", "Strength %", f"{label} Return %"],
            ascending=False
        )

        st.subheader("Ranked Scanner Results")
        st.dataframe(scanner_df, use_container_width=True, hide_index=True)

        st.subheader("Top 10 Strongest Stocks")
        st.dataframe(scanner_df.head(10), use_container_width=True, hide_index=True)

        st.download_button(
            label="Download Scanner Results CSV",
            data=scanner_df.to_csv(index=False),
            file_name=f"{index_name.lower().replace(' ', '_')}_{label.lower().replace(' ', '_')}_scanner.csv",
            mime="text/csv"
        )

def get_searchable_stock_list():
    lists = []

    for mode_name in ["Nifty 50 Scanner", "Nifty 100 Scanner", "Nifty 200 Scanner"]:
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

theme = st.sidebar.selectbox(
    "Theme",
    ["Light", "Dark", "Beige"]
)

apply_custom_theme(theme)

mode = st.sidebar.radio(
    "Choose mode",
    [
        "Single Stock Analysis",
        "Nifty 50 Scanner",
        "Nifty 100 Scanner",
        "Nifty 200 Scanner",
    ]
)

st.sidebar.markdown("---")

if mode == "Single Stock Analysis":
        stock_list = get_searchable_stock_list()

selected_stock = st.selectbox(
        "Search and select stock",
        options=stock_list["Display"].tolist(),
        index=None,
        placeholder="Type a company name or symbol..."
    )

if selected_stock:
        symbol = stock_list.loc[
            stock_list["Display"] == selected_stock,
            "Symbol"
        ].iloc[0]
else:
        symbol = None

if st.button("Analyze Stock", type="primary"):
        if symbol is None:
            st.warning("Please select a stock first.")
            st.stop()
            
        tab_5y, tab_10y = st.tabs(["Last 5 Years", "Last 10 Years"])

        with tab_5y:
            show_single_stock_analysis(symbol, "5y", "5Y")

        with tab_10y:
            show_single_stock_analysis(symbol, "10y", "10Y")

        st.warning("This dashboard is for research and education only. It is not financial advice.")

if mode in ["Nifty 50 Scanner", "Nifty 100 Scanner", "Nifty 200 Scanner"]:
    period_choice = st.sidebar.radio(
        "Scanner period",
        ["5Y", "10Y"]
    )

    period = "5y" if period_choice == "5Y" else "10y"

    run_scanner(mode, period, period_choice)

    st.warning("This scanner is for research and education only. It is not financial advice.")
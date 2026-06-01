import pandas as pd


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


def calculate_cagr(data):
    start_price = data["Close"].iloc[0]
    end_price = data["Close"].iloc[-1]

    days = (data.index[-1] - data.index[0]).days
    years = days / 365.25

    if start_price <= 0 or years <= 0:
        return 0

    return ((end_price / start_price) ** (1 / years) - 1) * 100
from src.indicators import calculate_cagr


def calculate_support_resistance(data, window=90):
    recent = data.tail(window)
    return recent["Low"].min(), recent["High"].max()


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
    if new_high < old_high and new_low < old_low:
        return "Bearish", "Lower highs and lower lows."

    return "Mixed", "Trend structure is not clearly bullish or bearish."


def get_final_signal(score, max_score):
    percentage = (score / max_score) * 100

    if percentage >= 75:
        return "Bullish", "The stock passes most major technical filters."
    if percentage >= 50:
        return "Neutral / Watchlist", "The stock has some strength, but confirmation is still needed."

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
    stock_cagr = calculate_cagr(data)

    if nifty_data is not None:
        nifty_return = ((nifty_data["Close"].iloc[-1] / nifty_data["Close"].iloc[0]) - 1) * 100
        nifty_cagr = calculate_cagr(nifty_data)
    else:
        nifty_return = 0
        nifty_cagr = 0

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

    analysis.append(("Trend Structure", structure, structure_reason))

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
        "stock_cagr": stock_cagr,
        "nifty_cagr": nifty_cagr,
        "volume_ratio": volume_ratio,
        "rsi": rsi,
        "current_price": current_price,
        "dma_50": dma_50,
        "dma_200": dma_200,
    }
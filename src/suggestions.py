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
        suggestions.append(("1 Month", "Positive", "Short-term setup looks strong because price is above 50 DMA, RSI supports momentum, and volume is healthy."))
    elif current_price < dma_50 or rsi < 45:
        suggestions.append(("1 Month", "Avoid / Wait", "Short-term setup is weak because price is below 50 DMA or RSI momentum is soft."))
    else:
        suggestions.append(("1 Month", "Watchlist", "Short-term setup is mixed. Wait for price strength or stronger volume confirmation."))

    if current_price > dma_50 and current_price > dma_200 and rsi >= 50:
        suggestions.append(("3 Months", "Positive", "Medium-term setup is constructive because price is above both key moving averages and RSI is not weak."))
    elif current_price < dma_200:
        suggestions.append(("3 Months", "Avoid / Wait", "Medium-term setup is weak because price is below the 200 DMA."))
    else:
        suggestions.append(("3 Months", "Watchlist", "Medium-term view is not clear yet. A move above key moving averages would improve the setup."))

    if strength >= 65 and current_price > dma_200:
        suggestions.append(("6 Months", "Positive", "Six-month setup looks favorable because the stock passes most filters and remains above the 200 DMA."))
    elif strength < 45 or current_price < dma_200:
        suggestions.append(("6 Months", "Avoid / Wait", "Six-month setup is weak because the stock fails several filters or trades below the 200 DMA."))
    else:
        suggestions.append(("6 Months", "Watchlist", "Six-month setup is balanced. More confirmation is needed before calling it strong."))

    if strength >= 70 and result["stock_return"] > result["nifty_return"] and current_price > dma_200:
        suggestions.append(("1 Year", "Positive", "Long-term setup looks strong because the stock is outperforming Nifty and remains in a long-term uptrend."))
    elif result["stock_return"] < result["nifty_return"] or current_price < dma_200:
        suggestions.append(("1 Year", "Avoid / Wait", "Long-term setup is weak because the stock is underperforming Nifty or trading below the 200 DMA."))
    else:
        suggestions.append(("1 Year", "Watchlist", "Long-term setup is mixed. It may need better relative strength or trend confirmation."))

    return suggestions
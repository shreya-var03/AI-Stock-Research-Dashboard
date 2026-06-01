import pandas as pd


def calculate_max_drawdown(equity_curve):
    running_max = equity_curve.cummax()
    drawdown = ((equity_curve - running_max) / running_max) * 100
    return drawdown.min()


def buy_and_hold_backtest(data):
    start_price = data["Close"].iloc[0]
    end_price = data["Close"].iloc[-1]

    total_return = ((end_price / start_price) - 1) * 100

    equity_curve = data["Close"] / start_price
    max_drawdown = calculate_max_drawdown(equity_curve)

    return {
        "Strategy": "Buy and Hold",
        "Total Return %": total_return,
        "Max Drawdown %": max_drawdown,
        "Trades": 1,
        "Win Rate %": None,
    }


def moving_average_crossover_backtest(data):
    data = data.copy()

    data["Signal"] = 0
    data.loc[data["DMA_50"] > data["DMA_200"], "Signal"] = 1

    data["Daily Return"] = data["Close"].pct_change()
    data["Strategy Return"] = data["Daily Return"] * data["Signal"].shift(1)

    equity_curve = (1 + data["Strategy Return"].fillna(0)).cumprod()

    total_return = (equity_curve.iloc[-1] - 1) * 100
    max_drawdown = calculate_max_drawdown(equity_curve)

    trades = (data["Signal"].diff() == 1).sum()

    trade_returns = []
    in_trade = False
    entry_price = None

    for _, row in data.iterrows():
        if row["Signal"] == 1 and not in_trade:
            in_trade = True
            entry_price = row["Close"]

        elif row["Signal"] == 0 and in_trade:
            exit_price = row["Close"]
            trade_returns.append((exit_price / entry_price - 1) * 100)
            in_trade = False

    if in_trade and entry_price is not None:
        exit_price = data["Close"].iloc[-1]
        trade_returns.append((exit_price / entry_price - 1) * 100)

    if len(trade_returns) > 0:
        win_rate = (sum(1 for trade in trade_returns if trade > 0) / len(trade_returns)) * 100
    else:
        win_rate = None

    return {
        "Strategy": "50/200 DMA Crossover",
        "Total Return %": total_return,
        "Max Drawdown %": max_drawdown,
        "Trades": int(trades),
        "Win Rate %": win_rate,
    }


def rsi_momentum_backtest(data):
    data = data.copy()

    data["Signal"] = 0
    data.loc[(data["RSI"] > 55) & (data["Close"] > data["DMA_200"]), "Signal"] = 1

    data["Daily Return"] = data["Close"].pct_change()
    data["Strategy Return"] = data["Daily Return"] * data["Signal"].shift(1)

    equity_curve = (1 + data["Strategy Return"].fillna(0)).cumprod()

    total_return = (equity_curve.iloc[-1] - 1) * 100
    max_drawdown = calculate_max_drawdown(equity_curve)

    trades = (data["Signal"].diff() == 1).sum()

    return {
        "Strategy": "RSI Momentum",
        "Total Return %": total_return,
        "Max Drawdown %": max_drawdown,
        "Trades": int(trades),
        "Win Rate %": None,
    }


def volume_breakout_backtest(data):
    data = data.copy()

    data["Resistance_60"] = data["High"].rolling(window=60).max().shift(1)

    data["Signal"] = 0
    data.loc[
        (data["Close"] > data["Resistance_60"])
        & (data["Volume"] > data["Avg_Volume_20"] * 1.5)
        & (data["Close"] > data["DMA_200"]),
        "Signal",
    ] = 1

    data["Signal"] = data["Signal"].replace(0, pd.NA).ffill(limit=20).fillna(0)

    data["Daily Return"] = data["Close"].pct_change()
    data["Strategy Return"] = data["Daily Return"] * data["Signal"].shift(1)

    equity_curve = (1 + data["Strategy Return"].fillna(0)).cumprod()

    total_return = (equity_curve.iloc[-1] - 1) * 100
    max_drawdown = calculate_max_drawdown(equity_curve)

    trades = (data["Signal"].diff() == 1).sum()

    return {
        "Strategy": "Volume Breakout",
        "Total Return %": total_return,
        "Max Drawdown %": max_drawdown,
        "Trades": int(trades),
        "Win Rate %": None,
    }


def run_backtests(data):
    clean_data = data.dropna().copy()

    if len(clean_data) < 220:
        return pd.DataFrame()

    results = [
        buy_and_hold_backtest(clean_data),
        moving_average_crossover_backtest(clean_data),
        rsi_momentum_backtest(clean_data),
        volume_breakout_backtest(clean_data),
    ]

    results_df = pd.DataFrame(results)

    numeric_columns = ["Total Return %", "Max Drawdown %", "Win Rate %"]

    for column in numeric_columns:
        results_df[column] = results_df[column].apply(
            lambda value: round(value, 2) if value is not None else None
        )

    return results_df
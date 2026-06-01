# AI-Assisted Stock Research & Backtesting Dashboard

A Streamlit-based stock research dashboard for Indian equities. The app helps users analyze stocks using technical filters such as trend, volume, support/resistance, relative strength, RSI momentum, and trend structure.

It supports single-stock analysis as well as Nifty 50, Nifty 100, and Nifty 200 scanning.

> This project is for education and research only. It is not financial advice.

## Features

- Search and analyze individual NSE stocks
- 5-year and 10-year technical analysis sections
- Nifty 50 scanner
- Nifty 100 scanner
- Nifty 200 scanner
- Six-tier technical scoring system
- Price chart with 50 DMA and 200 DMA
- Support and resistance levels
- RSI momentum analysis
- Volume comparison against 20-day average volume
- Relative strength comparison against Nifty
- Timeframe-based view for 1 month, 3 months, 6 months, and 1 year
- Light, dark, and beige themes
- Download scanner results as CSV

## Technical Filters Used

### 1. Trend

Checks whether the stock is trading above or below the 200-day moving average.

- Price above 200 DMA: long-term strength
- Price below 200 DMA: long-term weakness

Also compares the 50 DMA with the 200 DMA.

- 50 DMA above 200 DMA: bullish trend confirmation
- 50 DMA below 200 DMA: bearish trend confirmation

### 2. Volume

Compares current volume with the 20-day average volume.

A price move with higher-than-average volume is considered stronger than a move with weak volume.

### 3. Support and Resistance

Calculates recent support and resistance using recent price highs and lows.

The app checks whether the stock is close to support, near resistance, or breaking above resistance.

### 4. Relative Strength

Compares the stock’s return with Nifty’s return over the selected period.

If the stock outperforms Nifty, it is treated as stronger.

### 5. Momentum

Uses RSI to judge momentum.

- RSI above 60: strong momentum
- RSI between 45 and 60: neutral momentum
- RSI below 45: weak momentum

### 6. Trend Structure

Checks whether the stock is forming:

- Higher highs and higher lows: bullish structure
- Lower highs and lower lows: bearish structure
- Mixed structure: unclear trend

## Tech Stack

- Python
- Streamlit
- yfinance
- pandas
- Plotly

## Project Structure

```text
stock_backtesting/
  app.py
  requirements.txt
  nifty50.csv
  nifty100.csv
  nifty200.csv
  README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/shreya-var03/Stock-Backtesting.git
cd Stock-Backtesting
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## CSV Files

The app uses CSV files for index constituents:

- `nifty50.csv`
- `nifty100.csv`
- `nifty200.csv`

Each file should contain at least:

```csv
Company,Symbol
Reliance Industries Ltd.,RELIANCE
Tata Consultancy Services Ltd.,TCS
Infosys Ltd.,INFY
```

The app automatically adds `.NS` to NSE symbols when needed.

## How To Use

1. Run the Streamlit app.
2. Choose a theme from the sidebar.
3. Select one of the modes:
   - Single Stock Analysis
   - Nifty 50 Scanner
   - Nifty 100 Scanner
   - Nifty 200 Scanner
4. For single stock analysis, search and select a stock.
5. For scanners, choose 5Y or 10Y and run the scan.
6. Review the score, signal, technical explanation, and chart.

## Scoring System

Each stock receives a technical score based on:

- Price above 200 DMA
- 50 DMA above 200 DMA
- Bullish volume behavior
- Support/resistance position
- Relative strength vs Nifty
- RSI momentum
- Trend structure

The final signal is shown as:

- Bullish
- Neutral / Watchlist
- Bearish / Avoid for now

## Disclaimer

This dashboard is for educational and research purposes only. It does not provide financial advice, investment recommendations, or guaranteed predictions.

Always do your own research or consult a qualified financial advisor before making investment decisions.

```Happy Coding!```

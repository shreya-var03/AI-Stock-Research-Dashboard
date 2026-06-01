import streamlit as st
import yfinance as yf


def safe_get(info, key, default=None):
    value = info.get(key, default)
    return default if value is None else value


def format_large_number(value):
    if value is None:
        return "N/A"

    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"

    if abs(value) >= 1_00_000_00_00_000:
        return f"Rs. {value / 1_00_000_00_00_000:.2f} L Cr"

    if abs(value) >= 1_00_00_00_000:
        return f"Rs. {value / 1_00_00_00_000:.2f} Cr"

    if abs(value) >= 1_00_000:
        return f"Rs. {value / 1_00_000:.2f} L"

    return f"Rs. {value:,.0f}"


def format_percent(value):
    if value is None:
        return "N/A"

    try:
        return f"{value * 100:.2f}%"
    except (TypeError, ValueError):
        return "N/A"


def format_ratio(value):
    if value is None:
        return "N/A"

    try:
        return f"{value:.2f}"
    except (TypeError, ValueError):
        return "N/A"


def get_latest_cashflow_value(cashflow, possible_names):
    if cashflow is None or cashflow.empty:
        return None

    for name in possible_names:
        if name in cashflow.index:
            series = cashflow.loc[name].dropna()

            if not series.empty:
                return series.iloc[0]

    return None


def get_free_cash_flow(ticker):
    try:
        cashflow = ticker.cashflow
    except Exception:
        return None

    operating_cash_flow = get_latest_cashflow_value(
        cashflow,
        [
            "Operating Cash Flow",
            "Total Cash From Operating Activities",
        ],
    )

    capital_expenditure = get_latest_cashflow_value(
        cashflow,
        [
            "Capital Expenditure",
            "Capital Expenditures",
        ],
    )

    if operating_cash_flow is None or capital_expenditure is None:
        return None

    return operating_cash_flow + capital_expenditure


@st.cache_data(ttl=86400)
def get_fundamental_data(symbol):
    ticker = yf.Ticker(symbol)

    try:
        info = ticker.info
    except Exception:
        return None

    if not info:
        return None

    free_cash_flow = safe_get(info, "freeCashflow")

    if free_cash_flow is None:
        free_cash_flow = get_free_cash_flow(ticker)

    fundamentals = {
        "EPS": format_ratio(safe_get(info, "trailingEps")),
        "P/E Ratio": format_ratio(safe_get(info, "trailingPE")),
        "P/B Ratio": format_ratio(safe_get(info, "priceToBook")),
        "ROE": format_percent(safe_get(info, "returnOnEquity")),
        "Debt to Equity": format_ratio(safe_get(info, "debtToEquity")),
        "Free Cash Flow": format_large_number(free_cash_flow),
        "Operating Margin": format_percent(safe_get(info, "operatingMargins")),
        "Market Cap": format_large_number(safe_get(info, "marketCap")),
        "Revenue Growth": format_percent(safe_get(info, "revenueGrowth")),
        "Earnings Growth": format_percent(safe_get(info, "earningsGrowth")),
        "Profit Margin": format_percent(safe_get(info, "profitMargins")),
        "Dividend Yield": format_percent(safe_get(info, "dividendYield")),
        "Book Value": format_ratio(safe_get(info, "bookValue")),
        "Sector": safe_get(info, "sector", "N/A"),
        "Industry": safe_get(info, "industry", "N/A"),
    }

    qualitative = {
        "business_summary": safe_get(info, "longBusinessSummary", "Business summary unavailable."),
        "sector": safe_get(info, "sector", "N/A"),
        "industry": safe_get(info, "industry", "N/A"),
        "audit_risk": safe_get(info, "auditRisk"),
        "board_risk": safe_get(info, "boardRisk"),
        "shareholder_rights_risk": safe_get(info, "shareHolderRightsRisk"),
        "compensation_risk": safe_get(info, "compensationRisk"),
    }

    raw = {
        "eps": safe_get(info, "trailingEps"),
        "pe": safe_get(info, "trailingPE"),
        "price_to_book": safe_get(info, "priceToBook"),
        "roe": safe_get(info, "returnOnEquity"),
        "debt_to_equity": safe_get(info, "debtToEquity"),
        "free_cash_flow": free_cash_flow,
        "operating_margin": safe_get(info, "operatingMargins"),
        "revenue_growth": safe_get(info, "revenueGrowth"),
        "earnings_growth": safe_get(info, "earningsGrowth"),
        "profit_margin": safe_get(info, "profitMargins"),
    }

    return {
        "display": fundamentals,
        "raw": raw,
        "qualitative": qualitative,
    }


def score_fundamentals(fundamental_data):
    if fundamental_data is None:
        return {
            "score": 0,
            "max_score": 10,
            "rating": "Data unavailable",
            "analysis": [
                ("Data", "Unavailable", "Could not fetch fundamental data for this stock.")
            ],
        }

    raw = fundamental_data["raw"]
    qualitative = fundamental_data["qualitative"]

    score = 0
    max_score = 10
    analysis = []

    eps = raw["eps"]
    if eps is not None and eps > 0:
        score += 1
        analysis.append(("EPS", "Positive", "EPS is positive, meaning the company is profitable per share."))
    else:
        analysis.append(("EPS", "Weak / Missing", "EPS is negative or unavailable."))

    pe = raw["pe"]
    if pe is not None and 0 < pe <= 35:
        score += 1
        analysis.append(("P/E Ratio", "Reasonable", "P/E ratio is within a reasonable range."))
    elif pe is not None and pe > 35:
        analysis.append(("P/E Ratio", "Expensive", "P/E ratio is high, so valuation risk may exist."))
    else:
        analysis.append(("P/E Ratio", "Missing", "P/E ratio is unavailable."))

    price_to_book = raw["price_to_book"]
    if price_to_book is not None and 0 < price_to_book <= 5:
        score += 1
        analysis.append(("P/B Ratio", "Reasonable", "P/B ratio is not extremely expensive."))
    elif price_to_book is not None and price_to_book > 5:
        analysis.append(("P/B Ratio", "Expensive", "P/B ratio is high compared to book value."))
    else:
        analysis.append(("P/B Ratio", "Missing", "P/B ratio is unavailable."))

    roe = raw["roe"]
    if roe is not None and roe >= 0.15:
        score += 1
        analysis.append(("ROE", "Strong", "ROE is above 15%, showing good profitability."))
    elif roe is not None and roe >= 0.08:
        analysis.append(("ROE", "Average", "ROE is moderate."))
    else:
        analysis.append(("ROE", "Weak / Missing", "ROE is weak or unavailable."))

    debt_to_equity = raw["debt_to_equity"]
    if debt_to_equity is not None and debt_to_equity <= 100:
        score += 1
        analysis.append(("Debt-to-Equity", "Healthy", "Debt-to-equity appears manageable."))
    elif debt_to_equity is not None and debt_to_equity <= 200:
        analysis.append(("Debt-to-Equity", "Moderate", "Debt is present and should be watched."))
    else:
        analysis.append(("Debt-to-Equity", "High / Missing", "Debt is high or unavailable."))

    free_cash_flow = raw["free_cash_flow"]
    if free_cash_flow is not None and free_cash_flow > 0:
        score += 1
        analysis.append(("Free Cash Flow", "Positive", "Company is generating positive free cash flow."))
    else:
        analysis.append(("Free Cash Flow", "Weak / Missing", "Free cash flow is negative or unavailable."))

    operating_margin = raw["operating_margin"]
    if operating_margin is not None and operating_margin >= 0.15:
        score += 1
        analysis.append(("Operating Margin", "Strong", "Operating margin is above 15%, showing good operating efficiency."))
    elif operating_margin is not None and operating_margin > 0:
        analysis.append(("Operating Margin", "Average", "Operating margin is positive but not very high."))
    else:
        analysis.append(("Operating Margin", "Weak / Missing", "Operating margin is weak or unavailable."))

    business_summary = qualitative["business_summary"]
    if business_summary != "Business summary unavailable.":
        score += 1
        analysis.append(("Business Model & Moat", "Review Available", "Business summary is available. Review the company model, brand power, scale, and competitive advantage."))
    else:
        analysis.append(("Business Model & Moat", "Manual Review Needed", "Business model data is unavailable. This needs manual research."))

    governance_risks = [
        qualitative["audit_risk"],
        qualitative["board_risk"],
        qualitative["shareholder_rights_risk"],
        qualitative["compensation_risk"],
    ]

    available_risks = [risk for risk in governance_risks if risk is not None]

    if available_risks and max(available_risks) <= 5:
        score += 1
        analysis.append(("Management & Governance", "Acceptable", "Available governance risk indicators look acceptable. Still review promoter behavior and capital allocation manually."))
    elif available_risks:
        analysis.append(("Management & Governance", "Watch", "Some governance risk indicators are elevated. Manual review is recommended."))
    else:
        analysis.append(("Management & Governance", "Manual Review Needed", "Governance data is unavailable. Review management quality manually."))

    sector = qualitative["sector"]
    industry = qualitative["industry"]

    if sector != "N/A" and industry != "N/A":
        score += 1
        analysis.append(("Industry & Macro Outlook", "Review Available", f"The company operates in {sector} / {industry}. Review sector growth, competition, interest rates, inflation, and demand outlook."))
    else:
        analysis.append(("Industry & Macro Outlook", "Manual Review Needed", "Sector or industry data is unavailable."))

    strength = (score / max_score) * 100

    if strength >= 75:
        rating = "Strong Fundamentals"
    elif strength >= 50:
        rating = "Average Fundamentals"
    else:
        rating = "Weak Fundamentals"

    return {
        "score": score,
        "max_score": max_score,
        "rating": rating,
        "analysis": analysis,
    }
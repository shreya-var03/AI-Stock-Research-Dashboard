import pandas as pd
import streamlit as st

from src.config import INDEX_SOURCES
from src.data_loader import get_nifty_data, get_stock_data, load_index_stocks
from src.decision_engine import get_conflict_view
from src.fundamentals import get_fundamental_data, score_fundamentals
from src.technical_analysis import analyze_stock


def apply_scanner_filters(scanner_df, label, include_fundamentals):
    filtered_df = scanner_df.copy()

    st.subheader("Scanner Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        bullish_only = st.checkbox("Bullish technical signal only")
        above_200_dma = st.checkbox("Above 200 DMA only")
        rsi_above_55 = st.checkbox("RSI above 55")

    with filter_col2:
        outperforming_nifty = st.checkbox("Outperforming Nifty")
        positive_cagr = st.checkbox("Positive CAGR")

        min_technical_strength = st.slider(
            "Minimum technical strength %",
            min_value=0,
            max_value=100,
            value=0,
            step=5,
        )

    with filter_col3:
        if include_fundamentals:
            strong_fundamentals_only = st.checkbox("Strong fundamentals only")
            min_combined_strength = st.slider(
                "Minimum combined strength %",
                min_value=0,
                max_value=100,
                value=0,
                step=5,
            )
        else:
            strong_fundamentals_only = False
            min_combined_strength = 0

    if bullish_only:
        filtered_df = filtered_df[
            filtered_df["Technical Signal"].str.contains("Bullish", case=False, na=False)
        ]

    if above_200_dma:
        filtered_df = filtered_df[
            filtered_df["Current Price"] > filtered_df["200 DMA"]
        ]

    if rsi_above_55:
        filtered_df = filtered_df[
            filtered_df["RSI"] > 55
        ]

    if outperforming_nifty:
        filtered_df = filtered_df[
            filtered_df[f"{label} Return %"] > filtered_df[f"Nifty {label} Return %"]
        ]

    if positive_cagr:
        filtered_df = filtered_df[
            filtered_df[f"{label} CAGR %"] > 0
        ]

    filtered_df = filtered_df[
        filtered_df["Technical Strength %"] >= min_technical_strength
    ]

    if include_fundamentals:
        if strong_fundamentals_only:
            filtered_df = filtered_df[
                filtered_df["Fundamental Rating"] == "Strong Fundamentals"
            ]

        filtered_df = filtered_df[
            filtered_df["Combined Strength %"] >= min_combined_strength
        ]

    return filtered_df


def run_scanner(mode, period, label):
    index_name = INDEX_SOURCES[mode]["name"]

    st.subheader(f"{index_name} Technical + Fundamental Scanner")
    st.write(f"Scan {index_name} stocks using {label} data.")

    stocks = load_index_stocks(mode)

    if stocks is None:
        st.error(f"Could not load {index_name} list. Check internet connection or add a local CSV file.")
        return

    include_fundamentals = st.checkbox(
        "Include fundamental analysis in scanner",
        value=True,
        help="This is slower because fundamentals are fetched stock by stock.",
    )

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
                technical_result = analyze_stock(data, nifty_data)

                technical_strength = round(
                    (technical_result["score"] / technical_result["max_score"]) * 100,
                    2,
                )

                row_result = {
                    "Company": company,
                    "Symbol": symbol,
                    "Technical Signal": technical_result["signal"],
                    "Technical Score": technical_result["score"],
                    "Technical Max": technical_result["max_score"],
                    "Technical Strength %": technical_strength,
                    "Current Price": round(technical_result["current_price"], 2),
                    "50 DMA": round(technical_result["dma_50"], 2),
                    "200 DMA": round(technical_result["dma_200"], 2),
                    "RSI": round(technical_result["rsi"], 2),
                    "Volume vs 20D Avg": round(technical_result["volume_ratio"], 2),
                    f"{label} Return %": round(technical_result["stock_return"], 2),
                    f"{label} CAGR %": round(technical_result["stock_cagr"], 2),
                    f"Nifty {label} Return %": round(technical_result["nifty_return"], 2),
                    f"Nifty {label} CAGR %": round(technical_result["nifty_cagr"], 2),
                }

                if include_fundamentals:
                    fundamental_data = get_fundamental_data(symbol)
                    fundamental_score = score_fundamentals(fundamental_data)
                    conflict_view = get_conflict_view(technical_result, fundamental_score)

                    fundamental_strength = round(
                        (fundamental_score["score"] / fundamental_score["max_score"]) * 100,
                        2,
                    )

                    combined_strength = round(
                        (technical_strength + fundamental_strength) / 2,
                        2,
                    )

                    row_result.update({
                        "Fundamental Rating": fundamental_score["rating"],
                        "Fundamental Score": fundamental_score["score"],
                        "Fundamental Max": fundamental_score["max_score"],
                        "Fundamental Strength %": fundamental_strength,
                        "Combined Strength %": combined_strength,
                        "Decision View": conflict_view["action_view"],
                        "Verdict": conflict_view["verdict"],
                    })

                results.append(row_result)

            progress_bar.progress((index + 1) / len(stocks))

        status_text.write("Scan completed.")

        if len(results) == 0:
            st.error("No scanner results were generated.")
            return

        scanner_df = pd.DataFrame(results)

        if include_fundamentals:
            scanner_df = scanner_df.sort_values(
                by=["Combined Strength %", "Technical Strength %", f"{label} CAGR %"],
                ascending=False,
            )
        else:
            scanner_df = scanner_df.sort_values(
                by=["Technical Score", "Technical Strength %", f"{label} Return %"],
                ascending=False,
            )

        st.session_state["scanner_results"] = scanner_df
        st.session_state["scanner_label"] = label
        st.session_state["scanner_include_fundamentals"] = include_fundamentals
        st.session_state["scanner_index_name"] = index_name

    if "scanner_results" in st.session_state:
        scanner_df = st.session_state["scanner_results"]
        saved_label = st.session_state["scanner_label"]
        saved_include_fundamentals = st.session_state["scanner_include_fundamentals"]
        saved_index_name = st.session_state["scanner_index_name"]

        filtered_df = apply_scanner_filters(
            scanner_df,
            saved_label,
            saved_include_fundamentals,
        )

        st.subheader("Ranked Scanner Results")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        st.subheader("Top 10 Strongest Stocks")
        st.dataframe(filtered_df.head(10), use_container_width=True, hide_index=True)

        st.download_button(
            label="Download Scanner Results CSV",
            data=filtered_df.to_csv(index=False),
            file_name=f"{saved_index_name.lower().replace(' ', '_')}_{saved_label.lower().replace(' ', '_')}_scanner.csv",
            mime="text/csv",
        )
import streamlit as st


def apply_custom_theme(theme):
    themes = {
        "Light": {
            "bg": "#c4d4ec",
            "surface": "#ffffff",
            "table": "#f8fbff",
            "sidebar": "#7a8ca6",
            "input": "#ffffff",
            "text": "#1f2937",
            "muted": "#64748b",
            "border": "#d7e0ea",
            "primary": "#60a5fa",
            "accent": "#dbeafe",
            "shadow": "0 10px 30px rgba(15, 23, 42, 0.08)",
        },
        "Dark": {
            "bg": "#10192F",
            "surface": "#0d2e6a",
            "table": "#243044",
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
            "bg": "#d5c6ac",
            "surface": "#fdedd3",
            "table": "#fffaf0",
            "sidebar": "#f5cf95",
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
            min-height: 110px;
        }}

        div[data-testid="stMetricLabel"] {{
            color: {selected["muted"]};
            font-size: 13px;
            font-weight: 600;
        }}

        div[data-testid="stMetricValue"] {{
            color: {selected["text"]};
            font-size: 21px;
            line-height: 1.25;
            white-space: normal;
            overflow-wrap: anywhere;
            word-break: break-word;
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

        div[data-baseweb="popover"] div,
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

        div[data-testid="stTable"] {{
            border: 1px solid {selected["border"]};
            border-radius: 8px;
            overflow: hidden;
            box-shadow: {selected["shadow"]};
        }}

        div[data-testid="stTable"] table {{
            width: 100%;
            table-layout: auto;
            background-color: {selected["table"]};
            border-radius: 8px;
            overflow: hidden;
        }}

        div[data-testid="stTable"] th {{
            background-color: {selected["surface"]};
            color: {selected["text"]};
            font-weight: 700;
            white-space: normal !important;
            word-wrap: break-word !important;
            vertical-align: top !important;
            padding: 12px 14px !important;
        }}

        div[data-testid="stTable"] td {{
            background-color: {selected["table"]};
            color: {selected["text"]};
            white-space: normal !important;
            word-wrap: break-word !important;
            vertical-align: top !important;
            padding: 12px 14px !important;
            line-height: 1.5;
        }}

        .reason-box {{
            background-color: {selected["table"]};
            border: 1px solid {selected["border"]};
            border-radius: 8px;
            padding: 12px 14px;
            margin-bottom: 10px;
            color: {selected["text"]};
            box-shadow: {selected["shadow"]};
            line-height: 1.5;
        }}

        .stAlert {{
            border-radius: 8px;
        }}

        hr {{
            border-color: {selected["border"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
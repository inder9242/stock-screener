import streamlit as st
import pandas as pd
from io import BytesIO

# ---------- Page Config ----------
st.set_page_config(page_title="Stock Screener", layout="wide")

# ---------- Load Data ----------
df = pd.read_excel("EQUITY_Final.xlsx")

# ---------- Clean Column Names ----------
df.columns = df.columns.str.strip().str.upper()

# ---------- Header ----------
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>📊 Stock Screener </h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>Analyze 2500+ NSE-listed companies across Mainboard & SME platforms using NSE’s 4-level classification and 3 powerful ratio filters — Profitability, Valuation, and Financial Health.</p>",
    unsafe_allow_html=True
)

# ---------- Company Info Lookup ----------
with st.expander("🔍 Company Info Lookup"):
    company = st.text_input("Enter company symbol (e.g. RELIANCE):").strip().upper()
    if company:
        result = df[df["SYMBOL"].str.upper() == company]
        if not result.empty:
            row = result.iloc[0]
            st.markdown(f"""
            - **Series:** {row.get('SERIES', 'N/A')}
            - **Macro-Economic Sector:** {row.get('MACRO', 'N/A')}
            - **Sector:** {row.get('SECTOR', 'N/A')}
            - **Industry:** {row.get('INDUSTRY', 'N/A')}
            - **Basic Industry:** {row.get('BASICINDUSTRY', 'N/A')}
            """)
        else:
            st.warning("Company not found.")

# ---------- NSE Series Filter ----------
series_map = {
    "EQ": "Equity (Mainboard)",
    "BE": "Trade-for-Trade",
    "SM": "SME Stocks",
    "ST": "Surveillance",
    "BZ": "Z Category",
    "GC": "Government Securities",
    "MF": "Mutual Funds / ETFs"
}
available_series = sorted(df["SERIES"].dropna().unique())
pretty_names = [f"{code} – {series_map.get(code, 'Unknown')}" for code in available_series]
reverse_map = {f"{k} – {v}": k for k, v in series_map.items()}

st.subheader("🎯 Filter by NSE Series")
series_pretty_selected = st.multiselect("Select NSE Series", options=pretty_names)
series_selected = [reverse_map[name] for name in series_pretty_selected if name in reverse_map]

# ---------- Industry Filters ----------
st.subheader("🏢 Industry Filters (NSE classification)")

col1, col2 = st.columns(2)
macro_selected = col1.multiselect("Macro-Economic Sector", options=sorted(df["MACRO"].dropna().unique()))
sector_selected = col2.multiselect("Sector", options=sorted(df["SECTOR"].dropna().unique()))

col3, col4 = st.columns(2)
industry_selected = col3.multiselect("Industry", options=sorted(df["INDUSTRY"].dropna().unique()))
basic_selected = col4.multiselect("Basic Industry", options=sorted(df["BASICINDUSTRY"].dropna().unique()))

# ---------- Apply Filters ----------
filtered_df = df.copy()

if series_selected:
    filtered_df = filtered_df[filtered_df["SERIES"].isin(series_selected)]
if macro_selected:
    filtered_df = filtered_df[filtered_df["MACRO"].isin(macro_selected)]
if sector_selected:
    filtered_df = filtered_df[filtered_df["SECTOR"].isin(sector_selected)]
if industry_selected:
    filtered_df = filtered_df[filtered_df["INDUSTRY"].isin(industry_selected)]
if basic_selected:
    filtered_df = filtered_df[filtered_df["BASICINDUSTRY"].isin(basic_selected)]

# ---------- Ratio Filter Function ----------
def add_ratio_sliders(section_title, ratios, data, expander_key):
    with st.expander(section_title):
        for ratio in ratios:
            if ratio not in data.columns:
                continue
            col_data = data[ratio].dropna().replace([float('inf'), float('-inf')], pd.NA).dropna()
            if col_data.empty:
                continue
            min_val = float(col_data.min())
            max_val = float(col_data.max())
            if min_val == max_val:
                st.markdown(f"⚠️ Skipping slider for `{ratio}`: only one value ({min_val})")
                continue
            user_min, user_max = st.slider(
                f"{ratio} Range",
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val),
                step=0.1,
                key=f"{expander_key}_{ratio}"
            )
            if not (user_min == min_val and user_max == max_val):
                data = data[(data[ratio] >= user_min) & (data[ratio] <= user_max)]
    return data

# ---------- Ratio Groups ----------
st.subheader("📈 Filter by Financial Ratios")

profitability_ratios = ["ROE", "NET_PROFIT_MARGIN", "OPERATING_MARGIN", "GROSS_MARGIN", "EPS_TTM"]
valuation_ratios = ["P_E", "P_B", "EV_EBITDA", "EV_SALES"]
financial_health_ratios = ["DEBT_TO_EQUITY", "CURRENT_RATIO", "QUICK_RATIO"]

filtered_df = add_ratio_sliders("💹 Profitability Ratios", profitability_ratios, filtered_df, "profit")
filtered_df = add_ratio_sliders("💰 Valuation Ratios", valuation_ratios, filtered_df, "valuation")
filtered_df = add_ratio_sliders("🏦 Financial Health Ratios", financial_health_ratios, filtered_df, "health")

# ---------- Display Final Result ----------
st.subheader("📋 Filtered Results")
st.markdown(f"**Companies in current selection:** {len(filtered_df)}")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# ---------- Download Excel ----------
def to_excel_download(df):
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer

excel_data = to_excel_download(filtered_df)
st.download_button(
    label="📥 Download Filtered Results",
    data=excel_data,
    file_name="Filtered_Stocks.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ---------- Footer ----------
st.markdown("""
---
**Disclaimer:**
- This project is for educational use only and does not constitute investment advice. 
- It analyzes stocks using financial ratios from Yahoo Finance and industry classifications from the NSE. 
- NSE Indices industry classification follows 4 tier structure. Brief of four levels of classification for each company as detailed below:
- Macro-Economic Sector: Indicates business activity of a company at macro level
- Sector: Indicates specific sector of a company
- Industry: This level would indicate the industry classification of the company
- Basic Industry: This is a micro level classification to indicate the core business activities carried on by the company
- It consists of 12 Macro-Economic Sectors, 22 Sectors, 59 Industries and 197 Basic Industries.  
- This structured classification helps users drill down from broader economic sectors to niche industry segments.  
- "Use cases include relative valuation (trading comps), peer benchmarking, sectoral screening, investment research, and idea generation for portfolio construction."  
- 📩 For queries: indrajeetsingh9242@gmail.com
""")


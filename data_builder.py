import pandas as pd
import time
import yfinance as yf
from nsepython import nse_eq

# ---------- CONFIG ----------
input_path = "C:/Users/91914/Desktop/trading_comps_/EQUITY_Final.xlsx"
output_path = "C:/Users/91914/Desktop/trading_comps_/EQUITY_Final.xlsx"

# ---------- Step 1: Load Excel ----------
df = pd.read_excel(input_path)

# Ensure symbol column is named correctly
if df.columns[0] != "Symbol":
    df.rename(columns={df.columns[0]: "Symbol"}, inplace=True)

# ---------- Step 2: Ensure necessary columns exist ----------
industry_cols = ["Industry", "Sector", "macro", "basicIndustry"]
for col in industry_cols:
    if col not in df.columns:
        df[col] = ""

# Financial ratios (PEG, ROCE, Interest_Coverage, Market_Cap removed)
ratio_cols = {
    "ROE": "ROE",
    "Net_Profit_Margin": "Net_Profit_Margin",
    "Operating_Margin": "Operating_Margin",
    "Gross_Margin": "Gross_Margin",
    "EPS_TTM": "EPS_TTM",
    "P_E": "P_E",
    "P_B": "P_B",
    "EV_EBITDA": "EV_EBITDA",
    "EV_Sales": "EV_Sales",
    "Debt_to_Equity": "Debt_to_Equity",
    "Current_Ratio": "Current_Ratio",
    "Quick_Ratio": "Quick_Ratio",
    "Book_Value_per_Share": "Book_Value_per_Share"
}

for col in ratio_cols.values():
    if col not in df.columns:
        df[col] = None

# ---------- Step 3: Loop through each company ----------
for idx, row in df.iterrows():
    symbol = str(row["Symbol"]).strip().upper()
    if not symbol:
        continue

    # -------- NSE Industry Info Patch --------
    industry_missing = any(pd.isna(row[col]) or row[col] == "" for col in industry_cols)
    if industry_missing:
        try:
            data = nse_eq(symbol)
            info = data.get("industryInfo", {})
            df.at[idx, "Industry"] = info.get("industry", "")
            df.at[idx, "Sector"] = info.get("sector", "")
            df.at[idx, "macro"] = info.get("macro", "")
            df.at[idx, "basicIndustry"] = info.get("basicIndustry", "")
            print(f"🏷️ {symbol} — Industry info added")
            time.sleep(1.2)
        except Exception as e:
            print(f"⚠️ NSEPython error for {symbol}: {e}")

    # -------- Yahoo Finance Ratios Patch --------
    ratios_missing = any(pd.isna(row[col]) for col in ratio_cols.values())
    if ratios_missing:
        try:
            yf_symbol = f"{symbol}.NS"
            tkr = yf.Ticker(yf_symbol)
            info = tkr.info

            # Directly from .info
            df.at[idx, "ROE"] = info.get("returnOnEquity")
            df.at[idx, "Net_Profit_Margin"] = info.get("profitMargins")
            df.at[idx, "Operating_Margin"] = info.get("operatingMargins")
            df.at[idx, "Gross_Margin"] = info.get("grossMargins")
            df.at[idx, "EPS_TTM"] = info.get("trailingEps")
            df.at[idx, "P_E"] = info.get("trailingPE")
            df.at[idx, "P_B"] = info.get("priceToBook")
            df.at[idx, "EV_EBITDA"] = info.get("enterpriseToEbitda")
            df.at[idx, "EV_Sales"] = info.get("enterpriseToRevenue")
            df.at[idx, "Debt_to_Equity"] = info.get("debtToEquity")
            df.at[idx, "Current_Ratio"] = info.get("currentRatio")
            df.at[idx, "Quick_Ratio"] = info.get("quickRatio")
            df.at[idx, "Book_Value_per_Share"] = info.get("bookValue")

            print(f"📈 {symbol} — Ratios added")
            time.sleep(1.5)

        except Exception as e:
            print(f"⚠️ Yahoo Finance error for {symbol}: {e}")

# ---------- Step 4: Save Excel ----------
df.to_excel(output_path, index=False)
print(f"✅ File saved to '{output_path}'")

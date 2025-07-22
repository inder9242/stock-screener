# Stock Screener App

This is my first open-source GitHub project, created as part of my learning journey in finance and Python.  

This app is built using Python and Streamlit, and allows users to screen over 2500+ NSE-listed companies based on financial ratios and NSE’s 4-level classification system.

---

# Features

- Coverage:
  - 2500+ NSE-listed companies including both Mainboard and SME segments

- NSE’s 4-Layer Industry Classification Filters:
  - Macro-Economic Sector
  - Sector
  - Industry
  - Basic Industry

- NSE Series Filter:
  - Filter by series such as EQ, BE, SM, ST, etc.

- Company Info Lookup:
  - Enter a stock symbol to retrieve sector, industry, macro classification, and NSE series

- Financial Ratio Filters:
  - Profitability Ratios: ROE, Net Profit Margin, Operating Margin, EPS, etc.
  - Valuation Ratios: P/E, P/B, EV/EBITDA, EV/Sales
  - Financial Health Ratios: Debt-to-Equity, Current Ratio, Quick Ratio, Book Value per Share

- Export Results:
  - Download filtered results as an Excel file (`.xlsx`) using in-memory processing

- Interactive UI:
  - Built with Streamlit
  - Organized layout with collapsible filters and real-time updates

- Disclaimer Section:
  - Informative footer with intended use, data sources, and contact email

---

# Use Cases

- Peer benchmarking
- Trading comparables (comps) analysis
- Sectoral filtering
- Investment research
- Idea generation for portfolio construction

---

#  Data Sources

- Yahoo Finance (via `yfinance`)
- NSE India (classification structure)

---

# Contact

For queries, reach out at:indrajeetsingh9242@gmail.com

# Volatility and Growth ETF Comparative Dashboard

An **interactive Streamlit dashboard** that compares the performance of a **volatility ETF (UVXY)** and a **growth ETF (QQQ)** over multiple timeframes. This tool allows users to visualize positive/negative returns and cumulative performance for investment analysis or educational purposes.

---

## 1️⃣ Data Retrieval and Display

- **Download historical data:**  
  UVXY and QQQ are fetched via `yfinance`, including daily Open, Close, Adjusted Close, High, Low, and Volume.

- **Compute daily and cumulative returns:**  
  - Daily return: `pct_change()`  
  - Cumulative return: `(1 + Return).cumprod()`  

- **Purpose:**  
  Converts raw price data into intuitive return metrics, making it easy to compare investment performance.

---

## 2️⃣ Time Window Selection

- **Six pre-defined time windows:**  
  - Last 1 Month  
  - Last 3 Months  
  - Last 6 Months  
  - Year to Date  
  - Last 1 Year  
  - Last 3 Years  

- **Purpose:**  
  Allows users to flexibly observe short-term, medium-term, and long-term performance, and to spot trends and volatility over different periods.

---

## 3️⃣ Total Return Table

- Displays **total return (%)** for each ETF over the selected timeframe.
- Observed behavior:  
  - **UVXY:** Typically negative over long periods due to leveraged short-term volatility exposure.  
  - **QQQ:** Typically positive over long periods, representing growth in tech-heavy NASDAQ-100.

- **Purpose:**  
  Provides a quick, at-a-glance comparison of returns, highlighting the differences between a volatility-focused and a growth-focused asset.

---

## 4️⃣ Normalized Cumulative Return Plot

- **Visualization:**  
  Line chart normalized to 100 at the start of the period for both UVXY and QQQ.

- **Purpose:**  
  Allows clear visual comparison of short-term fluctuations and long-term trends, helping users understand the relationship between **risk and return**.

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/shaoxianduan/etf-dashboard.git
cd etf-dashboard

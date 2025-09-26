# app.py
import yfinance as yf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ------------------ Page Config ------------------
st.set_page_config(page_title="UVXY vs QQQ", layout="wide")
st.title("📈 UVXY vs QQQ Positive/Negative Return Comparison")

# ------------------ Dynamic Dates ------------------
end_date = datetime.today()
start_date = end_date - timedelta(days=3*365)  # Last 3 years
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

# ------------------ Download Data ------------------
uvxy = yf.download("UVXY", start=start_str, end=end_str, auto_adjust=False)
qqq = yf.download("QQQ",  start=start_str, end=end_str, auto_adjust=False)

# ------------------ Calculate Returns ------------------
for df in [uvxy, qqq]:
    df['Return'] = df['Adj Close'].pct_change()
    df['Cumulative_Return'] = (1 + df['Return']).cumprod()

# ------------------ Define Time Windows ------------------
end_dt = uvxy.index[-1]
window_dict = {
    "Last 1 Month": 21,
    "Last 3 Months": 63,
    "Last 6 Months": 126,
    "Year to Date": (end_dt - datetime(end_dt.year, 1, 1)).days,
    "Last 1 Year": 252,
    "Last 3 Years": len(uvxy)
}

# ------------------ Frontend Buttons ------------------
selected_window = st.radio("Select Time Window", list(window_dict.keys()))
period_days = window_dict[selected_window]
if period_days < 2:  # Ensure at least two trading days
    period_days = 2
if period_days > len(uvxy):
    period_days = len(uvxy)

uvxy_window = uvxy.iloc[-period_days:]
qqq_window = qqq.iloc[-period_days:]

# ------------------ Display Total Returns ------------------
returns_dict = {}
for label, df_window in zip(['UVXY', 'QQQ'], [uvxy_window, qqq_window]):
    try:
        start_price = float(df_window['Adj Close'].iloc[0])
        end_price = float(df_window['Adj Close'].iloc[-1])
        returns_dict[label] = (end_price / start_price - 1) * 100
    except:
        returns_dict[label] = float('nan')

st.subheader(f"{selected_window} Total Return (%)")
st.table(pd.DataFrame.from_dict(returns_dict, orient='index',
         columns=['Total Return (%)']).round(2))

# ------------------ Plot Normalized Cumulative Returns ------------------
st.subheader("Normalized Cumulative Returns (Start = 100)")

fig, ax = plt.subplots(figsize=(12, 6))
for df, label, color in zip([uvxy_window, qqq_window], ['UVXY', 'QQQ'], ['blue', 'orange']):
    normalized = df['Adj Close'] / df['Adj Close'].iloc[0] * 100
    ax.plot(df.index, normalized, label=label, color=color)

ax.set_xlabel("Date")
ax.set_ylabel("Normalized Price (Start = 100)")
ax.set_title(
    f"UVXY vs QQQ Positive/Negative Return Comparison ({selected_window})")
ax.legend()
ax.grid(True)
st.pyplot(fig)
